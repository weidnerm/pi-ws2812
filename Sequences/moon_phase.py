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
    
def pulse_red():
    start = 10
    brightness = start
    rate = 0.07
    dir_rate = rate
    delay = 25
    
    text.append('do')
    while(brightness < 255):
        brightness = (1+dir_rate)*brightness
        if brightness > 255:
            brightness = 255
        text.append('    fill 1,%02x0000,0,53;render;delay %d' % (int(brightness), delay))  # all off
    while(brightness > start):
        brightness = (1-dir_rate)*brightness
        text.append('    fill 1,%02x0000,0,53;render;delay %d' % (int(brightness), delay))  # all off
    text.append('loop') 

def pulse_red_and_green(delay):
    start = 10
    brightness = start
    rate = 0.15
    dir_rate = rate
    
    text.append('do')
    while(brightness < 255):
        brightness = (1+dir_rate)*brightness
        if brightness > 255:
            brightness = 255
        text.append('    fill 1,%02x0000,0,53;render;delay %d' % (int(brightness), delay))  # all off
    while(brightness > start):
        brightness = (1-dir_rate)*brightness
        text.append('    fill 1,%02x0000,0,53;render;delay %d' % (int(brightness), delay))  # all off
    text.append('loop 1') 
    brightness = start
    text.append('do')
    while(brightness < 255):
        brightness = (1+dir_rate)*brightness
        if brightness > 255:
            brightness = 255
        text.append('    fill 1,00%02x00,0,53;render;delay %d' % (int(brightness), delay))  # all off
    while(brightness > start):
        brightness = (1-dir_rate)*brightness
        text.append('    fill 1,00%02x00,0,53;render;delay %d' % (int(brightness), delay))  # all off
    text.append('loop 1') 
    text.append('loop ') 

def rotate_two_points(color,delay):

    text.append('fill 1,%s,0,8' %(color))  # a few red
    text.append('fill 1,%s,26,8' %(color))  # a few red
    
    text.append('do')
    text.append('    rotate 1,1,-1  ')
    text.append('    render')
    text.append('    delay %d' %(delay))
    text.append('loop') 

def rotate_fourth_of_july(delay):

    text.append('fill 1,%s,0,8' %('ff0000'))  # a few red
    text.append('fill 1,%s,18,8' %('ffffff'))  # a few red
    text.append('fill 1,%s,36,8' %('0000ff'))  # a few red
    
    text.append('do')
    text.append('    rotate 1,1,-1  ')
    text.append('    render')
    text.append('    delay %d' %(delay))
    text.append('loop') 

def rotate_xmas(delay):

    text.append('fill 1,%s,0,20' %('ff0000'))  # a few red
    text.append('fill 1,%s,26,20' %('00ff00'))  # a few red
    
    text.append('do')
    text.append('    rotate 1,1,-1  ')
    text.append('    render')
    text.append('    delay %d' %(delay))
    text.append('loop') 



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

if ((month==2) and (day==14)): # tammy
    rotate_two_points('ff00ff',100) # purple
    
elif ((month==9) and (day==19)): # courtney
    rotate_two_points('ffc000',100) # yellow
    
elif ((month==11) and (day==12)): # tiffany
    rotate_two_points('ff8080',100) # pink
    
elif ((month==9) and (day==12)): # mike
    rotate_two_points('00ffff',100) # cyan
    
elif ((month==4) and (day==13)): # andrew
    rotate_two_points('00ff00',100) # green
    
elif ((month==7) and (day==4)): # 4th of july
    rotate_fourth_of_july(100) # red white blue

elif ((month==3) and (day==17)): # st pats
    rotate_two_points('00ff00',100) # green

elif ((month==12) and (day==25)): # xmas
    rotate_xmas(100) # red green

# ~ elif ((month==5) and (day==25)):
    # ~ rotate_two_points('ffc000',100) # yellow
    
    
    
elif (sep_max>177.5):  # eclipse where moon in earths shadow
    if moon_alt_max>0:  # its visible. spin fast
        rotate_two_points('ff0000',25) # red
    else:
        rotate_two_points('ff0000',100) # red

elif (sep_min<0.9):  # eclipse where moon covers sun
    if moon_alt_min>0:  # its visible. spin fast
        rotate_two_points('ffffff',25) # white
    else:
        rotate_two_points('ffffff',100) # white
    
elif day_of_moon_phase == 23: # special alien party
    
    text.append('rainbow 1,1,0,53')

    text.append('do')
    text.append('    rotate 1,1,-1  ')
    text.append('    render')
    text.append('    delay 100')
    text.append('loop') 
    

else:  # normal
    text.append('fill 1')  # all off
    text.append( get_side_control_text('right', get_color_from_table('right', day_of_moon_phase)))
    text.append( get_side_control_text('top', get_color_from_table('top', day_of_moon_phase)))
    text.append( get_side_control_text('left', get_color_from_table('left', day_of_moon_phase)))
    text.append( get_side_control_text('bottom', get_color_from_table('bottom', day_of_moon_phase)))

    text.append('render')  # draw it
    text.append('delay 200')  # wait a bit



fh = open('moon_temp.sh', 'w')
fh.write('\n'.join(text)+'\n')
fh.close()

# ~ for day in range(31):
    # ~ print("%d %f" % (day+1, get_phase_on_day(2019,8,day+1)))

# ~ print get_phase_on_day(2019,7,28)

# ~ print get_moons_in_year(2019)
