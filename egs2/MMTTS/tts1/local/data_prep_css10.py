import argparse
import os
import sys


LANG_TO_CODE = {
   "german": "de",
   "greek": "el",
   "spanish": "es",
   "finnish": "fi",
   "french": "fr",
   "hungarian": "hu",
   "japanese": "ja",
   "dutch": "nl",
   "russian": "ru",
   "chinese": "zh"
}

LANG_TO_G2P = {
   "german": "espeak_ng_german",
   "greek": "espeak_ng_greek",
   "spanish": "espeak_ng_spanish",
   "finnish": "espeak_ng_finnish",
   "french": "espeak_ng_french",
   "hungarian": "espeak_ng_hungarian",
   "japanese": "espeak_ng_japanese", # TODO: add g2p to espnet2/text/phoneme_tokenizer.py
   "dutch": "espeak_ng_dutch",
   "russian": "espeak_ng_russian",
   "chinese": "espeak_ng_chinese" # TODO: add g2p to espnet2/text/phoneme_tokenizer.py
}

LANG_TO_SPEAKER = {
   "german": "Hokuspokus",
   "greek": "Rapunzelina",
   "spanish": "Tux",
   "finnish": "HarriTapaniYlilammi",
   "french": "GillesGLeBlanc",
   "hungarian": "DianaMajlinger",
   "japanese": "ekzemplaro", 
   "dutch": " 	BartdeLeeuw",
   "russian": "MarkChulsky",
   "chinese": "JingLi" 
}

def get_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("downloads_dir", type=str) # downloads data directory, ex: downloads/css10/german
   parser.add_argument("data_dir", type=str) # output data directory, ex: data/css10/german
   args = parser.parse_args()
   return args


def prepare_data_files(downloads_dir, data_dir):
   transcripts_file = os.path.join(downloads_dir, 'transcript.txt')
   _, dataset, lang = downloads_dir.split("/")
   lang_code = LANG_TO_CODE[lang]
   g2p = LANG_TO_G2P[lang]
   spkid = dataset + "_" + lang_code + "_" + LANG_TO_SPEAKER[lang]

   with open(transcripts_file, 'r', encoding="utf-8") as transcripts_f, open(
      os.path.join(data_dir, 'text'), 'w', encoding="utf-8"
   ) as text_f, open (
      os.path.join(data_dir, 'wav.scp'), 'w', encoding="utf-8"
   ) as wav_scp_f, open(
      os.path.join(data_dir, 'utt2spk'), 'w', encoding="utf-8"
   ) as utt2spk_f, open(
      os.path.join(data_dir, 'spk2utt', 'w', encoding="utf-8")
   ) as spk2utt_f:
      for line in transcripts_f:
         audio_f, transcript, _ = line.strip().split("|")
         uttid = dataset + "_" + lang_code + "_" + audio_f.split("/")[-1]

         wav_scp_f.write(f"{spkid}-{uttid} {audio_f}\n")
         text_f.write(f"{spkid}-{uttid} {transcript.strip()}\n")
         utt2spk_f.write(f"{spkid}-{uttid} {spkid}\n") 
         spk2utt_f.write(f"{spkid} {spkid}-{uttid}\n")



if __name__ == "__main__":
   args = get_args()
   prepare_data_files(args.downloads_dir, args.data_dir)