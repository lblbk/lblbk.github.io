import os
import json
import argparse
import sys

def main(args):
    to_save_file = open(args.file_name, 'w', encoding='utf-8')

    header = "## balabala..."
    body = "<head><style type=\"text/css\">h1:first-child {display:none;}</style></head>"
    quate = "> **我决定出发去找你。** \n" \
            "> \n" \
            "> **你说别来，你不合群，话少，无聊无趣，习惯独自一个人。** \n" \
            "> \n" \
            "> **我说挺好，有个外国老头说，离群索居者，不是神明，就是野兽。** \n" \
            "> \n" \
            "> **你是神明我就拜神，你是野兽我就献祭，** \n" \
            "> \n" \
            "> **反正闲着也是闲着。** \n"

    contents = ""
    for line in (header, body, quate):
        contents += line
        contents += "\n \n"

    print(contents)
    to_save_file.write(contents)
    to_save_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str, default="balabala.md")
    opt = parser.parse_args()

    main(opt)
