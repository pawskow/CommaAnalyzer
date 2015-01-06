#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from comma_analyzer.CommaAnalyzer import CommaAnalyzer

DEFAULT_FILE_NAME = 'input.txt'
RESULT_DIR = 'result'


def create_file_without_commas(file_path):
    sec_file_path = file_path+"_no_commas"
    with open(file_path, "r") as f_read:
        with open(sec_file_path, "w") as f_write:
            for l in f_read.readlines():
                f_write.write(l.replace(",", ""))
    return sec_file_path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = DEFAULT_FILE_NAME

    no_comma_file_path = create_file_without_commas(file_name)


    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    input_result_file = os.path.join(RESULT_DIR, "input.txt")
    output_result_file = os.path.join(RESULT_DIR, "output.txt")



    original_ca = CommaAnalyzer(file_name)
    analyzed_ca = CommaAnalyzer(no_comma_file_path)

    original_sentences = original_ca.raw_sentences()
    analyzed_sentences = analyzed_ca.done_sentences()

    with open(input_result_file, "w") as f_original:
        with open(output_result_file, "w") as f_analyzed:


            for original_sentence in original_sentences:
                analyzed_sentence = analyzed_sentences.next()
                f_original.write(original_sentence+'\n')
                f_analyzed.write(analyzed_sentence+'\n')
                print original_sentence
                print analyzed_sentence

