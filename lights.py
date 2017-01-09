import fcntl
import time
import array
import random

spidev = file("/dev/spidev0.0", "wb")
fcntl.ioctl(spidev, 0x40046b04, array.array('L', [400000]))

class rgb_light(object):
  def __init__(self, red = 0, green = 0, blue = 0):
    self.light=bytearray(3)
    self.light[0] = red
    self.light[1] = green
    self.light[2] = blue

max_lights=90

current_light_states = [rgb_light] * max_lights
init_light_state = bytearray(3)
init_light_state[0] = 0
init_light_state[1] = 0 
init_light_state[2] = 0


for x in range (0, max_lights):
  current_light_states[x] = init_light_state


def color_all(r, g, b):
  for x in range (0,max_lights):
    current_light_states[x] = set_color(r,g,b)
  change_lights()


def color_one(n, r, g, b):
  set_color(r,g,b);
  current_light_states[n] = set_color(r,g,b)
  change_lights()

 
def set_color(r, g, b):
  light_color = bytearray(3)
  light_color[0] = r
  light_color[1] = g
  light_color[2] = b 
  return light_color


def change_lights():
  time.sleep(0.05)
  for x in range (0,max_lights):
    spidev.write(current_light_states[x])
  spidev.flush()


def get_pixel_color(i_x, i_y):
  import PIL.Image
  import PIL.ImageStat
  import Xlib.display
  o_x_root = Xlib.display.Display().screen().root
  o_x_image = o_x_root.get_image(i_x, i_y, 1, 1, Xlib.X.ZPixmap, 0xffffffff)
  o_pil_image_rgb = PIL.Image.fromstring('RGB', (1,1), o_x_image.data, 'raw', 'BGRX')
  lf_color = PIL.ImageStat.Stat(o_pil_image_rgb).mean
  return tuple (map(int, lf_color))


def fill(r, g, b):
  for x in range(0, max_lights):
    color_one(x, r, g, b)

def loop_forever():
  while True:
    random_color_one = random.randrange(0, 180)
    random_color_two = random.randrange(0, 180)
    random_color_three = random.randrange(0, 180)
    fill(random_color_one, random_color_two, random_color_three)
    

def chase():
  second = 0
  third = 0
  fourth = 0
  while True:
    first = 0
    while first < max_lights:
      color_one(fourth, 20, 20, 20)
      color_one(first, 255, 0, 0)
      color_one(second, 0, 255, 0)
      color_one(third, 0, 0, 255)
      time.sleep(0.03)
      fourth = third
      third = second
      second = first
      first = first+1
	 
def pulse():
  x = 0
  while True:
    while x < 255:
      color_all(0, x, x) 
      x = x+1
    while x > 5:
      color_all(0, x, x)
      x = x-1

def helloworld():
 print "Hello world"


def xmas():
  x=0
  color_change_flag=0 
  while True:
    if color_change_flag == 0:
      red = set_color(65, 0, 0)
      green = set_color(0, 65, 0)
      color_change_flag = 1
    else:
      red = set_color(0, 65, 0)
      green = set_color(65, 0, 0)
      color_change_flag = 0

    x=0 

    while x+1 < max_lights:
      current_light_states[x] = red
      current_light_states[x+1] = green
      x = x+2
    change_lights()
    time.sleep(2)

def xmas_lights_twinkle():

  modifier = 5

  red_brightness   = 100
  green_brightness = 100
  white_brightness = 100
  brightness       = 100

  while True:

     if brightness == 20:
       modifier = 5
     elif brightness == 140:
       modifier = -5

     red_brightness     = red_brightness   + modifier   
     green_brightness   = green_brightness - modifier   
     white_brightness   = white_brightness + modifier   
     brightness         = brightness + modifier;

     red   = set_color(red_brightness, 0, 0)
     green = set_color(0, green_brightness, 0)
     white = set_color(white_brightness, white_brightness, white_brightness)

     x=0
     while x+1 < max_lights:
       current_light_states[x]   = red 
       current_light_states[x+1] = green
       current_light_states[x+2] = white
       x = x+3
       
     change_lights()
     time.sleep(.1)

def filler(t):
   while True:
    x = 0
    while x < 90:
       color_one(x, 0, 40, 0)
       time.sleep(t)
       x = x + 1
    x = 89 
    while x > 0:
       color_one(x, 0, 0, 40)
       time.sleep(t)
       x = x - 1

