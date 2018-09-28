#!/bin/bash
#################
#多线程并发bash #
#################
export PATH=$PATH:/bin:/usr/bin:/usr/local/bin
exec 3>>/tmp/del.log
echo "====================================================" >&3
echo -e "\n[`date +%Y/%m/%d\ %H:%M:%S`] del $RUNUSER PID:$$" >&3

tmpfile=$$.fifo  #创建管道名称
mkfifo $tmpfile       #创建管道
exec 4<>$tmpfile      #创建文件标示4，以读写方式操作管道$tmpfile
rm $tmpfile           #将创建的通道文件清楚
thred=50    #指定并发数线程+1
#####变量###########
seq=`cat appdl-url | awk '{print $NF}'`
#####################
#为并发线程创建相应的个数占位
for (( i=1; i<=$thred;i++)); do
    echo "";
done >&4

rm -rf  >/tmp/appdl_pre_log
n=0

for I in $seq ; do
    read -u4
        {    
            info=`curl -A "Dnion_Precache" -I -X HEAD "$I" -x 127.0.0.1:80 2>/dev/null | grep HitType| grep HIT`
            if [ "$info"x == ""x ];then
                code=`curl -A "Dnion_Precache" --limit-rate 5M -so /dev/null -w '%{http_code}\n' $I -x 127.0.0.1:80`
                echo "[`date +%Y/%m/%d\ %H:%M:%S`] $info $code $I" >>/tmp/appdl_pre_log
            else
                echo "[`date +%Y/%m/%d\ %H:%M:%S`] HIT $code $I" >>/tmp/appdl_pre_log
            fi
#            echo "[`date +%Y/%m/%d\ %H:%M:%S`] HIT $code $I" >>/tmp/appdl_pre_log
#            n=`cat -n  appdl-url | grep $I | awk '{print $1}'`
#            np=`gawk -v x=$n -v y=1545895 'BEGIN{printf "%.2f%%",x * 100/y}'`
            echo >&4
         }&

#np=`gawk -v x=$n -v y=100 'BEGIN{printf "%.2f%%",x * 100/y}'`


done
wait
exec 4>&-
exit 0
