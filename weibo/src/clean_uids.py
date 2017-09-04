# -*- coding: utf-8 -*-

raw_uids = []
with open('../docs/raw_uids.txt') as fp:
    for line in fp:
        raw_uids.append(line.strip())
fp.close()


bad_uids = []
with open('../docs/bad_uids.txt') as fp:
    for line in fp:
        bad_uids.append(line.strip())
fp.close()

uids = list(set(raw_uids) - set(bad_uids))
with open('../docs/uids.txt', 'w') as fout:
    for uid in uids:
        fout.write(uid + '\n')
fout.close()