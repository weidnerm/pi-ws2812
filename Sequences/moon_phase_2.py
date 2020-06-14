#!/usr/bin/python
import datetime
import time
import ephem


LEN = 53
leds = []
for index in range(LEN):
    leds.append(0)
CENTER = 26+7


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
 

def get_baseline_file():
    # ~ setup channel_1_count=53
    # ~ brightness 1,128
    base = []
    
    base.append('setup channel_1_count=53')
    base.append('brightness 1,128')
    base.append('')
    
    return base
    
def dump_leds():
    temp = []
    temp.append('')
    temp.append('fill 1')
    start = 0
    last_state = leds[0]
    for index in range(1,LEN):
        # ~ fill 1,404040,14,12 # top 
        state = leds[index]
        if (state != last_state) or (index == LEN-1):  # print previous line if necessary
            temp.append( 'fill 1,%02x%02x%02x,%d,%d' % (last_state,last_state,last_state, start, index-start) )
            last_state = state
            start = index
    return temp

today = time.time()
localtime = time.localtime(today)
year = localtime.tm_year
month = localtime.tm_mon
day = localtime.tm_mday
phase = get_phase_on_day(year, month, day)
day = int(phase * 24)

print(year, month, day, phase, day)


text = get_baseline_file()

# ~ for day in range(24):

if day == 23: # special alien party
    
    text.append('rainbow 1,1,0,53')

    text.append('do')
    text.append('    rotate 1,1,-1  ')
    text.append('    render')
    text.append('    delay 100')
    text.append('loop') 
    
else:  # normal
    for phase_int in range(LEN+16):
        # ~ phase_int = LEN/2+8+LEN/2+7
        for index in range(LEN/2+1):
            if phase_int < LEN/2+8:
                bright_clipped = phase_int - index
            else:
                bright_clipped = LEN/2+16-phase_int + index
                
            if bright_clipped > 8:
                bright_clipped = 8
            elif bright_clipped < 0:
                bright_clipped = 0
                
            leds[(CENTER-index+LEN)%LEN] = (2**bright_clipped)-1;
            leds[(CENTER+index+LEN)%LEN] = (2**bright_clipped)-1;


        
        text = text + dump_leds()

        text.append('render')  # draw it
        text.append('delay 200')  # wait a bit



fh = open('moon_temp.sh', 'w')
fh.write('\n'.join(text)+'\n')
fh.close()

# ~ for day in range(31):
    # ~ print("%d %f" % (day+1, get_phase_on_day(2019,8,day+1)))

# ~ print get_phase_on_day(2019,7,28)

# ~ print get_moons_in_year(2019)
