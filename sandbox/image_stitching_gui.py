import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import re
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from tools.image_stitching_zigzag_pattern import stitch_images

class ImageStitchingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Stitching Tool")
        self.root.geometry("800x600")

        # Variables
        self.rows = tk.StringVar(value="13")
        self.cols = tk.StringVar(value="8")
        self.h_overlap = tk.StringVar(value="300")
        self.v_overlap = tk.StringVar(value="400")
        self.filename_format = tk.StringVar(value="sequential")
        self.thumbnail_size = tk.StringVar(value="Medium: 150x150")

        self.images = []
        self.thumbnails = []

        self._create_gui()

    def _create_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Parameters frame
        params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="5")
        params_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        main_frame.columnconfigure(0, weight=1)

        # Grid parameters
        ttk.Label(params_frame, text="Rows:").grid(row=0, column=0, padx=5)
        ttk.Entry(params_frame, textvariable=self.rows, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(params_frame, text="Columns:").grid(row=0, column=2, padx=5)
        ttk.Entry(params_frame, textvariable=self.cols, width=10).grid(row=0, column=3, padx=5)

        # Overlap parameters
        ttk.Label(params_frame, text="Horizontal Overlap:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(params_frame, textvariable=self.h_overlap, width=10).grid(row=1, column=1, padx=5)

        ttk.Label(params_frame, text="Vertical Overlap:").grid(row=1, column=2, padx=5)
        ttk.Entry(params_frame, textvariable=self.v_overlap, width=10).grid(row=1, column=3, padx=5)

        # Format selection frame
        format_frame = ttk.LabelFrame(main_frame, text="Filename Format", padding="5")
        format_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Radiobutton(format_frame, text="Sequential", variable=self.filename_format,
                       value="sequential").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(format_frame, text="Row-Column", variable=self.filename_format,
                       value="row-column").pack(side=tk.LEFT, padx=20)

        # Thumbnail size selection
        size_frame = ttk.LabelFrame(main_frame, text="Thumbnail Size", padding="5")
        size_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        sizes = ["Small: 100x100", "Medium: 150x150", "Large: 200x200"]
        size_dropdown = ttk.Combobox(size_frame, textvariable=self.thumbnail_size,
                                   values=sizes, state="readonly")
        size_dropdown.pack(padx=5)
        size_dropdown.bind('<<ComboboxSelected>>', self._update_thumbnail_size)

        # Drop zone
        self.drop_frame = ttk.LabelFrame(main_frame, text="Drop Images Here", padding="10")
        self.drop_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(3, weight=1)

        # Canvas for thumbnails
        self.canvas = tk.Canvas(self.drop_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Configure drop zone
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self._handle_drop)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=10)

        ttk.Button(btn_frame, text="Clear Images", command=self._clear_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Stitch Images", command=self._stitch_images).pack(side=tk.LEFT, padx=5)

    def _handle_drop(self, event):
        files = self._parse_drop_data(event.data)
        self.images.extend([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        self._update_thumbnail_grid()

    def _parse_drop_data(self, data):
        # Parse the drop data based on OS format
        if isinstance(data, str):
            return [data]
        return data.split()

    def _update_thumbnail_grid(self):
        # Clear existing thumbnails
        for widget in self.thumbnail_grid.winfo_children():
            widget.destroy()

        # Sort images based on filename format
        self._sort_images()

        # Create new thumbnails
        size = int(self.thumbnail_size.get().split(':')[1].strip().split('x')[0])
        rows = int(self.rows.get())
        cols = int(self.cols.get())

        for idx, img_path in enumerate(self.images):
            row = idx // cols
            col = idx % cols if row % 2 == 1 else cols - (idx % cols) - 1

            # Create thumbnail
            img = Image.open(img_path)
            img.thumbnail((size, size))
            photo = ImageTk.PhotoImage(img)

            label = ttk.Label(self.thumbnail_grid, image=photo)
            label.image = photo  # Keep a reference
            label.grid(row=row, column=col, padx=2, pady=2)

    def _sort_images(self):
        if self.filename_format.get() == "sequential":
            # Extract numbers from filenames and sort
            self.images.sort(key=lambda x: int(re.findall(r'\d+', Path(x).stem)[0]))
        else:
            # Sort by row and column numbers
            def get_rc(filename):
                match = re.search(r'r(\d+)c(\d+)', Path(filename).stem)
                return (int(match.group(1)), int(match.group(2)))
            self.images.sort(key=get_rc)

    def _update_thumbnail_size(self, event=None):
        if self.images:
            self._update_thumbnail_grid()

    def _clear_images(self):
        self.images = []
        self._update_thumbnail_grid()

    def _stitch_images(self):
        if not self.images:
            tk.messagebox.showerror("Error", "No images to stitch!")
            return

        try:
            # Save image paths to temporary file
            temp_file = Path("temp_image_list.txt")
            with open(temp_file, 'w') as f:
                f.write('\n'.join(self.images))

            # Get save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
            )

            if save_path:
                # Call the stitching function
                result = stitch_images(
                    str(temp_file),
                    rows=int(self.rows.get()),
                    cols=int(self.cols.get()),
                    h_overlap=int(self.h_overlap.get()),
                    v_overlap=int(self.v_overlap.get()),
                    output_path=save_path
                )

                tk.messagebox.showinfo("Success", "Images stitched successfully!")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error during stitching: {str(e)}")
        finally:
            if temp_file.exists():
                temp_file.unlink()


def main():
    # Initialize TkinterDnD
    root = TkinterDnD.Tk()
    app = ImageStitchingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
