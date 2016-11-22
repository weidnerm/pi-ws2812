rpi_ws281x
==========

Userspace Raspberry Pi PWM library for WS281X LEDs
This includes WS2812 and SK6812RGB RGB LEDs
Preliminary support is now included for SK6812RGBW LEDs (yes, RGB + W)

### Background:

The BCM2835 in the Raspberry Pi has a PWM module that is well suited to
driving individually controllable WS281X LEDs.  Using the DMA, PWM FIFO,
and serial mode in the PWM, it's possible to control almost any number
of WS281X LEDs in a chain connected to the PWM output pin.

This library and test program set the clock rate of the PWM controller to
3X the desired output frequency and creates a bit pattern in RAM from an
array of colors where each bit is represented by 3 bits for the PWM
controller as follows.

    Bit 1 - 1 1 0
    Bit 0 - 1 0 0


### Hardware:

WS281X LEDs are generally driven at 5V, which requires that the data
signal be at the same level.  Converting the output from a Raspberry
Pi GPIO/PWM to a higher voltage through a level shifter is required.

It is possible to run the LEDs from a 3.3V - 3.6V power source, and
connect the GPIO directly at a cost of brightness, but this isn't
recommended.

The test program is designed to drive a 8x8 grid of LEDs from Adafruit
(http://www.adafruit.com/products/1487).  Please see the Adafruit
website for more information.

Know what you're doing with the hardware and electricity.  I take no
reponsibility for damage, harm, or mistakes.

### Build:

- Install Scons (on raspbian, apt-get install scons).
- Make sure to adjust the parameters in main.c to suit your hardare.
  - Signal rate (400kHz to 800kHz).  Default 800kHz.
  - ledstring.invert=1 if using a inverting level shifter.
  - Width and height of LED matrix (height=1 for LED string).
- Type 'scons' from inside the source directory.

### Running:

- Type 'sudo scons'.
- Type 'sudo ./test'.

### Limitations:

Since this library and the onboard Raspberry Pi audio both use the PWM,
they cannot be used together.  You will need to blacklist the Broadcom
audio kernel module by creating a file /etc/modprobe.d/snd-blacklist.conf
with

    blacklist snd_bcm2835

If the audio device is still loading after blacklisting, you may also
need to comment it out in the /etc/modules file.

Some distributions use audio by default, even if nothing is being played.
If audio is needed, you can use a USB audio device instead.

### Usage:

The API is very simple.  Make sure to create and initialize the ws2811_t
structure as seen in main.c.  From there it can be initialized
by calling ws2811_init().  LEDs are changed by modifying the color in
the .led[index] array and calling ws2811_render().  The rest is handled
by the library, which creates the DMA memory and starts the DMA/PWM.

Make sure to hook a signal handler for SIGKILL to do cleanup.  From the
handler make sure to call ws2811_fini().  It'll make sure that the DMA
is finished before program execution stops.

That's it.  Have fun.  This was a fun little weekend project.  I hope
you find it useful.

#Testing
Connect your LEDs to the PWM output of the Raspberry Pi and start the program:

* sudo ./test

Now first initialize the driver code from jgarff by typing 'setup'.
On the following line you must **replace 10** by the number of leds you have attached!.

* setup channel_1_count=10

Now you can type commands to change the color of the leds.
For example make them all red:

* fill 1,FF0000
* render

#Supported commands
Here is a list of commands you can type or send to the program. All commands have optional comma seperated parameters. The parameters must be in the correct order except for the 'setup' command.

* Setup command must be called everytime the program is started:
```
setup
   channel_1_count=1,        #number of leds on channel 1
   freq=800000,               #frequency used to talk to the leds
   dma=5,                     #dma channel
   channels=1,                #number of led strings / PWM outputs / channels used
   channel_1_gpio=18,         #GPIO number of channel 1
   channel_1_invert=0,        #Invert the output of channnel 1 (in case you are using an 3.3V->5V level shifter)
   channel_1_brightness=255,  #default brightness of the leds (can be changed with brightness command)
   channel_2_count=0,         #number of leds in channel 2
   channel_2_gpio=0,          #GPIO number for channel 2
   channel_2_invert=0,        #invert the output of channel 2
   channel_2_brightness=255   #brightness for channel 2

Example:
   setup channel_1_count=10
```

* Render command sends the internal buffer to all leds
```
render
    <channel>,          #send the internal color buffer to all the LEDS of <channel> default is 1
    <start>,            #before render change the color of led(s) beginning at <start> (0=led 1)
    <RRGGBBRRGGBB...>   #color to change the led at start Red+green+blue (no default)
```

* rotate command moves all color values of 1 channel
```
rotate
    <channel>,         #channel to rotate (default 1)
    <places>,          #number of places to move each color value (default 1)
    <direction>,       #direction (0 or 1) for forward and backwards rotating (default 0)
    <RRGGBB>           #first led(s) get this color instead of the color of the last led
```

* rainbow command creates rainbows or gradient fills
```
rainbow
    <channel>,         #channel to fill with a gradient/rainbow (default 1)
    <count>,           #number of times to repeat the rainbow in the channel (default 1)
    <start>,           #at which led should we start (default is 0)
    <len>              #number of leds to fill with the given color after start (default all leds)
    <start_color>,     #color to start with value from 0-255 where 0 is red and 255 pink (default is 0)
    <end_color>        #color to end with value from 0-255 where 0 is red and 255 pink (default 255)
```

* fill command fills number of leds with a color value
```
fill
    <channel>,          #channel to fill leds with color (default 1)
    <RRGGBB>,           #color to fill (default FF0000)
    <start>,            #at which led should we start (default is 0)
    <len>               #number of leds to fill with the given color after start (default all leds)
```

* candycane command creates a repeating 2 color stripe pattern
```
candycane
    <channel>,          #channel to fill leds with color (default 1)
    <RRGGBB>,           #color 1 to fill (default 000000)
    <count_1>,          #number of leds at color 2 (default is 0)
    <RRGGBB>,           #color 2 to fill (default 000000)
    <count_2>,          #number of leds at color 2 (default is 0)
    <start>,            #at which led should we start (default is 0)
    <len>               #number of leds to fill with the given color after start (default all leds)
```

* tricolor command creates a repeating 3 color stripe pattern
```
tricolor
    <channel>,          #channel to fill leds with color (default 1)
    <RRGGBB>,           #color 1 to fill (default 000000)
    <count_1>,          #number of leds at color 2 (default is 0)
    <RRGGBB>,           #color 2 to fill (default 000000)
    <count_2>,          #number of leds at color 2 (default is 0)
    <RRGGBB>,           #color 3 to fill (default 000000)
    <count_3>,          #number of leds at color 3 (default is 0)
    <start>,            #at which led should we start (default is 0)
    <len>               #number of leds to fill with the given color after start (default all leds)
```

* brightness command changes the brightness of the leds without affecting the color value
```
brightness
    <channel>,          #channel to change brightness (default 1)
    <brightness>        #brightness 0-255 (default 255)
```

* delay command waits for number of milliseconds
```
delay
    <milliseconds>      #enter number of milliseconds to wait
```

#Special keywords
You can add `do ... loop` to repeat commands when using a file or TCP connection.

For example the commands between `do` and `loop` will be executed 10 times:
```
do
   <enter commands here to repeat>
loop 10
```
(Endless loops can be made by removing the '10')

For `do ... loop` to work from a TCP connection we must start a new thread.
This thread will continue to execute the commands when the client disconnects from the TCP/IP connection.
The thread will automatically stop executing the next time the client reconnects (ideal for webservers).

For example:
```
thread_start
   do
      rotate 1,1,2
     render
     delay 200
  loop
thread_stop
<client must close connection now>
```

#PHP example
First start the server program:

* sudo ./ws2812svr -tcp

Then run the php code from the webserver:

```PHP
//create a rainbow for 10 leds on channel 1:
send_to_leds("setup channel_1_count=10;rainbow;brightness 1,32;");
function send_to_leds ($data){
   $sock = fsockopen("127.0.0.1", 9999);
   fwrite($sock, $data);
   fclose($sock);
}
```

#Command line parameters
* sudo ./ws2812svr -tcp 9999
  Listens for clients to connect to port 9999 (default).
* sudo ./ws2812svr -f text_file.txt
  Loads commands from text_file.txt.
* sudo ./ws2812svr -p /dev/ws281x
  Creates a file called `/dev/ws281x` where you can write you commands to with any other programming language (do-loop not supported here).

