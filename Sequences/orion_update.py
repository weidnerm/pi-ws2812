#!/usr/bin/python
import datetime
import time
import ephem
import sys

class Orion():
    def __init__(self):
        self.brightness_indexes = {1:0x10,  'A':0x10, 'B':0x20, 'C':0x40, 'D':0x80, 'E':0xff, 'F':-255}
        self.backligtht_rgb_settings = {
            'W': [0xff, 0, 0],
            'X': [0, 0x7f, 0],
            'Y': [0, 0, 0xff],
            'Z': [0, 0, 0],
            }
        self.morse = {
            'a' : '.-',
            'b' : '-...',
            'c' : '-.-.',
            'd' : '-..',
            'e' : '.',
            'f' : '..-.',
            'g' : '--.',
            'h' : '....',
            'i' : '..',
            'j' : '.---',
            'k' : '-.-',
            'l' : '.-..',
            'm' : '--',
            'n' : '-.',
            'o' : '---',
            'p' : '.--.',
            'q' : '--.-',
            'r' : '.-.',
            's' : '...',
            't' : '-',
            'u' : '..-',
            'v' : '...-',
            'w' : '.--',
            'x' : '-..-',
            'y' : '-.--',
            'z' : '--..',
            ' ' : ' '
                }
            
        self.messages_morse = {}
        self.messages = [
            { 'month' : [], 'day': [], 'hour': [], 'minute': [0,10,20], 'wday': [], 'messages' : {
                 2: {'text':'hi        hi'},
                 1: {'text':'     hi        hi'} } },
            { 'month' : [], 'day': [], 'hour': [], 'minute': [30,40,50], 'wday': [], 'messages' : {
                 3: {'text':'hi        hi'},
                 5: {'text':'     hi        hi'} } },
            { 'month' : [], 'day': [], 'hour': [22], 'minute': [0], 'wday': [], 'messages' : {
                 6: {'text': 'Wsos ABCDEEEEEEEEEEEEEEEEEEFZFFFFFFFFFFFFFFFFFFFF'} } },
            { 'month' : [9], 'day': [12], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday mike'} } },
            { 'month' : [9], 'day': [19], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday courtney'} } },
            { 'month' : [11], 'day': [12], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday tiffany'} } },
            { 'month' : [2], 'day': [14], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday tammy'} } },
            { 'month' : [4], 'day': [13], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday andrew'} } },
            { 'month' : [6], 'day': [14], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday paige'} } },
            { 'month' : [12], 'day': [28], 'hour': [], 'minute': [], 'wday': [], 'bday':1, 'messages' : {
                 0: {'text': 'happy birthday jennifer'} } },
                        ]
    
        
        slowness_factor=2  # how many 100ms intervals per morse time tick
        for batch_index in range(len(self.messages)):
            for star_num in self.messages[batch_index]['messages']:
                message = self.messages[batch_index]['messages'][star_num]['text']
                
                temp_morse = []
                
                for letter_index in range(len(message)):
                    letter = message[letter_index]
                    
                    if letter == ' ':
                        temp_morse += [0]*4*slowness_factor  # inter word gap

                    elif (letter in ['A', 'B', 'C', 'D', 'E', 'F']):
                        temp_morse += [letter]*2

                    elif (letter in ['W', 'X', 'Y', 'Z']):
                        temp_morse += [letter]

                    else:
                        for digit_index in range(len(self.morse[letter])):
                            digit = self.morse[letter][digit_index]
                            
                            if digit == '.':
                                temp_morse += [1]*slowness_factor
                            elif digit == '-':
                                temp_morse += [1]*3*slowness_factor
                                
                            temp_morse += [0]*slowness_factor  # inter digit gap
                           
                        temp_morse += [0]*2*slowness_factor  # inter letter gap 2+1 = 3
                    
                self.messages[batch_index]['messages'][star_num]['morse'] = temp_morse

        # ~ print(self.messages)

        self.allowed_range = [
                [0,  8.5, 22.5], # monday
                [1,  8.5, 22.5], # tuesday
                [2,  8.5, 22.5], # wednesday
                [3,  8.5, 22.5], # thursday
                [4,  8.5, 23.5], # friday
                [5,  9.0, 23.5], # saturday
                [6,  9.0, 23.5], # sunday
            ]


    def get_active_messages(self):
        
        tm_mon = self.localtime.tm_mon
        tm_mday = self.localtime.tm_mday
        tm_hour = self.localtime.tm_hour
        tm_min = self.localtime.tm_min
        tm_wday = self.localtime.tm_wday
        self.active_messages = {}
        bday = 0
        
        for entry_index in range(len(self.messages)):
            entry = self.messages[entry_index]
            
            # ~ { 'month' : [], 'day': [], 'hour': [], 'minute': [], 'wday': [], 'messages' : {
            if (entry['month'] == []) or (tm_mon in entry['month'] ):
                if (entry['day'] == []) or (tm_mday in entry['day'] ):
                    if (entry['hour'] == []) or (tm_hour in entry['hour'] ):
                        if (entry['minute'] == []) or (tm_min in entry['minute'] ):
                            if (entry['wday'] == []) or (tm_wday in entry['wday'] ):
                                for key in entry['messages']:
                                    self.active_messages[key] = entry['messages'][key]
                                if 'bday' in entry:
                                    bday = 1
        if len(sys.argv) >= 2:
            index = int(sys.argv[1])
            entry = self.messages[index]
            for key in entry['messages']:
                self.active_messages[key] = entry['messages'][key]
            if 'bday' in entry:
                bday = 1
             
                        
        return bday
        
             # ~ hour = self.localtime.tm_hour
        # ~ minute = self.localtime.tm_min
        # ~ wday = self.localtime.tm_wday # 0=monday
        # ~ month = self.localtime.tm_mon
        # ~ day = self.localtime.tm_mday
        
        # ~ self.messages = [
                            # ~ { #'date' : '', 'time': '', 
                             # ~ 'messages' :
                                # ~ {
                                 # ~ 6: {'text': 'sos ABCDEEEEEEEEEEEEEEEEEEFFFFFFFFFFFFFFFFFFFFF'},
                                 # ~ 2: {'text':'hi     hi'},
                                 # ~ 1: {'text':'    hi'} } },
        
                        
    def init_base_brightness(self):
        self.star_rgbs = [
            [16,16,48], # rigel_0_rgb     
            [16,16,16], # saiph_1_rgb     
            [16,16,16], # alnitak_2_rgb   
            [16,16,16], # alnilam_3_rgb   
            [16,16,16], # mintaka_4_rgb   
            [16,16,16], # bellatrix_5_rgb 
            [32,16,16]  # betelgeuse_6_rgb
            ] #
        self.backligtht_rgb = [0, 0,0]
       
    def get_baseline_file(self):
        base = []
        
        base.append('setup channel_1_count=57')
        base.append(self.get_default_brightness())
        base.append('')
        
        self.text = base
        
    def get_default_brightness(self):
        return 'brightness 1,128'
    
    def birthday_swirl(self):
  
        self.text.append('fill 1')
        self.text.append('brightness 1,32')
        self.text.append('rainbow 1,7,0,LEN')
        self.text.append('do')
        self.text.append('    rotate 1,1,1,0,LEN')
        self.text.append('    render')
        self.text.append('    delay 100')
        self.text.append('loop 600')
        self.text.append(self.get_default_brightness())
        self.text.append('fill 1')
        self.text.append('')
    
    def write_orion_stars(self):
        self.text.append('')
        
        for index in range(7):
            text = 'fill 1,%02x%02x%02x,%d,1' % (self.star_rgbs[index][0], self.star_rgbs[index][1], self.star_rgbs[index][2], index)
            self.text.append(text)
            
    def turn_all_off(self):
        text = 'fill 1,000000,0,LEN'
        self.text.append(text)

    def write_backlight(self):
        text = 'fill 1,%02x%02x%02x,7,50' % (self.backligtht_rgb[0], self.backligtht_rgb[1], self.backligtht_rgb[2])
        self.text.append(text)
        
    def render_and_wait(self, delay):
        self.text.append('render')
        if delay != 0:
            self.text.append('delay %d' % (delay))
        
        
    def write_and_close_file(self):
        fh = open('orion_temp.sh', 'w')
        fh.write('\n'.join(self.text)+'\n')
        fh.close()    
        
    def get_twinkle_offset(self, phase):
        return_value = 0
        
        phase_len=4
        phase_period = 4*phase_len
        multiples = int( self.animation_time*1000/ (phase_period*200)) - 1
        slope=2
        
        if (phase > 0) and (phase < multiples*phase_period):
            phase = phase % phase_period
        
        
        if (phase >= 0) and (phase < phase_len):
            return_value = slope*phase
            
        elif (phase >= phase_len) and (phase < phase_len*3):
            return_value = 2*slope*phase_len - slope*phase
            
        elif (phase >= phase_len*3) and (phase < phase_len*4):
            return_value = -4*slope*phase_len + slope*phase
            
        return return_value
            
    def twinkle_stars_for_a_while(self, secs):
        self.animation_time = secs
        elapsed = 0
        phase=0

        bday = self.get_active_messages()
        if bday == 1:
            self.birthday_swirl()
                    
        while(elapsed < secs*1000):
            self.init_base_brightness()
            
            for star_index in range(7):
                star = self.star_rgbs[star_index]
                
                if star_index in self.active_messages:
                    message = self.active_messages[star_index]['morse']
                
                    if phase < len(message):
                        digit = message[phase]
                        if digit in self.brightness_indexes:
                            offset = self.brightness_indexes[digit]
                            star[0] += offset
                            star[1] += offset
                            star[2] += offset
                        elif digit in self.backligtht_rgb_settings:
                            self.backligtht_rgb = self.backligtht_rgb_settings[digit]
                            self.write_backlight()
                
                for colorindex in range(3):
                    star[colorindex] += self.get_twinkle_offset( -13+phase+colorindex*4 + star_index )
                
                self.format_star(star, star_index)
                # ~ self.text.append('fill 1,%02x%02x%02x,%d,1' % (star[0], star[1], star[2], star_index))
            delay=200
            self.render_and_wait(delay)
            elapsed += delay
                
            phase += 1
            
    def format_star(self, star, star_index):
        red   = star[0]
        green = star[1]
        blue  = star[2]
        
        if red > 0xff:
            red = 0xff
        elif red < 0:
            red = 0
        if green > 0xff:
            green = 0xff
        elif green < 0:
            green = 0
        if blue > 0xff:
            blue = 0xff
        elif blue < 0:
            blue = 0
            
        self.text.append('fill 1,%02x%02x%02x,%d,1' % (red, green, blue, star_index))


    #returns a color from a 'color wheel' where wheelpos is the 'angle' 0-255
    def deg2color(self, WheelPos):
        if(WheelPos < 85):
            return_val = [255 - WheelPos * 3,WheelPos * 3 , 0];
        elif(WheelPos < 170):
            WheelPos -= 85;
            return_val = [0, 255 - WheelPos * 3, WheelPos * 3];
        else:
            WheelPos -= 170;
            return_val = [WheelPos * 3, 0, 255 - WheelPos * 3];

        max_brightness = 0x40
        return_val = [ int(return_val[0]*max_brightness/256),  int(return_val[1]*max_brightness/256),  int(return_val[2]*max_brightness/256)]
        
        return return_val

        
    # ~ def get_globe_color(self, moon_alt_degs, sun_alt_degs, hour, minute, wday):
        # ~ colorcmd = 'candycane 1,000000,1,000000,1,0,19'
        
        # ~ print('get_globe_color(moon_alt_degs=%f, sun_alt_degs=%f, hour=%d, minute=%d, wday=%d)' % (moon_alt_degs, sun_alt_degs, hour, minute, wday) )

        # ~ allowed_range = [
            # ~ [0,  8.5, 22.5], # monday
            # ~ [1,  8.5, 22.5], # tuesday
            # ~ [2,  8.5, 22.5], # wednesday
            # ~ [3,  8.5, 22.5], # thursday
            # ~ [4,  8.5, 23.5], # friday
            # ~ [5,  9.0, 23.5], # saturday
            # ~ [6,  9.0, 22.5], # sunday
        # ~ ]
        
        # ~ time_now_float = hour+minute/60.0-1.0/60.0  # (subtract a minute to avoid race conditions where triggers match thresholds
        
        # ~ is_on = False
        # ~ for entry in allowed_range:
            # ~ if ((wday == entry[0]) and (time_now_float >= entry[1]) and (time_now_float <= entry[2])):
                # ~ is_on = True
        
        # ~ if is_on == False:
            # ~ print('Off hours. no entries for wday=%d %02d:%02d = %f' % (wday, hour, minute, time_now_float))
            # ~ colorcmd = 'candycane 1,000000,1,000000,1,0,19' # off
        # ~ else:
            # ~ if (moon_alt_degs < 0):
                # ~ print('off since moon is below horizon moon_alt_degs=%f' % (moon_alt_degs) )
                # ~ colorcmd = 'candycane 1,000000,1,000000,1,0,19' # off
            # ~ else:
                # ~ if (sun_alt_degs > 0):
                    # ~ print('Day moon colors since sun_alt_degs=%f' % (sun_alt_degs) )
                    # ~ colorcmd = 'candycane 1,7f7f7f,1,00007f,1,0,19'  # day moon
                # ~ else:
                    # ~ if moon_alt_degs < 15:
                        # ~ print('moonrise colors since moon_alt_degs=%f' % (moon_alt_degs) )
                        # ~ colorcmd = 'candycane 1,000000,1,ff4000,1,0,19'  # moonrise
                    # ~ elif moon_alt_degs < 30:
                        # ~ print('high moonrise colors since moon_alt_degs=%f' % (moon_alt_degs) )
                        # ~ colorcmd = 'candycane 1,7f7f7f,1,ff4000,1,0,19'  # high moonrise
                    # ~ else:
                        # ~ print('high night moon since moon_alt_degs=%f' % (moon_alt_degs) )
                        # ~ colorcmd = 'candycane 1,7f7f7f,1,000000,1,0,19'  # high night moon

        # ~ return colorcmd
    # ~ http://www.sherrytowers.com/stars.py
    # ~ has starname stuffsource
    # ~ sirius  = ephem.star('Sirius')
    # ~ canopus = ephem.star('Canopus')
    # ~ arcturus = ephem.star('Arcturus')
    # ~ vega = ephem.star('Vega')
    # ~ rigel = ephem.star('Rigel')
    # ~ procyon = ephem.star('Procyon')
    # ~ betelgeuse = ephem.star('Betelgeuse')
    # ~ capella = ephem.star('Capella')
    # ~ altair = ephem.star('Altair')
    # ~ aldebaran = ephem.star('Aldebaran')
    # ~ spica = ephem.star('Spica')
    # ~ antares = ephem.star('Antares')
    # ~ pollux = ephem.star('Pollux')
        

# ~ today = time.time()
# ~ gmtime = time.gmtime(today)
# ~ year = gmtime.tm_year
# ~ month = gmtime.tm_mon
# ~ day = gmtime.tm_mday
# ~ hour = gmtime.tm_hour
# ~ minute = gmtime.tm_min
# ~ second = gmtime.tm_sec



# ~ moon = ephem.Moon()
# ~ sun = ephem.Sun()
# ~ observer = ephem.city("Miami")
# ~ observer.pressure = 0          # disable atmospheric refraction

# ~ curtime = datetime.datetime(year, month, day, hour, minute, second)

# ~ sep_min = 360
# ~ sep_max = 0
# ~ moon_alt_max = 0
# ~ moon_alt_min = 0
# ~ for index in range(1):
    # ~ observer.date = curtime

    # ~ # computer the position of the sun and the moon with respect to the observer
    # ~ moon.compute(observer)
    # ~ sun.compute(observer)

    # ~ moon_alt_degs = moon.alt/ 0.01745329252
    # ~ sun_alt_degs = sun.alt/ 0.01745329252
    # ~ #~ print('moon_alt_degs=%f  sun_alt_degs=%f' %(moon_alt_degs, sun_alt_degs) )
    # ~ curtime += datetime.timedelta(hours = 1)

# ~ localtime = time.localtime(today)
# ~ hour = localtime.tm_hour
# ~ minute = localtime.tm_min
# ~ wday = localtime.tm_wday # 0=monday


# ~ #~ get_globe_color(52, -9, 20, 0, 0)


# ~ text = get_baseline_file()

# ~ text.append( get_globe_color(moon_alt_degs, sun_alt_degs, hour, minute, wday))

# ~ text.append('render')  # draw it
# ~ text.append('delay 200')  # wait a bit



    def setup_star_patterns(self):

        today = time.time()
        self.localtime = time.localtime(today)
        hour = self.localtime.tm_hour
        minute = self.localtime.tm_min
        wday = self.localtime.tm_wday # 0=monday
        month = self.localtime.tm_mon
        day = self.localtime.tm_mday
        time_now_float = hour+minute/60.0-1.0/60.0  # (subtract a minute to avoid race conditions where triggers match thresholds
        print('%d/%2d %d:%02d' % (month,day,hour,minute))
    
        is_on = False
        for entry in self.allowed_range:
            if ((wday == entry[0]) and (time_now_float >= entry[1]) and (time_now_float <= entry[2])):
                is_on = True
        
        if is_on == False:
            self.turn_all_off()
            self.render_and_wait(0)

        else:
            self.write_orion_stars()
            self.write_backlight()
            self.render_and_wait(0)
            
            self.twinkle_stars_for_a_while(240)


def main():
    myOrion = Orion()
    
    myOrion.init_base_brightness()
    myOrion.get_baseline_file()
    
    myOrion.setup_star_patterns()
    
    myOrion.write_and_close_file()


if __name__ == "__main__":
    main()
