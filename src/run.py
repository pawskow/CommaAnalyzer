#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from comma_analyzer.CommaAnalyzer import CommaAnalyzer

DEFAULT_FILE_NAME = 'input.txt'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = DEFAULT_FILE_NAME

    ca = CommaAnalyzer(file_name)
    done = []
    for s in ca.done_sentences():
        done.append(s)
    print "\nwynik:"
    for s in done:
        print s
