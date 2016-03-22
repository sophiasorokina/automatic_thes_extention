__author__ = 'Lenovo'
from os import getcwd
from os.path import join, split
#import os.path as path
import jsonpickle, yaml     #use json or just jsonpickle instead yaml
import xml.etree.cElementTree as et
import gensim, logging
from classes import CandidateWord

#TO DO: something with temp files - they are awful

def main():
    proj_path = split(getcwd())[0]

    ruthes_path = join(proj_path, 'ruthes2015')
    syn_tree = et.parse(join(ruthes_path, 'synonyms.xml'))
    te_tree = et.parse(join(ruthes_path, 'text_entry.xml'))
    concept_tree = et.parse(join(ruthes_path, 'concepts.xml'))
    rel_tree = et.parse(join(ruthes_path, 'relations.xml'))

    temp_path = join(proj_path, 'temp')
    with open(join(temp_path, 'concepts for bindings with first-step synonyms2.txt')) as file:
        raw_data = file.read()
    candidate_words = jsonpickle.decode(raw_data)

    # with open(join(temp_path, 'mutual_freqs.yml')) as file:
    #     mutual_freqs = yaml.load(file)
    # with open(join(temp_path, 'pmi_w2v.yml')) as input_file:
    #     pmi_w2v = yaml.load(input_file)
    with open(join(temp_path, 'frequent_entries.yml')) as file:
        frequent_entries = yaml.load(file)

    model_path = join(proj_path, 'models', 'model_big morph right hyphen.txt')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = gensim.models.Word2Vec.load(model_path)

    #for each concept find related entries with frequences > freq_bound
    for word in candidate_words:
        for concept in word.concepts:
            #concept.get_syn_entries(syn_tree.getroot(), te_tree.getroot(), freq_bound=100, freqs=None)
            concept.get_syn_entries(syn_tree.getroot(), te_tree.getroot(), word.lemma, model, frequent_entries) #pmi_w2v, mutual_freqs
            #concept.sort_text_entries()
            break
        break

    out_pickle_path = join(proj_path, 'temp', 'concepts_for_binding_with_te2.txt')
    with open(out_pickle_path, 'w') as output_file:
        output_file.write(jsonpickle.encode(candidate_words))

if __name__ == '__main__':
    main()
    import winsound
    # Play Windows exit sound.
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)