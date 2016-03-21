# -*- coding: UTF-8 -*-
__author__ = 'Lenovo'
import re, os, sys
import collections, yaml

def parse_input(mi_path, mi_yaml_path):
    with open(mi_path) as input_file:
        with open(mi_yaml_path, 'w') as output_file:
            text_entries = {}
            dic = {}

            for l in input_file:
                line = l.decode('utf-8')
                #print line
                #line = l
                if len(line) > 1:
                    if '.' not in line:
                        if text_entries:
                            dic[word] = text_entries
                            text_entries = {}
                        word = line.rstrip()
                    else:
                        xs = line.split()
                        text_entry = ' '.join(xs[:-2])

                        text_entries[text_entry] = text_entries.get(text_entry, []) + xs[-2:]
            yaml.dump(dic, output_file)
            #print yaml.dump(dic)

# def parse_input(mi_path, mi_yaml_path):
#     with open(mi_path) as input_file:
#         with open(mi_yaml_path, 'w') as output_file:
#             text_entries = []
#             dic = []
#
#             for l in input_file:
#                 #line = l.decode('utf-8')
#                 #print line
#                 line = l
#                 if len(line) > 1:
#                     if '.' not in line:
#                         if text_entries:
#                             dic.append([word, text_entries])
#                             text_entries = []
#                         word = line.rstrip()
#                     else:
#                         xs = line.split()
#                         text_entry = ' '.join(xs[:-2])
#
#                         text_entries.append([text_entry, xs[-2:]])
#             yaml.dump(dic, output_file)

def main():
    script_dir = os.getcwd()
    parent_dir = os.path.split(script_dir)[0]

    cands_dir = os.path.join(parent_dir, 'similar')
    mi_path =  os.path.join(cands_dir, 'common_parents96.txt')
    mi_yaml_path =  os.path.join(cands_dir, 'common_parents_yaml3.txt')
    parse_input(mi_path, mi_yaml_path)

main()