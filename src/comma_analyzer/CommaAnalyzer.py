#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from tempfile import mkstemp

import corpus2
from comma_analyzer.CommaSentenceAnalyzer import CommaSentenceAnalyzer
from comma_analyzer import PRINT_ANNOTATED_FILE

TAGSET = 'nkjp'
INPUT_FORMAT = 'xces,ann'

TAG_COMMAND = 'wcrft-app nkjp_e2.ini -i text %s -O %s'

class CommaAnalyzer(object):
    def __init__(self, file_path):
        tagset = corpus2.get_named_tagset(TAGSET)

        tagged_file_path = self.get_tagged_file_path(file_path)
        if PRINT_ANNOTATED_FILE:
            with open(tagged_file_path, "r") as f:
                for l in f.readlines():
                    print l.rstrip()
                print "\n\n\n"
        self.__reader = corpus2.TokenReader.create_path_reader(INPUT_FORMAT, tagset, tagged_file_path)
        self.__sentence_analyzer = CommaSentenceAnalyzer()

    def done_sentences(self):
        while True:
            sent = self.__reader.get_next_sentence()
            if not sent:
                break # end of input
            res = self.__sentence_analyzer.do(sent)
            yield res

    def raw_sentences(self):
        while True:
            sent = self.__reader.get_next_sentence()
            if not sent:
                break # end of input
            res = self.__sentence_analyzer.get_string_sentence(sent)
            yield res

    def get_tagged_file_path(self, file_path):
        os_handle = mkstemp()
        full_tag_cmd = TAG_COMMAND %(file_path, os_handle[1])
        os.system(full_tag_cmd)
        return os_handle[1]