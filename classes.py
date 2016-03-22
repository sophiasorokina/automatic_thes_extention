# -*- coding: UTF-8 -*-
__author__ = 'Lenovo'
import json
from json import JSONDecoder, JSONEncoder

# TO DO: good exception handling - not prints!
#       change Concept.get_syn_entries() - it sucks

class TextEntry(object):
    ''' Class for RuThes text entry representation. '''
    def __init__(self, id=None, name=None, lemma=None, te_root = None, word=None, pmi_w2v=None): #TODO normal parameters, * or ** then check if there is such a var in dict. Or even a cycle py existing vars
        self.id = id            #int
        self.name = name        #unicode string
        self.lemma = lemma      #unicode string
        self.word = word
        if te_root:
            self.fill_te_fields(te_root, pmi_w2v)
        # if pmi:
        #     self.pmi = pmi
        # if w2v:
        #     self.w2v = w2v

    # def __hash__(self):
    #     return self.id
    #
    # def __eq__(self, other):
    #     return  self.id == other.id

    def fill_te_fields(self, te_root, pmi_w2v=None):
        if self.lemma:
            entry = te_root.find(".*[lemma='%s']" % self.lemma.upper())
            if entry:
                self.name = entry[0].text.lower()
                self.id = int(entry.get('id'))
            else:
                print "Error: no word '%(lemma)s' in text_entry.xml" % self.__dict__
        elif self.id:
            entry = te_root.find("./entry[@id='%(id)d']" % self.__dict__)
            if entry:
                self.name = entry[0].text.lower()
                self.lemma = entry[1].text.lower()
            else:
                print "Error: no word with id '%(id)s' in text_entry.xml" % self.__dict__
        if pmi_w2v:
            #print pmi_w2v[self.word]
            self.w2v_sim = float(pmi_w2v[self.word].get(self.lemma, [u'-1', u'-1'])[1])
        # if model:
        #     self.w2v_sim = -1
        #     try:
        #         s = model.n_similarity([self.word.encode('utf-8')], self.lemma.encode('utf-8').split())
        #     except KeyError:
        #         s = 0
        #     if s:
        #         self.w2v_sim = 3
                #print 'No w2v entry for word "%(word)s"' % self.__dict__

    def get_syn_concepts(self, syn_root, concept_root):
        entry_rels = syn_root.findall('./entry_rel[@entry_id="%(id)d"]' % self.__dict__)
        self.concepts = [Concept(id=int(entry_rel.get('concept_id')), concept_root=concept_root) for entry_rel in entry_rels]
        return self.concepts

    # def set_w2v_value(self, w2v_sim, cand_word):
    #     self.w2v_sim = w2v_sim
    #     self.cand_word = cand_word


class Concept(object):
    ''' Class for RuThes concept representation. '''
    def __init__(self, id, name='', concept_root=None, text_entries=None):
        self.id = id
        self.name = name
        if concept_root:
            self.fill_concept_fields(concept_root)
        if text_entries:
            self.text_entries = text_entries
        else:
            self.text_entries = []

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return  self.id == other.id

    def fill_concept_fields(self, concept_root):
        concept = concept_root.find('./concept[@id="%(id)d"]' % self.__dict__)  #if hadn'd found: return None or raise exception?
        if concept:
            self.name = concept[0].text.lower()
        else:
            print "Error: no concept with id '%(id)d'" % self.__dict__

    #def get_syn_entries(self, syn_root, te_root, freq_bound=None, freqs=None):
    def get_syn_entries(self, syn_root, te_root, word, pmi_w2v, frequent_entries=None): #pmi_w2v, mutual_freqs,
        ''' For each concept find related entries with frequences > freq_bound. '''
        entry_rels = syn_root.findall('./entry_rel[@concept_id="%(id)d"]' % self.__dict__)
        if frequent_entries:
            #self.text_entries = [TextEntry(id=int(entry_rel.get('entry_id')), te_root=te_root) for entry_rel in entry_rels]

            #all_te = [TextEntry(id=int(entry_rel.get('entry_id')), te_root=te_root) for entry_rel in entry_rels]
            #self.text_entries = [te for te in all_te if te.lemma in frequent_entries]

            text_entries = []
            for entry_rel in entry_rels:
                #te = TextEntry(id=int(entry_rel.get('entry_id')), te_root=te_root, word=word, model=model)
                #print word
                te = TextEntry(id=int(entry_rel.get('entry_id')), te_root=te_root, word=word, pmi_w2v=pmi_w2v)
                if te.lemma in frequent_entries:
                    text_entries.append(te)

            self.text_entries = text_entries
        else:
            self.text_entries = [TextEntry(id=int(entry_rel.get('entry_id')), te_root=te_root, word=word, pmi_w2v=pmi_w2v) for entry_rel in entry_rels]

    def get_rel_concepts(self, rel_root, concept_root, rel_types):
        for rel_type in rel_types:
            c_ids = rel_root.findall('./rel[@from="%d"][@name="%s"]' % (self.id, rel_type))
            if c_ids:
                 return [Concept(id=int(c_id.get('to')), concept_root=concept_root) for c_id in set(c_ids)]
            else:
                return []

    def sort_text_entries(self, key):
        self.text_entries.sort(key=key, reverse=True)

    @property
    def w2v_sum(self):
        return sum([entry.w2v_sim for entry in self.text_entries if entry.w2v_sim > 0])
        #self.w2v_sum = sum([entry.w2v_sim for entry in self.text_entries if entry.w2v_sim > 0])
        #print self.w2v_sum

    @property
    def w2v_mean(self):
        positive_te = [entry.w2v_sim for entry in self.text_entries if entry.w2v_sim > 0]
        try:
            return sum(positive_te) / len(positive_te)
        except ZeroDivisionError:
            return 0
    #def te_w2v_mean(self):
    #    self.te_w2v_sum() / len(self.text_entries)


class CandidateWord(object):
    ''' Class for word - candidate for embedding to small thesaurus. '''
    def __init__(self, lemma, concepts=None):
        self.lemma = lemma  #unicode string
        if concepts:
            self.concepts = concepts
        else:
            self.concepts = set()

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

        def add_higher_concepts(rec_depth, rel_root, concept_root, rel_types=[u'ВЫШЕ']):
            def rec_helper(concepts, rec_depth):
                if rec_depth > 0:
                    for concept in concepts:
                        higher_concepts = concept.get_rel_concepts(rel_root, concept_root, rel_types)
                        #self.concepts.extend(higher_concepts)

                        #not_set_concepts = self.concepts.extend(higher_concepts)[:]
                        #self.concepts = list(set(not_set_concepts))
                        self.concepts.update(higher_concepts)
                        rec_helper(higher_concepts, rec_depth-1)

            rec_helper(self.concepts.copy(), rec_depth)
            #self.concepts = list(set(self.concepts))

        sim_entries = most_similar(self.lemma, model)
        first_step_concepts = []
        for entry in sim_entries:
            first_step_concepts.extend(entry.get_syn_concepts(syn_tree.getroot(), concept_tree.getroot()))
        #self.concepts.extend(list(set(first_step_concepts)))
        self.concepts.update(first_step_concepts)

        add_higher_concepts(2, rel_tree.getroot(), concept_tree.getroot())

    def sort_concepts(self, key):
        sorted_concepts = list(self.concepts)
        sorted_concepts.sort(key=key, reverse=True)
        return sorted_concepts
