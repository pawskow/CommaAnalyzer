#!/usr/bin/python
# -*- coding: utf-8 -*-
import wccl
import corpus2
TAGSET = 'nkjp'
TAGSET_OBJECT = corpus2.get_named_tagset(TAGSET)


#metody pomocnicze, które mogą być nieużywane narazie, ale trochę mi zajęło zanim doszedłem jak to zrobić,
#więc zostawiam - może się przydadzą
def _get_token_all_classes(token):
    tag = token.get_preferred_lexeme(TAGSET_OBJECT).tag()
    return TAGSET_OBJECT.tag_to_symbol_string(tag).split(',')

def _get_token_classes(token, name):
    tag = token.get_preferred_lexeme(TAGSET_OBJECT).tag()
    mask = corpus2.get_attribute_mask(TAGSET_OBJECT, name)
    return TAGSET_OBJECT.tag_to_symbol_string(tag.get_masked(mask)).split(',')

def _check_token_belong_to_all(token, names):
    values = _get_token_all_classes(token)
    for name in names:
        if not name in values:
            return False
    return True



def _check_token_belong_to_any(token, names):
    values = _get_token_all_classes(token)
    for value in values:
        if value in names:
            return True
    return False

def spojnik_zlozony(asentence, result):
    #wstawia spojniki zlozone
    channel_name = "SpojnikZlozony"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        first_indice = ann.indices[0]
        map(result.add_sure_not_comma, ann.indices)
        if first_indice<1:
            continue #poczatek zdania
        result.add_sure_comma(first_indice-1, channel_name)


def zwykly_spojnik(asentence, result):
    #wstawia spojniki proste
    channel_name = "SpojnikPojedynczy"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    previous_end_index = -1 #wskazuje na koniec poprzedniego spojnika prostego. Potrzebne dla np.: bo kiedy
    for ann in ann_vec:
        first_indice = ann.indices[0]
        if previous_end_index>=first_indice-1 or not asentence.tokens()[first_indice].after_space() or result.sure_not_comma(first_indice-1):
            previous_end_index = ann.indices[-1]
            continue #poczatek zdania, nie ma spacji ("moglby"), juz byl wczesniej spojnik
        previous_end_index = ann.indices[-1]
        zloz = "SpojnikZlozony"
        if zloz not in asentence.all_channels():
             result.add_sure_comma(first_indice-1, channel_name)
        else:
              chan = asentence.get_channel(zloz)
              ann_vec = chan.make_annotation_vector()
              for ann in ann_vec:
                    ann_lenZ = len(ann.indices)
                    first = ann.indices[0]
                    if(first-1<first_indice and (first+ann_lenZ)>first_indice):#jezeli spojnik pojedynczy jest czescia któregos ze zlozonych to olac
                        continue
                    else:
                         if _check_token_belong_to_any(asentence.tokens()[first_indice-1], ["interp"]):
                            continue
                         else:
                            result.add_sure_comma(first_indice-1, channel_name)

def wydzielenie(asentence, result):
    #szuka typowych wyrażeń, które zwyczajowo są wydzielone przecinkami czyli przed i po wyrazeniu wstawiam
    channel_name = "Wydzielenie"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    count=1
    for ann in ann_vec:
        first_indice = ann.indices[0]
        map(result.add_sure_not_comma, ann.indices)
        ann_len = len(ann.indices)
        result.add_sure_comma(first_indice-1+ann_len, channel_name)
        if first_indice<1:
            continue #poczatek zdania
    result.add_sure_comma(first_indice-1, channel_name)

def orzeczenia(asentence, result):
    #próbuje znalezc dwa orzeczenia i jezeli nie ma spojnika badz przecinka pomiedzy nimi to trzeba cos zrobic
    channel_name = "Orzeczenie"
    if not channel_name in asentence.all_channels():
        return
    commas_with_prob = result.get_commas_with_prob(0.5)
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    numberVerb = len(ann_vec)
    if numberVerb>=2:
       idx=0
       while idx<(numberVerb-1):
          first = ann_vec[idx].indices[0]
          second= ann_vec[idx+1].indices[0]
          no_need_of_comma = False
          best_pos = None
          best_prob = 0.
          while first<second and not no_need_of_comma:
            if (_check_token_belong_to_any(asentence.tokens()[first], ['interp','conj'])):
                no_need_of_comma = True
                break #rozdzielony przecinkiem lub spojnikiem
            #jesli jakies sa, to znajdz nejlepiej pasujacy przecinek
            if first in commas_with_prob and commas_with_prob[first]>best_prob:
                best_prob = commas_with_prob[first]
                best_pos = first
            first+=1
          if not no_need_of_comma:
              if best_pos==None:
                 result.add_sure_comma(second-1, channel_name)
              else:
                 result.add_sure_comma(best_pos, channel_name)
          idx+=1


def wyrazenie_srodek(asentence, result):
    #szuka typowych wyrażeń dwuwyrazowych które rozdzielone są przecinkiem
    channel_name = "WyrazenieSrodek"
    if not channel_name in asentence.all_channels():
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()

    for ann in ann_vec:
        first_indice = ann.indices[0]
        if first_indice<1:
            continue #poczatek zdania

    result.add_sure_comma(first_indice, channel_name)

