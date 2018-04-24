#!/bin/bash
cd "$(dirname "$0")"

rm *.mp4
/usr/bin/python download_preroll_trailers.py

exit
