import math

leds = [68, 47, 79]

def fadeColor(colorRGB, duration, fadeIn):
	base = 1.0
	logBright = []
	brightnessTransSteps = int(duration/0.025)  # 25 msec steps
	scaleFactor = math.pow(10,math.log10(255)/brightnessTransSteps)
	base = scaleFactor

	if fadeIn:
		fadeText = "In"
	else:
		fadeText = "Out"
	print( "#" )
	print( "# Fade color %06x %s over %f seconds" % (colorRGB, fadeText, duration ) )

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
		


def timeRainbow(duration, repeats=1):
	steps = int(duration/0.025)  # 25 msec steps

	print( "#" )
	print( "# Rainbow for %f seconds repeated %d times" % (duration,repeats) )
	print( "brightness 1,%d;" % (255) )
	print( "do" )
	for index in xrange(steps):
		outText = "    "
		wheelFrac = float(index)/float(steps)*256
		for ledIndex in xrange(len(leds)):
			outText = outText + "rainbow 1,1,%d,1,%d,%d;" % ( leds[ledIndex], wheelFrac,wheelFrac) 
		outText = outText + "render;"
		outText = outText + "delay 25"
		print(outText)
	print( "loop %d" % (repeats) )


	
def spotlightMove(duration, repeats=1):
	rampDuration = duration/len(leds)
	print("brightness 1,255")
	print("fill 1")

	print( "#" )
	print( "# Ramp up spotlight over %f seconds" % (rampDuration) )
	__rampLedPair(rampDuration, 0, True, False)
	
	print( "#" )
	print( "# sweep spotlight over %f seconds %d times" % (duration,repeats) )
	print( "do" )
	for index in xrange(len(leds)):
		__rampLedPair(rampDuration, index+1, True, True)
	print( "loop %d" % repeats )
	
	print( "#" )
	print( "# Ramp down spotlight over %f seconds" % (rampDuration) )
	__rampLedPair(rampDuration, 1, False, True)

def __rampLedPair(duration, brightLedIndex, doBright, doDim):
	steps = int(duration/0.025)  # 25 msec steps

	for index in xrange(steps):
		outText = "    "
		timeFrac = float(index)/float(steps)
		
		if doBright:
			outText = outText + __getCmdForLEDBrightness(timeFrac, brightLedIndex)
		if doDim:
			outText = outText + __getCmdForLEDBrightness(1.0-timeFrac, (brightLedIndex-1) % len(leds) )
			
		outText = outText + "render;"
		outText = outText + "delay 25"
		print(outText)
		


def __getCmdForLEDBrightness(brightFrac, ledIndex):
	outText = ""
	
	rawBright = int(brightFrac*256)
	
	if rawBright >= 256:
		rawBright = 255 # cap the brightness
	
	outText = outText + "fill 1,%02x%02x%02x,%d,1;" % (
		rawBright,rawBright,rawBright,
		leds[ledIndex % len(leds)] )
	return outText
	


def setup():
	print("setup channel_1_count=150")
	print("brightness 1,255")
	print("fill 1")
	print("render")

def do():
	print("do")
	
def loop(count=0):
	if count == 0:
		print("loop")
	else:
		print("loop %d" % count)

if __name__ == "__main__":
	setup();
	do()
	spotlightMove(3.0, 4)

	fadeColor(0xff0000, 1.0, True)
	timeRainbow(5.0, 3)
	fadeColor(0xff0000, 1.0, False)

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
	loop()
