#!/bin/bash
export PYTHONIOENCODING=utf-8;
cd "$(dirname "$0")"

rm *.mp4
/usr/bin/python download_preroll_trailers.py 2>&1 | tee download_preroll_trailers.log

exit
