from flask import Flask, request, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///witc.db')
app = Flask(__name__)
api = Api(app)

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

api.add_resource(Sentences, '/sentences')
api.add_resource(Stories, '/stories')
api.add_resource(Authors, '/authors')
api.add_resource(Votes, '/votes')

api.add_resource(Sentence, '/sentence/<sentence_id>')
api.add_resource(Story, '/story/<story_id>')
api.add_resource(Vote, '/vote/<sentence_id>')

if __name__ == '__main__':
    app.run(port='5003')
