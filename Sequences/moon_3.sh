setup channel_1_count=53
#https://github.com/tom-2015/rpi-ws2812-server
brightness 1,128
# g,r,b

fill 1,404040,0,13
fill 1,808080,13,13
fill 1,ffffff,26,13
fill 1,808080,39,14
render
#~ delay 4000

do
    rotate 1,1,-1
    render
    delay 100
    
loop 252

fill 1
render
