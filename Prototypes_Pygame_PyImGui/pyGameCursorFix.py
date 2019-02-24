import sys, pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    # Initialise screen
    pygame.init()
    size = width, height = 800, 800

    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    pygame.display.set_caption('PyGame Boilerplate')

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == KEYDOWN and event.key == K_q:
                sys.exit()
        pygame.display.flip()


if __name__ == '__main__': main()