def wow(t):
   point = 9 
   while True:
      star_points = 5
      while star_points > 0:
         point = (point + 18)%90 - 1
         current_light_states[point] = set_color(0, 0, 40)
         star_points = star_points - 1

      change_lights()
      time.sleep(t)  

def fade(maxBrightness=255):
  red = 0
  green = 0
  blue = 0
  while True:
    while red < maxBrightness:
      color_all(red, green, blue)
      red = red + 1
    while blue > 0:
      color_all(red, green, blue)
      blue = blue - 1
    while green < maxBrightness:
      color_all(red, green, blue)
      green = green + 1
    while red > 0:
      color_all(red, green, blue)
      red = red - 1
    while blue < maxBrightness:
      color_all(red, green, blue)
      blue = blue + 1
    while green > 0:
      color_all(red, green, blue)
      green = green - 1


def strobe(slow=0, r=255, g=255, b=255):
  while True:
    color_all(r, g, b)
    if slow > 0:
      time.sleep(slow)
    color_all(0, 0, 0)
    if slow > 0:
      time.sleep(slow)

def rainbowChase(maxBrightness=255, slow=0):
  step = 5 # must be a mulitple of maxBrightness such that the color will land on maxBrightness
  r = 0
  g = 0
  b = 0
 
  while True:
    x = 0
    while x < max_lights:
      y = x
      while y > 0:
        current_light_states[y] = current_light_states[y - 1]
        y = y - 1
      current_light_states[y] = rainbowHelper(maxBrightness, r, g, b, step)
      r = current_light_states[y][0]
      g = current_light_states[y][1]
      b = current_light_states[y][2]
      x += 1 
      if slow > 0:
	time.sleep(slow)
      change_lights()

def rainbowHelper(maxBrightness, red, green, blue, step):
    if red < maxBrightness and green == 0 and blue == 0: # begining state
      if red + step <= maxBrightness:
        red = red + step
    elif red < maxBrightness and green == 0 and blue == maxBrightness:
      if red + step <= maxBrightness:
        red = red + step
    elif red == maxBrightness and green == 0 and blue > 0:
      if blue - step >= 0:
        blue = blue - step
    elif red == maxBrightness and green < maxBrightness and blue == 0:
      if green + step <= maxBrightness:
        green = green + step
    elif red > 0 and green == maxBrightness and blue == 0:
      if red - step >= 0:
        red = red - step
    elif red == 0 and green == maxBrightness and blue < maxBrightness:
      if blue + step <= maxBrightness:
        blue = blue + step
    elif red == 0 and green > 0 and blue == maxBrightness:
      if green - step >= 0:
        green = green - step      
    return set_color(red, green, blue)

def ringAroundTheRainbow(animate=0, slow=0):
  maxBrightness = 255
  step = 17
  r = 255
  g = 0
  b = 0
  x = 0
 
  global current_light_states 
 
  while x < max_lights:
    current_light_states[x] = rainbowHelper(maxBrightness, r, g, b, step)
    r = current_light_states[x][0]
    g = current_light_states[x][1]
    b = current_light_states[x][2]
    x += 1

  if animate == 0:
    change_lights()
  else:
    while True:
      change_lights()
      current_light_states = shift(current_light_states,1)
      if slow > 0:
        time.sleep(slow)

def shift(array, n):
    return array[-n:] + array[:-n]

