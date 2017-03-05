#!/bin/bash
LOG_FILE=/var/log/weixind/weixind_watchdog.log
if [ ! -f ${LOG_FILE} ]; then
  touch ${LOG_FILE}
fi

TS=`date`
ps -ef|grep python | grep weixind.py
if [ $? -eq 0 ]; then
  echo "${TS} weixind is running" >> ${LOG_FILE}
else
  echo "${TS} weixind is not runing, start it" >> ${LOG_FILE}
  cd ~/workspace/Weixind
  python weixind/weixind.py &
  cd -
fi
