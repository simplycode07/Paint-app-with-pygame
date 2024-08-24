import pygame

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pathlib import Path
# from . import drawing_area, timeline

allowed_imagefiles =  [".jpeg", ".jpg", ".png"]

class Image:
    def __init__(self) -> None:
        self.img = None

    def start(self):
        filepath = Path(open_file_dialog())
        if filepath.suffix in allowed_imagefiles:
            self.img = pygame.image.load(filepath)
            print(filepath)

        else:
            print("invalid file type selected\nSelect from the following", allowed_imagefiles)


def open_file_dialog():
    Gtk.init([])

    dialog = Gtk.FileChooserDialog(
        title="Select a file",
        action=Gtk.FileChooserAction.OPEN,
    )

    dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
    dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    response = dialog.run()

    file_path = ""
    if response == Gtk.ResponseType.OK:
        file_path = dialog.get_filename()
    
    dialog.destroy()
    return file_path


