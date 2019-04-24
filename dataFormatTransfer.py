# -*- coding: utf-8 -*-
# @Author: wuzida
# @Date:   2019-04-22 09:59:56
# @Last Modified by:   wuzida
# @Last Modified time: 2019-04-22 16:13:31
import csv
import timeTransfer
#import numpy as np
rosFilename = 'ros_20190411.txt'
basestationFilename = 'baseStation_20190411_3.txt'

outRosFilename = "post_ros_data.txt"
outRosFile = open(outRosFilename, "a+")
outBaseFilename = "post_basestation_data.txt"
outBaseFile = open(outBaseFilename,"a+")
outputFile = open("ros_basestation_data.txt", "a+")


defaultUnixStamp = 0
isAddUnixTimestamp2basedata = 0

with open(rosFilename) as ros_object:
    ros_reader = csv.reader(ros_object)
    ros_header_ros = next(ros_reader)
    post_ros_data = []
    line = 0
    writelines = 1
    for row_ros in ros_reader:
        sep = ','

        if line == 0:
            ros_timestamp = float(row_ros[0])
            post_ros_data.append(int(ros_timestamp))
            line = line + 1
            outRosFile.writelines(sep.join(row_ros))
            outRosFile.write("\n")
            temp_list1 = row_ros
        else:
            ros_timestamp = float(row_ros[0])
            post_ros_data.append(int(ros_timestamp))

            if (int(ros_timestamp)) == post_ros_data[line-1]:
                temp_list2 = row_ros
                for i in range(0,3):
                    temp_list2[i] = str((float(temp_list1[i]) + float(row_ros[i])) / 2)
                temp_list2[0] = row_ros[0]
                temp_list1 = temp_list2
                print("Dulplicate ros timestap lines: %d", line)
            else:
                outRosFile.writelines(sep.join(temp_list1))
                outRosFile.write("\n")
                outRosFile.flush()
                writelines = writelines + 1
                temp_list1 = row_ros
            line = line + 1
with open(outRosFilename) as post_ros_object:
    ros_reader2 = csv.reader(post_ros_object)
    ros_header_ros2 = next(ros_reader2)
    post_ros_data2 = []
    #ros_header_ros2 = next(ros_reader2)
    for row_ros2 in ros_reader2:
        post_ros_data2.append(int(float(row_ros2[0])))

with open(outRosFilename) as post_ros_object2:
    postRosLines = post_ros_object2.readlines()
    post_ros_object2.flush()
    with open(basestationFilename) as baseStation_object:
        stationDataLines = baseStation_object.readlines()
        baseStation_object.flush()
        post_basestation_data = []
        i = 0
        position = 0;
        for n in range(1,len(stationDataLines)):
            row_basestation = stationDataLines[n].split()
            if (int (row_basestation[3])) == 4:  #判断月份用于判断基站
                if n == 1 :
                    basestation_timestamp = timeTransfer.rawBaseList2unixstamp(row_basestation)
                    post_basestation_data.append( basestation_timestamp)
                    i = i + 1
                else:
                    basestation_timestamp = timeTransfer.rawBaseList2unixstamp(row_basestation)
                    post_basestation_data.append( basestation_timestamp )
                    if basestation_timestamp == post_basestation_data[i-1]:
                            print("Dulplicate basestation timestap lines %d ", n)
                    else:
                        try:
                            position = post_ros_data2.index(basestation_timestamp)
                        except ValueError:
                            position = -1
                        # diff = basestation_timestamp - post_basestation_data[i-1]
                        # position = position + diff;
                        if (position >=0 & position <= len(postRosLines)):
                            outputFile.writelines(postRosLines[position+1].strip('\n') + stationDataLines[n])
                            outputFile.flush()
                        # outputFile.write("\n")
                        i = i + 1

if isAddUnixTimestamp2basedata == 1:
    with open(basestationFilename) as baseStation_object2: #给基站数据加Unix时间戳
        stationDataLines2 = baseStation_object2.readlines()
        baseStation_object2.flush()
        post_basestation_data2 = []
        position = 0
        for n in range(1,len(stationDataLines2)):
            row_basestation2 = stationDataLines2[n].split()

            basestation_timestamp = timeTransfer.rawBaseList2unixstamp(row_basestation2)
            outBaseFile.writelines(str(basestation_timestamp) +"\t"+ stationDataLines2[n])
            outBaseFile.flush()



