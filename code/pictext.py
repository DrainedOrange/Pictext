from PIL import Image
import os, re
import random as r
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.font_manager


# --------------------------------------------------
# PART 1: Mosaic the picture into a sortable block grid with RGB info.
# --------------------------------------------------

# Acquire grid width and height depending on an exact scaling factor.
# Scaling factor represents how many blocks in total to be placed.
def acquire_gird_size(scl):
    img = Image.open(img_path)
    # img = img.rotate(-90, expand=True)
    org_width, org_height = img.size

    t = (scl / (org_width * org_height)) ** 0.5
    width, height = int(org_width * t), int(org_height * t)
    print(f'Grid width = {width}, height = {height}')
    return width, height

# Create mscd_pic color grid.
def msc_pic(scl):
    img = Image.open(img_path)
    # img = img.rotate(-90, expand=True)
    org_width, org_height = img.size

    t = (scl / (org_width * org_height)) ** 0.5
    width, height = int(org_width * t), int(org_height * t)
    anti_scl_hrz, anti_scl_vtc = org_width / width, org_height / height

    vtc = []
    for q in range(height):
        hrz = []
        for p in range(width):
            color = img.getpixel((p * anti_scl_hrz, -q * anti_scl_vtc))
            hrz.append(tuple(i / 255 for i in color))
        vtc.append(hrz)
    print('Picture mosaiced successfully')
    return vtc

# Acquire color of a point in the mosaiced picture.
def color(point, mscd_pic):
    return mscd_pic[point[1]][point[0]]

# --------------------------------------------------
# PART 2: Fill the blocks with strings given in the passage, then output print info.
# --------------------------------------------------

# Divide a whole passage into string pieces.
def divide_passage(passage_path):
    with open(passage_path, 'r', encoding='utf-8') as f:
        passage = f.read()
    string_group = re.split(r'[，。、；：“”‘’（）《》……！？\n]', passage)
    string_group = [string for string in string_group if string.strip() != '']
    string_group.sort(key=len, reverse=1)
    return string_group

# Random font size and font type.
def font_group(font_path):
    return ['./font/' + path for path in os.listdir(font_path)]   
def r_ftsz():
    return r.randint(ftsz_m, ftsz_M)

# Giving the next one's position. m is current font size and n is the next one's.
# REMINDER: The first index refers to vertical and the second refers to horizonal.
def next_position(current, n):
    next_p = current[0][0] + current[1]
    ceiling = 1 - max(current[1], n)
    floor = min(current[1], n) - 1
    next_q = current[0][1] + r.randint(ceiling, floor)
    if not width - next_p:
        next_p = 0
    return [(next_p, next_q), n]

# Create available blocks list.
def empty_list_blocks(width, height):
    empty_list_blocks = []
    for i in range(width):
        for j in range(height):
                empty_list_blocks.append((i, j))
    return empty_list_blocks

# Giving a random position including font size.
def r_point(available_blocks):
    return [r.choice(available_blocks), r_ftsz()]

# Judge if the blocks to be occupied are empty.
def fillable(point, available_blocks):
    fillable = 1
    for i in range(point[0][0], point[0][0] + point[1]):
        for j in range(point[0][1], point[0][1] + point[1]):
            if (i, j) not in available_blocks:
                fillable = 0
    return fillable

# Remove blocks occupied.
def remove_blocks(point, available_blocks):
    for i in range(point[0][0], point[0][0] + point[1]):
        for j in range(point[0][1], point[0][1] + point[1]):
            try:
                available_blocks.remove((i, j))
            except:
                continue

# WRITE TO PRINT STRINGS!
def fill_in_strings(string_group, font_path_group, width, height, mscd_pic):
    to_print_strings = []
    whole_steps = len(string_group)
    print(f'Find {whole_steps} strings')
    step = 0
    
    # Create available blocks list, then delete occupied ones till empty. SO COMLICATED.
    available_blocks = empty_list_blocks(width, height)
    
    while available_blocks != []:

        for string in string_group:
            if available_blocks == []:
                break
            current_fttp = r.choice(font_path_group)
            current_point = r_point(available_blocks)
            for text in string:
                if available_blocks == []:
                    break
                if not fillable(current_point, available_blocks):
                    continue
                try:
                    remove_blocks(current_point, available_blocks)
                    to_print_strings.append(
                    # Processed info added.
                    # position | font_size | content | text_color | font_path
                        current_point + [text, color(current_point[0], mscd_pic), current_fttp]
                    )
                    current_point = next_position(current_point, r_ftsz())
                except:
                    continue
            step += 1

    print('Strings filled successfully')

    return to_print_strings

def save_to_print_strings(to_print_strings, file_name):
    with open(f'./output/{file_name}.txt', 'w', encoding='utf-8') as f:
        for i in to_print_strings:
            f.write(str(i) + '\n')
    print(f'To print strings saved to ./output/{file_name}.txt')

# This one is wrong. It's just the inverse of above. But how to convent the txt file to a list?
""" def read_to_print_strings(file_name):
    to_print_strings = []
    with open(f'./output/{file_name}.txt', 'r', encoding='utf-8') as f:
        to_print_strings.append(f.read())
    return to_print_strings """

# --------------------------------------------------
# PART 3: Draw then output the pictext.
# --------------------------------------------------

def draw(document, to_print_strings, overlapping=1):
    plt.figure(figsize=(width/10, height/10))
    plt.axis('off')
    plt.plot(np.linspace(0, width, 2), np.linspace(0, height, 2), linestyle='none')
    try:
        for position, font_size, content, text_color, font_path in to_print_strings:
            current_fttp = matplotlib.font_manager.FontProperties(fname=font_path)
            plt.text(position[0], position[1],
                content, fontsize=font_size * 6 * overlapping, color=text_color, fontproperties=current_fttp)
        plt.savefig(f'./output/{document}.pdf', dpi=10)
        print('PDF file saved successfully')
    except Exception as e:
        print(f'ERROR: {e}')

# --------------------------------------------------
# Program runs here.
# --------------------------------------------------

img_path = './input/moon.jpg'
string_group = divide_passage('./input/passage.txt')
font_path_group = font_group('./font')

width, height = acquire_gird_size(20000)
ftsz_m, ftsz_M = 1, 4
mscd_pic = msc_pic(20000)

to_print_strings = fill_in_strings(string_group, font_path_group, width, height, mscd_pic)
save_to_print_strings(to_print_strings, 'to_print_strings')

draw('test', to_print_strings, overlapping=1)