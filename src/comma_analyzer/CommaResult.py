#!/usr/bin/python
# -*- coding: utf-8 -*-

class CommaResult(object):
    def __init__(self):
        self.__commas = []

    def get_commas(self):
        return self.__commas

    def add_sure_comma(self, idx, comment=""):
        self.__commas.append((idx, 1., comment))

    def add_comma(self, idx, prob, comment=""):
        self.__commas.append((idx, prob, comment))

    def get_sure_commas(self):
        sure_commas = set()
        for idx, prob, comment in self.__commas:
            if int(prob)==1:
                sure_commas.add(idx)
        return sure_commas

    def optimise_probabilities(self):
        new_commas_dict = {}
        for idx, prob, comment in self.__commas:
            if not idx in new_commas_dict:
                new_commas_dict[idx] = (prob, comment)
            else:
                (old_prob, old_comment) = new_commas_dict[idx]
                if old_prob<prob:
                    new_commas_dict[idx] = (prob, comment)

        new_commas = []
        for key, value in new_commas_dict.iteritems():
            new_commas.append((key, value[0], value[1]))
        self.__commas = new_commas