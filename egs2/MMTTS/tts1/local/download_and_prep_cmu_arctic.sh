#!/usr/bin/env bash

set -e
set -u
set -o pipefail

# reference: egs2/cmu_indic/tts1/local/data.sh

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0

text_format=raw
threshold=35
nj=32

log "$0 $*"
# shellcheck disable=SC1091
. utils/parse_options.sh

if [ $# -ne 0 ]; then
   log "Error: No positional arguments are required."
   exit 2
fi

# shellcheck disable=SC1091
. ./path.sh || exit 1;
# shellcheck disable=SC1091
. ./cmd.sh || exit 1;
# shellcheck disable=SC1091
. ./db.sh || exit 1;

BASE_DIR=$(pwd)

lang_code="us-en"
lang="english"
spkrs="slt clb bdl rms jmk awb ksp"

log 'STARTING DOWNLOAD AND DATA PREPARATION FOR CMU ARCTIC'

DOWNLOADS_DIR=downloads/cmu_arctic
DATA_DIR=data
mkdir -p "${DOWNLOADS_DIR}" "${DATA_DIR}"

for spkr in ${spkrs}; do
   if [ ! -e "${DOWNLOADS_DIR}"/"${lang}"_"${spkr}".done ]; then
      # download data
      log Downloading "${lang}" speech data from speaker "${spkr}"...
      mkdir -p "${DOWNLOADS_DIR}"/"${lang}"/"${spkr}"
      wget http://festvox.org/cmu_arctic/cmu_arctic/packed/cmu_us_${spkr}_arctic-0.95-release.tar.bz2
      tar xf cmu_us_${spkr}*.tar.bz2 --directory "${DOWNLOADS_DIR}"/"${lang}"/"${spkr}"
      rm cmu_us_${spkr}*.tar.bz2
      touch "${DOWNLOADS_DIR}"/"${lang}"_"${spkr}".done
      log Finished downloading "${lang}"_"${spkr}" speech data
   else
      log "${lang}"_"${spkr}" speech data already downloaded. Please manually check the "${DOWNLOADS_DIR}"/"${lang}"/"${spkr}" directory to make sure the data is there
   fi
done

log Preparing "${lang}" data files
mkdir -p "${DATA_DIR}"/"${lang}"
python local/data_prep_cmu_arctic.py "${DOWNLOADS_DIR}"/"${lang}" "${DATA_DIR}"/"${lang}"
log Finished preparing "${lang}" data files in "${DATA_DIR}"/"${lang}"


log 'CMU ARCTIC DOWNLOAD AND DATA PREPARATION COMPLETED'
touch downloads/cmu_indic.done
echo "" >> db.sh
echo CMU_ARCTIC="${BASE_DIR}"/"${DOWNLOADS_DIR}" >> db.sh

cd "${BASE_DIR}"

# log "stage 1: scripts/audio/trim_silence.sh"
# for lang in ${langs}; do
#    # shellcheck disable=SC2154
#    scripts/audio/trim_silence.sh \
#       --cmd "${train_cmd}" \
#       --nj "${nj}" \
#       --fs 22050 \
#       --win_length 1024 \
#       --shift_length 256 \
#       --threshold "${threshold}" \
#       "data/${lang}" "data/${lang}/log"
# done


# log "stage 2: pyscripts/utils/convert_text_to_phn.py"
# # define g2p dict
# declare -A g2p_dict=(
#    ["english"]="espeak_ng_english_us_vits"
# )

# for lang in ${langs}; do
#    g2p=${g2p_dict[${lang}]}
#    utils/copy_data_dir.sh "${DATA_DIR}"/"${lang}" "${DATA_DIR}"/"${lang}"_phn
#    pyscripts/utils/convert_text_to_phn.py \
#       --g2p "${g2p}" --nj "${nj}" \
#       "data/${lang}/text" "data/${lang}_phn/text"
#    utils/fix_data_dir.sh "data/${lang}_phn"
# done


log "Successfully finished. [elapsed=${SECONDS}s]"