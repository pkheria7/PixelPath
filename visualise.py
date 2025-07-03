import os
import numpy as np
from PIL import Image, ImageDraw
import imageio
from encoder import get_info_visual

# Update this function in your visualise.py file
def vis(max_size=800, low_memory_mode=True, fps=30, dot_size=2, dot_color=(255, 0, 0)):
    """
    Generate a visualization showing the traversal path used to hide a message in an image.
    
    Parameters:
    -----------
    max_size : int
        Maximum dimension (width or height) for visualization
    low_memory_mode : bool
        If True, use memory-efficient processing techniques
    fps : int
        Frames per second in the output video
    dot_size : int
        Size of the dots marking the path
    dot_color : tuple
        RGB color for the path dots
    """
    print("Starting visualization generation...")
    
    # Get visited points and original image from the encoder
    visited_points, original_img = get_info_visual()
    
    if not visited_points:
        print("No path data available for visualization")
        return
    
    print(f"Received {len(visited_points)} path points for visualization")
    
    # Ensure the image is in RGB format
    if original_img.mode != "RGB":
        original_img = original_img.convert("RGB")
    
    # Resize image if it's too large and low_memory_mode is enabled
    canvas_width, canvas_height = original_img.size
    if low_memory_mode and (canvas_width > max_size or canvas_height > max_size):
        # Calculate new dimensions while preserving aspect ratio
        if canvas_width > canvas_height:
            new_width = max_size
            new_height = int(canvas_height * (max_size / canvas_width))
        else:
            new_height = max_size
            new_width = int(canvas_width * (max_size / canvas_height))
        
        print(f"Resizing image from {canvas_width}x{canvas_height} to {new_width}x{new_height} to conserve memory")
        original_img = original_img.resize((new_width, new_height), Image.LANCZOS)
        
        # Also scale down the coordinates
        scale_x = new_width / canvas_width
        scale_y = new_height / canvas_height
        visited_points = [(int(x * scale_x), int(y * scale_y)) for x, y in visited_points]
    
    # Create canvas for drawing
    canvas = original_img.copy()
    
    # In low memory mode, we'll sample points to reduce frame count
    if low_memory_mode and len(visited_points) > 1000:
        # Sample a subset of points to reduce memory usage
        sample_rate = max(1, len(visited_points) // 1000)
        visited_points = visited_points[::sample_rate]
        print(f"Sampling points at rate 1:{sample_rate} for memory efficiency - using {len(visited_points)} points")
    
    # Initialize frames list
    frames = []
    
    # Calculate how many points to include per frame to keep video length reasonable
    points_per_frame = max(1, len(visited_points) // min(len(visited_points), 300))
    
    # Generate frames showing the path progression
    print("Generating video frames...")
    for i in range(0, len(visited_points), points_per_frame):
        # Create a new frame
        frame_canvas = canvas.copy()
        frame_draw = ImageDraw.Draw(frame_canvas)
        
        # Draw all points up to current position
        for point in visited_points[:i+1]:
            x, y = point
            radius = dot_size
            frame_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=dot_color)
        
        # Convert to numpy array for imageio
        frame_array = np.array(frame_canvas)
        
        # Add frame to our list
        frames.append(frame_array)
        
        # Print progress periodically
        if i % max(1, len(visited_points) // 10) == 0:
            print(f"Creating frames: {min(100, int(100 * i / len(visited_points)))}% complete")
    
    # Save only as GIF - no MP4 attempts
    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'path_visualization.gif')
    print(f"Writing {len(frames)} frames to GIF...")
    
    try:
        imageio.mimsave(gif_path, frames, fps=fps//2)  # Lower fps for GIF to reduce size
        print(f"Visualization complete! GIF saved to: {gif_path}")
    except Exception as e:
        print(f"Error saving GIF: {str(e)}")
        return

if __name__ == "__main__":
    # When run directly, use default settings
    vis()