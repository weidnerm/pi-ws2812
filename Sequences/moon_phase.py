#!/usr/bin/python
import datetime
import time
import ephem

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

    date=ephem.Date(datetime.date(year,01,01))
    while date.datetime().year==year:
        date=ephem.next_full_moon(date)
        moons.append( (date,'full') )

    date=ephem.Date(datetime.date(year,01,01))
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
            
    
        
def get_color_text(red, green, blue, brightness):
    color = '%02x%02x%02x' % (int(red*brightness/256),int(green*brightness/256),int(blue*brightness/256))
    
    return color
   
    
def get_side_control_text(side, color):

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
    
    return text
    
    
def get_baseline_file():
    # ~ setup channel_1_count=53
    # ~ brightness 1,128
    base = []
    
    base.append('setup channel_1_count=53')
    base.append('brightness 1,128')
    base.append('')
    
    return base
    

today = time.time()
localtime = time.localtime(today)
year = localtime.tm_year
month = localtime.tm_mon
day = localtime.tm_mday+7
phase = get_phase_on_day(year, month, day)

print(year, month, day, phase)


text = get_baseline_file()

# ~ for day in range(24):
day = int(phase * 24)
    
fraction = day/24.0
text.append('fill 1')  # all off
text.append( get_side_control_text('right', get_color_text(255,255,255, get_channel_brightness('right', day))) )
text.append( get_side_control_text('top', get_color_text(255,255,255, get_channel_brightness('top', day))) )
text.append( get_side_control_text('left', get_color_text(255,255,255, get_channel_brightness('left', day))) )
text.append( get_side_control_text('bottom', get_color_text(255,255,255, get_channel_brightness('bottom', day))) )

text.append('render')  # draw it
text.append('delay 100')  # wait a bit



fh = open('moon_temp.sh', 'w')
fh.write('\n'.join(text)+'\n')
fh.close()

# ~ for day in range(31):
    # ~ print("%d %f" % (day+1, get_phase_on_day(2019,8,day+1)))

# ~ print get_phase_on_day(2019,7,28)

# ~ print get_moons_in_year(2019)
