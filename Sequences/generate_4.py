import random

maxEachTime = 2
maxSizeEach = 10
delayDuration = 100
numLeds = 240

def deg2color(WheelPos):
    if WheelPos < 85:
        color = "%02X%02X%02X" % (255 - WheelPos * 3,WheelPos * 3 , 0)
    elif WheelPos < 170:
        WheelPos = WheelPos -85
        color = "%02X%02X%02X" % (0, 255 - WheelPos * 3, WheelPos * 3)
    else:
        WheelPos = WheelPos -170
        color = "%02X%02X%02X" % (WheelPos * 3, 0, 255 - WheelPos * 3)
    
    return color



fileHandle = open("color_bonanza.txt", "w")

fileHandle.write("setup channel_1_count=%d\n" % (numLeds) )
fileHandle.write("brightness 1,128\n")
fileHandle.write("fill 1;render\n")
fileHandle.write("do\n")

for index in range(120):
    numPatches = random.randint(1,maxEachTime)
    
    output = ""
    for patchNum in range(numPatches):
        startpos = random.randint(0,numLeds-maxSizeEach-1)
        length = random.randint(1,maxSizeEach)
        colorDegs = (random.randint(0,12)*255/12 ) %255
        
        output = output + '    fill 1,%s,%d,%d\n' % ( deg2color(colorDegs), startpos, length )
        
    fileHandle.write(output)
    fileHandle.write("render\n")
    fileHandle.write("delay %d\n" % delayDuration)

# rotate it around once
fileHandle.write("do\n")
fileHandle.write('    rotate 1,1,0\n')
fileHandle.write("    render\n")
fileHandle.write("    delay 25\n")
fileHandle.write("loop 60\n")

fileHandle.write("loop\n")


fileHandle.close();
