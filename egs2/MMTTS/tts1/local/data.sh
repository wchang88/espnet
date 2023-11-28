#!/usr/bin/env bash

set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0


log "Stage 0: Download data and preliminary data prep..."

# download, unzip, data prep, g2p
log "\t0.1: Downloading CMU Arctic dataset and prepping"
local/download_and_prep_cmu_arctic.sh

log "\t0.2: Downloading CMU Indic dataset and prepping"
local/download_and_prep_cmu_indic.sh

log "\t0.3: Downloading CSS10 dataset and prepping"
local/download_and_prep_css10.sh

log "\t0.4: Downloading KSS dataset and prepping"
local/download_and_prep_kss.sh

log "\t0.5: Downloading Talromur2 dataset and prepping"
local/download_and_prep_talromur.sh

# log "\t0.4: Downloading CML-TTS dataset and prepping"
# local/download_and_prep_cmltts.sh

log "Stage 1: Partition train/dev/test per lang and merge"
train_set=train
dev_set=dev
eval_set=test
suffix=""
text_format=phn
if [ "${text_format}" = phn ]; then
   suffix="_phn"
fi
combine_train_dirs=()
combine_dev_dirs=()
combine_eval_dirs=()
for lang in ${langs}; do
   utils/subset_data_dir.sh "data/${lang}${suffix}" 100 "data/${lang}_deveval${suffix}"
   utils/subset_data_dir.sh --first "data/${lang}_deveval${suffix}" 50 "data/${lang}_${dev_set}${suffix}"
   utils/subset_data_dir.sh --last "data/${lang}_deveval${suffix}" 50 "data/${lang}_${eval_set}${suffix}"
   utils/copy_data_dir.sh "data/${lang}${suffix}" "data/${lang}_${train_set}${suffix}"
   utils/filter_scp.pl --exclude "data/${lang}_deveval${suffix}/wav.scp" \
      "data/${lang}${suffix}/wav.scp" > "data/${lang}_${train_set}${suffix}/wav.scp"
   utils/fix_data_dir.sh "data/${lang}_${train_set}${suffix}"
   combine_train_dirs+=("data/${lang}_${train_set}${suffix}")
   combine_dev_dirs+=("data/${lang}_${dev_set}${suffix}")
   combine_eval_dirs+=("data/${lang}_${eval_set}${suffix}")
done
utils/combine_data.sh "data/${train_set}${suffix}" "${combine_train_dirs[@]}"
utils/combine_data.sh "data/${dev_set}${suffix}" "${combine_dev_dirs[@]}"
utils/combine_data.sh "data/${eval_set}${suffix}" "${combine_eval_dirs[@]}"