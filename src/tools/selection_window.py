import pygame

from pathlib import Path
from tkinter import filedialog

from . import drawing_area, timeline

allowed_imagefiles =  [".jpeg", ".jpg", ".png"]

class Image:
    def __init__(self) -> None:
        self.img = None
        self.img_rect = None

        self.image = [pygame.image.load(
            "img/pen.png"), pygame.image.load("img/pen_selected.png")]

    def start(self):
        filepath = Path(open_file_dialog())
        if filepath.suffix in allowed_imagefiles:
            self.img = pygame.image.load(filepath).convert_alpha()
            print(filepath)

        else:
            print("invalid file type selected\nSelect from the following", allowed_imagefiles)
            return
        
        self.img_rect = pygame.Rect(0, 0, drawing_area.width//2, drawing_area.height//2)
        self.img_rect.center = (drawing_area.width//2, drawing_area.height//2)

        self.img = pygame.transform.scale(self.img, self.img_rect.size)
        
        drawing_area.area.blit(self.img, self.img_rect)




def open_file_dialog():
    filename = filedialog.askopenfilename()
    return filename

