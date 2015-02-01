#!/bin/bash
# How to build nginx:
# ./configure --add-module=/home/sources/nginx-rtmp-module --with-ipv6
# make -j2; make install

NGINX="/home/sources/nginx-1.7.9/objs/nginx -c `pwd`/nginx.conf"
UPSTREAM="rtmp://localhost/rtmp/live"
case  $1  in
  start)
    $NGINX
    #raspivid -n -mm matrix -w 1280 -h 720 -fps 25 -g 250 -t 0 -b 10000000 -vf -o - \
    raspivid -n -mm matrix -w 1280 -h 720 -fps 25 -g 250 -t 0 -b 10000000  -o - \
    | ffmpeg -y -i - -c:v copy -map 0:0 -f flv \
    -loglevel error \
    -rtmp_buffer 100 -rtmp_live live $UPSTREAM &
  ;;
  stop)
    $NGINX -s quit 2> /dev/null
    killall nginx ffmpeg raspivid 2> /dev/null
  ;;
  *)
    echo "$0 start|stop"
esac


