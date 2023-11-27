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