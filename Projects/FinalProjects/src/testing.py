import pygame


def run() -> None:
    try:
        pygame.init()
        surface = pygame.display.set_mode((700, 600))

        color_amount = 0
        color_delta = 1
        clock = pygame.time.Clock()

        running  = True

        while running:

            clock.tick(30) # frame oer second
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            color_amount += color_delta

            if color_amount == 0 or color_amount == 255:
                color_delta = -color_delta

            
            surface.fill(pygame.Color(color_amount, color_amount, color_amount))

            pygame.draw.circle(surface, pygame.Color(255,255,0), (350, 300), 100)

            pygame.display.flip()
            
    finally:
        pygame.quit()


if __name__ == '__main__':
    run()
