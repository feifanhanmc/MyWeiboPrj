# -*- coding: utf-8 -*-
import numpy


def integrate_baseinfo_sim():
    location_sim = numpy.loadtxt(open('../docs/sim/location_sim.csv', 'r'),delimiter=",",skiprows=0)
    gender_sim = numpy.loadtxt(open('../docs/sim/gender_sim.csv', 'r'),delimiter=",",skiprows=0)
    usetime_sim = numpy.loadtxt(open('../docs/sim/usetime_sim.csv', 'r'),delimiter=",",skiprows=0)
    
    location_weight = 0.504864147
    gender_weight = 0.382227636
    usetime_weight = 0.112908216
    
    baseinfo_sim = location_sim*location_weight + gender_sim*gender_weight + usetime_sim*usetime_weight
    return baseinfo_sim

def save_baseinfo_sim(baseinfo_sim):
    numpy.savetxt('../docs/sim/baseinfo_sim.csv', baseinfo_sim, fmt = '%.3f', delimiter = ',')
    
def main():
    baseinfo_sim = integrate_baseinfo_sim()
    save_baseinfo_sim(baseinfo_sim)
    
main()    