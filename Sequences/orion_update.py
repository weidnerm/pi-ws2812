#!/usr/bin/python
import datetime
import time
import ephem


class Orion():
    def __init__(self):
        self.text = []
        
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
        self.backligtht_rgb = [0,0,0]
       
    def get_baseline_file(self):
        base = []
        
        base.append('setup channel_1_count=51')
        base.append('brightness 1,128')
        base.append('')
        
        self.text = base
        
    def write_orion_stars(self):
        # ~ self.text.append('')
        
        for index in range(7):
            text = 'fill 1,%02x%02x%02x,%d,1' % (self.star_rgbs[index][0], self.star_rgbs[index][1], self.star_rgbs[index][2], index)
            self.text.append(text)
            
    def write_backlight(self):
        text = 'fill 1,%02x%02x%02x,7,44' % (self.backligtht_rgb[0], self.backligtht_rgb[1], self.backligtht_rgb[2])
        self.text.append(text)
        
    def render_and_wait(self, delay):
        self.text.append('render')
        if delay != 0:
            self.text.append('delay %d' % (delay))
        
        
    def write_and_close_file(self):
        fh = open('orion_temp.sh', 'w')
        fh.write('\n'.join(self.text)+'\n')
        fh.close()    
        
    def twinkle_stars_for_a_while(self, secs):
        elapsed = 0
        phase=0
        while(elapsed < secs*1000):
            self.init_base_brightness()
            for index in range(7):
                colorIndex = (index+phase)%3
                self.star_rgbs[index][colorIndex] += 8
                self.text.append('fill 1,%02x%02x%02x,%d,1' % (self.star_rgbs[index][0], self.star_rgbs[index][1], self.star_rgbs[index][2], index))
            delay=500
            self.render_and_wait(delay)
            elapsed += delay
                
            phase += 1
                
        
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






def main():
    myOrion = Orion()
    myOrion.init_base_brightness()
    myOrion.get_baseline_file()
    myOrion.write_orion_stars()
    myOrion.write_backlight()
    myOrion.render_and_wait(0)
    myOrion.twinkle_stars_for_a_while(20)
    myOrion.write_and_close_file()


if __name__ == "__main__":
    main()
