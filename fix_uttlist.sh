#!/bin/bash
in_dir=/workspace/espnet/egs2/aishell/asr1/data_zhaoli/local/test/
out_dir=/workspace/espnet/egs2/aishell/asr1/data_zhaoli/test/
utils/filter_scp.pl -f 1 ${in_dir}/utt.list_new ${in_dir}/trans_org.txt > ${in_dir}/transcripts.txt
awk '{print $1}' ${in_dir}/transcripts.txt > ${in_dir}/utt.list
utils/filter_scp.pl -f 1 ${in_dir}/utt.list ${in_dir}/utt2spk_all | sort -u > ${out_dir}utt2spk
utils/filter_scp.pl -f 1 ${in_dir}/utt.list ${in_dir}/wav.scp_all | sort -u > ${out_dir}/wav.scp
sort -u ${in_dir}/transcripts.txt > ${out_dir}/text
utils/utt2spk_to_spk2utt.pl ${out_dir}/utt2spk > ${out_dir}/spk2utt
