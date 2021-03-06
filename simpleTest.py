# -*- coding: utf-8 -*-
from flask import *
from flask import request
from TFIDFSearcher import TFIDFSearcher
from cutkum.tokenizer import Cutkum
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
ck = Cutkum()
searcher = TFIDFSearcher()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/getDocuments', methods=['GET'])
def get_documents():
    query = request.args.get('query')
    print(query)
    query = tokenize(query)
    results = searcher.search(query, 10)
    # results are SearchResult, need to work with the offset and convert to Document object
    for result in results:
        if result.score > 0:
            result.document.set_query_offset(query)
        else:
            result.document.query_offset = 0

    for i in range(len(results)):
        results[i] = results[i].document
    jsons = jsonify([e.serialize() for e in results])
    # r = Response(response="OK", status=200, mimetype="text/html")
    r = app.make_response(jsons)
    r.headers["Context-Type"] = "text/html; charset=utf-8"
    return r
    # return jsonify([e.serialize() for e in results])
    # return jsonify(query=query)


def tokenize(string):
    return ck.tokenize(string)
