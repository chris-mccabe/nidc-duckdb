import json

import spacy

import duckdb
from duckdb.typing import *

con = duckdb.connect('nerdemo.db')
nlp = spacy.load("en_core_web_lg")

def extract_ents(text):
    """
    Will return a list of ents from a string
    :type text: str
    :param text:
    :return:
    """

    # Process the text using spaCy NLP model
    doc = nlp(text)

    # Extract entities and their type as a list of tuples
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return json.dumps(entities)


con.create_function('extract_ents', extract_ents, [VARCHAR], VARCHAR)

con.sql("create table articles as select * from '../data/articles.json'")

res = con.sql(
    """CREATE TABLE entities as select link, extract_ents(short_description)  from articles limit 10""")

result = con.sql("""select * from entities""").fetchall()


print(result)