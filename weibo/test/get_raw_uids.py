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
    "size": 2
}
users = es_user_profile.search(index = 'user_portrait_1222', doc_type = 'user', body = query)['hits']['hits']
with open('../docs/test_uids.txt', 'w') as fout:
    for user in users:
#         print user['_source']
        if user['_source']['topic_string'].startswith(u'生活类'):
            fout.write(user['_id'] + '\n')
fout.close()
