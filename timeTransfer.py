# -*- coding: utf-8 -*-
# @Author: wuzida
# @Date:   2019-04-22 09:59:56
# @Last Modified by:   wuzida
# @Last Modified time: 2019-04-22 16:13:31
import time
#dateformat utctime = 201804110712
def rawBaseList2unixstamp(row_basestation):
    utctime = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(int(row_basestation[2]), int(row_basestation[3]),
                                                             int(row_basestation[4]),
                                                             int(row_basestation[5])+8, int(row_basestation[6]),
                                                             int(row_basestation[7]))  # 转换为时间数组
    timeArray = time.strptime(utctime, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timestamp = time.mktime(timeArray)


    return int(timestamp)