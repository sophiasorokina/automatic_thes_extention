# -*- coding: UTF-8 -*-
__author__ = 'Lenovo'

import xml.etree.cElementTree as et
#import cPickle, yaml, json
import jsonpickle, yaml
import classes
from os import getcwd
from os.path import join, split

country_data_as_string = '''<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank updated="yes">5</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank updated="yes">69</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>'''

root = et.fromstring(country_data_as_string)
#print root.find(".*[year='%s']" % u'2011').get('name')

#print cPickle.dumps('привет')
with open ('./test.txt', 'w+') as f:
    #yaml.dump('привет', f, encoding='utf-8')
    #json.dump(['привет', 'пока'], f, ensure_ascii=False)
    #json.dump(classes.CandidateWord(u'лала'), f, cls=classes.CustomObjEncoder, ensure_ascii=False)
    #json.dump(classes.Concept(123), f, cls=classes.CustomObjEncoder, ensure_ascii=False)
    cw = classes.CandidateWord(u'лала')
    concept = classes.Concept(123)
    cw.concepts.add(concept)
    cw_json = jsonpickle.encode(cw)
    # print cw_json
    # print jsonpickle.decode(cw_json)

    #cw_yaml = yaml.dump(cw, f)
    #print yaml.load(f)
    #json.dump(cw, f, cls=classes.CustomObjEncoder, ensure_ascii=False, indent=4)
#print json.dumps(['привет', 'пока'], ensure_ascii=False)

#with open ('./input.txt') as f:
    #print json.load(f, cls=classes.CandWordDecoder)

proj_path = split(getcwd())[0]
temp_path = join(proj_path, 'temp')
with open(join(temp_path, 'concepts for bindings with first-step synonyms3.txt')) as file:
    raw_data = file.read()
candidate_words = jsonpickle.decode(raw_data)
for word in candidate_words:
    print word.lemma
    for concept in word.concepts:
        print concept.name, concept.id
    print '\n'
    break



