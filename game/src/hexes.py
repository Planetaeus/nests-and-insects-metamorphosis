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

pit = ["****",
       "****",
       "****"]
       
pillar = ["/--\\",
          "|--|",
          "\\--/"]
          
exit = ["\\  /",
        " >< ",
        "/  \\"]
        
clear = ["    "] * 3
        
ascii_hex = ["   ______   ",
             "  / CCRR \\  ",
             " /        \\ ",
             "/          \\",
             "\\          /",
             " \\        / ",
             "  \\______/  "]
# Hexagon courtesy of https://ascii.co.uk/art/hexagon
        
blank_space = 9 * " "
        
layer_prompt = "Enter Number of Layers: "
pit_prompt = "Enter list of Pit Hexes: "
pillar_prompt = "Enter list of Pillar Hexes: "
exit_prompt = "Enter list of Exit Hexes: "
player_prompt = "Enter list of Player Hexes: "
clear_prompt = "Enter list of Hexes to Clear: "
retry_prompt = "Retry? (y/n): "
filename_prompt = "Enter filename: "

layers = int(input(layer_prompt))

def copy_grid(grid):
    new_grid = [""] * len(grid)
    
    for line, i in zip(grid, range(len(grid))):
        new_grid[i] = line
        
    return new_grid

def print_lines(lines):
    for line in lines:
        print(str(line))

def cols_rows_to_lines_index(rr, cc, lays):
    start_line = 0
    start_index = 0
    
    if lays % 2 == 0:
        if cc % 2 == 0:
            start_line = 3 + rr * 6
            start_index = 6 + 9 * cc - 2
        elif cc % 2 == 1:
            start_line = 6 + rr * 6
            start_index = 6 + 9 * cc - 2
    else:
        if cc % 2 == 0:
            start_line = 6 + rr * 6
            start_index = 6 + 9 * cc - 2
        elif cc % 2 == 1:
            start_line = 3 + rr * 6
            start_index = 6 + 9 * cc - 2
    
    return start_line, start_index

def place_in_grid(grid, start_line, start_index, source):
    
    out_grid = copy_grid(grid)
    
    for (l,s) in zip(range(start_line, start_line + 3),source):
        line = grid[l]
        line = line[0:start_index] + s + line[start_index+4:]
        out_grid[l] = line
    
    return out_grid
    
def place_many_in_grid(rows, cols, grid, sources, layer):
    out_grid = copy_grid(grid)
    
    for r, c, source in zip(rows, cols, sources):
        start_line, start_index = cols_rows_to_lines_index(r, c, layer)
        out_grid = place_in_grid(out_grid, start_line, start_index, source)
    
    return out_grid
    
def parse_grid_list(gl):
    
    hexes = gl.split()
    rows = [0] * len(hexes)
    cols = [0] * len(hexes)
    
    if len(hexes) > 0:
        for h in range(len(hexes)):
            rows[h] = int(hexes[h][0:2])
            cols[h] = int(hexes[h][2:])
    else:
        rows = -1
        cols = -1
        
    return rows, cols
    
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
               
for line in hex_grid:
    print(line)
    
def prompt_retries(prompt, type, grid, layer):
    retry = True
    out_grid = [""] * len(grid)
    
    while retry:
        
        answer = input(prompt)
        cols, rows = parse_grid_list(answer)
        
        if isinstance(rows,list):
            types = [type] * len(rows)
            
            out_grid = place_many_in_grid(rows, cols, grid, types, layer)
            
        print_lines(out_grid)
        
        if not "y" in input(retry_prompt):
            retry = False
    return out_grid
    
    
hex_grid = prompt_retries(pillar_prompt, pillar, hex_grid, layers)
hex_grid = prompt_retries(pit_prompt, pit, hex_grid, layers)
hex_grid = prompt_retries(exit_prompt, exit, hex_grid, layers)
hex_grid = prompt_retries(player_prompt, player, hex_grid, layers)

out_filename = input(filename_prompt)

with open(out_filename, 'w', encoding='utf-8') as out_file:
    for line in hex_grid:
        out_file.write(line + u"\n")

"""
print_lines(hex_grid)
print_lines(pillar_grid)
print_lines(pit_grid)
print_lines(exit_grid)
print_lines(player_grid)
"""
