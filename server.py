from flask import Flask, request, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify


##
import configparser
import json
import random

from languagemodel import LanguageModel
from textgenerator import TextGenerator
from normaliser import FrogNormaliser, NormaliserFactory
from sentence_semantics import SentenceSemantics
##

db_connect = create_engine('sqlite:///witc.db')
app = Flask(__name__)
api = Api(app)

config = configparser.ConfigParser()
config.read('witc.ini')

cache_file = config['INPUT']['CacheFile']
minimum_paragraph_length = int(config['OUTPUT'].get('MinimumParagraphLength', 30))
w2v_model = config['INPUT']['W2V']
testout = config['OUTPUT']['StoryFile']

if cache_file:
    print("+ Reading cache file")
    with open(cache_file) as data_file:
        data = json.load(data_file)
else:
        print("+ Reading from text file")
        print(" -- Currently not implemented")

NormaliserFactory(data, config['INPUT']['Normalisers'])

print("+ Creating language model")
lm = LanguageModel(data)

print("+ Loading Word2Vec model")
ss = SentenceSemantics()
ss.load_model(w2v_model)
ss.load_lm(data)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class Sentences(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Sentences")
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Sentence(Resource):
    def get(self, sentence_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Sentences where sentence_id =%d " %int(sentence_id))
        return {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}

class Stories(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Stories")
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Story(Resource):
    def get(self, story_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Stories where story_id =%d " %int(story_id))
        return {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}

class Authors(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Authors")
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Votes(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Votes")
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Vote(Resource):
    def get(self, sentence_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Votes where vote_id =%d " %int(sentence_id))
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

    def put(self, sentence_id):
        something = request.form['data']
        # if number and number corresponds to sentence
        conn = db_connect.connect()
        query = conn.execute("select sentence_id from Sentences")
        sentence_ids = [i for i in query.cursor]
        if (int(sentence_id),) in sentence_ids:
            query = conn.execute("insert into Votes (sentence_id) values (%d) " %int(sentence_id))
            result = {'vote_id': query.lastrowid}
            return jsonify(result)
        else:
            result = {'invalid_input': sentence_id}
            return jsonify(result)

# This class needs attention, but cannot test without data
class Suggestions(Resource):
    def get(self, author_id):
        tg = TextGenerator(lm, minimum_paragraph_length)
        target = tg.generate_sentence()
        for i in range(50):
            sources = [tg.generate_sentence() for x in range(150)]
            candidates = ss.return_sentence_candidates(target,sources,3) # will return three sentences formatted as [['salient word',[sentence]],['salient word',[sentence]],['salient word',[sentence]]]
            target = random.choice([x[0][1] for x in candidates])
            #
            conn = db_connect.connect()
            query = conn.execute("insert into Sentences (sentence_id, sentence, author_id) values (%d, %s, %d) " %int(sentence_id), target, %int(author_id))
            result = {'sentence_id': query.lastrowid}
            return jsonify(result)


api.add_resource(Sentences, '/sentences')
api.add_resource(Stories, '/stories')
api.add_resource(Authors, '/authors')
api.add_resource(Votes, '/votes')

api.add_resource(Sentence, '/sentence/<sentence_id>')
api.add_resource(Story, '/story/<story_id>')
api.add_resource(Vote, '/vote/<sentence_id>')
api.add_resource(Suggestions, '/suggestion/<author_id>')

if __name__ == '__main__':
    app.run(port='5003')
