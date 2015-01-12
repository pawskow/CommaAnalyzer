#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

DEBUG = False
PRINT_ANNOTATED_FILE = False

__CURR_DIR__ = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = os.path.join(__CURR_DIR__, "rules")
__WCCL_FILES = []
__WCCL_IN_ORDER = ['BezPrzecinkaPo.txt','BezPrzecinkaPomiedzy.txt','Rozdzielacz.txt','SpojnikZlozony.txt','Wydzielenie.txt','WyrazenieSrodek.txt','Miedzy.txt','Porownania.txt','PowtorzeniaANI.txt', 'SpojnikPojedynczy.txt' ,'rules.ccl', 'wolaczReguly.ccl',]

RULE_PARTS = [
"""match_rules(
""",
"""apply(
        match(
""",
"""            optional(inter(class[0], {prep})),
""",
"            equal(lower(base[0]), \"%s\")",
"""
        ),
        cond(
            not(isannpart(first(M), "%s"))
        ),
        actions(
            remark(M, "%s")
        )
    )""",
")"
]

def generate(file_path):
    dest_file_path = '%s.ccl' %file_path.rsplit(os.path.extsep, 1)[0]
    rule_name = os.path.basename(file_path).rsplit(os.path.extsep, 1)[0]
    add_prep_rule = False
    with open(os.path.join(RULES_DIR, file_path), "r") as w_f:
        with open(os.path.join(RULES_DIR, dest_file_path), "w") as r_f:
            r_f.write(RULE_PARTS[0])
            first_line = True
            for l in w_f.readlines():
                if first_line and l.startswith("#optional_prep"):
                    add_prep_rule = True
                    continue
                if not first_line:
                    r_f.write(";\n")
                r_f.write(RULE_PARTS[1])
                if add_prep_rule:
                    r_f.write(RULE_PARTS[2])
                words_rules = map(lambda w: (RULE_PARTS[3] %w), l.strip().split(" "))
                r_f.write(',\n'.join(words_rules))
                r_f.write(RULE_PARTS[4] %(rule_name,rule_name))
                first_line = False
            r_f.write(RULE_PARTS[5])
    __WCCL_FILES.append(dest_file_path)

def generate_rules():
    for f_name in __WCCL_IN_ORDER:
        if(f_name.endswith("ccl")):
            __WCCL_FILES.append(f_name)
        else:
            generate(f_name)

def get_wccl_files():
    return map(lambda x: os.path.join(RULES_DIR, x), __WCCL_FILES)

generate_rules()