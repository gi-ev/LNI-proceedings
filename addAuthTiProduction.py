#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8

import os
import re
import sys

from pyparsing import nestedExpr


# TODO: adapt this table to your conference
def lookup_workshop(workshop_id):
    workshops = {
        "A1": "1. Eingeladener Vortrag",
        "A2": "2. Eingeladener Vortrag",
        "B1": "Topic1",
        "B2": "Topic2 with a very long title which requires a lot of space and, hence, also requires a line break",
        "B3": "Word-Papers",
        "B33": "Workshop zur Demonstration der Metadatenextraktion",
        "C1": "Doktorandensymposium",
    }
    return workshops[workshop_id]


def joinNestedList(nestedList, opener, closer):
    res = ""
    for tmp in nestedList:
        if type(tmp) is list:
            res += opener + joinNestedList(tmp, opener, closer) + closer
        else:
            res += " " + tmp

    return res.strip()


def extractAuthTitle(paperFileName):
    authors = "AUTHOR"
    data = open(paperFileName).read()
    pos = data.find("\\author")
    if pos > -1:
        data = data[pos + len("\\author"):]
        if data.startswith("["):
            authorsList = nestedExpr("[", "]").parseString(data).asList()[0]
            authors = " ".join(authorsList)
            # does not work properly because the list of authors is specified in 500 different ways...
            # if data.startswith("{"):
            #    data = re.sub(r"\$.*?\$", r"", data)
            #    data = re.sub(r"\\footnote{.*?\}", r"\and", data)
            #    data = re.sub(r"\\n", r"\and", data, 0, re.MULTILINE)
            #    authorsList = nestedExpr("{", "}").parseString(data).asList()[0][:-1]
            #    #authors = " ".join(authorsList)

    title = "TITLE"
    data = open(paperFileName).read()
    pos = data.find(r"\title")
    if pos > -1:
        data = data[pos + len(r"\title"):].strip()
        if data[0] == "[":
            titleList = nestedExpr("[", "]").parseString(data).asList()[0]
            title = joinNestedList(titleList, "{", "}")
            title = title.strip()
        else:
            data = re.sub(r"^ *\[.*?\] *", "", data)
            if data.startswith("{"):
                titleList = nestedExpr("{", "}").parseString(data).asList()[0]
                title = joinNestedList(titleList, "{", "}")
                title = title.replace("%", "")
                title = title.replace(r"\\", "")
                title = title.replace("\n", "")
                title = title.replace("\break", "")
                title = title.replace("\centering", "")
                title = re.sub(r"\s+", " ", title)
                title = re.sub(r"\[.*?\] *", "", title)
                title = re.sub(r"\\(textnormal|vspace|small|large){.*?}", "", title)
                title = re.sub(r"\\(systemname){.*?} :", "", title)
                title = re.sub(r"---.*$", "", title)
                title = re.sub(r"\\large.*$", "", title)

                title = title.strip()
    return authors, title


# to override the extraction of author and title for a specific paper, just put a the desired \addpaper statement into the paper.tex of that paper
# this function checks for these fixed \addpaper statements and copies them to proceedings.tex instead of extracting from \author and \title
def check_for_fixed_adaptions(paper_file_name):
    fixed_add_paper = ''
    data = open(paper_file_name).read()
    pos = data.find("\\addpaper")
    if pos > -1:
        fixed_add_paper = data
    return fixed_add_paper

def force_utf8(text):
    char_replacement_map = {"0x96": "-", "0xe9": "é", "0xa2": "ó", "0xc4": "Ä", "0xd6": "Ö", "0xdc": "Ü",
                            "0xdf": "ß", "0xe4": "ä", "0xf6": "ö", "0xfc": "ü", "0xf1": "ñ"}
    try:
        text.decode(encoding = 'utf-8')
    except UnicodeError:
        converted_text = ""
        for char in text:
            try:
                char.decode(encoding = 'utf-8')
                converted_text += char
            except UnicodeError:
                hex_char = hex(ord(char))
                print("Invalid char: " + hex_char)
                if hex_char in char_replacement_map:
                    replacement = char_replacement_map[hex_char]
                else:
                    replacement = "Provide a replacement for this character:"
                    char_replacement_map[hex_char] = replacement
                converted_text += replacement
        text = converted_text.decode('utf-8')
    return text

# replaces special characters with proper TeX equivalent
def texify(text):
    tex_replacement_map = {'é': "\\'e", 'ó': "\\'{o}", 'ć': "\\'{c}", 'Ä': '\\"A', 'Ö': '\\"O', 'Ü': '\\"U',
                           'ß': '{\\ss}', 'ä': '\\"a', 'ö': '\\"o', 'ü': '\\"u', 'ñ': '\\~{n}', 'ń': "\\'n",
                           '„': '\\glqq', '“': '\\grqq', '”': "''", '’': "'{}", ' - ': ' --- '}
    for char in tex_replacement_map:
        text = text.replace(char, tex_replacement_map[char])
    return text

overviewPaper = open(sys.argv[1]).read()
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w')
old_workshopId = ""
paperFolders = sys.argv[3:]
print(paperFolders)
paperFolders.sort()
for curFileName in paperFolders:
    print("Processing " + curFileName)
    paperId = curFileName.split("/")[0]
    fixedAddPaper = check_for_fixed_adaptions(curFileName)
    if fixedAddPaper == '':
        (paperAuthor, paperTitle) = extractAuthTitle(curFileName)
    else:
        print("Found fixed addPaper statement")
    temp = u""
    workshopId = ""
    addpaper_line = False
    for curLine in overviewPaper.split("\n"):
        m = re.match(".*\\\\addpaper{%s}.*" % paperId, curLine)
        m_not_added = re.match(".*%add_paper_lines_here.*", curLine)
        if m:
            if fixedAddPaper == '':
                temp += u"\\addpaper{{{0}}}{{{1}}}{{{2}}}".format(paperId, paperAuthor, paperTitle) + "\n"
            else:
                temp += fixedAddPaper
            addpaper_line = True
        elif m_not_added and not addpaper_line:
            workshopId = paperId.split("-")[0]
            if old_workshopId != workshopId:
                workshop_name = lookup_workshop(workshopId)
                temp += "%%\n%%%s\n%%\n\\addchap{%s}\n" % (workshopId, texify(workshop_name))
            if fixedAddPaper == '':
                temp += u"\\addpaper{{{0}}}{{{1}}}{{{2}}}".format(paperId, paperAuthor,
                                                                  paperTitle) + "\n" + curLine + "\n"
            else:
                temp += fixedAddPaper + "\n" + curLine + u"\n"
        else:
            temp += curLine + "\n"
    old_workshopId = workshopId
    overviewPaper = temp

output = overviewPaper.strip()
open(sys.argv[2], 'w').write(output)
