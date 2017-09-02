#!/bin/bash
filename="$1"
shrink=0

if [ -z $filename ]; then
    echo "Preparation: copy $0 and the pdf of the proceedings you want to split up"
    echo "in the folder containing the pages.txt (and the folder structure used to create"
    echo "the proceedings)"
    echo "Usage: $0 pdf-file-to-split-up"
    echo "Hint if you copy shrinkpdf.sh as well, the splitted pdfs will be shrinked using gs"
    exit 1;
fi

if [ -f "shrinkpdf.sh" ]; then
    echo "shrinkpdf.sh script detected"
    shrink=1
else
    echo "no shrinkpdf.sh script found. just splitting"
fi


while read -r line
do

    l=$line
    # read page no from pages.txt and add 1 (offset because of title page)
    pages1=$(($(echo $line | cut -d " " -f 2)+1))
    # read id from pages.txt
    id=$(echo "$l" | cut -d " " -f 1)
    # read page size of original paper using id (this is needed because simply cutting
    # papers from the preceedings will result in many white pages or headings of the
    # scientific tracks at the end of some papers)
    length=$(pdftk ./$id/paper.pdf dump_data | grep NumberOfPages | cut -d " " -f 2)
    # calculate end of paper
    pages2=$((${pages1}+${length}-1))
    echo "Processing $id with $length pages"
    # cut and save it to paper_web.pdf
    if [ $shrink -eq 1 ]; then
       pdftk $filename cat $pages1-$pages2 output $id/paper_tmp.pdf
       ./shrinkpdf.sh $id/paper_tmp.pdf $id/paper_web.pdf
       rm $id/paper_tmp.pdf
    else
       pdftk $filename cat $pages1-$pages2 output $id/paper_web.pdf
    fi

done < pages.txt
