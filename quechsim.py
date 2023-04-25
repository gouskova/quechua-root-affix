#!/usr/bin/env python3

import random, sys
import numpy
import scipy.stats
from matplotlib import pyplot as plt


def natlex(**kwargs):
    '''
    counts number of words with a particular natural class in file, puts results in 2 dictionaries
    '''
    wdic, ldic = {},{'natclass':0, 'no_natclass':0}
    d = kwargs['infile']
    natclass = kwargs['natclass']
    with open(d, 'r', encoding='utf-8') as f:
        for line in f:
            segs = set(line.rstrip('\n').split())
            wnat = len(segs&set(natclass))
            wdic[line.rstrip('\n')]=wnat>0
            if wnat>0:
                ldic['natclass']+=1
            else:
                ldic['no_natclass']+=1
    return wdic, ldic


def ransample(**kwargs):
    '''
    samples N times from the dictionary of words, and counts words in the sample that have segments from some pre-specified natural class (e.g., 'asps' and 'ejecs') (see 'natlex')
    the number of samples is given in kwargs
    '''
    wdic = kwargs['wdic']
    samsize = kwargs['samsize']
    nsamples = kwargs['nsamples']
    printt = kwargs['print']
    #let's count how often a randomly drawn sample contains neither laryngeal
    sdic = {'natclass':0, 'no_natclass':0, 'ratios':[]}
    for n in range(nsamples):
        wds = random.choices(list(wdic), k=samsize)
        owds = [x for x in wds if (wdic[x]==True)]
        if printt:
            print(wds)
            print(owds)
        if len(owds)>0:
            sdic['natclass']+=1
        else:
            sdic['no_natclass']+=1
        sdic['ratios'].append(len(owds)/len(wds))
    return sdic

def runsim(**kwargs):
    sim = ransample(**kwargs)
    for k in ['natclass', 'no_natclass']:
        print(f'{k}\t{sim[k]}\n')
    ci = ci_long(sim['ratios'])
    plot_hist(sim['ratios'], ci)

def ci_long(inlist):
    '''
    manual method
    '''
    mean = sum(inlist)/len(inlist)
    std = numpy.std(inlist)
    lowerb = mean-1.96*(std/numpy.sqrt(len(inlist)))
    upperb = mean+1.96*(std/numpy.sqrt(len(inlist)))
    return (lowerb, upperb)


def plot_hist(values, ci, bins=30):
    fig = plt.hist(values, bins)
    plt.axvline(ci[0], color='r')
    plt.axvline(ci[1], color='r')
    plt.show()
    plt.clf()
    plt.close()


def fisher_test(nums):
    x = scipy.stats.fisher_exact(nums)
    print(f'fishers test: {x[0]}, p = {x[1]:5f}')
    return x 

def chisq(nums):
    x = scipy.stats.chi2_contingency(nums)
    #x[0] is odds ratio
    #x[1] is p val
    #x[2] is degs of freedom
    print(f'X2{x[2]} = {x[0]}, p={x[1]}')
    return x


if __name__=='__main__':
    print("\nThe utility will print out a natural class plus how often segments from that class occur in a randomly drawn sample of 76 morphemes. (The "76" number is how many affixes are attested in Gallagher's newspaper corpus of Quechua).\n\nNote: you will have to close each histogram plot manually for the program to advance.")
    kwargs={}
    asps = 'pʰ tʰ kʰ ʧʰ qʰ'.split()
    ejecs = "p' t' k' ʧ' q'".split()
    plains = 'p t k ʧ q'.split()
    nasals = 'm n ŋ ɲ ɴ'.split() 
    uvulars = "q q' qʰ ɴ x".split()
    velars = "k k' kʰ ŋ".split()
    approxs  = 'l r ʎ j w'.split()
    frics = 's ʃ x h'.split()
    affricates = "ʧ ʧ' ʧʰ".split()
    stridents = ['s', 'ʃ']+affricates
    sibs = ['s', 'ʃ']
    labstops = ['p', "p'", "pʰ"]
    liqs = ['l', 'r', 'ʎ']
    natclasses = [asps, ejecs, asps+ejecs, plains, nasals, uvulars, velars, liqs, frics, affricates, ['h'], asps+ejecs+['h']]
    #natclasses=[liqs]
    if 'counts' in sys.argv:
        kwargs['infile']=sys.argv[1]
    else: 
        kwargs['infile']='quechua_morphemes.txt'
        kwargs['natclass']=affricates
        kwargs['samsize']=76
        kwargs['nsamples']=1000000
        if not 'print' in sys.argv:
            kwargs['print']=False
        else:
            kwargs['print']=True
    for natcl in natclasses:
        print(natcl)
        kwargs['natclass']=natcl
        w, l = natlex(**kwargs)
        kwargs['wdic']=w
        lenr = sum(l.values())
        print('lexical distribution of your natural class in roots\n')
        for k in l:
            print(f'{k}\t{l[k]}\tproportion\t{l[k]/lenr}\n')
        runsim(**kwargs)
    if 'chisq' in sys.argv:
        'some fisher tests for ya'
        arry = [[2479-1169,1169],[76,0]] #num of roots, num of roots with eject/aspirates, num of affixes, num of affixes w ejects/aspirates
        print('laryngeals, minus h\n')
        fisher_test(arry)
        arry = [[2479-726,726],[76-20,20]]
        print(f'uvulars\n')
        fisher_test(arry)
        arry = [[2479-501,501],[76-14,14]]
        print(f'affricates\n')
        fisher_test(arry)
        arry = [[2479-818,818],[76-29,29]]
        print(f'nasals\n')
        fisher_test(arry)
        arry = [[2479-144,144],[76,0]]
        print(f'nat class: (h)\n')
        fisher_test(arry)
        print(f'nat class: all the laryngeals plus [h]\n')
        arry = [[2479-1255,1255],[76,0]]
        fisher_test(arry)


