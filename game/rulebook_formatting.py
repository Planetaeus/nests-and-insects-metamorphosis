# Imports

raw_filename = 'New_Rulebook_Raw.txt'
out_filename = 'Nests_And_Insects_Metamorphosis.txt'

page_header = '╔══════► Nests & Insects: Metamorphosis ◄═════════════════════════════════════► Rulebook ◄══╗'
page_footer_left = '╚═══════════════════════════════════════════'
page_footer_right = '═══════════════════════════════════════════╝'
page_footer = page_footer_left + '═════' + page_footer_right
margin_left = '║ '
margin_right = ' ║'
page_width = 89
line_break = '─' * page_width

def update_header(headers, rl):
    hs = headers
    h_level = 0
    if '/h1' in rl: # Header 1
        hs[0] = hs[0] + 1
        hs[1] = 0
        hs[2] = 0
        hs[3] = 0
        h_level = 1
    elif '/h2' in rl: # Header 2
        hs[1] = hs[1] + 1
        hs[2] = 0
        hs[3] = 0
        h_level = 2
    elif '/h3' in rl: # Header 3
        hs[2] = hs[2] + 1
        hs[3] = 0
        h_level = 3
    elif '/h4' in rl: # Header 4
        hs[3] = hs[3] + 1
        h_level = 4
    else:
        hs = [0,0,0,0]
    
    return hs, h_level
     
def header_to_string(hs):
    return str(hs[0]) + '.' + str(hs[1]) + '.' + str(hs[2]) + '.' + str(hs[3])
    
def format_header(h_nums, rl):
    hn, h_level = update_header(h_nums, rl)

    hn_string = header_to_string(hn)
    
    wl = h_level * '  ' + hn_string + rl[3:]
    
    return hn, wl, h_level
    
def pad_right(s, target_width):
    len_diff = target_width - len(s)
    if len_diff > 0:
        s = s + len_diff * ' '
    
    return s

def pads_right(lines, target_width):
    out_line = []
    if isinstance(lines, str):
        out_line = pad_right(lines, target_width)
    else:
        for line in lines:
            out_line.append(pad_right(line, target_width))
    
    return out_line
        
def add_margins(s):
    return margin_left + s + margin_right
        
def adds_margins(lines):
    out_line = []
    if isinstance(lines, str):
        out_line = add_margins(lines)
    else:
        for line in lines:
            out_line.append(add_margins(line))
    
    return out_line

def format_cols(columns):
    cols = columns.split('|')
    for i in range(len(cols)):
        col = cols[i].split(';')
        col_w = 0
        for j in range(len(col)):
            if len(col[j]) > col_w:
                col_w = len(col[j])
        for j in range(len(col)):
            col[j] = pad_right(col[j], col_w)
            
        cols[i] = col
    col_num = len(cols)
    row_num = len(cols[0])
    rows = [''] * row_num
    for row in range(row_num):
        for col in range(col_num):
            rows[row] = rows[row] + ' | ' + cols[col][row]
        rows[row] = rows[row] + ' | '
    
    out_rows = (row_num + 3) * ['']
    out_rows[0] = line_break
    out_rows[1] = rows[0]
    out_rows[2] = line_break
    for i in range(1,row_num):
        out_rows[i+2] = rows[i]
    out_rows[-1] = line_break
    
    return out_rows

def format_table_header(table_num, rl):
    tn = table_num + 1
    wl = 'Table ' + str(tn) + ': ' + rl[3:]
    
    return tn, wl
    
def trim_line(lines):
    out_lines = ['']
    col = 0
    line_index = 0
    if isinstance(lines,str):
        l = lines.strip()
        words = l.split()
        for word in words:
            if col + 1 + len(word) >= 89:
                out_lines[line_index] = out_lines[line_index]
                col = len(word)
                line_index = line_index + 1
                out_lines.append(word)
            elif col == 0:
                col = len(word)
                out_lines[line_index] = word
            else:
                col = col + 1 + len(word)
                out_lines[line_index] = out_lines[line_index] + ' ' + word
            
            out_lines[line_index].strip()
    else:
        for line in lines:
            l = line.strip()
            out_lines.append(l)
    
    return out_lines
    
def format_line(headers, header_pages, h_nums, tables, t_num, t_pages, p_num, rl):
    wl = ''
    rl = rl.strip()
    if len(rl) > 0:
        if '/' in rl[0]: # Does the line start with the formatting character?
            if 'h' in rl[1]:
                h_nums, wl, hl = format_header(h_nums, rl)
                headers.append(wl)
                header_pages.append(str(p_num))
            elif '/table' in rl:
                t_num, wl = format_table_header(t_num, rl)
                tables.append(wl)
                t_pages.append(str(p_num))
            elif '/cols' in rl:
                wl = format_cols(rl[6:])
        else:
            wl = rl.strip()
    wl = trim_line(wl)
    wl = pads_right(wl, page_width)
    wl = adds_margins(wl)
    return headers, t_num, wl

def format_page_footer(page_num):
    num_string = ''
    if page_num / 10 < 1:
        num_string = '--' + str(page_num) + '--'
    elif page_num / 100 < 1:
        num_string = '--' + str(page_num) + '-'
    elif page_num / 1000 < 1:
        num_string = '-' + str(page_num) + '-'
        
    return page_footer_left + num_string + page_footer_right

def format_toc_line(title,page):
    diff = page_width - len(str(title)) - len(str(page))
    out_line = str(title) + diff * '.' + str(page)
    return out_line

headers = []
header_pages = []
tables = []
table_pages = []

with open(raw_filename, 'r', encoding='utf-8') as raw_file, open(temp_filename, 'w', encoding='utf-8') as temp_file:
    read_line = '' 
    write_line = ''
    header_num = [0,0,0,0]
    line_index = 0
    lines_read = 0
    headers = [0,0,0,0]
    page_index = 1
    
    while True:
        
        read_line = raw_file.readline()
        lines_read = lines_read + 1
        if read_line == '': # Is the string empty?
            break
        else:
            headers, table_num, write_lines = format_line(headers, header_pages, header_num, tables, table_num, table_pages, page_index, read_line)
            
            for wl in write_lines:
                write_line = wl
                
                temp_file.write(write_line + u'\n')
                
                line_index = line_index + 1
                if line_index % 48 == 47:
                    page_index = page_index + 1
    write_line = margin_left + page_width * ' ' + margin_right

        out_file.write(write_line + u'\n')
        if line_index % 48 == 47:
        line_index = line_index + 1
    
       