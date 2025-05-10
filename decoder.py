import numpy as np
from PIL import Image
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

def decrypt_image(image_path, password): 
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        get_width(width)
        get_height(height)
        
        entry = password
        
        try:
            # First try to decode the password
            info = get_info(hex_to_binary(entry))
            check_point = get_password(info[6][0].rstrip('@'))
            get_depth_limit(int(info[2]))
            start_points = generate_starting_points(width, height, int(info[5]), 50)
            random.shuffle(start_points)
            start_x, start_y = int(info[3]), int(info[4])
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
                    
                    # Check if message_extraction is valid
                    if len(message_extraction) < 32:
                        return "Invalid data extracted from image. Try a different password."
                    
                    next_x = decode_number(message_extraction[0:16])
                    next_y = decode_number(message_extraction[16:32])
                    
                    # Make sure binary_to_message returns valid text
                    donne, check = binary_to_message(message_extraction[32:])
                    
                    # Sanity check on the decoded message
                    if isinstance(donne, bytes):
                        donne = donne.decode('utf-8', errors='replace')
                    elif not isinstance(donne, str):
                        donne = str(donne)
                    
                    final_message += donne
                    start_x, start_y = next_x, next_y
                    if check:
                        break
                except UnicodeDecodeError:
                    return "The extracted data contains invalid characters. Please try another password."
                except Exception as e:
                    return f"Decryption error: Unable to extract message. {type(e).__name__}: {str(e)}"
            
            return final_message
            
        except Exception as e:
            return f"Password error: Invalid password format. {type(e).__name__}: {str(e)}"
            
    except Exception as e:
        return f"Image processing error: {type(e).__name__}: {str(e)}"

