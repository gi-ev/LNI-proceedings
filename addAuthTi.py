#! /usr/bin/python
import re
import sys
import pyparsing
from pyparsing import nestedExpr

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
    if pos > 0:
        data = data[pos + len("\\author"):]
        if data.startswith("["):
            authorsList = nestedExpr("[", "]").parseString(data).asList()[0]
            authors = " ".join(authorsList)
        # does not work properly because the list of authors is specified in 500 different ways... 
        #if data.startswith("{"):
        #    data = re.sub(r"\$.*?\$", r"", data)
        #    data = re.sub(r"\\footnote{.*?\}", r"\and", data)
        #    data = re.sub(r"\\n", r"\and", data, 0, re.MULTILINE)
        #    authorsList = nestedExpr("{", "}").parseString(data).asList()[0][:-1]
        #    #authors = " ".join(authorsList)

    title = "TITLE"
    data = open(paperFileName).read()
    pos = data.find(r"\title")
    if pos > 0:
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
                title = title.replace(r"\break", "")
                title = title.replace(r"\centering", "")
                title = re.sub(r"\s+", " ", title)
                title = re.sub(r"\[.*?\] *", "", title)
                title = re.sub(r"\\(textnormal|vspace|small|large){.*?}", "", title)
                title = re.sub(r"\\(systemname){.*?} :", "", title)
                title = re.sub(r"---.*$", "", title)
                title = re.sub(r"\\large.*$", "", title)

                title = title.strip()
    return authors, title
    
overviewPaper=open(sys.argv[1]).read()

for curFileName in sys.argv[2:]:
    paperId = curFileName.split("/")[0]
    (paperAuthor, paperTitle) = extractAuthTitle(curFileName)
    bla = ""
    for curLine in overviewPaper.split("\n"):
        m = re.match(".*\\\\addpaper{%s}.*"%paperId, curLine)
        if m:
            bla += "\\addpaper{%s}{%s}{%s}\n"%(paperId, paperAuthor, paperTitle)
        else:
            bla += curLine + "\n"

    overviewPaper = bla

print overviewPaper.strip()
