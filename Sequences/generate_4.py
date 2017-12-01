import random
import argparse

#~ numLeds = 240

class Generate_Sequence:
    
    def __init__(self, num_leds):
        self.numLeds = num_leds
        
    def deg2color(self, WheelPos):
        if WheelPos < 85:
            color = "%02X%02X%02X" % (255 - WheelPos * 3,WheelPos * 3 , 0)
        elif WheelPos < 170:
            WheelPos = WheelPos -85
            color = "%02X%02X%02X" % (0, 255 - WheelPos * 3, WheelPos * 3)
        else:
            WheelPos = WheelPos -170
            color = "%02X%02X%02X" % (WheelPos * 3, 0, 255 - WheelPos * 3)
        
        return color

    def create_file_with_header(self, filename):
        self.fileHandle = open(filename, "w")

        self.fileHandle.write("setup channel_1_count=%d\n" % (self.numLeds) )
        self.fileHandle.write("brightness 1,128\n")
        self.fileHandle.write("fill 1;render\n")

    def close_sequence_file(self):
        self.fileHandle.close();

    def generate_color_bonanza_1(self, which_seq):
        maxEachTime = 2
        maxSizeEach = 10
        delayDuration = 100

        self.create_file_with_header(which_seq+".txt")
        self.fileHandle.write("do\n")
        
        for index in range(120):
            numPatches = random.randint(1,maxEachTime)
            
            output = ""
            for patchNum in range(numPatches):
                startpos = random.randint(0,self.numLeds-maxSizeEach-1)
                length = random.randint(1,maxSizeEach)
                colorDegs = (random.randint(0,12)*255/12 ) %255
                
                output = output + '    fill 1,%s,%d,%d\n' % ( self.deg2color(colorDegs), startpos, length )
                
            self.fileHandle.write(output)
            self.fileHandle.write("render\n")
            self.fileHandle.write("delay %d\n" % delayDuration)

        # rotate it around once
        self.fileHandle.write("do\n")
        self.fileHandle.write('    rotate 1,1,0\n')
        self.fileHandle.write("    render\n")
        self.fileHandle.write("    delay 25\n")
        self.fileHandle.write("loop 60\n")

        self.fileHandle.write("loop\n")
        self.close_sequence_file()
    
    def generate_color_bonanza_2(self, which_seq):
        delayDuration = 1000
        colorDegs = -1

        self.create_file_with_header(which_seq+".txt")
        self.fileHandle.write("do\n")
        
        for index in range(120):
            output = ""
            last_color_degs = colorDegs
            
            while last_color_degs == colorDegs: # make it random and different. seems like it stutters when same multiple times in a row.
                colorDegs = (random.randint(0,12)*255/12 ) %255
            
            output = output + '    fill 1,%s,0,LEN\n' % ( self.deg2color(colorDegs) )
                
            self.fileHandle.write(output)
            self.fileHandle.write("render\n")
            self.fileHandle.write("delay %d\n" % delayDuration)

        self.fileHandle.write("loop\n")
        self.close_sequence_file()
    
    def generate_color_full_rainbow_1(self, which_seq):
        delayDuration = 25

        self.create_file_with_header(which_seq+".txt")
        self.fileHandle.write("do\n")
        
        for colorDegs in range(255):
            output = ""
            output = output + '    fill 1,%s,0,LEN\n' % ( self.deg2color(colorDegs) )
                
            self.fileHandle.write(output)
            self.fileHandle.write("render\n")
            self.fileHandle.write("delay %d\n" % delayDuration)

        self.fileHandle.write("loop\n")
        self.close_sequence_file()
    
    def handle_generate(self, which_seq):
        if which_seq == 'color_bonanza':
            self.generate_color_bonanza_1(which_seq)
        elif which_seq == 'color_bonanza_2':
            self.generate_color_bonanza_2(which_seq)
        elif which_seq == 'color_full_rainbow':
            self.generate_color_full_rainbow_1(which_seq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sequences.')
    parser.add_argument('-n', '--num_leds', default=240, help='number of leds in the list.')
    parser.add_argument('-w', '--which_seq', default='color_bonanza', choices=['color_bonanza','color_full_rainbow','color_bonanza_2'], help='which sequence to generate')

    args = parser.parse_args()
    myGenerate_Sequence = Generate_Sequence(args.num_leds)
    myGenerate_Sequence.handle_generate(args.which_seq)


    
    
