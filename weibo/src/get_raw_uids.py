# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

user_profile_host = 'http://219.224.134.216:9201'
es_user_profile = Elasticsearch(user_profile_host, timeout=600)

query = {        
    "query": {
        "filtered": {
            "query":    { "match_all": {}}
        }
    },
    "size": 30000
}
results = es_user_profile.search(index = 'user_portrait_1222', doc_type = 'user', body = query)['hits']['hits']
raw_uids = []
for r in results:
    if r['_source']['topic_string'].startswith(u'生活类'):
        raw_uids.append(r['_id'])
        
with open('../docs/raw_uids.txt', 'w') as fout:
    for uid in raw_uids:
        fout.write(uid + '\n')
fout.close()
