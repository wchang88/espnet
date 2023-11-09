#!/usr/bin/env bash

set -e
set -u
set -o pipefail

log() {
   local fname=${BASH_SOURCE[1]##*/}
   echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0

db=$1
lang=$2

available_langs=(
   "dutch "french" "german" "italian" "polish" "portuguese" "spanish" "ru_RU" "pl_PL"
)

# check arguments
if [ $# != 2 ]; then
   echo "Usage: $0 <tar_dir> <lang_tag>"
   echo "Available languages: ${available_langs[*]}"
   exit 1
fi

# check language
if ! $(echo ${available_langs[*]} | grep -q ${lang}); then
   echo "Specified language is not available or not supported."
   exit 1
fi

# download dataset
cwd=`pwd`
if [ ! -e ${db}/${lang} ]; then
   mkdir -p ${db}
   cd ${db}
   wget https://www.openslr.org/resources/146/cml_tts_dataset_${lang}_v0.1.tar.bz
   tar xvf cml_tts_dataset_${lang}_v0.1.tar.bz
   rm cml_tts_dataset_${lang}_v0.1.tar.bz
   cd $cwd
   echo "Successfully finished download."
else
   echo "Already exists. Skip download."
fi