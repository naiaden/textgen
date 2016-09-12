import json

import sys    
sys.path.insert(0,"/home/louis/Software/textgen")
from languagemodel import LanguageModel
from textgenerator import TextGenerator

cache_file = '/home/louis/Software/textgen/couperus_feats.json'
input_file = ''

#data = [[{u'word': u'Ik', u'pos': u'VNW(pers,pron,nomin,vol,1,ev)'}, {u'word': u'heb', u'pos': u'WW(pv,tgw,ev)'}, {u'word': u'het', u'pos': u'VNW(pers,pron,stan,red,3,ev,onz)'}, {u'word': u'aan', u'pos': u'VZ(init)'}, {u'word': u'den', u'pos': u'LID(bep,dial)'}, {u'word': u'heer', u'pos': u'N(soort,ev,basis,zijd,stan)'}, {u'word': u'Van', u'pos': u'SPEC(deeleigen)'}, {u'word': u'Someren', u'pos': u'SPEC(deeleigen)'}, {u'word': u'te', u'pos': u'VZ(init)'}, {u'word': u'danken', u'pos': u'WW(inf,vrij,zonder)'}, {u'word': u',', u'pos': u'LET()'}, {u'word': u'dat', u'pos': u'VG(onder)'}, {u'word': u'ik', u'pos': u'VNW(pers,pron,nomin,vol,1,ev)'}, {u'word': u'over', u'pos': u'VZ(init)'}, {u'word': u'dit', u'pos': u'VNW(aanw,det,stan,prenom,zonder,evon)'}, {u'word': u'onderwerp', u'pos': u'N(soort,ev,basis,onz,stan)'}, {u'word': u'iets', u'pos': u'VNW(onbep,pron,stan,vol,3o,ev)'}, {u'word': u'nieuws', u'pos': u'ADJ(postnom,basis,met-s)'}, {u'word': u'kan', u'pos': u'WW(pv,tgw,ev)'}, {u'word': u'schrijven', u'pos': u'WW(inf,vrij,zonder)'}, {u'word': u'.', u'pos': u'LET()'}], [{u'word': u'Hij', u'pos': u'VNW(pers,pron,nomin,vol,3,ev,masc)'}, {u'word': u'heeft', u'pos': u'WW(pv,tgw,met-t)'}, {u'word': u'bouwstof', u'pos': u'N(soort,ev,basis,zijd,stan)'}, {u'word': u',', u'pos': u'LET()'}, {u'word': u'die', u'pos': u'VNW(betr,pron,stan,vol,persoon,getal)'}, {u'word': u'nog', u'pos': u'BW()'}, {u'word': u'altijd', u'pos': u'BW()'}, {u'word': u'ongebruikt', u'pos': u'ADJ(vrij,basis,zonder)'}, {u'word': u'in', u'pos': u'VZ(init)'}, {u'word': u'de', u'pos': u'LID(bep,stan,rest)'}, {u'word': u'bibliotheken', u'pos': u'N(soort,mv,basis)'}, {u'word': u'berustte', u'pos': u'WW(pv,verl,ev)'}, {u'word': u',', u'pos': u'LET()'}, {u'word': u'voor', u'pos': u'VZ(init)'}, {u'word': u'den', u'pos': u'LID(bep,dial)'}, {u'word': u'dag', u'pos': u'N(soort,ev,basis,zijd,stan)'}, {u'word': u'gehaald', u'pos': u'WW(vd,vrij,zonder)'}, {u'word': u'en', u'pos': u'VG(neven)'}, {u'word': u'uitgegeven', u'pos': u'WW(vd,vrij,zonder)'}, {u'word': u',', u'pos': u'LET()'}, {u'word': u'het', u'pos': u'VNW(pers,pron,stan,red,3,ev,onz)'}, {u'word': u'aan', u'pos': u'VZ(init)'}, {u'word': u'een', u'pos': u'LID(onbep,stan,agr)'}, {u'word': u'ieder', u'pos': u'VNW(onbep,det,stan,vrij,zonder)'}, {u'word': u'die', u'pos': u'VNW(aanw,pron,stan,vol,3,getal)'}, {u'word': u'wil', u'pos': u'WW(pv,tgw,ev)'}, {u'word': u'overlatende', u'pos': u'WW(pv,verl,ev)'}, {u'word': u'om', u'pos': u'VZ(init)'}, {u'word': u'ze', u'pos': u'VNW(pers,pron,stan,red,3,mv)'}, {u'word': u'aan', u'pos': u'VZ(init)'}, {u'word': u'de', u'pos': u'LID(bep,stan,rest)'}, {u'word': u'geschiedenis', u'pos': u'N(soort,ev,basis,zijd,stan)'}, {u'word': u'des', u'pos': u'LID(bep,gen,evmo)'}, {u'word': u'Vaderlands', u'pos': u'ADJ(prenom,basis,zonder)'}, {u'word': u'dienstbaar', u'pos': u'ADJ(vrij,basis,zonder)'}, {u'word': u'te', u'pos': u'VZ(init)'}, {u'word': u'maken', u'pos': u'WW(inf,vrij,zonder)'}, {u'word': u'.', u'pos': u'LET()'}]]

if cache_file:
    with open(cache_file) as data_file:    
        data = json.load(data_file)


#print(data[0:2])

lm = LanguageModel(data)
#lm.print_features()

tg = TextGenerator(lm)


