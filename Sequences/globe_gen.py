
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


def main2():
	
	print("do")
	for reps in xrange(10):
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
				ledBrightnesses[0] = (index-0)*4
			if index >= 64 and index < 128:
				ledBrightnesses[0] = (128-index)*4
				ledBrightnesses[1] = (index-64)*4
			if index >= 128 and index < 192:
				ledBrightnesses[1] = (192-index)*4
				ledBrightnesses[2] = (index-128)*4
			if index >= 192 and index < 256:
				ledBrightnesses[2] = (256-index)*4
			
			for ledindex in xrange(len(leds)):
				if ledBrightnesses[ledindex] >= 256:
					ledBrightnesses[ledindex] = 255 # cap the brightness
						
			for ledindex in xrange(len(leds)):
				print("    fill 1,%02x%02x%02x,%d,1" % ( 
					ledBrightnesses[ledindex],
					ledBrightnesses[ledindex],
					ledBrightnesses[ledindex],
					leds[ledindex]
					))

			print("    render")
			print("    delay 25")


		for index in xrange(255,0,-1):
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
				ledBrightnesses[0] = (index-0)*4
			if index >= 64 and index < 128:
				ledBrightnesses[0] = (128-index)*4
				ledBrightnesses[1] = (index-64)*4
			if index >= 128 and index < 192:
				ledBrightnesses[1] = (192-index)*4
				ledBrightnesses[2] = (index-128)*4
			if index >= 192 and index < 256:
				ledBrightnesses[2] = (256-index)*4
			
			for ledindex in xrange(len(leds)):
				if ledBrightnesses[ledindex] >= 256:
					ledBrightnesses[ledindex] = 255 # cap the brightness
						
			for ledindex in xrange(len(leds)):
				print("    fill 1,%02x%02x%02x,%d,1" % ( 
					ledBrightnesses[ledindex],
					ledBrightnesses[ledindex],
					ledBrightnesses[ledindex],
					leds[ledindex]
					))

			print("    render")
			print("    delay 25")


	print("loop")

def setup():
	print("setup channel_1_count=150")
	print("brightness 1,255")
	print("fill 1")
	print("render")


if __name__ == "__main__":
    setup();
    main2();
