#!/usr/bin/env python

from date_helper import str_to_time, get_add_datest2
import log_helper
import subprocess, time, datetime, os

delay1_date = get_add_datest2(-1)
global __log__path
__log__path = "/opt/scripts/appv/result/%s" %(str(delay1_date))

def logger(mes):
    log_helper.get_logger(__log__path).info(mes)

def awk(file):
    start = datetime.datetime.now()
    cmd = 'awk -F"|" \'{print $9}\' %s | sort -u' % (file)
    p = subprocess.Popen(cmd, bufsize=10000, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=True)
    while p.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > 300:
            try:
                p.terminate()
            except Exception as e:
                return None
    return p.stdout.read().strip().split('\n')


def ticket_lines(file):
    f = open(file, 'r')
    line = f.readline()
    while line:
        # yield line
        yield line.split("|")
        line = f.readline()
    f.close()
    yield None


def diff_time(connent_list=[]):
    start_time = str_to_time(connent_list[6])
    end_time = str_to_time(connent_list[7])
    time_diff = (end_time - start_time)
    return time_diff


def play_version(play_list=[]):
    for play_v in play_list:
        if connent[10] == play_v:
            diff_time(connent)
            num += 1
            diff_time(connent)


if __name__ == "__main__":
    play_info = {}
    ticket_file = "/data/ftpsite/DataCenter/tysx_hms_%s_ver1.txt" %(str(delay1_date))
    play_list = awk(ticket_file)
    for play_v in play_list:
        a = [0, ]
        for ticket_log_line in ticket_lines(ticket_file):
            try:
                if str(ticket_log_line[8]) == str(play_v):
                    time_diff = diff_time(ticket_log_line)
                    a.append(time_diff)
            except Exception as e:
                print e
        play_sum = sum(a)
        logger("paly %s sum is %d" %(play_v, play_sum))
        play_num = len(a)
        logger("play %s num is %d" %(play_v, play_num))
        play_avg = play_sum / play_num
        logger("play %s play_avg_time is %d" %(play_v, play_avg))
        play_info['play_%s' %str(play_v)] = play_avg

    print play_info
    mail_mes = "TYSX Play INFO: \n"
    for i in play_info:
        m = "%s:%d \n" %(i,play_info[i])
        mail_mes += m
   
logger(mail_mes)
