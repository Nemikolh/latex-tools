#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import xml.etree.ElementTree as ET
import os.path
import re
import codecs


parser = argparse.ArgumentParser(
    description='Convert a docx into a tex file.')
parser.add_argument('-i', '--input', dest='input_docx', help='The docx file', default='document.xml')
parser.add_argument('-o', '--output', dest='output_tex', help='The output latex file', default='tfe_generated.tex')

# Function to obtain the chapter
regex_chapter = re.compile('Chapitre(.*:)(.*)')
def get_chapter(p):
    m = regex_chapter.match(p)
    if m is not None:
        return m.group(2).strip()
    else:
        return None

# Function to obtain the section
regex_section = re.compile('[0-9]\.[0-9]\)*(.*)')
def get_section(p):
    m = regex_section.match(p)
    if m is not None:
        return m.group(1).strip()
    else:
        return None

# Function to obtain the subsection
regex_subsection = re.compile('[0-9]\.[0-9]\.[0-9]\)*(.*)')
def get_subsection(p):
    m = regex_subsection.match(p)
    if m is not None:
        return m.group(1).strip()
    else:
        return None

regex_talk = re.compile(u'(Moi :|Infirmière :)')
def handle_special_case(paragraph):
    return regex_talk.sub(r'\\textit{\1}', paragraph)

def add_latex_tags(paragraph):
    if paragraph.startswith('-'):
        return '\\item ' + paragraph
    if len(paragraph) > 120:
        return '\\indent ' + handle_special_case(paragraph)
    return handle_special_case(paragraph)

# function defined for my personnal needs."
def convert_to_latex(paragraph):
    if len(paragraph) > 120:
        return add_latex_tags(paragraph) + ' \\\\'
    subsection = get_subsection(paragraph)
    if subsection is not None:
        return '\\subsection{'+ subsection + '}'
    section = get_section(paragraph)
    if section is not None:
        return '\\section{'+ section + '}'
    chapter = get_chapter(paragraph)
    if chapter is not None:
        return '\\chapter{'+ chapter + '}'
    return add_latex_tags(paragraph)

# Main function
def main():
    paragraph_tag = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'
    text_tag = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
    args = parser.parse_args()
    output_file = args.output_tex
    
    if(os.path.exists(args.input_docx)):
        tree = ET.parse(args.input_docx)
        root = tree.getroot()
    else:
        print "Input file not found."
        return
    
    content = ''
    count_p = 0
    for paragraph in root.iter(paragraph_tag):
        p_content = ''
        for child in paragraph.iter(text_tag):
            p_content += child.text
        content += convert_to_latex(p_content)
        content += '\n'
        count_p += 1
    
    print 'Paragraphs parsed: ', count_p
    
    with codecs.open(output_file, 'w', 'utf-8') as f:
        print 'Writing output...',
        f.write(content)
        print ' done.'

if __name__ == '__main__':
    main()
