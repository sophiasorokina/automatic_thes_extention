# -*- coding: UTF-8 -*-
__author__ = 'Lenovo'
import gensim, logging
from os import getcwd
import os.path as path
#import cPickle
#import json
import jsonpickle
import xml.etree.cElementTree as et
from classes import CandidateWord, Concept, TextEntry

def main():
    project_path = path.split(getcwd())[0]
    ruthes_path = path.join(project_path, 'ruthes2015')
    thes_full_path = path.join(ruthes_path, 'thes_full.txt')
    model_path = path.join(project_path, 'models', 'model_big morph right hyphen.txt')

    te_tree = et.parse(path.join(ruthes_path, 'text_entry.xml'))
    syn_tree = et.parse(path.join(ruthes_path, 'synonyms.xml'))
    concept_tree = et.parse(path.join(ruthes_path, 'concepts.xml'))
    rel_tree = et.parse(path.join(ruthes_path, 'relations.xml'))

    thes_full = []
    with open(thes_full_path) as file:
        for line in file:
            thes_full.append(line.decode('mac_cyrillic').rstrip())

    embed_words = ['мчс','цска','мкс','втб','ммвб','кпрф','егэ','мкад','ввп','нтв','газпром','единоросс',
                   'европарламент','каско','цру','грэс','блогер','блог','роснефть','евровидение','автоледи',
                   'авиабилет','мосгордума','ндфл','днепропетровщина','блоггер','еврооблигация', 'миноритарий', 'эрмитаж','ижевчанка','сумщина','рэпер','коап','эпилепсия']

    # concepts_for_binding = get_concepts_for_binding(embed_words, text_entry_tree,
    #                                                 synonym_tree, concept_tree,
    #                                                 relation_tree, model_path)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = gensim.models.Word2Vec.load(model_path)

    candidate_words = [CandidateWord(word.decode('utf-8')) for word in embed_words]
    for cand_word in candidate_words:
        cand_word.get_concepts_for_binding(te_tree,syn_tree, concept_tree,
                                           rel_tree, model)

    out_pickle_path = path.join(project_path, 'temp',
                            'concepts for bindings with first-step synonyms3.txt')
    with open(out_pickle_path, 'w') as output_file:
        output_file.write(jsonpickle.encode(candidate_words))

if __name__ == '__main__':
    main()
    import winsound
    # Play Windows exit sound.
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)