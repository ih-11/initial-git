#!/usr/bin/env python3

import argparse
import gzip
import korflab

parser = argparse.ArgumentParser(
	description='systematically sample fastq reads')
parser.add_argument('output', help='output fastq.gz file')
parser.add_argument('fastq', nargs='+', help='input fastq file(s)')
parser.add_argument('-n', type=int, default=1000,
	help='number of reads [%(default)d]')
arg = parser.parse_args()

total = 0

for file in arg.fastq:
	for header, seq, plus, qual in korflab.readfastq(file):
		total += 1

if total < arg.n:
	raise SystemExit(f'error: requested {arg.n} reads, but input only has {total}')

selected = set()

if arg.n == 1:
	selected.add(0)
else:
	for i in range(arg.n):
		idx = round(i * (total - 1) / (arg.n - 1))
		selected.add(idx)

count = 0
written = 0

with gzip.open(arg.output, 'wt') as fp:
	for file in arg.fastq:
		for header, seq, plus, qual in korflab.readfastq(file):
			if count in selected:
				fp.write(f'@{header}\n')
				fp.write(f'{seq}\n')
				fp.write('+\n')
				fp.write(f'{qual}\n')
				written += 1
			count += 1

print('input_files', len(arg.fastq), sep='\t')
print('input_reads', total, sep='\t')
print('requested_reads', arg.n, sep='\t')
print('sampled_reads', written, sep='\t')
print('output', arg.output, sep='\t')