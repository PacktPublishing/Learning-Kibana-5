import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from elasticsearch import helpers
from elasticsearch import Elasticsearch

csvFilename="Posts.csv"
indexName="stackoverflow"


server = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]

es = Elasticsearch([server], http_auth=(user, password))
es.indices.delete(index=indexName, ignore=[400, 404])
indexSettings={
     "settings": {
            "number_of_replicas": "0",
            "number_of_shards": "1"
      },
      "mappings": {
         "qna": {
            "properties": {
                "user":{
                    "type": "string",
                    "index":"not_analyzed"
                },
                "tag":{
                    "type": "string",
                    "index":"not_analyzed"
                }
            }
         }
      }
   }
es.indices.create(index=indexName, body=indexSettings)

actions=[]
rowNum=0

with open(csvFilename, 'rb') as csvfile:
    csvreader = csv.reader(csvfile,  quotechar='"')
    for row in csvreader:
        rowNum+=1
        if rowNum==1:
            continue

        tags =[]
        if len(row[0])>0:
            tags=re.split("[,]+", row[0])
            tags = [x for x in tags if len(x)>0]

        users =[]
        if len(row[1])>0:
            users=re.split("[,]+", row[1])
            users = [x for x in users if len(x)>0]

        doc={
            "tag":tags,
            "user": users
        }
        action = {
                    "_index": indexName,
                    '_op_type': 'index',
                    "_type": "qna",
                    "_source": doc
        }
        actions.append(action)
        if len(actions) >= 5000:
            print rowNum
            helpers.bulk(es, actions)
            del actions[0:len(actions)]


if len(actions) > 0:
    helpers.bulk(es, actions)
