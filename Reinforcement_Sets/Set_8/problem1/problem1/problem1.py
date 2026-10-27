import pygame


def _draw_text(surface: pygame.Surface, font: pygame.font.SysFont, text: str) -> None:
    text_image = font.render(text, True, pygame.Color(255, 255, 255))
    surface.blit(text_image, (10, 10))


def _list_to_string(list_of_words: list[str])-> str:
    'Receives a list of strings and turns them into a sorted string'

    list_of_words.sort()

    word = ""

    for letter in list_of_words:
        word += letter.upper()

    return word


def run() -> None:
    pygame.init()

    try:
        surface = pygame.display.set_mode((600, 600))
        font = pygame.font.SysFont(None, 24)
        clock = pygame.time.Clock()

        running = True

        keys = ""
        key_letters = []

        while running:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    letter = f"{event.unicode}"
                    if letter.isalnum():
                        key_letters.append(letter)
                elif  event.type == pygame.KEYUP:
                    letter = f"{event.unicode}"
                    if letter.isalnum():
                        key_letters.remove(letter)

                print(event)

            keys = _list_to_string(key_letters)

            surface.fill(pygame.Color(128, 128, 128))

            _draw_text(surface, font, keys)
            
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    run()
