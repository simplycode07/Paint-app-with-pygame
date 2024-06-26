import pygame
from src import settings, tools

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")
pen = tools.Pen((0, 0, 0), 15)

running = True

display.fill((255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos = list(pygame.mouse.get_pos())
            pos[1] -= settings.ui_height
            canvas = pen.draw(pos)
            display.blit(canvas, (0, settings.ui_height))

    pygame.display.flip()


pygame.quit()
