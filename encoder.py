import numpy as np
from PIL import Image
import os
from common import message_to_binary,encode_number ,generate_starting_points , binary_to_hex
from main_encrypt import dfs_encryption
from config import get_depth_limit, get_height, get_width, get_password
from ordered_set import OrderedSet

visited = OrderedSet()
img = ""

def get_Password(image_path, keyword, prime_number, random_number):
    """
    Generates a password based on the provided parameters.
    
    Args:
        image_path (str): Path to the input image
        keyword (str): User-provided keyword
        prime_number (int): Prime number chosen by user (19, 23, or 29)
        random_number (int): Random number less than 1000
        secret_message (str): The message to hide in the image
        
    Returns:
        str: Generated password
    """
    # Generate a password based on inputs
    # In a real implementation, this would be much more secure
    global img
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    get_width(width)
    get_height(height)
    get_depth_limit(prime_number)
    get_password(keyword)
    while len(keyword) <15:
        keyword += "@"
    if len(keyword) >15:
        keyword = keyword[:15]

    start_points = generate_starting_points(width,height,random_number,50)
    start = start_points[0]

    My_password = encode_number(width) + encode_number(height)+ encode_number(prime_number)+ encode_number(start[0]) + encode_number(start[1])+ encode_number(random_number)+ message_to_binary(keyword)+"11111111111111111111111111111111"
    return binary_to_hex(My_password)

def encrypt_image(image_path, random_number,secret_message,output_path):
    global visited
    print(f"encrypt_image called with: image_path={image_path}, random_number={random_number}")
    print(f"secret_message length: {len(secret_message)}, output_path: {output_path}")
    try:
        # Your existing code...
        img = Image.open(image_path).convert("RGBA")
        pixels = img.load()
        width, height = img.size
        start_points = generate_starting_points(width,height,random_number,50)
        print("Message Length",len(secret_message))
        for coordinate in start_points:
            visited.add(coordinate)
        path = []
        enc_msg = message_to_binary(secret_message)
        i =0
        data_index = 0
        while True:
            start_x, start_y = start_points[i]
            next_start_x, next_start_y = start_points[i+1]
            next_point_binary = encode_number(next_start_x) + encode_number(next_start_y)
            enc_msg = enc_msg[:data_index]+next_point_binary+enc_msg[data_index:]
            data_index = dfs_encryption(start_x, start_y,False,enc_msg, pixels, visited, path, data_index)
            if data_index >= len(enc_msg):
                break
            i+=1

        # At the end, before returning:
        print(f"Saving image to {output_path}")
        img.save(output_path)
        
        # Verify the file was saved
        if os.path.exists(output_path):
            print(f"File saved successfully: {os.path.getsize(output_path)} bytes")
        else:
            print("WARNING: File was not saved!")
            
        return output_path
    except Exception as e:
        print(f"Exception in encrypt_image: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise     
   
def get_info_visual():
    global visited, img
    return visited, img
