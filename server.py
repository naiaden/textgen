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


##
config = configparser.ConfigParser()
config.read('witc.ini')

cache_file = config['INPUT']['CacheFile']
author_lm = eval(cache_file) # [{"author_id": 1, "file": "couperus_feats.json"}]

for l in author_lm:
    lm = LanguageModel()
    lm.load_model(l['file'])
    l['model'] = lm
    l['generator'] = TextGenerator(lm, 10)

    print("+ Reading author: " + str(l['author_id']))

minimum_paragraph_length = int(config['OUTPUT'].get('MinimumParagraphLength', 30))
w2v_model = config['INPUT']['W2V']
testout = config['OUTPUT']['StoryFile']

#NormaliserFactory(data, config['INPUT']['Normalisers'])

print("+ Loading Word2Vec model")
ss = SentenceSemantics()
ss.load_model(w2v_model)


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
        story_id = sentence_id
        something = request.form['data']
        # if number and number corresponds to sentence
        conn = db_connect.connect()
        query = conn.execute("select sentence from Suggestions where suggestion_id =%d" %(int(sentence_id)))
        sentence = query.first()[0]

        query = conn.execute("insert into Sentences (sentence) values (%s) " %("\"" + sentence + "\""))
        sentence_id = query.lastrowid

        query = conn.execute("insert into Votes (sentence_id) values (%d) " %(int(sentence_id)))
        vote_id = query.lastrowid

        #
        query = conn.execute("select max(position) from Stories where story_id =%d " %int(story_id))
        new_position = query.scalar()

        if new_position:
            new_position += 1
        else:
            new_position = 1
        
        query = conn.execute("insert into Stories (story_id, sentence_id, position) values (%d, %d, %d) " %(int(story_id), int(sentence_id), int(new_position)))
        #

        return jsonify({"vote_id": vote_id})
        #sentence_ids = [i for i in query.cursor]
        #if (int(sentence_id),) in sentence_ids:
        #    query = conn.execute("insert into Votes (suggestion_id) values (%d) " %int(sentence_id))
        #    result = {'vote_id': query.lastrowid}
        #    return jsonify(result)
        #else:
        #    result = {'invalid_input': sentence_id}
        #    return jsonify(result)

class Suggestions(Resource):
    def get(self, story_id):
        conn = db_connect.connect()
        query = conn.execute("select * from StoryAuthor where story_id =%d " %int(story_id))
        author = query.first()[1]
        
        a_lm = (item for item in author_lm if item['author_id'] == 1).next()
        lm = a_lm['model'] 
        tg = a_lm['generator']

        #query = conn.execute("select max(position) from Stories where story_id =%d " %int(story_id))
        #last_position = query.scalar()

        #conn = db_connect.connect()
        query = conn.execute("select * from Stories where story_id =%d " %int(story_id))
        sentences = [i for i in query.cursor]
        sentences.sort(key=lambda x: x[2], reverse=True)
        last_sentence_id = sentences[0][1] 
        
        query = conn.execute("select sentence from Sentences where sentence_id =%d " %int(last_sentence_id))
        last_sentence = query.first()
        print(last_sentence)

        sources = [tg.generate_sentence() for x in range(100)]

        candidates = ss.return_sentence_candidates(last_sentence,sources, 10) #andere ranks

        return_candidates = []
        for candidate in candidates:
            string_candidate = ' '.join(candidate[0])
            #conn = db_connect.connect()
            query = conn.execute("insert into Suggestions (sentence, story_id) values (%s, %d) " %("\"" + string_candidate + "\"", int(story_id)))
            return_candidates.append({'suggestion_id': query.lastrowid, 'sentence': string_candidate})
            #return_candidates.append(string_candidate)
        print(return_candidates)
        return jsonify(return_candidates)

class AddSentence(Resource):
    #def get(self, story_id):
    #    return jsonify({"status": "not implemented. Use PUT"})
    #
    def put(self, story_id):
        conn = db_connect.connect()
        #last position
        query = conn.execute("select max(position) from Stories where story_id =%d " %int(story_id))
        new_position = query.scalar()

        if new_position:
            new_position += 1
        else:
            new_position = 1

        query = conn.execute("insert into Sentences (sentence) values (%s) " %("\"" + str(request.form['data']) + "\""))
        new_sentence_id = query.lastrowid

        query = conn.execute("insert into Stories (story_id, sentence_id, position) values (%d, %d, %d) " %(int(story_id), new_sentence_id, new_position))
        return jsonify({'status': 'sentence added'})

class CreateStory(Resource):
    def get(self, author_id):
        conn = db_connect.connect()
        query = conn.execute("insert into StoryAuthor (author_id) values (%d) " %(int(author_id)))
        return jsonify({'story_id': query.lastrowid})

api.add_resource(Sentences, '/sentences')
api.add_resource(Stories, '/stories')
api.add_resource(Authors, '/authors')
api.add_resource(Votes, '/votes')

api.add_resource(Sentence, '/sentence/<sentence_id>')
api.add_resource(Story, '/story/<story_id>')
api.add_resource(Vote, '/vote/<sentence_id>')
api.add_resource(Suggestions, '/suggestion/<story_id>')

api.add_resource(CreateStory, '/createstory/<author_id>')
api.add_resource(AddSentence, '/addsentence/<story_id>')


if __name__ == '__main__':
    app.run(port='5003')
