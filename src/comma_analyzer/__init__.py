#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

DEBUG = True
PRINT_ANNOTATED_FILE = True

__CURR_DIR__ = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = os.path.join(__CURR_DIR__, "rules")
__WCCL_FILES = []
__WCCL_IN_ORDER = ['SpojnikZlozony.txt', 'rules.ccl', 'wolaczReguly.ccl']

RULE_PARTS = [
"""match_rules(
""",
"""apply(
        match(
""",
"            equal(lower(base[0]), \"%s\")",
"""
        ),
        actions(
            mark(M, "%s")
        )
    )""",
")"
]

def generate(file_path):
    dest_file_path = '%s.ccl' %file_path.rsplit(os.path.extsep, 1)[0]
    rule_name = os.path.basename(file_path).rsplit(os.path.extsep, 1)[0]
    with open(os.path.join(RULES_DIR, file_path), "r") as w_f:
        with open(os.path.join(RULES_DIR, dest_file_path), "w") as r_f:
            r_f.write(RULE_PARTS[0])
            first_line = True
            for l in w_f.readlines():
                if not first_line:
                    r_f.write(";\n")
                r_f.write(RULE_PARTS[1])

                words_rules = map(lambda w: (RULE_PARTS[2] %w), l.strip().split(" "))
                r_f.write(',\n'.join(words_rules))
                r_f.write(RULE_PARTS[3] %rule_name)
                first_line = False
            r_f.write(RULE_PARTS[4])
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