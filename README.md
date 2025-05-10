# PixelPath - Secure Message Transmission

## Project Overview

PixelPath is a secure steganography platform that allows users to hide secret messages within images. By leveraging advanced encryption techniques, PixelPath ensures that only intended recipients can access the hidden messages, making it an ideal solution for private communications. This project combines web development with image processing to create a user-friendly interface for transmitting and receiving encoded messages.

## Features

- **Image Upload**: Users can upload images to encode secret messages.(Note that the image should be a .png file)
- **Password Generation**: A unique password is generated for each transmission based on user inputs and image properties.
- **Message Encoding**: The application encodes secret messages into the uploaded images using steganography techniques.
- **Message Decoding**: Recipients can upload the encoded images and provide the password to retrieve the hidden messages.
- **Downloadable Encoded Images**: Users can download the encoded images for sharing.

## Tech Stack

- **Flask**: A micro web framework for Python, used to build the web application.
- **Werkzeug**: A comprehensive WSGI web application library that Flask is built on.
- **Pillow (PIL)**: A Python Imaging Library used for image processing.
- **NumPy**: A library for numerical computations, used for handling image data.
- **HTML/CSS/JavaScript**: For building the front-end user interface.
- **Jinja2**: A templating engine for rendering HTML pages.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pkheria7/PixelPath.git
   cd pixelpath
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:5000`.

## Deployed

use the link `https://pixelpath.onrender.com/` and try the website yourself

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors and the open-source community for their support and resources.
