from common import get_seeded_neighbors

def update_pixels(x, y,pixels, data_index, enc_msg):
    r, g, b,a = pixels[x, y]
    r = (r & ~3) | int(enc_msg[data_index:data_index+2])
    data_index+=2
    g = (g & ~3) | int(enc_msg[data_index:data_index+2])
    data_index+=2
    b = (b & ~3) | int(enc_msg[data_index:data_index+2])
    data_index+=2
    a = (a & ~3) | int(enc_msg[data_index:data_index+2])
    data_index+=2
    pixels[x, y] = (r, g, b,a)
    return pixels[x,y]


def dfs_encryption(x, y,isStart,enc_msg, pixels, visited, path, data_index):
    from config import width,height,depth_limit
    if ((x, y) in visited and isStart) or len(path) >= depth_limit or data_index >= len(enc_msg):
        return data_index
    visited.add((x, y))
    path.append((x, y))
    pixels[x,y] = update_pixels(x, y,pixels, data_index, enc_msg)
    data_index+=8
    for nx, ny in get_seeded_neighbors(x, y, width, height):
        if (nx, ny) not in visited:
            data_index = dfs_encryption(nx, ny, True,enc_msg, pixels, visited, path, data_index)
    path.pop()
    return data_index