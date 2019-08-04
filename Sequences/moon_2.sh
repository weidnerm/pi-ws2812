setup channel_1_count=53
#https://github.com/tom-2015/rpi-ws2812-server
brightness 1,32
# g,r,b

do

    fill 1,ff0000,0,53
    render
    delay 300
    fill 1
    render
    delay 300
loop 3
    
#~ fill 1,ff0000,0,30
#~ render
do
    rotate 1,1,-1,0,LEN,ff0000
    render
    delay 100
loop 53

#~ fill 1,00ff00,0,30
#~ render
do
    rotate 1,1,-1,0,LEN,00ff00
    render
    delay 100
loop 53

#~ fill 1,0000ff,0,30
#~ render
do
    rotate 1,1,-1,0,LEN,0000ff
    render
    delay 100
loop 53



fill 1,ff0000,0,30
render
do
    rotate 1,1,-1
    render
    delay 100
loop 53

fill 1
fill 1,00ff00,0,30
render
do
    rotate 1,1,-1
    render
    delay 100
loop 53

fill 1
fill 1,0000ff,0,30
render
do
    rotate 1,1,-1
    render
    delay 100
loop 53



fill 1
render
