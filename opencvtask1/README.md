# Image Editor Pro

A powerful, interactive web-based image editing application built with Streamlit. Upload an image and apply real-time filters, adjustments, and effects with a sleek side-panel interface for seamless editing and comparison.

## Tools Used

- **Streamlit** - Interactive web app framework
- **OpenCV (cv2)** - Image processing and computer vision library
- **PIL (Pillow)** - Python Imaging Library for image handling
- **NumPy** - Numerical computing for image arrays
- **streamlit-image_comparison** - Side-by-side image comparison component

## Features

- **Image Upload** - Drag & drop or browse to upload images
- **Real-time Resize** - Custom width/height controls (default 700x700)
- **Color Filters** - Original, Grayscale, Blur options
- **Warm/Cool Balance** - RGB temperature adjustment slider
- **Brightness/Contrast** - Fine-tune exposure and detail
- **Blur Effects** - Configurable Gaussian blur levels
- **Sharpen Effects** - Enhance edges and details
- **Edge Detection** - Laplacian edge highlighting
- **Interactive Comparison** - Slider-based before/after view
- **Download Edited Image** - Save processed output as PNG

## Steps to Run

1. **Clone/Download** the project
2. **Install dependencies**:
   ```bash
   pip install streamlit opencv-python pillow numpy streamlit-image_comparison


3. **Save your code as app.py**

4. **Run the app:**

   ```bash
   streamlit run app.py

5. **Open http://localhost:8501 in your browser**
