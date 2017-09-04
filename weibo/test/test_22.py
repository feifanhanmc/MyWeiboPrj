# -*- coding: utf-8 -*-

def load_final_uids():
    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
    return final_uids

def main():
    final_uids = load_final_uids()
    raw_row = 9
    raw_column = 91
    row = raw_row
    column = (raw_column + 5)/6
    
    print final_uids[row - 1] 
    print final_uids[column - 1] 
    
main()