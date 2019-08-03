#!/bin/bash
if [ "`ps -ef|grep -m 1 python |grep -v grep|wc -l`" != "0"  ];then
    kill -9 `ps -ef|grep python |grep -v grep|grep -v kill|awk '{print $2}'`
else
    echo python ' No Found Process'
fi
nohup python -u ../run.py > /logs/spider.log 2>&1 &
tail -f /logs/spider.log