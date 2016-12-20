import time;
import math;
import random;

class StarObject:
	def __init__(self, rampUpTicks, onTicks, rampDownTicks, offTicks, baseColor, initialDelay, position, relocate):
		self.position = position;
		self.offRemaining = initialDelay;
		self.brighteningRemaining = 0;
		self.dimmingRemaining = 0;
		self.onRemaining = 0;
		if baseColor == 0:
			self.baseColor = deg2color( random.randint(0,255))
		else:
			self.baseColor = baseColor;
		self.currentBrightness = 0;
		self.rampUpTicks = rampUpTicks;
		self.onTicks = onTicks;
		self.rampDownTicks = rampDownTicks;
		self.offTicks = offTicks;
		self.relocate = relocate;
		
	def handleTick(self):
		relocate = 0;
		
		if self.offRemaining > 0:
			self.offRemaining = self.offRemaining -1;
			self.currentBrightness = 0;
			if ( self.offRemaining == 0 ):
				self.brighteningRemaining = self.rampUpTicks;
				
		elif self.brighteningRemaining > 0:
			self.brighteningRemaining = self.brighteningRemaining -1;
			self.currentBrightness = (self.rampUpTicks - self.brighteningRemaining)*128/self.rampUpTicks;
			if ( self.brighteningRemaining == 0 ):
				self.onRemaining = self.onTicks;
				
		elif self.onRemaining > 0:
			self.onRemaining = self.onRemaining -1;
			self.currentBrightness = 128;
			if ( self.onRemaining == 0 ):
				self.dimmingRemaining = self.rampDownTicks;
				
		elif self.dimmingRemaining > 0:
			self.dimmingRemaining = self.dimmingRemaining -1;
			self.currentBrightness = (self.dimmingRemaining)*128/self.rampDownTicks;
#			print("currentBrightness=%d" %(self.currentBrightness));
			if ( self.dimmingRemaining == 0 ):
				self.offRemaining = self.offTicks;
				
				relocate =  self.relocate
				
#		print("offRemaining=%d" %(self.offRemaining));
		scaledColorR = (int(((self.baseColor >> 16)&0xff)*self.currentBrightness)/128) << 16
		scaledColorG = (int(((self.baseColor >> 8 )&0xff)*self.currentBrightness)/128) << 8 
		scaledColorB = (int(((self.baseColor >> 0 )&0xff)*self.currentBrightness)/128) << 0
		scaledColor = scaledColorR | scaledColorG | scaledColorB
#		print("baseColor=%06x, currentBrightness=%d, R=%02x G=%02x B=%02x  scaledColor=%06x" % (self.baseColor, self.currentBrightness, scaledColorR, scaledColorG, scaledColorB, scaledColor));
		retVal = "fill 1,%06x,%d,1" %(scaledColor, self.position)


		if ( relocate == 1) : 
			self.position = random.randint(0,149); # move to new random position.
			self.baseColor = deg2color( random.randint(0,255))

		return retVal;


		

class Twinkler:
		
	m_numStars = 0
		
	def __init__(self,colorList, countList):
		f = open("/dev/rgbled", "w")
		f.write("setup channel_1_count=150\n")
		f.write("brightness 1,255\n")
		f.close()
		
		self.m_stars = []
		self.m_numStars = 0
		
		
		for index in xrange(len(colorList)):
			self.m_numStars = self.m_numStars + countList[index]
			for starIndex in xrange(countList[index]):
				star = StarObject(random.randint(10,60),random.randint(20,60),20,random.randint(20,60),colorList[index], starIndex*10, random.randint(0,149) , 1)
				self.m_stars.append(star);

	def sendSequence(self,sequence):
		f = open("/dev/rgbled", "w")
		for index in xrange(len(sequence)):
			f.write(sequence[index] + "\n")
		f.write("render\n")
		f.close()
		
	def main(self):		
		while(True):
			sequence = []
			for star in xrange(self.m_numStars):
				sequence.append( self.m_stars[star].handleTick() );
			
			self.sendSequence(sequence);
			time.sleep(0.05);


def color (r, g, b):
	return (g << 16) + (r << 8) + b;

#returns a color from a 'color wheel' where wheelpos is the 'angle' 0-255
def deg2color(WheelPos):
	if(WheelPos < 85):
		return color(255 - WheelPos * 3,WheelPos * 3 , 0);
	elif(WheelPos < 170):
		WheelPos -= 85;
		return color(0, 255 - WheelPos * 3, WheelPos * 3);
	else:
		WheelPos -= 170;
		return color(WheelPos * 3, 0, 255 - WheelPos * 3);



if __name__ == '__main__':
	colorList = [];
	countList = [];
	
	# random rainbow
	colorList.append( 0 ); countList.append( 80 );

	
	# forth of july
	#colorList.append( int("00ff00",16) ); countList.append( 20 );colorList.append( int("ffffff",16) ); countList.append( 20 ); colorList.append( int("ff0000",16) ); countList.append( 20 ); colorList.append( int("0000ff",16) ); countList.append( 20 );
	
	# xmas
#	colorList.append( int("ff0000",16) ); countList.append( 20 ); colorList.append( int("00ff00",16) ); countList.append( 20 );
	
	# ligthtning bugs
	#colorList.append( int("a0ff00",16) ); countList.append( 30 );

	# stars
	#colorList.append( int("ffffff",16) ); countList.append( 40 );
	
	myTwinkler = Twinkler( colorList, countList );
	myTwinkler.main()

	
	
		
		
