import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import math

def double_digits(d):
    d = d % 100
    if d < 10:
        return "0" + str(d)
    else:
        return str(d)
        
player = ["\\()/",
          "-()-",
          "/()\\"]
          

        
def place_player(grid,cc,rr):
    start_line = 0
    start_index = 0
    if int((len(grid)-1)/6)-1 % 2 == 1:
        print("yes")
        if cc % 2 == 0:
            start_line = rr * 6 + 3
            start_index = 6 + 9 * cc - 2
        elif cc % 2 == 1:
            start_line = rr * 6
            start_index = 6 + 9 * cc - 2
    else:
        if cc % 2 == 0:
            start_line = rr * 6
            start_index = 6 + 9 * cc - 2
        elif cc % 2 == 1:
            print("Yes?")
            start_line = rr * 6 + 3
            start_index = 6 + 9 * cc - 2
    
    for (l,p) in zip(range(start_line, start_line + 3),player):
        line = grid[l]
        line = line[0:start_index] + p + line[start_index+4:]
        grid[l] = line
    return grid
    

layers = 5
ascii_hex = ["   ______   ",
             "  / CCRR \\  ",
             " /        \\ ",
             "/          \\",
             "\\          /",
             " \\        / ",
             "  \\______/  "]
# Hexagon courtesy of https://ascii.co.uk/art/hexagon

blank_space = 9 * " "
for line in ascii_hex:
    print(line)
    
hex_grid = [""] * (1 + (len(ascii_hex)-1) * (2*layers + 1))
layer_tracker = (layers + 1) * [-1]
layer_tracker[0] = 0
for i in range(int(len(hex_grid)/2)+1):
    space = ""
    top_row = ""
    bot_row = ""
    top_left = ""
    bot_left = ""
    top_right = ""
    bot_right = ""
    for l in range(len(layer_tracker)):
        layer = layer_tracker[l]
        if l == 0:
            top_row = ascii_hex[layer]
            bot_row = ascii_hex[-layer]
            layer_tracker[l] = (layer % 6) + 1
        elif layer > -1 and l > 0:
            layer_tracker[l] = (layer % 6) + 1
            layer = layer_tracker[l]
            top_left = ascii_hex[layer][:9] + top_left
            bot_left = ascii_hex[-layer][:9] + bot_left
            top_right = top_right + ascii_hex[layer][3:]
            bot_right = bot_right + ascii_hex[-layer][3:]

    if i <= layers * 3:
        space = (layers - math.floor(i/3)) * blank_space
        if i > 0 and i % 3 == 0:
            layer = int(i / 3)
            layer_tracker[layer] = 0
            top_left = ascii_hex[0][:9] + top_left
            bot_left = blank_space + bot_left
            top_right = top_right + ascii_hex[0][3:]
            bot_right = bot_right + blank_space

    hex_grid[i] = space + top_left + top_row + top_right + space
    hex_grid[-i] = space + bot_left + bot_row + bot_right + space

for i in range(len(hex_grid)):
    line = hex_grid[i]
    if i % 3 == 1:
        line = line.split("CCRR")
        l = line[0]
        cc = int((len(l) - 4) / 9)
        rr = 0
        rr = math.floor(i/6)
        for s in line[1:]:
            l = l + double_digits(cc) + double_digits(rr) + s
            cc = cc + 2
        line = l
        hex_grid[i] = line
                
    print(line)
    
new_grid = place_player(hex_grid,7,6)

for line in new_grid:
    print(line)
            