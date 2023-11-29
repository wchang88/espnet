import argparse
import os
import sys


LANG_TO_CODE = {
   "korean": "ko",
}

def get_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("downloads_dir", type=str) # downloads data directory, ex: downloads/css10/german
   parser.add_argument("data_dir", type=str) # output data directory, ex: data/css10/german
   args = parser.parse_args()
   return args


def prepare_data_files(downloads_dir, data_dir):
   transcripts_file = os.path.join(downloads_dir, 'transcript.v.1.4.txt')
   _, dataset, lang = downloads_dir.split("/")
   lang_code = LANG_TO_CODE[lang]
   spkid = dataset + "_" + lang_code

   with open(transcripts_file, 'r', encoding="utf-8") as transcripts_f, open(
      os.path.join(data_dir, 'text'), 'w', encoding="utf-8"
   ) as text_f, open (
      os.path.join(data_dir, 'wav.scp'), 'w', encoding="utf-8"
   ) as wav_scp_f, open(
      os.path.join(data_dir, 'utt2spk'), 'w', encoding="utf-8"
   ) as utt2spk_f, open(
      os.path.join(data_dir, 'spk2utt'), 'w', encoding="utf-8"
   ) as spk2utt_f:
      for line in transcripts_f:
         audio_f, _, transcript, _, _, _ = line.strip().split("|")
         if len(transcript) == 0:
            continue
         uttid = dataset + "_" + lang_code + "_" + audio_f.split("/")[-1].split(".")[0]

         wav_scp_f.write(f"{spkid}-{uttid} {os.path.join(downloads_dir, 'kss', audio_f)}\n")
         text_f.write(f"{spkid}-{uttid} {transcript.strip()}\n")
         utt2spk_f.write(f"{spkid}-{uttid} {spkid}\n") 
         spk2utt_f.write(f"{spkid} {spkid}-{uttid}\n")
   
   with open(os.path.join(data_dir, 'spk2gender'), 'w', encoding='utf-8') as spk2gender_f:
      spk2gender_f.write(f"{dataset + '_' + lang_code} f")



if __name__ == "__main__":
   args = get_args()
   prepare_data_files(args.downloads_dir, args.data_dir)