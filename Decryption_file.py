from PIL import Image, ImageDraw
from common import binary_to_message, decode_number, generate_starting_points, hex_to_binary
from main_decrypt import dfs_decryption
from config import get_depth_limit, get_height, get_width, get_password
import random
import sys

def get_info(binary_message):
    return_lst = []
    try:
        for i in range(0, 6):
            return_lst.append(decode_number(binary_message[i * 16:(i + 1) * 16]))
        return_lst.append(binary_to_message(binary_message[96:176]))
    except Exception as e:
        print("Caught some error in get_info:", e)
    return return_lst

def decrypting(img, starting_x, starting_y):
    start_x, start_y = starting_x, starting_y
    pixels = img.load()
    visited = set()
    for i in start_points:
        visited.add(i)
    path = []
    final_message = ""
    i = 0
    
    while True:
        message_extraction = ""
        try:
            message_extraction = dfs_decryption(start_x, start_y, False, pixels, visited, path, message_extraction)
            next_x = decode_number(message_extraction[0:16])
            next_y = decode_number(message_extraction[16:32])
            donne, check = binary_to_message(message_extraction[32:])
            final_message += donne
            start_x, start_y = next_x, next_y
            if check:
                break
        except Exception as e:
            print("Caught some error in decrypting:", e)
            break  # Exit the loop on error

    return final_message

if __name__ == "__main__":
    try:
        img = Image.open("output.png").convert("RGBA")
        width, height = img.size
        get_width(width)
        get_height(height)
        
        if len(sys.argv) > 1:
            entry = sys.argv[1]
        else:
            entry = input("Enter the password:\n")
        
        info = get_info(hex_to_binary(entry))
        check_point = get_password(info[6][0].rstrip('@'))
        get_depth_limit(int(info[2]))
        start_points = generate_starting_points(width, height, int(info[5]), 50)
        random.shuffle(start_points)
        
        answer = decrypting(img, int(info[3]), int(info[4]))
        print(answer)
    except Exception as e:
        print("Caught some error in the main execution:", e)
