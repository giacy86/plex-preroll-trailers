#!/bin/bash
cd "$(dirname "$0")"
output="preroll_trailers.mp4"

rm $output
/usr/bin/python mix_preroll_trailers.py
ffmpeg -f concat -safe 0 -i selected_trailers.txt -c copy $output

exit
