#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
import csv

gtf_path = 'gencode.v32.GRCh38.novel.trans.gtf'
out_intron_gtf_path = 'introns.gtf'
out_sig_ex_trans_path = 'sig_ex.gtf'

# process transcript by transcript

gtf = pd.read_csv(gtf_path, sep = '\t', header = None, comment = '#')
exons = gtf[gtf[2] == 'exon']

transcripts = []
for i in exons[8]:
    trans_name = re.findall(r"transcript_id \"(.*?)\";", i)[0]
    transcripts.append(trans_name)
exons[9] = transcripts
# sort the exon table by chromosome, transcript name and then the start position
exons = exons.sort_values(by = [1, 9, 3]).reset_index(drop = True)

sig_ex_trans = pd.DataFrame()
multi_ex_trans = ''

exon_num = 1
meter = 1
for i in range(len(exons) - 1): # minus 1 to skip the last line
    chromosome = exons[0][i]
    source = exons[1][i]
    strand = exons[6][i]
    info = exons[8][i]
    this_trans = exons[9][i]
    next_trans = exons[9][i + 1]
    
    if exon_num == 1:
        if this_trans != next_trans:
            sig_ex_line = exons[exons[9].str.contains(this_trans)]
            sig_ex_trans = sig_ex_trans.append(sig_ex_line)
            
    if this_trans == next_trans:
        start_intron = exons[4][i] + 1
        end_intron = exons[3][i + 1] - 1
        multi_ex_trans +=  str(chromosome) + '\t' + source + '\t' + 'intron' + '\t' + str(start_intron) + '\t' + str(end_intron) + '\t' + '.' + '\t' + strand + '\t' + '.' + '\t' + info + '\n'
        exon_num += 1
        
    else:
        exon_num = 1
        
    print(str(meter) + '/' + str(len(exons)) + ' done.')
    meter += 1

# save stuff!!!
sig_ex_trans.to_csv(out_sig_ex_trans_path, sep = '\t', index = False, header = False, quoting = csv.QUOTE_NONE)

with open(out_intron_gtf_path, 'w') as w:
    w.write(multi_ex_trans)

