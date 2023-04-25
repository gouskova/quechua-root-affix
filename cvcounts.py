#!/usr/bin/env python3

def make_cvc_dic(**kwargs):
    '''
    replaces all words with CV skeleta, and counts up types
    '''
    if 'vowels' in kwargs:
        vowels = kwargs['vowels']
    else:
        vowels = ['a','e','i','o','u']
    outdic = {}
    with open(kwargs['inpath'], 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                line = line.split('\t')[0].split()
            else:
                line = line.strip('\n').split()
            CV=[]
            for i in range(len(line)):
                if line[i] in vowels:
                    CV.append("V")
                else:
                    CV.append("C")
            CV=' '.join(CV)
            if CV in outdic:
                outdic[CV]+=1
            else:
                outdic[CV]=1
    return outdic

def print_CV(**kwargs):
    d = kwargs['dic']
    for k in sorted(d, key=d.get, reverse=True):
        print(f'{k}\t{d[k]}')

                

if __name__=='__main__':
    import sys
    d = {}
    d['inpath'] = sys.argv[1]
    if len(sys.argv)>2:
        d['vowels']=sys.argv[2].split(' ')
    d['dic']=make_cvc_dic(**d)
    print_CV(**d)
