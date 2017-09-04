# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship
import numpy
import time

def connect_db():
    return Graph("http://localhost:7474", username="neo4j", password="admin")

def load_final_uids():
    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
    return final_uids

def create_nodes(final_uids, db):
    for uid in final_uids:
        db.create(Node("UID_LABEL", uid = uid))

def create_relationship(final_uids, statuses_sim, tags_sim, location_sim, sr_sim, gender_sim, usetime_sim, db):
    #neo4j是只能创建有向边的，这里只创建了单向边（从uid较小的节点到uid较大的节点）
    N = len(final_uids)
    for i in range(N):
        j = i + 1
        while j < N :
            Ui = db.find_one("UID_LABEL", property_key="uid", property_value=final_uids[i])
            Uj = db.find_one("UID_LABEL", property_key="uid", property_value=final_uids[j])
            db.create(Relationship(Ui, 'WEIGHT_LABEL', Uj, statuses_sim=statuses_sim[i][j], \
                                   tags_sim=tags_sim[i][j], location_sim=location_sim[i][j], \
                                   sr_sim=sr_sim[i][j], gender_sim=gender_sim[i][j], usetime_sim=usetime_sim[i][j]))
            j += 1

def load_weight(filename):
    return numpy.loadtxt(open(filename, 'r'),delimiter=",",skiprows=0)

def main():
    final_uids = load_final_uids()
    db = connect_db()
    create_nodes(final_uids, db)
    
    statuses_sim = load_weight('../docs/sim/statuses_sim.csv')
    time.sleep(10)
    tags_sim = load_weight('../docs/sim/tags_sim.csv')
    time.sleep(10)
    location_sim = load_weight('../docs/sim/location_sim.csv')
    time.sleep(10)
    sr_sim = load_weight('../docs/sim/sr_sim.csv')
    time.sleep(10)
    gender_sim = load_weight('../docs/sim/gender_sim.csv')
    time.sleep(10)
    usetime_sim = load_weight('../docs/sim/usetime_sim.csv')
    time.sleep(10)

    start = time.clock()
    create_relationship(final_uids, statuses_sim, tags_sim, location_sim, sr_sim, gender_sim, usetime_sim, db)
    elapsed = (time.clock() - start)
    print 'elapsed', elapsed
     
    

     
    
        
main()