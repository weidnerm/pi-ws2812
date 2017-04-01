import math

leds = [68, 47, 79]

def main():

	print("do")
	for index in xrange(255):
		print("    rainbow 1,1,47,1,%d,%d" % ((index+0*255/3)%255,(index+0*255/3)%255) )
		print("    rainbow 1,1,68,1,%d,%d" % ((index+0*255/3)%255,(index+0*255/3)%255) )
		print("    rainbow 1,1,79,1,%d,%d" % ((index+0*255/3)%255,(index+0*255/3)%255) )
		#~ if index == 25:
			#~ print("    fill 1,ffffff,47,1")
		#~ if index == 30:
			#~ print("    fill 1,ffffff,68,1")
		#~ if index == 60:
			#~ print("    fill 1,ffffff,79,1")
		print("    render")
		print("    delay 25")
	print("loop")


def fadeColor(colorRGB, duration, fadeIn):
	base = 1.0
	logBright = []
	brightnessTransSteps = int(duration/0.025)  # 25 msec steps
	scaleFactor = math.pow(10,math.log10(255)/brightnessTransSteps)
	base = scaleFactor
	#~ print("# brightnessTransSteps=%d" % brightnessTransSteps)
	#~ print("# scaleFactor=%f" % scaleFactor)
	for index in xrange(brightnessTransSteps):
		logBright.append(int(base))
		base = base * scaleFactor

	for index in xrange(brightnessTransSteps):
		outText = ""
		if fadeIn:
			brightnessIndex = index
		else:
			brightnessIndex = brightnessTransSteps-index-1
			
		outText = outText + "brightness 1,%d;" % (logBright[brightnessIndex])
		for ledIndex in xrange(len(leds)):
			outText = outText + "fill 1,%06x,%d,1;" % (colorRGB, leds[ledIndex]) 
		outText = outText + "render;"
		outText = outText + "delay 25"
	
		print(outText)
		


def main2():
	base = 1.0
	logBright = []
	brightnessTransSteps = 40
	scaleFactor = math.log(255)/brightnessTransSteps
	for index in xrange(brightnessTransSteps):
		logBright.append(int(base))
		base = base * scaleFactor

	print("do")
	for reps in xrange(3):
		for index in xrange(255):
			ledBrightnesses = []
			for ledindex in xrange(len(leds)):
				ledBrightnesses.append(0)
				
			#~ if index >= 0 and index < 64:
				#~ ledBrightnesses[0] = 255
			#~ if index >= 64 and index < 128:
				#~ ledBrightnesses[1] = 255
			#~ if index >= 128 and index < 192:
				#~ ledBrightnesses[2] = 255


			if index >= 0 and index < 64:
				ledBrightnesses[0] = logBright[index-0]
			if index >= 64 and index < 128:
				ledBrightnesses[0] = logBright[127-index]
				ledBrightnesses[1] = logBright[index-64]
			if index >= 128 and index < 192:
				ledBrightnesses[1] = logBright[191-index]
				ledBrightnesses[2] = logBright[index-128]
			if index >= 192 and index < 256:
				ledBrightnesses[2] = logBright[255-index]
			
			for ledindex in xrange(len(leds)):
				if ledBrightnesses[ledindex] >= 256:
					ledBrightnesses[ledindex] = 255 # cap the brightness
						
			for ledindex in xrange(len(leds)):
				print("    fill 1,%02x%02x%02x,%d,1" % ( 
					ledBrightnesses[ledindex]*(reps==0),
					ledBrightnesses[ledindex]*(reps==1),
					ledBrightnesses[ledindex]*(reps==2),
					leds[ledindex]
					))

			print("    render")
			print("    delay 25")


		#~ for index in xrange(255,0,-1):
			#~ ledBrightnesses = []
			#~ for ledindex in xrange(len(leds)):
				#~ ledBrightnesses.append(0)
#~ 
#~ 
			#~ if index >= 0 and index < 64:
				#~ ledBrightnesses[0] = (index-0)*4
			#~ if index >= 64 and index < 128:
				#~ ledBrightnesses[0] = (128-index)*4
				#~ ledBrightnesses[1] = (index-64)*4
			#~ if index >= 128 and index < 192:
				#~ ledBrightnesses[1] = (192-index)*4
				#~ ledBrightnesses[2] = (index-128)*4
			#~ if index >= 192 and index < 256:
				#~ ledBrightnesses[2] = (256-index)*4
			#~ 
			#~ for ledindex in xrange(len(leds)):
				#~ if ledBrightnesses[ledindex] >= 256:
					#~ ledBrightnesses[ledindex] = 255 # cap the brightness
						#~ 
			#~ for ledindex in xrange(len(leds)):
				#~ print("    fill 1,%02x%02x%02x,%d,1" % ( 
					#~ ledBrightnesses[ledindex],
					#~ ledBrightnesses[ledindex],
					#~ ledBrightnesses[ledindex],
					#~ leds[ledindex]
					#~ ))
#~ 
			#~ print("    render")
			#~ print("    delay 25")


	print("loop")

def setup():
	print("setup channel_1_count=150")
	print("brightness 1,255")
	print("fill 1")
	print("render")


if __name__ == "__main__":
    setup();
    fadeColor(0xff0000, 1.0, True)
    fadeColor(0xff0000, 1.0, False)
    fadeColor(0xed3000, 1.0, True)
    fadeColor(0xed3000, 1.0, False)
    fadeColor(0xffc000, 1.0, True)
    fadeColor(0xffc000, 1.0, False)
    fadeColor(0x00ff00, 1.0, True)
    fadeColor(0x00ff00, 1.0, False)
    fadeColor(0x0000ff, 1.0, True)
    fadeColor(0x0000ff, 1.0, False)
    fadeColor(0xff00ff, 1.0, True)
    fadeColor(0xff00ff, 1.0, False)
    #~ main2();
