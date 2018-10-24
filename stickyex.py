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

dst = '/Documents/stickyex/'

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
    home = os.environ['HOME']
    fn = home + '/Library/StickiesDatabase'
    try:
        fp = open(fn, 'rb')
    except Exception as e:
        print e
        return -1
    dst = home + dst
    if not os.path.isdir(dst):
        try:
            os.mkdir(dst)
        except Exception as e:
            print e
    fn = dst + "STICKY-0.txt"
    try:
        out = open(fn, 'w')
    except Exception as e:
        print e
        return -1
    count = 0
    state = 0
    #print >> out, fn
    for line in fp:
        #print >> out, line
        if '}\x01' in line:
            count += 1
            state = 1
            #print >> out, ('@'*40)+'\n%d' % count
            continue
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
        #text = pat9.sub('', text)
        text = pat.sub('', text)
        text = text.strip(';')
        text = text.strip()
        if text and not pat9.search(text):
            if state:
                state = 0
                fn = ''
                for c in text:
                    if c.isalnum():
                        fn += c
                fn = fn[:40]
                fn = dst + "STICKY-%s-%d.txt" % (fn, count)
                try:
                    out.close()
                    out = open(fn, 'w')
                except Exception as e:
                    print e
                print >> out, text
            else:
                print >> out, text
    fp.close()
    out.close()

if __name__ == '__main__':
    main()
