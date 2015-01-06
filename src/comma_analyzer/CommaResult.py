#!/usr/bin/python
# -*- coding: utf-8 -*-

class CommaResult(object):
    def __init__(self):
        self.__commas = []
        self.__sure_not_commas = set()

    def get_commas(self):
        return self.__commas

    def add_sure_comma(self, idx, comment="", force=False):
        self.add_comma(idx, 1., comment, force)

    def add_comma(self, idx, prob, comment="", force=False):
        if not force and idx in self.__sure_not_commas:
            return
        self.__commas.append((idx, prob, comment))

    def get_sure_commas(self):
        return self.get_commas_with_prob(1.)

    def get_commas_with_prob(self, given_prob):
        commas = set()
        for idx, prob, comment in self.__commas:
            if prob>=given_prob:
                commas.add(idx)
        return commas

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

    def add_sure_not_comma(self, ind):
        return self.__sure_not_commas.add(ind)

    def sure_not_comma(self, ind):
        return ind in self.__sure_not_commas

