#!/usr/bin/env python

import collections
import operator
import argparse
import codecs
import sys

parser = argparse.ArgumentParser(
    description='Tool to replace all the 0xa0 character from a file, by a 0x20.')
parser.add_argument('-i', '--input', dest='input_location', help='The file containing the\
                    unicode input', default='tfe_pauline.tex')

def clean_char(char):
    if hex(ord(char)) == '0xa0':
        return ' '
    return char

def main():
    args = parser.parse_args()

    content_cleaned = ""
    try:
        with codecs.open(args.input_location, 'r', 'utf-8') as f:
            print "Reading file..."
            for line in f:
                for c in line:
                    content_cleaned += clean_char(c)
    except:
        print 'Could not read the file %s' % args.input_location
        print 'Exception: %s' % sys.exc_info()[0]
        return
    
    extension = args.input_location[-4:]
    output = args.input_location[:-4] + '_cleaned' + extension
    with codecs.open(output, 'w', 'utf-8') as f:
        print "Writing to %s..." % output
        f.write(content_cleaned)#.encode('UTF-8')


if __name__ == '__main__':
    main()
