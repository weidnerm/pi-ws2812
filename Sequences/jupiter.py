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
			

if __name__ == '__main__':
	moonList = [];

	moonList.append( Moon( int("7f7f7f",16),       0, 1.0000, 2, "Jupiter")); # 
	moonList.append( Moon( int("ff0000",16),  421700, 1.7691, 1, "Io" )); # Io
	moonList.append( Moon( int("ffff00",16),  671034, 3.5512, 1, "Europa" )); # Europa
	moonList.append( Moon( int("00ff00",16), 1070412, 7.1546, 1, "Ganymede" )); # Ganymede
	moonList.append( Moon( int("0000ff",16), 1882709, 16.689, 1, "Callisto" )); # Callisto
	
	

	
	myTwinkler = Twinkler( moonList, 1.0/(48.0) );
	myTwinkler.main()

	
	
		
		
