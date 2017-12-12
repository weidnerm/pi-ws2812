import time;
import math;

strandLen = 240
    
f = open("/dev/rgbled", "w")
f.write("setup channel_1_count=%d\n" % strandLen)
f.write("brightness 1,128\n")
f.close()

def sendSegment(f, pos, length, color):
    
    start1 = math.floor(pos) % strandLen
    length1 = length
    if start1+length > strandLen:
        length1 = strandLen - start1
        
    f.write("fill 1,%s,%d,%d\n" % (color, start1, length1) )

    if length != length1:
        length2 = length - length1
        start2 = 0
        f.write("fill 1,%s,%d,%d\n" % (color, start2, length2) )

try:
    i = 200

    while True:
        f = open("/dev/rgbled", "w")
        f.write("rainbow 1,5\n" )
        f.write("rotate 1,%d,0\n" % (math.floor(i/2)%strandLen) )
        sendSegment(f, strandLen-1-((i/2+0 ) % strandLen), 5, 'ffffff')
        sendSegment(f, strandLen-1-((i/3+15 ) % strandLen), 5, 'ffffff')
        sendSegment(f, strandLen-1-((i/2+75) % strandLen), 5, 'ffffff')
        sendSegment(f, strandLen-1-((i/2+150) % strandLen), 5, 'ffffff')
        sendSegment(f, 0+(i%strandLen)       , 7, '000000')

        f.write("render\n")
        f.close()
        i = i + 1
        if i == 240*1000:
            i = 0

        time.sleep(0.050)
        
        
finally:
    f = open("/dev/rgbled", "w")
    f.write("fill 1\n" )
    f.write("render\n")
    f.close()

