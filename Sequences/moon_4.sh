setup channel_1_count=53
#https://github.com/tom-2015/rpi-ws2812-server
brightness 1,128
# g,r,b

rainbow 1,1,0,53

do
    rotate 1,1,-1
    render
    delay 100
loop 

