#!/usr/bin/python
import datetime
import time
import ephem
import argparse
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 53     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 128      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def get_phase_on_day(year,month,day):
    """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
    #Ephem stores its date numbers as floating points, which the following uses
    #to conveniently extract the percent time between one new moon and the next
    #This corresponds (somewhat roughly) to the phase of the moon.

    #Use Year, Month, Day as arguments
    date=ephem.Date(datetime.date(year,month,day))

    nnm = ephem.next_new_moon        (date)
    pnm = ephem.previous_new_moon(date)

    lunation=(date-pnm)/(nnm-pnm)

    #Note that there is a ephem.Moon().phase() command, but this returns the
    #percentage of the moon which is illuminated. This is not really what we want.

    return lunation

def get_moons_in_year(year):
    """Returns a list of the full and new moons in a year. The list contains tuples
of either the form (DATE,'full') or the form (DATE,'new')"""
    moons=[]

    date=ephem.Date(datetime.date(year,1,1))
    while date.datetime().year==year:
        date=ephem.next_full_moon(date)
        moons.append( (date,'full') )

    date=ephem.Date(datetime.date(year,1,1))
    while date.datetime().year==year:
        date=ephem.next_new_moon(date)
        moons.append( (date,'new') )

    #Note that previous_first_quarter_moon() and previous_last_quarter_moon()
    #are also methods

    moons.sort(key=lambda x: x[0])

    return moons
    
def get_brightness(sub_fraction):
    if int(sub_fraction) == 0:
        brightness = 0x40
        
    elif int(sub_fraction) == 1:
        brightness = 0x80
        
    else:
        brightness = 0xff
        
    return brightness
    
def get_channel_brightness(channel, phase_24):
    # fraction has whole numbers of 1-8 that control which phase and fractional values that control brightness of sub-phase
    
    brightness = 0
    day = 3 # steps per day
    which_eighth = int(phase_24/day)
    phase_int = phase_24 - which_eighth*day
    
    if channel == 'right':
        starting = 0
    if channel == 'top':
        starting = 1
    if channel == 'bottom':
        starting = 2
    if channel == 'left':
        starting = 3
        

    if which_eighth < starting:
        brightness = 0
    elif which_eighth < starting+1:
        brightness = get_brightness(phase_int)
    elif which_eighth < starting+4:
        brightness = 255
    elif which_eighth < starting+1+4:
        brightness = get_brightness(2-phase_int)
    else:
        brightness = 0
    
    return brightness
            
    

    
def set_side_control_text(side, color):

    # ~ fill 1,404040,14,12 # top 
    # ~ fill 1,ffffff,26,15 # right
    # ~ fill 1,000000,0,14 # left
    # ~ fill 1,000000,41,12 # bottom

    if side=='left':
        start=0
        len=14
    elif side=='top':
        start=14
        len=12
    elif side=='right':
        start=26
        len=15
    else:
        start=41
        len=12

    text = 'fill 1,%s,%d,%d # %s' % (color, start, len, side)
    
    colorObj = Color(int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)) 
    for i in range(start,start+len):
        strip.setPixelColor(i, colorObj)
    strip.show()

# returns a color from a 'color wheel' where wheelpos is the 'angle' 0-255
def deg2color(wheelPos):
    if(wheelPos < 85):
        return Color(255 - wheelPos * 3,wheelPos * 3 , 0);
    elif(wheelPos < 170):
        wheelPos -= 85;
        return Color(0, 255 - wheelPos * 3, wheelPos * 3);
    else:
        wheelPos -= 170;
        return Color(wheelPos * 3, 0, 255 - wheelPos * 3);


def get_color_from_table(side, phase_24_int):
    table = [
    {'left' : '000000',  'bottom' : '000000', 'top' : '000000', 'right' : '3f3f3f' }, # 0
    {'left' : '000000',  'bottom' : '000000', 'top' : '3f3f3f', 'right' : '3f3f3f' }, # 1
    {'left' : '000000',  'bottom' : '000000', 'top' : '3f3f3f', 'right' : '7f7f7f' }, # 2
    {'left' : '000000',  'bottom' : '000000', 'top' : '7f7f7f', 'right' : '7f7f7f' }, # 3
    {'left' : '000000',  'bottom' : '000000', 'top' : '7f7f7f', 'right' : 'ffffff' }, # 4
    {'left' : '000000',  'bottom' : '000000', 'top' : 'ffffff', 'right' : 'ffffff' }, # 5

    {'left' : '000000',  'bottom' : '3f3f3f', 'top' : 'ffffff', 'right' : 'ffffff' }, # 6
    {'left' : '3f3f3f',  'bottom' : '3f3f3f', 'top' : 'ffffff', 'right' : 'ffffff' }, # 7
    {'left' : '3f3f3f',  'bottom' : '7f7f7f', 'top' : 'ffffff', 'right' : 'ffffff' }, # 8
    {'left' : '7f7f7f',  'bottom' : '7f7f7f', 'top' : 'ffffff', 'right' : 'ffffff' }, # 9
    {'left' : '7f7f7f',  'bottom' : 'ffffff', 'top' : 'ffffff', 'right' : 'ffffff' }, # 10
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : 'ffffff', 'right' : 'ffffff' }, # 11

    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : 'ffffff', 'right' : '7f7f7f' }, # 12
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : '7f7f7f', 'right' : '7f7f7f' }, # 13
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : '7f7f7f', 'right' : '3f3f3f' }, # 14
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : '3f3f3f', 'right' : '3f3f3f' }, # 15
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : '3f3f3f', 'right' : '000000' }, # 16
    {'left' : 'ffffff',  'bottom' : 'ffffff', 'top' : '000000', 'right' : '000000' }, # 17

    {'left' : 'ffffff',  'bottom' : '7f7f7f', 'top' : '000000', 'right' : '000000' }, # 18
    {'left' : '7f7f7f',  'bottom' : '7f7f7f', 'top' : '000000', 'right' : '000000' }, # 19
    {'left' : '7f7f7f',  'bottom' : '3f3f3f', 'top' : '000000', 'right' : '000000' }, # 20
    {'left' : '3f3f3f',  'bottom' : '3f3f3f', 'top' : '000000', 'right' : '000000' }, # 21
    {'left' : '3f3f3f',  'bottom' : '000000', 'top' : '000000', 'right' : '000000' }, # 22
    {'left' : '000000',  'bottom' : '000000', 'top' : '000000', 'right' : '000000' }, # 23
    ]
    color = table[phase_24_int][side]
    
    return color
    

def get_baseline_file():
    # ~ setup channel_1_count=53
    # ~ brightness 1,128
    base = []
    
    base.append('setup channel_1_count=53')
    base.append('brightness 1,128')
    base.append('')
    
    return base

def rotate_color_segments(colors, delay, num_points=8):

    # ~ text.append('fill 1,%s,0,8' %(color))  # a few red
    # ~ text.append('fill 1,%s,26,8' %(color))  # a few red
    
    # ~ text.append('do')
    # ~ text.append('    rotate 1,1,-1  ')
    # ~ text.append('    render')
    # ~ text.append('    delay %d' %(delay))
    # ~ text.append('loop') 
    
    offset = 0
    colorObjs = []
    for color in colors:
        colorObjs.append(Color(int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)) )
    if len(colors) == 1:  # single color.  propagate to two
        colorObjs.append(colorObjs[0])
        colorsplit = 26
    elif len(colors) >= 2:
        colorsplit = int(53/len(colors))
    colorOff = Color(0,0,0) 
    while True:
        for i in range(53):
            strip.setPixelColor(i, colorOff)
        for i in range(num_points):
            strip.setPixelColor((0+i+offset)%53, colorObjs[0])
        for i in range(num_points):
            strip.setPixelColor((colorsplit+i+offset)%53, colorObjs[1])
        if len(colorObjs) >= 3:
            for i in range(num_points):
                strip.setPixelColor((colorsplit*2+i+offset)%53, colorObjs[2])
        offset = offset + 1
        time.sleep(0.1)
        strip.show()

def rotating_rainbow(delay):
    offset = 0
    while True:
        for i in range(53):
            strip.setPixelColor((i+offset)%53, deg2color(int(i*256/53)))
        
        offset = offset + 1
        time.sleep(0.1)
        strip.show()

def turn_off():
    off = Color(0,0,0)
    for i in range(53):
        strip.setPixelColor(i, off)
    strip.show()


# ~ # Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    colorWipe(strip, Color(255,0,0), wait_ms=50)


    today = time.time()
    localtime = time.localtime(today)
    year = localtime.tm_year
    month = localtime.tm_mon
    day = localtime.tm_mday
    hour = localtime.tm_hour
    minute = localtime.tm_min
    second = localtime.tm_sec
    phase = get_phase_on_day(year, month, day)
    day_of_moon_phase = int(phase * 24)

    print(year, month, day, phase, day_of_moon_phase)


    moon = ephem.Moon()
    sun = ephem.Sun()
    observer = ephem.city("Miami")
    # ~ observer.elevation = -6371000  # place the observer at the center of the Earth
    observer.pressure = 0          # disable atmospheric refraction

    curtime = datetime.datetime(year, month, day, hour, minute, second)
    # ~ curtime = datetime.datetime(2020, 11, 29, 0, 0, 0)
    # ~ curtime = datetime.datetime(2020, 6, 5, 0, 0, 0)
    # ~ curtime = datetime.datetime(2020, 7, 20, 0, 0, 0)
    # ~ curtime = datetime.datetime(2020, 7, 5, 0, 0, 0)
    # ~ curtime = datetime.datetime(2020, 11, 29, 0, 0, 0)
    # ~ curtime = datetime.datetime(2020, 12, 14, 0, 0, 0)
    # ~ curtime = datetime.datetime(2021, 5, 26, 0, 0, 0)
    # ~ curtime = datetime.datetime(2021, 11, 19, 0, 0, 0)
    # ~ curtime = datetime.datetime(2023, 10, 14, 0, 0, 0)

    sep_min = 360
    sep_max = 0
    moon_alt_max = 0
    moon_alt_min = 0
    for index in range(25):
        observer.date = curtime

        # computer the position of the sun and the moon with respect to the observer
        moon.compute(observer)
        sun.compute(observer)

        # calculate the separation between the moon and the sun, convert
        # it from radians to degrees
        sep = abs((float(ephem.separation(moon, sun)) / 0.01745329252) )
        if sep>sep_max:
            sep_max = sep
            moon_alt_max = moon.alt/ 0.01745329252
        if sep<sep_min:
            sep_min = sep
            moon_alt_min = moon.alt/ 0.01745329252
        curtime += datetime.timedelta(hours = 1)
    print('sep_max=%s  sep_min=%s  moon_alt_max=%f  moon_alt_min=%f' % (sep_max,sep_min,moon_alt_max,moon_alt_min) )

    text = get_baseline_file()

    # ~ for day in range(24):
    if args.clear == True:
        turn_off()

    elif ((month==2) and (day==14)): # tammy
        rotate_color_segments(['ff00ff'],100) # purple
        
    elif ((month==9) and (day==19)): # courtney
        rotate_color_segments(['ffc000'],100) # yellow
        
    elif ((month==11) and (day==12)): # tiffany
        rotate_color_segments(['ff8080'],100) # pink
        
    elif ((month==9) and (day==12)): # mike
        rotate_color_segments(['00ffff'],100) # cyan
        
    elif ((month==4) and (day==13)): # andrew
        rotate_color_segments(['00ff00'],100) # green
        
    elif ((month==7) and (day==4)): # 4th of july
        rotate_color_segments(['ff0000','ffffff','0000ff'],100) # red white blue

    elif ((month==3) and (day==17)): # st pats
        rotate_color_segments(['00ff00'],100) # green

    elif ((month==12) and (day==25)): # xmas
        rotate_color_segments(['ff0000','00ff00'],100,num_points=20) # red green

    # ~ elif ((month==5) and (day==25)):
        # ~ rotate_color_segments('ffc000',100) # yellow
        
        
        
    elif (sep_max>177.5):  # eclipse where moon in earths shadow
        if moon_alt_max>0:  # its visible. spin fast
            rotate_color_segments(['ff0000'],25) # red
        else:
            rotate_color_segments(['ff0000'],100) # red

    elif (sep_min<0.9):  # eclipse where moon covers sun
        if moon_alt_min>0:  # its visible. spin fast
            rotate_color_segments(['ffffff'],25) # white
        else:
            rotate_color_segments(['ffffff'],100) # white
        
    elif day_of_moon_phase == 23: # special alien party
        rotating_rainbow(100)


    else:  # normal
        set_side_control_text('right', get_color_from_table('right', day_of_moon_phase))
        set_side_control_text('top', get_color_from_table('top', day_of_moon_phase))
        set_side_control_text('left', get_color_from_table('left', day_of_moon_phase))
        set_side_control_text('bottom', get_color_from_table('bottom', day_of_moon_phase))





