width=0
height=0
depth_limit=23
password = ""
def get_password(word):
    global password
    password = word
    return "password set"

def get_width(num):
    global width
    width = num
def get_height(num):
    global height
    height = num
def get_depth_limit(num):
    global depth_limit
    depth_limit = num