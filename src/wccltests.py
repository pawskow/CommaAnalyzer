__author__ = 'pawel'

from wccl import Sentence_create_sent
import os
import subprocess

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

TAG_COMMAND = 'wcrft-app nkjp_e2.ini -i text %s -O %s'
WCCL_COMMAND = 'python wccl-rules.py -A %s -i xces,ann -t nkjp -o ccl < %s'

TMP_TAGGED_FILE = os.path.join(CURR_DIR, "resources/tagged.xml")

def run_rules_on_file(rules_file, input_file):
    if os.path.exists(TMP_TAGGED_FILE):
        os.remove(TMP_TAGGED_FILE)
    abs_rules_file_path = os.path.join(CURR_DIR, rules_file)
    abs_input_file_path = os.path.join(CURR_DIR, input_file)

    full_tag_cmd = TAG_COMMAND %(abs_input_file_path, TMP_TAGGED_FILE)
    full_rules_cmd = WCCL_COMMAND %(abs_rules_file_path, TMP_TAGGED_FILE)
    os.system(full_tag_cmd)
    os.system(full_rules_cmd)



if __name__ == "__main__":
    input_file = "resources/input.txt"
    rules_file = "comma_analyzer/rules/wolaczReguly.ccl"
    run_rules_on_file(rules_file, input_file)