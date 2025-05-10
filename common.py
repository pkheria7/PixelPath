import hashlib
import random
import base64

# Shared directions
directions = [(-3, -3), (-3, 0), (-3, 3),
              (0, -3),         (0, 3),
              (3, -3),  (3, 0), (3, 3)]
def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message) + '11111111'

def binary_to_message(mess_convert):
    message = ""
    flag = False
    for i in range(0, len(mess_convert), 8):
        byte = mess_convert[i:i+8]
        if byte == '11111111':
            flag = True
            break
        message += chr(int(byte, 2))
    return message, flag

def get_neighbors(x, y, width, height):
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    return neighbors

def get_seeded_neighbors(x, y, width, height):
    from config import password
    neighbors = get_neighbors(x, y, width, height)
    seed_input = f"{x}-{y}-{password}"
    seed = int(hashlib.sha256(seed_input.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    rng.shuffle(neighbors)
    return neighbors

def encode_number(num):
    bin_num = format(num, '012b')
    first_6 = bin_num[:6]
    second_6 = bin_num[6:]
    encoded = '00' + first_6 + '00' + second_6
    return encoded 

def decode_number(encoded):

    first_6 = encoded[2:8]
    second_6 = encoded[10:16]
    full_bin = first_6 + second_6
    num = int(full_bin, 2)
    return num


def generate_starting_points(width , height ,seedValue,margin):
    random.seed(seedValue)
    all_points = [(x, y) for x in range(margin+10, width - (margin+50),61) for y in range(margin +10, height - (margin+50),61)]
    random.shuffle(all_points)
    return all_points

def binary_to_hex(binary_string):
    """Compress a 256-bit binary string into ~43-44 character Base64 string."""
    byte_data = int(binary_string, 2).to_bytes(32, byteorder='big')  # 256 bits = 32 bytes
    encoded = base64.urlsafe_b64encode(byte_data).decode('utf-8')
    return encoded  # Remove padding '=' to make it even shorter

def hex_to_binary(encoded_string):
    """Expand the Base64 encoded short password back into 256-bit binary string."""
    padded = encoded_string
    byte_data = base64.urlsafe_b64decode(padded)
    return bin(int.from_bytes(byte_data, byteorder='big'))[2:].zfill(256)