def starBurst(slow=0):
  maxBrightness = 153 # 255
  step = 51
  r = maxBrightness
  g = 0
  b = 0

  white = set_color(maxBrightness,maxBrightness,maxBrightness)
  red = set_color(maxBrightness,0,0)
  orange = set_color(maxBrightness,25,0)
  yellow = set_color(maxBrightness,maxBrightness,0)
  green = set_color(0,maxBrightness,0)
  dkGreen = set_color(34,maxBrightness,12)
  cyan = set_color(0,maxBrightness,maxBrightness)
  blue = set_color(0,0,255)
  purple = set_color(20,0,192)
  gold = set_color(maxBrightness,129,0)
  pink = set_color(maxBrightness,20,147)
  magenta = set_color(maxBrightness,0,127)

  off = set_color(0,0,0)
  # color0 = set_color(r, g, b)
  # color1 = set_color(r, g, b)
  # color2 = set_color(r, g, b)
  # color3 = set_color(r, g, b)
  # color4 = set_color(r, g, b)
  # color5 = set_color(r, g, b)
  # color6 = set_color(r, g, b)
  # color7 = set_color(r, g, b)
  # color8 = set_color(r, g, b)
  # color9 = set_color(r, g, b)
  
  color0 = white
  color1 = red
  color2 = white
  color3 = red
  color4 = white
  color5 = red
  color6 = white
  color7 = red
  color8 = white
  color9 = red

  ring0 = [17,35,53,71,89]
  ring1 = [0,16,18,34,36,52,54,70,72,88]
  ring2 = [1,15,19,33,37,51,55,69,73,87]
  ring3 = [2,14,20,32,38,50,56,68,74,86]
  ring4 = [3,13,21,31,39,49,57,67,75,85]
  ring5 = [4,12,22,30,40,48,58,66,76,84]
  ring6 = [5,11,23,29,41,47,59,65,77,83]
  ring7 = [6,10,24,28,42,46,60,64,78,82]
  ring8 = [7,9,25,27,43,45,61,63,79,81]
  ring9 = [8,26,44,62,80]

  while True:
    # color0 = rainbowHelper(maxBrightness, r, g, b, step)
    color0 = color9
    i = 0
    while i < len(ring0):
      current_light_states[ring0[i]] = color0
      current_light_states[ring9[i]] = color9
      i += 1
    r = current_light_states[ring0[0]][0]
    g = current_light_states[ring0[0]][1]
    b = current_light_states[ring0[0]][2]
    j = 0
    while j < len(ring1):
      current_light_states[ring1[j]] = color1
      current_light_states[ring2[j]] = color2
      current_light_states[ring3[j]] = color3
      current_light_states[ring4[j]] = color4
      current_light_states[ring5[j]] = color5
      current_light_states[ring6[j]] = color6
      current_light_states[ring7[j]] = color7
      current_light_states[ring8[j]] = color8
      j += 1
    change_lights()
    color9 = color8
    color8 = color7
    color7 = color6
    color6 = color5
    color5 = color4
    color4 = color3
    color3 = color2
    color2 = color1
    color1 = color0
    if slow > 0:
        time.sleep(slow)

def barSpin(slow=0):
  maxBrightness = 255
  step = 51
  r = 255
  g = 0
  b = 0

  blue = set_color(0,0,255)
  green = set_color(0,255,0)

  color0 = blue
  color1 = green
  color2 = blue
  color3 = green
  color4 = blue
  color5 = green
  color6 = blue
  color7 = green
  color8 = blue
  color9 = green

  # color0 = set_color(r, g, b)
  # color1 = set_color(r, g, b)
  # color2 = set_color(r, g, b)
  # color3 = set_color(r, g, b)
  # color4 = set_color(r, g, b)
  # color5 = set_color(r, g, b)
  # color6 = set_color(r, g, b)
  # color7 = set_color(r, g, b)
  # color8 = set_color(r, g, b)
  # color9 = set_color(r, g, b)

  ray0 = [89,0,1,2,3,4,5,6,7,8]
  ray1 = [17,16,15,14,13,12,11,10,9,8]
  ray2 = [17,18,19,20,21,22,23,24,25,26]
  ray3 = [35,34,33,32,31,30,29,28,27,26]
  ray4 = [35,36,37,38,39,40,41,42,43,44]
  ray5 = [53,52,51,50,49,48,47,46,45,44]
  ray6 = [53,54,55,56,57,58,59,60,61,62]
  ray7 = [71,70,69,68,67,66,65,64,63,62]
  ray8 = [71,72,73,74,75,76,77,78,79,80]
  ray9 = [89,88,87,86,85,84,83,82,81,80]

  while True:
    # color0 = rainbowHelper(maxBrightness, r, g, b, step)
    color0 = color9
    j = 0
    while j < len(ray0):
      current_light_states[ray9[j]] = color9
      current_light_states[ray8[j]] = color8
      current_light_states[ray7[j]] = color7
      current_light_states[ray6[j]] = color6
      current_light_states[ray5[j]] = color5
      current_light_states[ray4[j]] = color4
      current_light_states[ray3[j]] = color3
      current_light_states[ray2[j]] = color2
      current_light_states[ray1[j]] = color1
      current_light_states[ray0[j]] = color0
      j += 1
    r = current_light_states[ray0[1]][0]
    g = current_light_states[ray0[1]][1]
    b = current_light_states[ray0[1]][2]
    change_lights()
    color9 = color8
    color8 = color7
    color7 = color6
    color6 = color5
    color5 = color4
    color4 = color3
    color3 = color2
    color2 = color1
    color1 = color0
    if slow > 0:
        time.sleep(slow)
