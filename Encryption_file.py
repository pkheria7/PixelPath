from PIL import Image ,ImageDraw
from common import message_to_binary,encode_number ,generate_starting_points , binary_to_hex
from main_encrypt import dfs_encryption
from config import get_depth_limit, get_height, get_width, get_password
import subprocess

def encrptying(start_points, message):
    pixels = img.load()
    print("Message Length",len(message))
    visited = set()
    for coordinate in start_points:
        visited.add(coordinate)
    path = []
    enc_msg = message_to_binary(message)
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

    img.save("output.png")
def get_message():
    global message
    message = input("Enter your Secret Message :\n")
    return message

if __name__ == "__main__":
    img = Image.open("image.png").convert("RGBA")
    width, height = img.size
    message = ""
    get_width(width)
    get_height(height)
    word = input("Enter a word (must not be more than 10 letters):\n")
    check_point = get_password(word)
    print(word)
    while len(word) <15:
        word += "@"
    if len(word) >15:
        word = word[:15]

    prime = int(input("choose one 19 or 23 or 29:\n"))
    get_depth_limit(prime)
    randomise_it = int(input("toggle value (enter a value less than 2000): \n"))
    message = get_message()
    while True:
        start_points = generate_starting_points(width,height,randomise_it,50)
        start = start_points[0]

        My_password = encode_number(width) + encode_number(height)+ encode_number(prime)+ encode_number(start[0]) + encode_number(start[1])+ encode_number(randomise_it)+ message_to_binary(word)+"11111111111111111111111111111111"

        encrptying(start_points, message)
        result = subprocess.run(["python", "Decryption_file.py", binary_to_hex(My_password)], capture_output=True, text=True)
        message_from_decryption = result.stdout.strip()
        if message == message_from_decryption.strip():
            print("Your Password :",binary_to_hex(My_password))
            break
        else :
            randomise_it += 1
