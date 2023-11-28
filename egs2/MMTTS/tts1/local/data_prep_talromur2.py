import argparse
import os
import sys


LANG_TO_CODE = {
   "icelandic": "is",
}

SPKR_TO_GENDER = {
   's180': 'f', 
   's228': 'f', 
   's188': 'm',
   's273': 'm'
}

SPKRS = ['s180', 's228', 's188', 's273']

def get_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("downloads_dir", type=str) # downloads data directory, ex: downloads/css10/german
   parser.add_argument("data_dir", type=str) # output data directory, ex: data/css10/german
   args = parser.parse_args()
   return args


def prepare_data_files(downloads_dir, data_dir):
   with open(
      os.path.join(data_dir, 'text'), 'w', encoding="utf-8"
   ) as text_f, open (
      os.path.join(data_dir, 'wav.scp'), 'w', encoding="utf-8"
   ) as wav_scp_f, open(
      os.path.join(data_dir, 'utt2spk'), 'w', encoding="utf-8"
   ) as utt2spk_f, open(
      os.path.join(data_dir, 'spk2utt'), 'w', encoding="utf-8"
   ) as spk2utt_f:
      for spkr in SPKRS:
         transcripts_file = os.path.join(downloads_dir, spkr, 'index.tsv')
         _, dataset, lang = downloads_dir.split("/")
         lang_code = LANG_TO_CODE[lang]
         spkid = dataset + "_" + lang_code + "_" + spkr

         with open(transcripts_file, 'r', encoding="utf-8") as transcripts_f:
            for line in transcripts_f:
               parts = line.strip().split("\t")
               audio_f, _, transcript, _, bad_recording = parts[:5]
               if bad_recording == '0':
                  uttid = dataset + "_" + lang_code + "_" + audio_f

                  wav_scp_f.write(f"{spkid}-{uttid} {os.path.join(downloads_dir, spkr, 'audio', audio_f + 'wav')}\n")
                  text_f.write(f"{spkid}-{uttid} {transcript.strip()}\n")
                  utt2spk_f.write(f"{spkid}-{uttid} {spkid}\n") 
                  spk2utt_f.write(f"{spkid} {spkid}-{uttid}\n")



if __name__ == "__main__":
   args = get_args()
   prepare_data_files(args.downloads_dir, args.data_dir)