def dwa_podobne_skladniki(asentence, result): #prosta metoda na powtórzenia
  index=1
  tokens = len(asentence.tokens())
  while index<tokens:
      class1 = _get_token_all_classes(asentence.tokens()[index-1])
      class2 = _get_token_all_classes(asentence.tokens()[index])
      if(class1==class2):
          result.add_sure_comma(index-1, "DwiePodobneCzęściMowy")
      index+=1

def dwa_takie_same_wyrazy(asentence, result):
  index=1
  tokens = len(asentence.tokens())
  while index<tokens:
      if asentence.tokens()[index-1].orth_utf8().lower() == asentence.tokens()[index].orth_utf8().lower() and not _check_token_belong_to_any(asentence.tokens()[index], ["interp"]):
          result.add_sure_comma(index-1, "IdentyczneWyrazy")
      index+=1
def miedzy_a(asentence, result):
    channel_name = "Miedzy"
    if not asentence.has_channel(channel_name):
        return

    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()

    for ann in ann_vec:
        first_indice = ann.indices[0]
        idx = first_indice
        length = len(asentence.tokens())
        while idx<length:
            if(asentence.tokens()[idx].orth_utf8().lower()=='a'):
               result.add_sure_not_comma(idx-1)
            idx+=1



def ani_powtorzenie(asentence,result):

    channel_name = "PowtorzeniaANI"
    if not asentence.has_channel(channel_name):
        return

    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()

    if(len(ann_vec)<2):
        return
    count=0
    for ann in ann_vec:
        first_indice = ann.indices[0]
        if(count>0):
               result.add_sure_comma(first_indice-1, channel_name)
        count=count+1
def porownania(asentence, result):
    channel_name = "Porownania"
    if not asentence.has_channel(channel_name):
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    wyrazenie_wykluczajace = ['bądź','czy','ani','lub','albo','oraz','i']
    wyrazenie_wykluczajace2 = ['gdyby','i']
    for ann in ann_vec:
        first_indice = ann.indices[0]
        index = first_indice
        length = len(asentence.tokens())
        while index<length:
            if asentence.tokens()[index].orth_utf8().lower() in wyrazenie_wykluczajace:
                return
            if(asentence.tokens()[index].orth_utf8().lower()=="jak"):
                 if not asentence.tokens()[index+1].orth_utf8().lower() in wyrazenie_wykluczajace2:
                   result.add_sure_comma(index-1, channel_name)
            index+=1

def bez_przecinka_po(asentence, result):
    channel_name = "BezPrzecinkaPo"
    if not asentence.has_channel(channel_name):
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        last_index = ann.indices[-1]
        result.add_sure_not_comma(last_index)

def wolacz_na_poczatku_zdania(asentence, result):
    channel_name = "WolaczRzeczownik"
    podzdanie_channel_name = "PodzdanieZCzasownikiemNaPoczatku"
    if not asentence.has_channel(channel_name):
        return


    #wolacz na poczatku zdania, wiec patrzymy tylko do początku pierwszego podzdania z czasownikiem!
    if asentence.has_channel(podzdanie_channel_name):
        podzdanie_chan = asentence.get_channel(podzdanie_channel_name)
        podzdanie_ann_vec = podzdanie_chan.make_annotation_vector()
        first_podzdanie_end = podzdanie_ann_vec[0].indices[0] #pierwszy czasownik
    else:
        first_podzdanie_end = len(asentence.tokens())

    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    last_annotation = ann_vec[-1] #znajdz ostatni
    last_index  = last_annotation.indices[0] # ma tylko jedno
    if last_index > first_podzdanie_end:
        return

    tokens = len(asentence.tokens())
    token = asentence.tokens()[last_index]
    class_names = _get_token_classes(token, 'gnd') + _get_token_classes(token, 'nmb') #wez rodzaj i liczbe tego wolacza

    #znajdz ostatni przymiotnik pasujacy do wolacza

    place_to_put = last_index
    sure_commas = result.get_sure_commas()
    while last_index<first_podzdanie_end-1:
        if last_index in sure_commas:
            return #olej calosc jesli trafisz przecinek po drodze
        if _check_token_belong_to_any(asentence.tokens()[last_index+1], ['pos', 'com', 'sup']):
            place_to_put = last_index+1
            if not _check_token_belong_to_all(asentence.tokens()[last_index+1], class_names):
                break
        last_index+=1
    result.add_sure_comma(place_to_put, channel_name)

def mozliwy_rozdzielacz(asentence, result):
    channel_name = "Rozdzielacz"
    if not asentence.has_channel(channel_name):
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        first_index = ann.indices[0]
        result.add_comma(first_index-1, 0.6, "Rozdzielacz")

def bez_przecinka_pomiedzy(asentence, result):
    #wstawia spojniki zlozone
    channel_name = "BezPrzecinkaPomiedzy"
    if not asentence.has_channel(channel_name):
        return
    chan = asentence.get_channel(channel_name)
    ann_vec = chan.make_annotation_vector()
    for ann in ann_vec:
        map(result.add_sure_not_comma, ann.indices)