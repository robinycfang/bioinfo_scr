#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
import csv

gtf_path = 'gencode.v32.GRCh38.gtf'
out_intron_gtf_path = 'introns.gtf'
out_sig_ex_trans_path = 'sig_ex.gtf'

# collect all transcripts

all_trans = []

with open(gtf_path, 'r') as gtf:
    while True:
        line = gtf.readline()
        if len(line) == 0:
            break
    
        # re.findall() returns a list
        trans = re.findall(r"transcript_id \"(.*?)\";", line)
        if len(trans) != 0:
            trans = trans[0]
            all_trans.append(trans)
            
# use set() to create a set object that has unique values          
all_trans = set(all_trans)
# unpack the set object into a list
all_trans = [*all_trans,]
                
# process transcript by transcript

gtf = pd.read_csv(gtf_path, sep = '\t', header = None, comment = '#')
exons = gtf[gtf[2] == 'exon']
sig_ex_trans = pd.DataFrame()
multi_ex_trans = ''
processed = 0

for trans in all_trans:
    processed += 1
    print(str(processed) + '/' + str(len(all_trans)) + ' done.')
    
    # gather all exons for an individual transcript 
    exons_of_a_trans = exons[exons[8].str.contains(trans)].reset_index(drop = True)
    
    # for single-exon transcripts
    if len(exons_of_a_trans) == 1:
        sig_ex_trans = sig_ex_trans.append(exons_of_a_trans)
    
    # for multiple-exon transcripts
    else:
        exons_of_a_trans = exons_of_a_trans.sort_values(by = [3])
        chromosome = exons_of_a_trans[0][0]
        source = exons_of_a_trans[1][0]
        strand = exons_of_a_trans[6][0]
        length = exons_of_a_trans[7][0]
        info = exons_of_a_trans[8][0]
        
        for i in range(len(exons_of_a_trans)):
            try:
                in_start = exons_of_a_trans[4][i] + 1
                in_end = exons_of_a_trans[3][i+1] - 1
                multi_ex_trans += str(chromosome) + '\t' + source + '\t' + 'intron' + '\t' +                 str(in_start) + '\t' + str(in_end) + '\t' + '.' + '\t' + strand + '\t' + info + '\n'
            
            # the last line can raise KeyError
            except KeyError:
                break

# save stuff!!!
sig_ex_trans.to_csv(out_sig_ex_trans_path, sep = '\t', index = False, header = False, quoting = csv.QUOTE_NONE)

with open(out_intron_gtf_path, 'w') as w:
    w.write(multi_ex_trans)



