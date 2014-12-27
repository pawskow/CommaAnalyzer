#!/usr/bin/python
# -*- coding: utf-8 -*-

def spojnik_zlozony(asentence, result):
    #wstawia spojniki zlozone
    channel_name = "SpojnikZlozony"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        first_indice = ann.indices[0]
        if first_indice<1:
            continue #poczatek zdania
        result.add_sure_comma(first_indice-1, channel_name)


def zwykly_spojnik(asentence, result):
    #wstawia spojniki proste
    channel_name = "Spojnik"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        first_indice = ann.indices[0]
        if first_indice<1:
            continue #poczatek zdania
        result.add_sure_comma(first_indice-1, channel_name)