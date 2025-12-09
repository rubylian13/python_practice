"""
A website that finds the most common colours in an uploaded image.
"""
import io
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import base64


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
NUMBER_COLORS = 10


def allowed_file(filename):
    """Checks if a filename has an allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(rgb_tuple):
    """Converts an RGB tuple (0-255) to a hexadecimal color string."""
    # Ensure values are within 0-255 range and are integers
    r = int(max(0, min(255, rgb_tuple[0])))
    g = int(max(0, min(255, rgb_tuple[1])))
    b = int(max(0, min(255, rgb_tuple[2])))
    return f'#{r:02x}{g:02x}{b:02x}'


def analyze_image_colors(image_file):
    try:
        img = Image.open(io.BytesIO(image_file.read()))
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

    max_pixels = 10000
    width, height = img.size
    aspect_ratio = width / height

    new_height = int(np.sqrt(max_pixels / aspect_ratio))
    new_width = int(new_height * aspect_ratio)

    img = img.resize((new_width, new_height))

    img = img.convert('RGB')

    # Convert image pixels into a list of RGB values
    pixels = np.array(img.getdata()).reshape(-1, 3)

    # Use K-Means clustering to find the dominant colors
    # The cluster centers will represent the dominant colors
    kmeans = KMeans(n_clusters=NUMBER_COLORS, n_init='auto', random_state=42)
    kmeans.fit(pixels)

    label_counts = Counter(kmeans.labels_)

    total_pixels = len(kmeans.labels_)

    # The cluster centers are the dominant colors (RGB values)
    colors = kmeans.cluster_centers_

    results = []
    for label, count in label_counts.most_common():
        rgb = colors[label]
        percentage = (count / total_pixels) * 100
        hex_code = rgb_to_hex(rgb)

        results.append({
            'hex': hex_code,
            'rgb': tuple(int(x) for x in rgb),
            'percentage': round(percentage, 2)
        })

    return results


@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    image_url = None
    error_message = None

    if request.method == 'POST':
        if 'image_file' not in request.files:
            error_message = "No file part in the request."

        else:
            file = request.files['image_file']

            if file.filename == '':
                error_message = "No image selected for upload."

            elif file and allowed_file(file.filename):
                file_data = file.read()

                # Create data URI for image preview in the HTML
                image_url = "data:" + file.content_type + ";base64," + base64.b64encode(file_data).decode('utf-8')

                # Use the file data for analysis
                file_stream = io.BytesIO(file_data)

                results = analyze_image_colors(file_stream)

                if results is None:
                    error_message = "Could not process the image file."

            else:
                error_message = "File type not allowed. Please upload PNG, JPG, JPEG, or GIF."

    # Render the index template with the results (if any) and image preview
    return render_template('index.html', results=results, image_url=image_url, error=error_message)


if __name__ == '__main__':
    app.run(debug=True, port=8000)