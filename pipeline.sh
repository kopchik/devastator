#!/bin/bash
NGINX="/home/sources/nginx-1.7.7/objs/nginx -c `pwd`/nginx.conf"
UPSTREAM="rtmp://localhost/rtmp/live"
case  $1  in
  start)
    $NGINX
    raspivid -n -w 640 -h 480 -fps 30 -t 0 -b 100000 -vf -o - \
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

