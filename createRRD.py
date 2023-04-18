
#!/usr/bin/env python
import rrdtool
def rrdtool_create(db_name):
    db_name = db_name +'.rdd'
    ret = rrdtool.create(db_name,
                        "--start",'N',
                        "--step",'60',
                        "DS:packunicast:COUNTER:120:U:U",
                        "DS:packproip:COUNTER:120:U:U",
                        "DS:menICMP:COUNTER:120:U:U",
                        "DS:segmentos:COUNTER:120:U:U",
                        "DS:dataUDP:COUNTER:120:U:U",
                        "RRA:AVERAGE:0.5:5:5",
                        "RRA:AVERAGE:0.5:1:20")

    if ret:
        print (rrdtool.error())