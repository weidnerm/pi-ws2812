import time;
import math;
import random;


class Moon:
	def __init__(self, baseColor, orbitRadius, orbitPeriod, pixels, name ):
		self.orbitRadius = orbitRadius;
		self.baseColor = baseColor;
		self.orbitPeriod = orbitPeriod;
		self.pixels = pixels;
		self.name = name;
		self.x = 0; # sideways distance sort of. 
		self.y = 0; # distance from earth sort of.
		
		self.pixelScaleFactor = 1882709/30;   # max orbit radius in km/ display radius in pixels

		
	def calculatePos(self, time):
		self.y = math.sin(time/self.orbitPeriod*2*math.pi)*self.orbitRadius/self.pixelScaleFactor;
		self.x = math.cos(time/self.orbitPeriod*2*math.pi)*self.orbitRadius/self.pixelScaleFactor;
#		print("%s %f %f" % (self.name, self.x, self.y));
		
	def drawObject(self, offset):
		retVal = "fill 1,%06x,%d,%d" %(self.baseColor, int(self.x)+offset, self.pixels )
		return retVal;




		

class Twinkler:
		
	def __init__(self,objectList, daysPerTick):
		f = open("/dev/rgbled", "w")
		f.write("setup channel_1_count=150\n")
		f.write("brightness 1,128\n")
		f.close()
		
		self.objectList = objectList;
		self.daysPerTick = daysPerTick;
		
		self.center = 48;
		
	def dumpSystem(self):
		output = [];
		output.append("fill");
		
		handled = []
		for index in xrange(len(self.objectList)):
			handled.append(0);
		
		for objectIndex in xrange(len(self.objectList)):
			tempMin = 1.0e+12;
			tempIndex = 0;
			
			for findMin in xrange(len(self.objectList)):
				if (self.objectList[findMin].y < tempMin) and (handled[findMin] == 0):
					tempMin = self.objectList[findMin].y
					tempIndex = findMin;
					
			handled[tempIndex] = 1;	
			output.append( self.objectList[tempIndex].drawObject(self.center) );
		
		self.sendSequence(output);
		

	def sendSequence(self,sequence):
		f = open("/dev/rgbled", "w")
		for index in xrange(len(sequence)):
			f.write(sequence[index] + "\n")
		f.write("render\n")
		f.close()
		
	def main(self):		
		for tick in xrange(20000):
			currentTime = self.daysPerTick * tick;
			
			for star in xrange(len(self.objectList)):
				self.objectList[star].calculatePos(currentTime);
			
#			self.sendSequence(sequence);
			self.dumpSystem();
			time.sleep(0.050);
			

class Fire:
	def __init__(self, numLeds):
		f = open("/dev/rgbled", "w")
		f.write("setup channel_1_count=150\n")
		f.write("brightness 1,128\n")
		f.close()
		
		self.NUM_LEDS = numLeds
		self.output = [];
		self.heat = []
		for index in xrange(self.NUM_LEDS):
			self.heat.append(0)
	
	def showStrip(self):
		self.sendSequence(self.output)
		self.output = []
		
	def setPixel(self,pixelNum, red, green, blue):
		self.output.append("fill 1,%02x%02x%02x,%d,1" % (red,green,blue,pixelNum) )
	
	def setAll(self,red,green,blue):
		for index in xrange(self.NUM_LEDS):
			self.setPixel(index,red,green,blue)
			
	def sendSequence(self,sequence):
		f = open("/dev/rgbled", "w")
		for index in xrange(len(sequence)):
			f.write(sequence[index] + "\n")
		f.write("render\n")
		f.close()
		
	def fire(self, Cooling, Sparkling, SpeedDelay):
		cooldown = 0
		

		# Step 1.  Cool down every cell a little
		for i in xrange(self.NUM_LEDS):
			cooldown = random.randint(0, ((Cooling * 10) / self.NUM_LEDS) + 2);

			if(cooldown>self.heat[i]):
				self.heat[i]=0;
			else:
				self.heat[i] = self.heat[i]-cooldown;

		# Step 2.  Heat from each cell drifts 'up' and diffuses a little
		for k_raw in xrange(self.NUM_LEDS - 1 -2):
			#for( int k= NUM_LEDS - 1; k >= 2; k--) {
			k = self.NUM_LEDS - k_raw -1
			self.heat[k] = (self.heat[k - 1] + self.heat[k - 2] + self.heat[k - 2]) / 3;


		# Step 3.  Randomly ignite new 'sparks' near the bottom
		if( random.randint(0,255) < Sparkling ):
			y = random.randint(0,7);
			self.heat[y] = self.heat[y] + random.randint(160,255);

		# Step 4.  Convert heat to LED colors
		for j in xrange(self.NUM_LEDS):
			self.setPixelHeatColor(j, self.heat[j] );

		self.showStrip();
		time.sleep(SpeedDelay/1000.0);
			
	def setPixelHeatColor(self, Pixel, temperature):
		# Scale 'heat' down from 0-255 to 0-191
		t192 = int((temperature/255.0)*191);
	 
		# calculate ramp up from
		heatramp = t192 & 0x3F; # 0..63
		heatramp = heatramp << 2; # scale up to 0..252
	 
		# figure out which third of the spectrum we're in:
		if( t192 > 0x80):                   # hottest
			self.setPixel(Pixel, 255, 255, heatramp);
		elif( t192 > 0x40 ):          # middle
			self.setPixel(Pixel, 255, heatramp, 0);
		else :                              # coolest
			self.setPixel(Pixel, heatramp, 0, 0);



if __name__ == '__main__':
	fire = Fire(75)
	while(True):
		# cooling, sparkling, speed
		fire.fire(150,75,15)
	


	
	
		
		
