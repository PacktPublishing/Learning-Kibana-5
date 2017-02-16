#!/usr/bin/python

import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def pullPrelertResults( url ):
   return requests.get(url);

es = Elasticsearch(['localhost:9200'], http_auth=('elastic', 'changeme'));
# Pass your Prelert Record API URL, ex: http://localhost:8081/engine/v2/results/cpu-anomaly-detection/records
url = sys.argv[1]
response = pullPrelertResults(url);
while response.json()['nextPage']:
	print response.json()['nextPage'].replace('&anomalyScore=0%2C0&normalizedProbability=0%2C0', '');
	url = response.json()['nextPage'].replace('&anomalyScore=0%2C0&normalizedProbability=0%2C0', ''); 
	actions = []
	for record in response.json()['documents']:
		action = {
			"_index": "cpu-anomaly-detection-results",
			"_type": "record",
			"_source": record
		}
		actions.append(action)

	if len(actions) > 0:
		helpers.bulk(es, actions)
	response = pullPrelertResults(url);
	print response.json()