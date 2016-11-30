import time;
import math;

f = open("/dev/rgbled", "w")
f.write("setup channel_1_count=150\n")
f.write("brightness 1,128\n")
f.close()


for i in xrange(1000):
    f = open("/dev/rgbled", "w")
    f.write("rainbow 1,10\n" )
    f.write("rotate 1,%d,0\n" % (math.floor(i/2)%150) )
    f.write("fill 1,ffffff,%d,10\n" % (139-(i%140)) )
    f.write("fill 1,ffffff,%d,10\n" % (139-((i+75)%140)) )
    f.write("fill 1,101010,%d,10\n" % (0+(i%140)) )

    f.write("render\n")

    f.close()
    time.sleep(0.050)



