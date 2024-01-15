#!/bin/bash -e

rm -rf mp3/examples/*
for input_wav_file in $(find wav/examples -type f -name *.wav)
do
  subject_id="$(basename $input_wav_file .wav)"
  ffmpeg -i $input_wav_file -vn -ar 44100 -ac 2 -b:a 192k mp3/examples/$subject_id.mp3
done
