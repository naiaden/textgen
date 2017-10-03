import sys

import configparser
import json
from sqlalchemy import create_engine

#
config = configparser.ConfigParser()
config.read('witc.ini')

#
database_handle = 'sqlite:///' + config['INPUT']['Database']
db_connect = create_engine(database_handle)

#
cache_file = config['INPUT']['CacheFile']
authors = eval(cache_file)

conn = db_connect.connect()
query = conn.execute("CREATE TABLE `Authors` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL);")

for author in authors:
    query = conn.execute("INSERT INTO Authors (id, name) VALUES (%d, %s); " %(int(author['author_id']), "\"" + author['author'] + "\""))

query = conn.execute("CREATE TABLE `Sentences` ( `sentence_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, `sentence` TEXT);")

query = conn.execute("CREATE TABLE `Stories` ( `story_id` INTEGER NOT NULL, `sentence_id` INTEGER NOT NULL, `position` INTEGER NOT NULL);")

query = conn.execute("CREATE TABLE `StoryAuthor` ( `story_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `author_id` INTEGER NOT NULL);")

query = conn.execute("CREATE TABLE `Suggestions` ( `suggestion_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `sentence` TEXT NOT NULL, `story_id` INTEGER NOT NULL);")

query = conn.execute("CREATE TABLE `Votes` ( `vote_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `sentence_id` INTEGER NOT NULL, `source` TEXT, `time` TEXT);")

