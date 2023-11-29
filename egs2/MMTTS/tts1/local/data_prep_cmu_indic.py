import argparse
import os
import sys


LANG_TO_CODE = {
   "hindi": "hi",
   "telugu": "te",
   "tamil": "ta",
   "kannada": "kn",
   "marathi": "mr",
   "gujarati": "gu",
   "bengali": "bn",
}


LANG_TO_SPEAKER = {
   "hindi": "ab",
   "telugu": "ss",
   "tamil": "sdr",
   "kannada": "plv",
   "marathi": "slp",
   "gujarati": "dp",
   "bengali": "rm",
}

LANG_TO_AUDIO = {
   "hindi": "hindi",
   "telugu": "tel",
   "tamil": "tamil",
   "kannada": "kan",
   "marathi": "data",
   "gujarati": "gu",
   "bengali": "bn",
}

def get_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("downloads_dir", type=str) # downloads data directory, ex: downloads/css10/german
   parser.add_argument("data_dir", type=str) # output data directory, ex: data/css10/german
   args = parser.parse_args()
   return args


def prepare_data_files(downloads_dir, data_dir):
   transcripts_file = os.path.join(downloads_dir, 'etc', 'txt.done.data')
   # /ocean/projects/cis230075p/wchang1/espnet/egs2/MMTTS/tts1/downloads/cmu_indic/bengali/cmu_indic_ben_rm/
   _, dataset, lang, _ = downloads_dir.split("/")
   lang_code = LANG_TO_CODE[lang]
   spkid = dataset + "_" + lang_code + "_" + LANG_TO_SPEAKER[lang]

   with open(transcripts_file, 'r', encoding="utf-8") as transcripts_f, open(
      os.path.join(data_dir, 'text'), 'w', encoding="utf-8"
   ) as text_f, open (
      os.path.join(data_dir, 'wav.scp'), 'w', encoding="utf-8"
   ) as wav_scp_f, open(
      os.path.join(data_dir, 'utt2spk'), 'w', encoding="utf-8"
   ) as utt2spk_f, open(
      os.path.join(data_dir, 'spk2utt'), 'w', encoding="utf-8"
   ) as spk2utt_f:
      valid_audiofile = LANG_TO_AUDIO[lang]
      for line in transcripts_f:
         line = line.strip("( )")
         if line.startswith(valid_audiofile):
            # This is not an arctic audio file
            utt, transcript, _ = line.split('"')
            utt = utt.strip()
            transcript = transcript.strip()
            uttid = dataset + "_" + lang_code + "_" + utt
            audio_f = utt + ".wav"

            wav_scp_f.write(f"{spkid}-{uttid} {os.path.join(downloads_dir, 'wav', audio_f)}\n")
            text_f.write(f"{spkid}-{uttid} {transcript.strip()}\n")
            utt2spk_f.write(f"{spkid}-{uttid} {spkid}\n") 
            spk2utt_f.write(f"{spkid} {spkid}-{uttid}\n")

   with open(os.path.join(data_dir, 'spk2gender'), 'w', encoding="utf-8") as spk2gender_f:
      spk2gender_f.write(f"{dataset + '_' + lang_code + '_' + LANG_TO_SPEAKER[lang]} f")


if __name__ == "__main__":
   args = get_args()
   prepare_data_files(args.downloads_dir, args.data_dir)