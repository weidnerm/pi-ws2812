
# red and green lines moving from ends to middle
for index in xrange(1,38):
	print("fill 1,ff0000,%d,%d" % ( (75+2*37-2*index),(2*index) ) );
	print("fill 1,00ff00,%d,%d" % ( (       1       ),(2*index) ) );
	print("render");
	print("delay %d" % (10+index*2));
	
	
