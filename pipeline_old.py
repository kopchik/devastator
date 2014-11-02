#!/usr/bin/env python3
import atexit
import csv
from subprocess import Popen, check_call, DEVNULL
from os import path

OUTPUT = "/home/stream/"
SEGMENTS_INDEX = OUTPUT + "segments.csv"
PIPELINE = """
raspivid -w 800 -h 600 -o - -t 9999999 \
 | ffmpeg -y -i - -c:v copy -map 0:0 \
     -f ssegment -segment_time 10 \
     -segment_list {idx} -segment_list_flags live -segment_list_size 10 \
     -loglevel warning \
     -movflags faststart \
     {out}/%08d.mp4
"""
#-segment_format_options movflags=+faststart \
CONVERT = """ffmpeg -y -i {inpt} -vcodec copy -acodec copy {out}"""

def start():
  cmd = PIPELINE.format(out=OUTPUT, idx=SEGMENTS_INDEX)
  pipeline = Popen(cmd, shell=True)
  def cleanup():
    check_call("rm -rf %s/*" % OUTPUT, shell=True)
  atexit.register(cleanup)
  atexit.register(pipeline.terminate)
  return pipeline


def get_latest():
  with open(SEGMENTS_INDEX, 'rt') as fd:
    for f, start, end in csv.reader(fd):
      pass
  print("the latest segment is", f)
  return f
