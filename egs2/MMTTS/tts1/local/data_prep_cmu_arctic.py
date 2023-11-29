import argparse
import os
import sys


LANG_TO_CODE = {
   "english": "en_us",
}

SPKRS = ["awb", "bdl", "clb", "jmk", "ksp", "rms", "slt"]

SPKRS_TO_GENDER = {
   "awb":'m', 
   "bdl":'m', 
   "clb":'f', 
   "jmk":'m', 
   "ksp":'m', 
   "rms":'m', 
   "slt":'f'
}

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
         transcripts_file = os.path.join(downloads_dir, spkr, f"cmu_us_{spkr}_arctic", 'etc', 'txt.done.data')

         _, dataset, lang = downloads_dir.split("/")
         lang_code = LANG_TO_CODE[lang]
         spkid = dataset + "_" + lang_code + "_" + spkr

         with open(transcripts_file, 'r', encoding="utf-8") as transcripts_f:
            for line in transcripts_f:
               line = line.strip("( )")
               if line.startswith("arctic_a"):
                  # This is the a version of the arctic files
                  utt, transcript, _ = line.split('"')
                  utt = utt.strip()
                  transcript = transcript.strip()
                  if len(transcript) == 0:
                     continue
                  uttid = dataset + "_" + lang_code + "_" + spkr + "_" + utt
                  audio_f = utt + ".wav"

                  wav_scp_f.write(f"{spkid}-{uttid} {os.path.join(downloads_dir, spkr, f'cmu_us_{spkr}_arctic', 'wav', audio_f)}\n")
                  text_f.write(f"{spkid}-{uttid} {transcript.strip()}\n")
                  utt2spk_f.write(f"{spkid}-{uttid} {spkid}\n") 
                  spk2utt_f.write(f"{spkid} {spkid}-{uttid}\n")

   with open(os.path.join(data_dir, 'spk2gender'), 'w', encoding="utf-8") as spk2gender_f:
      for spkr in SPKRS_TO_GENDER:
         spk2gender_f.write(f"{dataset + '_' + lang_code + '_' + spkr} {SPKRS_TO_GENDER[spkr]}\n")



if __name__ == "__main__":
   args = get_args()
   prepare_data_files(args.downloads_dir, args.data_dir)