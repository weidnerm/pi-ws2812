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

    def create_file_with_header(self, filename, bright=128):
        self.fileHandle = open(filename, "w")

        self.fileHandle.write("setup channel_1_count=%d\n" % (self.numLeds) )
        self.fileHandle.write("brightness 1,%d\n" % (bright) )
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

    def generate_color_full_rainbow_2(self, which_seq):
        delayDuration = 25
        colorDegs = -1

        self.create_file_with_header(which_seq+".txt")
        self.fileHandle.write("do\n")

        for index in range(120):
            last_color_degs = colorDegs
            while last_color_degs == colorDegs: # make it random and different. seems like it stutters when same multiple times in a row.
                colorDegs = (random.randint(0,12)*255/12 ) %255

            self.fileHandle.write("do\n")

            self.fileHandle.write('    rotate 1,6,%d,0,LEN,%s\n' % ( index%2, self.deg2color(colorDegs) ) )
            self.fileHandle.write("render\n")
            self.fileHandle.write("delay %d\n" % delayDuration)
            self.fileHandle.write("loop 60\n")

        self.fileHandle.write("loop\n")
        self.close_sequence_file()

    def generate_3d_test(self, which_seq):
        delayDuration = 25

        self.create_file_with_header(which_seq+".txt")
        self.fileHandle.write("do\n")

        for pos in range(3):
            center = 80
            delayDuration = 250
            output = '    fill 1\n'
            self.fileHandle.write(output)
            if pos == 0:
                output = '    fill 1,%s,%d,1\n' % ( 'ff00ff', center-pos )
                self.fileHandle.write(output)
            else:
                output = '    fill 1,%s,%d,1\n' % ( '0000ff', center-pos )
                self.fileHandle.write(output)
                output = '    fill 1,%s,%d,1\n' % ( 'ff0000', center+pos )
                self.fileHandle.write(output)


            self.fileHandle.write("render\n")
            self.fileHandle.write("delay %d\n" % delayDuration)

        self.fileHandle.write("loop\n")
        self.close_sequence_file()

    def generate_police_mode(self, which_seq):
        on_duration = 50
        off_duration = 50
        interpattern_duration = 100
        overall_pause_duration = 100
        
        seg_start = [54, 68, 89, 103]
        patterns = [
            #~ ['RRRR','RRRR','RRRR','BBBB','RRRR','RRRR','RRRR','BBBB','BBBB','BBBB','BBBB','BBBB','BBBB','RRRR','RRRR','RRRR','BBBB','RRRR','RRRR','RRRR','BBBB','BBBB','BBBB','BBBB','BBBB','BBBB',],
            ['WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW','WWWW',],
            ['WW--','WW--','WW--','--WW','--WW','--WW','WW--','WW--','WW--','--WW','--WW','--WW',],
            ['W-W-','W-W-','W-W-','-W-W','-W-W','-W-W','W-W-','W-W-','W-W-','-W-W','-W-W','-W-W',],
            ['BR--','BR--','BR--','--RB','--RB','--RB','BR--','BR--','BR--','--RB','--RB','--RB',],
            ['R--B','R--B','R--B','-BR-','-BR-','-BR-','R--B','R--B','R--B','-BR-','-BR-','-BR-',],
            ['R--R','R--R','R--R','-RR-','-RR-','-RR-','R--R','R--R','R--R','-RR-','-RR-','-RR-',],
            ['B--B','B--B','B--B','-BB-','-BB-','-BB-','B--B','B--B','B--B','-BB-','-BB-','-BB-',],
            #~ ['RBBR','RBBR','RBBR','BRRB','BRRB','BRRB','RBBR','RBBR','RBBR','BRRB','BRRB','BRRB',],
            ['R-R-','R-R-','R-R-','-R-R','-R-R','-R-R','R-R-','R-R-','R-R-','-R-R','-R-R','-R-R',],
            ['B-B-','B-B-','B-B-','-B-B','-B-B','-B-B','B-B-','B-B-','B-B-','-B-B','-B-B','-B-B',],
            ['RR--','RR--','RR--','--BB','--BB','--BB','RR--','RR--','RR--','--BB','--BB','--BB'],
            ['BB--','BB--','BB--','--RR','--RR','--RR','BB--','BB--','BB--','--RR','--RR','--RR',],
            ['BB--','BB--','BB--','--RR','--RR','--RR','BB--','BB--','BB--','--RR','--RR','--RR',],
            ]
        seg_length = 13
        # 60-110 roughly.
        # fill 1;fill 1,0000ff,54,13;fill 1,0000ff,68,13; fill 1,0000ff,89,13;fill 1,0000ff,103,13; render

        self.create_file_with_header(which_seq+".txt", bright=255)
        self.fileHandle.write("do\n")

        


        for pattern in patterns:
            for block in pattern:
                output = 'fill 1;'  # turn everything off.
                for index in range(4):
                    color = self.get_police_color_from_digit( block[index:index+1] )
                    output = output + "; fill 1,%s,%d,%d" % (color, seg_start[index], seg_length)
                output = output + "; render; delay %d\n" % (on_duration )
                self.fileHandle.write(output)
                self.fileHandle.write('fill 1; render; delay %d\n' % ( off_duration) )
            self.fileHandle.write('fill 1; render; delay %d\n' % ( interpattern_duration) )
        self.fileHandle.write('fill 1; render; delay %d\n' % ( overall_pause_duration) )

        output = ''
        for index in range(4):
            color = self.get_police_color_from_digit( 'BBBB'[index:index+1] )
            output = output + "; fill 1,%s,%d,%d" % (color, seg_start[index], seg_length)
        output = output + "; render; delay %d\n" % (on_duration )
        self.fileHandle.write(output)
        self.fileHandle.write('do; rotate 1,2,1,0,LEN; render; loop 120\n')

        output = ''
        for index in range(4):
            color = self.get_police_color_from_digit( 'RRRR'[index:index+1] )
            output = output + "; fill 1,%s,%d,%d" % (color, seg_start[index], seg_length)
        output = output + "; render; delay %d\n" % (on_duration )
        self.fileHandle.write(output)
        self.fileHandle.write('do; rotate 1,2,0,0,LEN; render; loop 120\n')
        
        output = ''
        for index in range(4):
            color = self.get_police_color_from_digit( 'WWWW'[index:index+1] )
            output = output + "; fill 1,%s,%d,%d" % (color, seg_start[index], seg_length)
        output = output + "; render; delay %d\n" % (on_duration )
        self.fileHandle.write(output)
        #~ self.fileHandle.write('do; rotate 1,2,0,0,LEN; render; loop 120\n')
        self.fileHandle.write('do; rotate 1,2,1,0,LEN; render; loop 120\n')
        

        self.fileHandle.write("loop\n")
        self.close_sequence_file()
        
    def get_police_color_from_digit(self, digit):
        if digit == 'R':
            return_val = 'ff0000'
        elif digit == 'B':
            return_val = '0000ff'
        elif digit == 'W':
            return_val = 'ffffff'
        else:
            return_val = '000000'
        return return_val

    def handle_generate(self, which_seq):
        if which_seq == 'color_bonanza':
            self.generate_color_bonanza_1(which_seq)
        elif which_seq == 'color_bonanza_2':
            self.generate_color_bonanza_2(which_seq)
        elif which_seq == 'color_full_rainbow':
            self.generate_color_full_rainbow_1(which_seq)
        elif which_seq == 'color_full_rainbow_2':
            self.generate_color_full_rainbow_2(which_seq)
        elif which_seq == '3d_test':
            self.generate_3d_test(which_seq)
        elif which_seq == 'police_mode':
            self.generate_police_mode(which_seq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sequences.')
    parser.add_argument('-n', '--num_leds', default=240, help='number of leds in the list.')
    parser.add_argument('-w', '--which_seq', default='color_bonanza', choices=['color_bonanza',
        'color_full_rainbow','color_full_rainbow_2','color_bonanza_2','3d_test','police_mode'],
         help='which sequence to generate')

    args = parser.parse_args()
    myGenerate_Sequence = Generate_Sequence(args.num_leds)
    myGenerate_Sequence.handle_generate(args.which_seq)




