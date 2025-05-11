from encoder import get_info_visual
from PIL import Image, ImageDraw
import imageio
import numpy as np

def vis():
    # Get the visited points and image dimensions
    visited, img = get_info_visual()

    # Create a video writer
    video_filename = 'visualization.mp4'
    video_writer = imageio.get_writer(video_filename, fps=40)  # Adjust fps as needed

    # Create a white canvas of the same dimensions as img
    canvas_width, canvas_height = img.size  # Assuming img is a PIL Image
    canvas = Image.new('RGBA', (canvas_width, canvas_height), 'white')
    # Draw points on the canvas using small filled circles
    for point in visited:
        draw = ImageDraw.Draw(canvas)
        x, y = point
        radius = 2
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(0, 0, 0, 255))
        video_writer.append_data(np.array(canvas))

    # Close the video writer
    video_writer.close()

    print(f"Visualization video saved as {video_filename}")

# Call the function if this script is executed directly
if __name__ == "__main__":
    pass
