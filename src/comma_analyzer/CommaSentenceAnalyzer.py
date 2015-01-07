#!/usr/bin/python
# -*- coding: utf-8 -*-
import corpus2
import wccl

from comma_analyzer import get_wccl_files, RULES_DIR, DEBUG
from CommaResult import CommaResult
from comma_analyzer import comma_input_methods


TAGSET = 'nkjp'
INPUT_FORMAT = 'xces,ann'

#tutaj wrzucamy metody do odpalania w odpowiedniej kolejnosci
COMMA_INPUT_METHODS = [
                        comma_input_methods.bez_przecinka_po,
                        comma_input_methods.mozliwy_rozdzielacz,
                        comma_input_methods.spojnik_zlozony,
                        comma_input_methods.wydzielenie,
                        comma_input_methods.miedzy_a,
                        comma_input_methods.zwykly_spojnik,
                        comma_input_methods.wyrazenie_srodek,
                        comma_input_methods.wolacz_na_poczatku_zdania,
                        #comma_input_methods.dwa_podobne_skladniki,
                        comma_input_methods.dwa_takie_same_wyrazy,
                        comma_input_methods.orzeczenia,
                        comma_input_methods.ani_powtorzenie,
                        comma_input_methods.porownania


                    ]

class CommaSentenceAnalyzer(object):

    def __init__(self):
        self.__wccl_files = []
        tagset = corpus2.get_named_tagset(TAGSET)
        p = wccl.Parser(tagset)
        for f in get_wccl_files():
            self.__wccl_files.append(p.parseWcclFileFromPath(f, RULES_DIR))

    def do(self, sentence):
        asent = corpus2.AnnotatedSentence.wrap_sentence(sentence)
        for wccl_f in self.__wccl_files:
            match_rules = wccl_f.get_match_rules_ptr()
            match_rules.apply_all(asent)
        if DEBUG:
            print self.get_string_sentence(asent)
            print asent.annotation_info()


        result = CommaResult()

        for comma_method in COMMA_INPUT_METHODS:
            comma_method(asent, result)
        self.__make_last_decisions(asent, result)
        if DEBUG:
            print result.get_commas()
        return self.__get_string_sentence_with_commas(asent, result)


    def __make_last_decisions(self, asent, result):
        result.optimise_probabilities()
        commas = result.get_commas()
        new_commas = []
        for idx, prob, comment in commas:
            if prob<1.0 and prob>=0.7:
                new_commas.append((idx, comment))
        for  idx, comment in new_commas:
            result.add_sure_comma(idx, comment)
        result.optimise_probabilities()


    def __get_string_sentence_with_commas(self, asent, result):
        sure = result.get_sure_commas()
        string_result = ""
        for idx, token in enumerate(asent.tokens()):
            if idx>0 and token.after_space():
                string_result += " "
            string_result += token.orth_utf8()
            if idx in sure:
                string_result += ","
        return string_result

    def get_string_sentence(self, asent):
        string_result = ""
        for idx, token in enumerate(asent.tokens()):
            if idx>0 and token.after_space():
                string_result += " "
            string_result += token.orth_utf8()
        return string_result