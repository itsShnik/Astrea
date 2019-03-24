from elasticsearch import Elasticsearch,exceptions
import ast
import sys


#usage >  python db_gen.py EXTRACTED_1000_1500.txt test docs 

def connect(filename, indexname, doc_type):
    ES_HOST   = {"host":"localhost","port":9200}
    es = Elasticsearch(hosts=[ES_HOST])
    INDEX_NAME = indexname
    try:
        response = es.indices.create(index=INDEX_NAME,body=
   { "settings": {
        "index" : {
            "analysis" : {
                "analyzer" : {
                    "synonym" : {
                        "tokenizer" : "whitespace",
                        "filter" : ["synonym"]
                    }
                },
                "filter" : {
                    "synonym" : {
                        "type" : "synonym",
                        "synonyms_path" : "new.txt"
                    }
                }
            }
        }
    }})
    except exceptions.RequestError:
        print("Index Already Created")
        return
    print(response)
    db = open(filename)
    lists = db.readlines()
    i=1
    for line in lists:
        body = ast.literal_eval(line)
        resp = es.index(index=INDEX_NAME,doc_type=doc_type,body=body,id=i)
        i=i+1
        print(resp)


if __name__ == "__main__":
    connect(sys.argv[1],sys.argv[2],sys.argv[3])
