#!/usr/bin/env python

'''
stickyex - a command-line utility to export the Mac Stickies database to files.
Copyright (C) 2018  Andy Poo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License (LGPL) as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for a description of the LGPL.
'''

import re
import os

# destination location of where to write the exported files
dst = '/Documents/stickyex/'

# patterns of formatting codes to strip from the Stickies file
pat = re.compile(r'\\')
pat1 = re.compile(r'\\fs[\d]*')
pat2 = re.compile(r'(\\expnd[\d]|\\expndtw[\d]|\\kerning[\d]|deftab[\d]*)')
pat3 = re.compile(r'\\c[bf][\d]*')
pat4 = re.compile(r'(f0 |\'a0)')
pat5 = re.compile(r'(\\red[\d]+|\\green[\d]+|\\blue[\d]+)')
pat6 = re.compile(r'uc?[\d]+')
pat7 = re.compile(r'}$')
pat8 = re.compile(r';$')
pat9 = re.compile(r'^(css|csgeneric|rgbc)')

def main():
    global dst

    # your home directory
    home = os.environ['HOME']

    # location of the Stickies file
    fn = home + '/Library/StickiesDatabase'
    try:
        fp = open(fn, 'rb')
    except Exception as e:
        print(e)
        return -1

    # make the destination directory
    dst = home + dst
    if not os.path.isdir(dst):
        try:
            os.mkdir(dst)
        except Exception as e:
            print(e)

    # we need an initial name for the first exported file
    fn = dst + "STICKY-0.txt"

    # open it for creation
    try:
        out = open(fn, 'w')
    except Exception as e:
        print(e)
        return -1

    # track which note we are on and use a state machine to detect the start of a new note
    count = 0
    state = 0
    for line in fp:
        # is this the start of a new note?
        if '}\x01' in line:
            count += 1
            state = 1
            continue

        # discard all formatting codes
        if '{\\' in line:
            continue
        text = line
        if '\\pard' in line:
            continue
        text = pat1.sub('', text)
        #print text
        text = pat2.sub('', text)
        text = pat3.sub('', text)
        text = pat4.sub('', text)
        text = pat5.sub('', text)
        text = pat6.sub('', text)
        text = pat7.sub('', text)
        text = pat8.sub('', text)
        text = pat.sub('', text)
        text = text.strip(';')
        text = text.strip()
        if text and not pat9.search(text):
            if state:
                # this was the start of a new note
                state = 0

                # create a file name for the exported note
                # using the first 40 alphanumeric characters of the note
                fn = ''
                for c in text:
                    if c.isalnum():
                        fn += c
                fn = fn[:40]
                fn = dst + "STICKY-%s-%d.txt" % (fn, count)
                try:
                    # close the previous exported note and open the new one
                    out.close()
                    out = open(fn, 'w')
                except Exception as e:
                    print(e)
                # write the text from the note to the exported file
                print(text, file=out)
            else:
                print(text, file=out)
    # close open files
    fp.close()
    out.close()

# are we running this file from the command line?
if __name__ == '__main__':
    main()