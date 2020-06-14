#!/usr/bin/python
import datetime
import time
import ephem

def get_baseline_file():
    # ~ setup channel_1_count=53
    # ~ brightness 1,128
    base = []
    
    base.append('setup channel_1_count=53')
    base.append('brightness 1,128')
    base.append('')
    
    return base
    
def get_globe_color(moon_alt_degs, sun_alt_degs, hour, minute, wday):
    colorcmd = 'candycane 1,000000,1,000000,1,0,19'
    
    print('get_globe_color(moon_alt_degs=%f, sun_alt_degs=%f, hour=%d, minute=%d, wday=%d)' % (moon_alt_degs, sun_alt_degs, hour, minute, wday) )

    allowed_range = [
        [0,  16.5, 22.5], # monday
        [1,  16.5, 22.5], # tuesday
        [2,  16.5, 22.5], # wednesday
        [3,  16.5, 22.5], # thursday
        [4,  16.5, 22.5], # friday
        [5,  9, 22.5], # saturday
        [6,  9, 22.5], # sunday
    ]
    
    time_now_float = hour+minute/60.0-1  # (subtract a minute to avoid race conditions where triggers match thresholds
    
    is_on = False
    for entry in allowed_range:
        if ((wday == entry[0]) and (time_now_float >= entry[1]) and (time_now_float <= entry[2])):
            is_on = True
    
    if is_on == False:
        print('Off hours. no entries for wday=%d %02d:%02d = %f' % (wday, hour, minute, time_now_float))
        colorcmd = 'candycane 1,000000,1,000000,1,0,19' # off
    else:
        if (moon_alt_degs < 0):
            print('off since moon is below horizon moon_alt_degs=%f' % (moon_alt_degs) )
            colorcmd = 'candycane 1,000000,1,000000,1,0,19' # off
        else:
            if (sun_alt_degs > 0):
                print('Day moon colors since sun_alt_degs=%f' % (sun_alt_degs) )
                colorcmd = 'candycane 1,7f7f7f,1,00007f,1,0,19'  # day moon
            else:
                if moon_alt_degs < 15:
                    print('moonrise colors since moon_alt_degs=%f' % (moon_alt_degs) )
                    colorcmd = 'candycane 1,000000,1,ff4000,1,0,19'  # moonrise
                elif moon_alt_degs < 30:
                    print('high moonrise colors since moon_alt_degs=%f' % (moon_alt_degs) )
                    colorcmd = 'candycane 1,7f7f7f,1,ff4000,1,0,19'  # high moonrise
                else:
                    print('high night moon since moon_alt_degs=%f' % (moon_alt_degs) )
                    colorcmd = 'candycane 1,7f7f7f,1,000000,1,0,19'  # high night moon

    return colorcmd
    

today = time.time()
gmtime = time.gmtime(today)
year = gmtime.tm_year
month = gmtime.tm_mon
day = gmtime.tm_mday
hour = gmtime.tm_hour
minute = gmtime.tm_min
second = gmtime.tm_sec



moon = ephem.Moon()
sun = ephem.Sun()
observer = ephem.city("Miami")
observer.pressure = 0          # disable atmospheric refraction

curtime = datetime.datetime(year, month, day, hour, minute, second)

sep_min = 360
sep_max = 0
moon_alt_max = 0
moon_alt_min = 0
for index in range(1):
    observer.date = curtime

    # computer the position of the sun and the moon with respect to the observer
    moon.compute(observer)
    sun.compute(observer)

    moon_alt_degs = moon.alt/ 0.01745329252
    sun_alt_degs = sun.alt/ 0.01745329252
    #~ print('moon_alt_degs=%f  sun_alt_degs=%f' %(moon_alt_degs, sun_alt_degs) )
    curtime += datetime.timedelta(hours = 1)

localtime = time.localtime(today)
hour = localtime.tm_hour
minute = localtime.tm_min
wday = localtime.tm_wday # 0=monday


get_globe_color(5, 5, 20, 0, 0)


text = get_baseline_file()

#~ text.append( get_globe_color(moon_alt_degs, sun_alt_degs, hour, minute, wday))

text.append('render')  # draw it
text.append('delay 200')  # wait a bit



fh = open('moon_temp.sh', 'w')
fh.write('\n'.join(text)+'\n')
fh.close()
