import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import functools
import logging

log = logging.getLogger(__name__)
newline = "\n"


class ImageBrowser:
    def __init__(self, image_lists: list[list[Path]]):
        self.image_lists: list[list[Path]] = image_lists
        self.current_list_index = 0
        self.available_images = {}
        self.selected_images = {}
        self.images = set()

        # create the main window
        self.root = tk.Tk()
        self.root.title("Image Browser")

        self.button_frame_1 = tk.Frame(self.root)

        self.button_frame_2 = tk.Frame(self.root)

        self.button_frame_3 = tk.Frame(self.root)

        # create the image display area
        self.image_canvas = tk.Canvas(self.root, width=500, height=500)
        self.image_canvas.pack(side=tk.TOP)

        self.on_close = lambda: log.info("Exiting Script!")

        # display the first list of images
        self.display_images()

        # start the main loop
        try:
            self.root.mainloop()

        except KeyboardInterrupt:
            self.on_close()
            exit()

    def render_widgets(self):
        log.debug("Rendering widgets")
        self.button_frame_1.destroy()
        self.button_frame_2.destroy()
        self.button_frame_3.destroy()

        self.button_frame_1 = tk.Frame(self.root)
        self.button_frame_2 = tk.Frame(self.root)
        self.button_frame_3 = tk.Frame(self.root)

        # create the selection and control buttons
        def on_select(event: tk.Event):
            if event.widget.curselection():
                self.delete_button.config(state=tk.NORMAL)
            else:
                self.delete_button.config(state=tk.DISABLED)

        self.select_dd = tk.Listbox(self.button_frame_1, selectmode=tk.MULTIPLE, justify="center")
        self.select_dd.bind("<<ListboxSelect>>", on_select)
        self.select_dd.pack(padx=10, pady=20)
        for label, image in self.available_images.items():
            self.select_dd.insert(tk.END, label)
            # self.select_dd.itemconfig(self.select_dd.size() - 1, image=image)

        self.delete_button = ttk.Button(
            self.button_frame_1, text="Delete", command=self.delete_images
        )
        self.delete_button.config(state=tk.DISABLED)
        self.delete_button.pack(padx=10)

        self.previous_button = ttk.Button(
            self.button_frame_2, text="<<", command=self.previous_list
        )
        self.previous_button.pack(side=tk.LEFT, padx=10)

        if self.current_list_index == 0:
            self.previous_button.config(state=tk.DISABLED)

        else:
            self.previous_button.config(state=tk.NORMAL)

        self.page_number = tk.Label(
            self.button_frame_2,
            text=f"Page {self.current_list_index + 1} of {len(self.image_lists)}",
        )
        self.page_number.pack(side=tk.LEFT, padx=10, expand=True)

        self.next_button = ttk.Button(self.button_frame_2, text=">>", command=self.next_list)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        if self.current_list_index == len(self.image_lists) - 1:
            self.next_button.config(state=tk.DISABLED)

        else:
            self.next_button.config(state=tk.NORMAL)

        self.cancel_button = ttk.Button(
            self.button_frame_3, text="Cancel", command=self.root.destroy
        )
        self.cancel_button.pack(padx=10)

        self.button_frame_3.pack(side=tk.BOTTOM, fill=tk.X)
        self.button_frame_2.pack(side=tk.BOTTOM, fill=tk.X)
        self.button_frame_1.pack(side=tk.BOTTOM, fill=tk.X)

    def display_images(self):
        # delete any existing images from the canvas
        self.image_canvas.delete("all")

        # display the images in the current list
        image_paths = self.image_lists[self.current_list_index]
        images = [ImageTk.PhotoImage(file=image_path) for image_path in image_paths]

        no_of_images = len(image_paths)

        log.debug(f"Displaying {no_of_images} images:\n{newline.join(map(str, image_paths))}")

        total_rows, last_row_cols = divmod(no_of_images, 3)
        total_rows += last_row_cols > 0

        log.debug(f"Total rows: {total_rows}, last row cols: {last_row_cols}")

        row, col = 0, 0
        max_height, max_width = functools.reduce(
            lambda x, y: (max(x[0], y[0]), max(x[1], y[1])),
            map(lambda x: (x.height(), x.width()), images),
        )

        log.debug(f"Max height: {max_height}, max width: {max_width}")

        canvas_width = max_width * min(3, max(last_row_cols, no_of_images)) + 10
        canvas_height = max_height * total_rows + 20

        log.debug(f"Canvas width: {canvas_width}, canvas height: {canvas_height}")

        for index, photo in enumerate(images):
            # calculate the x and y coordinates for the image
            y = (row * (max_height + 30) + max_height / 2) + 20

            if not row or not row == (total_rows - 1):
                x = col * (max_width + 10) + max_width / 2
            else:
                # if someday you ask me what this does, I'll tell you I don't know
                # because I really don't.
                # But it works (somewhat), so I'm not touching it.
                av_sp = canvas_width - (max_width * last_row_cols)  # available space
                x = col * (max_width + 20) + (max_width + 10) / 2 + av_sp / (last_row_cols + 1)
                # x = (canvas_width - photo.width() * last_row_cols) / 2
                # x = (canvas_width - (photo.width() * last_row_cols)) / (last_row_cols + 1)

            log.debug(f"Row: {row}, col: {col}, x: {x}, y: {y}")

            self.images.add(photo)

            image = self.image_canvas.create_image((x, y), image=photo, anchor="center")

            # Get the bounding box of the image
            image_bbox = self.image_canvas.bbox(image)

            # Calculate the position of the text
            text_x = (image_bbox[0] + image_bbox[2]) / 2
            text_y = image_bbox[1] - 10
            self.image_canvas.create_text(
                (text_x, text_y), text=f"Image # {index+1}", font=("Arial", 12), fill="red"
            )

            col += 1
            if col == 3:
                col = 0
                row += 1

            # x += image.width + 10
            # if (index + 1) % 3 == 0:
            #     y += image.height + 10
            #     x = 0

        self.image_canvas.config(width=canvas_width, height=canvas_height)
        self.image_canvas.update()

        self.available_images = {f"Image # {ind}": im for ind, im in enumerate(image_paths, 1)}

        self.render_widgets()

    def delete_images(self):
        # delete the selected images from the canvas and the image list
        for index in self.select_dd.curselection():
            item = self.select_dd.get(index)
            self.image_canvas.delete(item)
            item = self.available_images.pop(item)
            self.image_lists[self.current_list_index].remove(item)
            item.unlink()

        self.select_dd.select_clear(0, tk.END)

        if not self.image_lists[self.current_list_index]:
            self.image_lists.pop(self.current_list_index)
            return self.next_list()

        # clear the selection list and update the display
        self.display_images()

    def previous_list(self):
        self.current_list_index -= 1
        if self.current_list_index < 0:
            self.current_list_index = len(self.image_lists) - 1
        self.display_images()

    def next_list(self):
        # move to the next list of images
        self.current_list_index += 1
        if self.current_list_index >= len(self.image_lists):
            self.current_list_index = 0
        self.display_images()
