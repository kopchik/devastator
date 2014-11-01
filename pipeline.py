#!/usr/bin/env python3
import atexit
from subprocess import Popen, DEVNULL

OUTPUT = "/home/stream"
PIPELINE = """
raspivid -w 800 -h 600 -o - -t 9999999 \
 | ffmpeg -y -i - -c:v copy -map 0:0 \
     -f ssegment -segment_time 10 -segment_format mpegts \
     -segment_list out.csv -segment_list_flags live -segment_list_size 10 \
     {}/%08d.ts
"""
cmd = PIPELINE.format(OUTPUT)
pipeline = Popen(cmd, shell=True)
atexit(pipeline.terminate)
pipeline.wait()