# -*- coding: UTF-8 -*-
__author__ = 'Lenovo'
import json
from json import JSONDecoder, JSONEncoder

# TO DO: good exception handling - not prints!

class TextEntry(object):
    ''' Class for RuThes text entry representation. '''
    def __init__(self, id=None, name=None, lemma=None, te_root = None):
        self.id = id            #int
        self.name = name        #unicode string
        self.lemma = lemma      #unicode string
        if te_root:
            self.fill_te_fields(te_root)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return  self.id == other.id

    def fill_te_fields(self, te_root):
        if self.lemma:
            entry = te_root.find(".*[lemma='%s']" % self.lemma.upper())
            if entry:
                self.name = entry[0].text.lower()
                self.id = int(entry.get('id'))
            else:
                print "Error: no word '%(lemma)s' in text_entry.xml" % self.__dict__

    def get_syn_concepts(self, syn_root, concept_root):
        concepts = syn_root.findall('./entry_rel[@entry_id="%(id)d"]' % self.__dict__)
        self.concepts = [Concept(id=int(concept.get('concept_id')), concept_root=concept_root) for concept in concepts]
        return self.concepts

    # def set_w2v_value(self, w2v_sim, cand_word):
    #     self.w2v_sim = w2v_sim
    #     self.cand_word = cand_word


class Concept(object):
    ''' Class for RuThes concept representation. '''
    def __init__(self, id=None, name=None, concept_root=None):
        self.id = id
        self.name = name
        self.text_entries = []
        if concept_root:
            self.fill_concept_fields(concept_root)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return  self.id == other.id

    def fill_concept_fields(self, concept_root):
        if self.id:
            concept = concept_root.find('./concept[@id="%(id)d"]' % self.__dict__)  #if hadn'd found: return None or raise exception?
            if concept:
                self.name = concept[0].text.lower()
            else:
                print "Error: no concept with id '%(id)d'" % self.__dict__
        else:
            print "the concept id is None" # TO DO: good exception handling - not prints!


    def get_syn_entries(self):
        pass

    def get_rel_concepts(self, rel_root, concept_root, rel_types):
        if self.id:
            for rel_type in rel_types:
                c_ids = rel_root.findall('./rel[@from="%d"][@name="%s"]' % (self.id, rel_type))
                if c_ids:
                     return [Concept(id=int(c_id.get('to')), concept_root=concept_root) for c_id in set(c_ids)]
                else:
                    return []
        print "the concept id is None"
        return None

    def sort_text_entries(self, key):
        self.text_entries.sorted(key=key)

    def te_w2v_sum(self):
        sum([entry.w2v for entry in self.text_entries])

    def te_w2v_mean(self):
        self.te_w2v_sum() / len(self.text_entries)


class CandidateWord(object):
    ''' Class for word - candidate for embedding to small thesaurus. '''
    def __init__(self, lemma, concepts=None):
        self.lemma = lemma  #unicode string
        if concepts == None:
            self.concepts = []            #set()
        else:
            self.concepts = concepts

    def get_concepts_for_binding(self, te_tree, syn_tree,
                                 concept_tree, rel_tree, model):
        ''' For each embeddable word find most similar (according to word2vec) text entries and
        get their concepts. Then add concepts which are connected with last obtained concepts
        by 'rel_type'. Last operation repeat recursively as deep as 'depth'.
        Return all founded concepts. '''
        def get_small_thes(te_root):
            return [lemma.text.lower() for lemma in te_root.iter('lemma') if ' ' not in lemma.text]

        def most_similar(word, model, topn=10):
            """
            Returns 'topn' words contained in small thesaurus and most similar to 'word'
            (according to word2vec).
            'model_path' is the path to the trained word2vec model.
            """
            sim_words = model.most_similar(positive=[word.encode('utf-8')], topn=200)
            uni_sim_words = [(word.decode('utf-8'), w2v_sim) for (word, w2v_sim) in sim_words]

            te_root = te_tree.getroot()
            small_thes = get_small_thes(te_root)
            thes_sim_words = [(entry_lemma, w2v_sim) for (entry_lemma, w2v_sim) in uni_sim_words
                                       if entry_lemma in small_thes]
            topn_similar_entries = [TextEntry(lemma=entry_lemma, te_root=te_root)
                                    for (i, (entry_lemma, w2v_sim)) in enumerate(thes_sim_words) if i < topn]
            #self.first_step_entries = topn_similar_entries
            return topn_similar_entries

        def add_higher_concepts(concepts, rec_depth, rel_root, concept_root, rel_types=[u'ВЫШЕ']):
            def rec_helper(concepts, rec_depth):
                if rec_depth > 0:
                    for concept in concepts:
                        higher_concepts = concept.get_rel_concepts(rel_root, concept_root, rel_types)
                        self.concepts.extend(higher_concepts)
                        rec_helper(higher_concepts, rec_depth-1)
            rec_helper(concepts, rec_depth)
            self.concepts = list(set(self.concepts))

        sim_entries = most_similar(self.lemma, model)
        first_step_concepts = []
        for entry in sim_entries:
            first_step_concepts.extend(entry.get_syn_concepts(syn_tree.getroot(), concept_tree.getroot()))

        add_higher_concepts(first_step_concepts, 2, rel_tree.getroot(), concept_tree.getroot())

    def sort_concepts(self, key):
        self.concepts.sorted(key=key)
