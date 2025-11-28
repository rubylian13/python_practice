import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


class WatermarkApp:
    """
    A Desktop program where you can upload images and add a watermark.
    """
    def __init__(self, window):
        """Initializes the Watermark Application GUI and state."""
        self.window = window
        self.window.title("Image Watermarking")
        self.window.geometry("800x600")

        self.image = None
        self.tk_image = None
        # Store the currently open image file path
        self.current_filepath = None

        # --- UI SETUP ---
        # Frame for controls
        control_frame = tk.Frame(window)
        control_frame.pack(pady=10)

        select_images_button = tk.Button(control_frame, text="Select Image", command=self.select_images, bg="#4CAF50",
                                         fg="white", font=('Helvetica', 10, 'bold'))
        select_images_button.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Watermark Text:", font=('Helvetica', 10)).pack(side=tk.LEFT, padx=(15, 5))
        self.watermark_text = tk.Entry(control_frame, width=30, font=('Helvetica', 10))
        self.watermark_text.insert(0, "YOUR WATERMARK")
        self.watermark_text.pack(side=tk.LEFT, padx=5)

        apply_watermark_button = tk.Button(control_frame, text="Apply Watermark", command=self.apply_watermark,
                                           bg="#2196F3", fg="white", font=('Helvetica', 10, 'bold'))
        apply_watermark_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(window, text="Save Watermarked Image As...", command=self.save_images, bg="#FF9800",
                                fg="white", font=('Helvetica', 10, 'bold'))
        save_button.pack(pady=10)

        # Canvas for image display
        self.canvas = tk.Canvas(window, width=750, height=450, bg="#E0E0E0", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(padx=10, pady=10)

    def select_images(self):
        """Opens file dialog to select a single image."""
        file = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")]
        )
        if not file:
            return

        try:
            self.current_filepath = file
            self.image = Image.open(file)
            self.show_image(self.image)
        except IOError:
            messagebox.showerror("Error", "Could not open the selected image file.")

    def show_image(self, img):
        """Resizes and displays the image on the canvas."""
        self.canvas.delete("all")  # Clear previous image

        # Calculate resize ratio
        canvas_width = 750
        canvas_height = 450
        img_width, img_height = img.size

        ratio = min(canvas_width / img_width, canvas_height / img_height)

        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        img_resized = img.copy().resize((new_width, new_height))
        self.tk_image = ImageTk.PhotoImage(img_resized)

        # Center the image on the canvas
        x_center = canvas_width // 2
        y_center = canvas_height // 2

        self.canvas.create_image(x_center, y_center, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def get_robust_font(self, size):
        """
        Attempts to load a standard system font, falling back to a default.
        This fixes the 'OSError: cannot open resource'.
        """
        try:
            # 1. Try to load 'Helvetica.ttf' directly
            return ImageFont.truetype("Helvetica.ttf", size)
        except (OSError, IOError):
            try:
                # 2. Try loading 'Helvetica' by name (often works on Windows/macOS)
                return ImageFont.truetype("Helvetica", size)
            except (OSError, IOError):
                # 3. Final fallback: Use the built-in Pillow default font
                messagebox.showwarning("Font Warning", "Could not find 'Helvetica' font. Using generic built-in font.")
                return ImageFont.load_default()

    def apply_watermark(self):
        """Applies the watermark text to the current image."""
        if self.image is None:
            messagebox.showerror("Error", "Please select an image first.")
            return

        text = self.watermark_text.get()
        if not text:
            messagebox.showwarning("Warning", "Please enter a watermarking text.")
            return

        img_copy = self.image.copy()
        draw = ImageDraw.Draw(img_copy)
        width, height = img_copy.size

        # Calculate font size relative to image height (e.g., 3% of height)
        font_size = max(20, int(height * 0.03))

        # Load font using the robust method
        font = self.get_robust_font(font_size)

        # Use modern Pillow method to get text dimensions (left, top, right, bottom)
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            # Fallback for older Pillow versions
            text_w, text_h = draw.textsize(text, font=font)

        # Position: Right-bottom corner with a 20-pixel margin
        margin = 20
        pos = (width - text_w - margin, height - text_h - margin)

        # Draw the watermark (White text with 50% opacity/alpha)
        # Note: 'fill=(R, G, B, A)' for transparency only works on PNGs or when saving to PNG
        draw.text(pos, text, font=font, fill=(255, 255, 255, 128))

        self.image = img_copy  # Update the internal image state
        self.show_image(self.image)  # Update the display

    def save_images(self):
        """Opens file dialog to save the watermarked image."""
        if self.image is None:
            messagebox.showerror("Error", "No watermarked image to save.")
            return

        # Suggest a default filename based on the original path
        initial_file = os.path.basename(self.current_filepath) if self.current_filepath else "watermarked_image"
        if '.' in initial_file:
            name, ext = initial_file.rsplit('.', 1)
            default_name = f"{name}_watermarked.{ext}"
        else:
            default_name = f"{initial_file}_watermarked.png"

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
        )

        if save_path:
            try:
                # Save the current, watermarked image
                self.image.save(save_path)
                messagebox.showinfo("Success", f"Image successfully saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving: {e}")


if __name__ == "__main__":
    window = tk.Tk()
    app = WatermarkApp(window)
    window.mainloop()