#!/bin/bash

OUTPUTDIR="/mnt/h/merged_fastq"
mkdir -p "$OUTPUTDIR"

echo "Input : /mnt/h/Sequence"
echo "Output: $OUTPUTDIR"
echo

for sample_dir in /mnt/h/Sequence/Sample*
do
	sample=$(basename "$sample_dir")
	sample_lower=$(echo "$sample" | tr 'A-Z' 'a-z')
	output_file="$OUTPUTDIR/${sample_lower}.fastq.gz"

	echo "========================================="
	echo "Processing: $sample"

	files=( "$sample_dir"/FC1/*/fastq_pass/*.fastq.gz )
	n_files=${#files[@]}

	if [ ! -e "${files[0]}" ]; then
		echo "No FASTQ files found. Skipping."
		echo
		continue
	fi

	echo "FASTQ chunks: $n_files"
	echo "Output: $output_file"

	rm -f "$output_file"

	i=0
	for fq in "${files[@]}"
	do
		i=$((i + 1))
		echo "  [$i/$n_files] adding $(basename "$fq")"
		cat "$fq" >> "$output_file"
	done

	echo "Done: $output_file"
	ls -lh "$output_file"
	echo
done

echo "All merging complete."