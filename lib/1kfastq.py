#!/usr/bin/env python3

import argparse
import korflab

parser = argparse.ArgumentParser(
	description='check systematic fastq sampling indexes')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('-n', type=int, default=1000,
	help='number of reads [%(default)d]')
arg = parser.parse_args()

total = 0

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	total += 1

if total < arg.n:
	raise SystemExit(f'error: requested {arg.n} reads, but input only has {total}')

selected = []

if arg.n == 1:
	selected.append(0)
else:
	for i in range(arg.n):
		idx = round(i * (total - 1) / (arg.n - 1))
		selected.append(idx)

print('input_reads', total, sep='\t')
print('requested_reads', arg.n, sep='\t')
print('selected_reads', len(selected), sep='\t')
print('first_index', selected[0], sep='\t')
print('last_index', selected[-1], sep='\t')

print()
print('first_10_indexes')
for idx in selected[:10]:
	print(idx)

print()
print('last_10_indexes')
for idx in selected[-10:]:
	print(idx)
