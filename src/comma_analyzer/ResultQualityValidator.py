#!/usr/bin/python
# -*- coding: utf-8 -*-

class ResultQualityValidator(object):
    def __init__(self):
        self.__correct = 0
        self.__incorrect = 0
        self.__missing = 0

    def check_sentence(self, orig, result):
        longer_length = max(len(orig), len(result))
        orig_length = len(orig)
        result_length = len(result)
        orig_ind = 0
        result_ind = 0

        curr_correct = 0
        curr_incorrect = 0
        should_be = 0

        while result_ind<result_length or orig_ind<orig_length:
            if result_ind<result_length and orig_ind<orig_length and orig[orig_ind] == result[result_ind] == ',':
                curr_correct += 1
                orig_ind+=1
                result_ind+=1
                should_be+=1
            elif orig_ind<orig_length and orig[orig_ind] == ',':
                orig_ind+=1
                should_be+=1
            elif result_ind<result_length and result[result_ind] == ',':
                curr_incorrect+=1
                result_ind+=1
            else:
                orig_ind+=1
                result_ind+=1
        curr_missing = max(0, should_be - (curr_correct+curr_incorrect))
        self.__correct += curr_correct
        self.__incorrect += curr_incorrect
        self.__missing += curr_missing
        print curr_correct, curr_incorrect, curr_missing
        print ""

    def get_correct(self):
        return self.__correct


    def get_incorrect(self):
        return self.__incorrect


    def get_missing(self):
        return self.__missing
