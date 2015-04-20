'''----------------------------------------------------------------------------
Author: Caleb R. Weir, 4/20/15
-------------------------------------------------------------------------------

 Example of how to run this:
 
   python generator.py specX.json outputX.png hexcode1 hexcode2

   <interpreter> = python (with path set properly, python should be found)
   <script name> = the name used to find this script
           ex: 'C:\Users\<user>\workspace\payline_generator\generator.py'
   <spec name>   = .json file with properties:
           2D list 'paylines'; and int 'windowHeight';
   <output path> = any valid name for image file: .png, .jpg, etc.
   <hexcode1> = hexcode, RGB or RGB with alpha
   <hexcode2> = same; 2 is the inactive payline, 1 is active;

 Hexcode example:

   #71ceb4
   #f7b97e

 RGB/RGBA example:
 
   (255, 100, 0) = RGB
   (255, 100, 0, 50) = RGB with 50% alpha transparency
   (0, 40, 200, 100) = RGB with 100% alpha transparency
   (0, 50, 100, 0) = RGB with 0% alpha transparency

----------------------------------------------------------------------------'''

'''Local imports'''
import json
import sys

'''3rd party imports'''
from PIL import Image
from PIL import ImageDraw

'''Globals
 -- editable! read the comments on these first so you know wtf is going on;'''
TOTAL_COLUMNS_ACROSS = 10 - 1 # subtract 1 from whatever it actually is
SIZE = 8 * 2 # ONLY EVENS; Size of both width and length of payline box;
FILLED_SCALE = 2 # ONLY EVENS; Pixel border is half this number;

'''-------------------------------------------------------------------------'''

'''Extracts data from the .json file that is applicable to current
payline generation'''
def get_json(path): # Takes .json path and returns spec values
    json_data = open(path); data = json.load(json_data);
    return data['paylines'], data['windowHeight'], len(data['paylines'][0]), json_data

'''Finds sizing based on preferences'''
def get_size():
    return SIZE*W_WIDTH+EDGE_BUFFER, SIZE*W_HEIGHT+EDGE_BUFFER

'''Finds the correct configuration based on .json'''
def get_payline_dimensions():
    return len(PAYLINES), len(PAYLINES)/TOTAL_COLUMNS_ACROSS, TOTAL_COLUMNS_ACROSS

'''Creates the new image that we are drawing on'''
def get_image(total_rows, total_columns):
    dimensions = (get_image_width(total_columns), get_image_height(total_rows))
    img = Image.new('RGBA', dimensions, (0,0,0,0))
    return img, ImageDraw.Draw(img)

'''Finds the correct sizing based on preferences'''
def get_image_height(total_rows):
    if (total_rows-2) >= 1:
        return (EDGE_BUFFER*(total_rows-1))+(SIZE*W_HEIGHT)*total_rows
    else:
        return (SIZE*W_HEIGHT)*(total_rows)+EDGE_BUFFER

'''Finds the correct sizing based on preferences'''
def get_image_width(total_columns):
    global EDGE_BUFFER; EDGE_BUFFER = SIZE*(W_WIDTH/4);
    if (total_columns-2) >= 1:
        return (EDGE_BUFFER*total_columns)+(SIZE*W_WIDTH)*(total_columns+1)
    else:
        return (SIZE*W_WIDTH)*(total_columns+1)+EDGE_BUFFER

'''Draw alpha pattern to trim windows'''
def draw_payline_cutoffs(draw, payline, x_point, y_point):
    for y in range(W_HEIGHT): # Draws an alpha line surrounding each pay window
        for x in range(W_WIDTH): 
            x_base = (x_point+x*SIZE); y_base = (y_point+y*SIZE);
            x_end = x_base+SIZE; y_end = y_base+SIZE;
            draw.rectangle([x_base, y_base, x_end, y_end], outline=(0,0,0,0))

'''Draw payline with empty color'''
def draw_inactive(draw, payline, x_point, y_point, fill_color):
    for x in range(W_WIDTH):
        for y in range(W_HEIGHT):
            x_base = x_point+x*SIZE+FILLED_SCALE; y_base = y_point+y*SIZE+FILLED_SCALE;
            x_end = x_base+SIZE-FILLED_SCALE*2; y_end = y_base+SIZE-FILLED_SCALE*2;
            draw.rectangle([x_base, y_base, x_end, y_end], fill=fill_color)

'''Draw payline with hit color'''            
def draw_active(draw, payline, x_pos, y_pos, fill_color):
    for x in range(W_WIDTH):
        for y in range(W_HEIGHT):
            '''This if statement is the only thing separating us from the animals'''
            if payline[x] == y:
                x_base = x_pos+x*SIZE+FILLED_SCALE; y_base = y_pos+y*SIZE+FILLED_SCALE;
                x_end = x_base+SIZE-FILLED_SCALE*2; y_end = y_base+SIZE-FILLED_SCALE*2;
                draw.rectangle([x_base, y_base, x_end, y_end], fill=fill_color)

'''Essentially just draws the same thing multiple times, with the
latest function being the visual showing on top -- could potentially
mute the lower draws when wasteful'''
def draw_paylines(draw, payline, x_point, y_point, active_color, inactive_color):
    draw_inactive(draw, payline, x_point, y_point, inactive_color)
    draw_active(draw, payline, x_point, y_point, active_color)
    draw_payline_cutoffs(draw, payline, x_point, y_point)

'''Handles the variance in payline structures and tells the other
functions when/where to draw specific paylines'''
def generate_formatted_paylines(active_color, inactive_color):
    total = 0; y_count = 0; x_count = 0;
    total_paylines, total_rows, total_columns = get_payline_dimensions()
    img, draw = get_image(total_rows, total_columns); x_size, y_size = get_size();
    print 'Drawing out %i paylines: %i rows and %i columns' % (
        total_paylines, total_rows, total_columns+1)
    print 'PS: Tell Channing to give me more dev tasks.'
    for payline in PAYLINES:
        x_point = x_size*x_count; y_point = y_size*y_count;
        draw_paylines(draw, PAYLINES[total], x_point, y_point, active_color, inactive_color)
        total += 1
        if x_count >= total_columns: # Checks if we need new row
            x_count = 0; y_count +=  1; # Increment row position and reset column;
        else: x_count +=  1 # If not, just move right one
    return img # All done

'''-------------------------------------------------------------------------'''

'''Default run logic'''
def main(json_path, output_path, active_color, inactive_color):
    print 'generate_paylines.py script initialized.'
    global PAYLINES, W_HEIGHT, W_WIDTH; # Close the .json. Fuck off memory leaks.
    PAYLINES, W_HEIGHT, W_WIDTH, json_data = get_json(json_path); json_data.close(); 
    generate_formatted_paylines(active_color, inactive_color).save(output_path)
    print 'generate_paylines.py script completed.'

'''If user does not run properly, run the script manually to show
how the script functions'''
def failsafe():
    import random
    num = random.randint(0, 1)
    spec = 'spec%i.json' % num
    path = 'example%i.png' % num
    active = ((255, 20, 20, 100), '#71ceb4')
    inactive = ((50, 0, 255, 100), '#f7b97e')
    main(spec, path, active[num], inactive[num])

'''-------------------------------------------------------------------------'''

args = []
for arg in sys.argv:
    args.append(arg)
try:
    main(args[1], args[2], args[3], args[4]) # Runs args 1-4 because 0 is the script itself
except IndexError:
    print '''Not enough arguments to run script. \n
    Script is now running example failsafe.'''
    failsafe()

'''-------------------------------------------------------------------------'''
