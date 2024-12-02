# spots_ui.py

import pygame
import spots

_BACKGROUND_COLOR = pygame.Color(109,24, 216)
_SPOT_COLOR = pygame.Color(131,216, 24)

class SpotsGame:
    def __init__(self):
        self._running = True
        self._state = spots.SpotsState()

        
    def run(self) -> None:
        pygame.init()

        self._resize_surface((700, 700))

        clock = pygame.time.Clock()

        while self._running:
            clock.tick(30)
            self._handle_events()
            self._redraw()

        pygame.quit()


    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button(event.pos)

        self._move_spots()


    def _redraw(self) -> None:
        surface = pygame.display.get_surface()

        surface.fill(_BACKGROUND_COLOR)
        self._draw_spots()

        pygame.display.flip()


    def _draw_spots(self) -> None:
        for spot in self._state.all_spots():
            self._draw_spot(spot)


    def _draw_spot(self, spot: spots.Spot) -> None:
        frac_x, frac_y = spot.center()
        
        topleft_frac_x = frac_x - spot.radius()
        topleft_frac_y = frac_y - spot.radius()

        frac_width = spot.radius() * 2
        frac_height = spot.radius() * 2

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        topleft_pixel_x = topleft_frac_x * width
        topleft_pixel_y = topleft_frac_y * height

        pixel_width = frac_width * width
        pixel_height = frac_height * height

        pygame.draw.ellipse(
            surface, pygame.Color(0, 0, 0),
            pygame.Rect(
                topleft_pixel_x, topleft_pixel_y,
                pixel_width, pixel_height))


    def _end_game(self) -> None:
        self._running = False
        

if __name__ == '__main__':
    SpotsGame().run()
            
                
