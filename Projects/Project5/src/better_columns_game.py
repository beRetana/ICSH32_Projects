# better_columns_game.py

import pygame
import columns_game
import visuals
import random
from cell import Cell, Location
from gem import Gem, GemState


_FRAME_RATE = 60
_INITIAL_WINDOW_SIZE = (860, 540)
_BACKGROUND_COLOR = pygame.Color(50, 50, 50)
_GRID_SIZE_LOGIC = (13, 6)
_GRID_SIZE_VISUALS = (.3, 0)
_GRID_COLOR = pygame.Color(79, 47, 117)
_TIME_DELTA = 1.5
_GAME_SPEED = 1000

class BetterColumnsGame():

    def __init__(self):

        self._game_logic = columns_game.ColumnsGame(_GRID_SIZE_LOGIC)
        self._game_logic.create_empty()
        self._running = True
        self._gem_colors = ["S", "T", "V", "W", "X", "Y", "Z"]
        self._gem_color_map = {"S": "red", "T": "blue", "V": "dark_blue", "W": "lilac",
                               "X": "gold", "Y": "green", "Z": "purple"}
        self._matches = []


    def _create_image_asset(self, image_name, location)-> visuals.ImageAsset:
        'Gathers the image assets from the folder Assets to then store them and use them as needed'

        image = pygame.image.load(f'{image_name}')

        width = image.get_width()/self._surface.get_width()
        height = image.get_height()/self._surface.get_height()

        return visuals.ImageAsset(image, width, height, location)


    def _load_images(self) -> None:
        'Loads the images necessary for the game'
        
        images_to_load = {"game_grid":"columns_game_grid.png"}
        images_to_load["game_over"] = "game_over.png"

        gem_types = ["faller", "frozen", "match", "landed"]

        for gem_type in gem_types:
            for gem_color in self._gem_colors:
                gem_color = self._gem_color_map[gem_color]
                key = f"{gem_type}_{gem_color}"
                image_name = f"{key}.png"
                images_to_load[key] = image_name

        for image_name in images_to_load:

            images_to_load[image_name] = self._create_image_asset(images_to_load[image_name], (0.0775,0.0620))

        self._visual_assets = images_to_load


    def _frac_to_pixel_width(self, frac: float) -> float:
        'Converts a value in fractions to pixels for width of the window'

        return (frac * self._surface.get_width())


    def _pixel_to_frac_width(self, pixel: float) -> float:
        'Converts a value in pixels to fractions for width of the window'

        width = self._surface.get_width()

        return (pixel/width)
    

    def _frac_to_pixel_height(self, frac: float) -> float:
        'Converts a value in fractions to pixels for the height of the window'

        return (frac * self._surface.get_height())


    def _pixel_to_frac_height(self, pixel: float) -> float:
        'Converts a value in pixels to fractions for height of the window'

        height = self._surface.get_height()

        return (pixel/height)
    

    def _frac_to_pixel_size(self, frac_x: float, frac_y: float) -> tuple[float,float]:
        'Converst two floats from fractions to pixels'

        pixel_x = self._frac_to_pixel_width(frac_x)
        pixel_y = self._frac_to_pixel_height(frac_y)

        return (pixel_x, pixel_y)


    def _pixel_to_frac_size(self, frac_x: float, frac_y: float) -> tuple[float,float]:
        'Converst two floats from pixels to fractions'
        pixel_x = self._pixel_to_frac_width(frac_x)
        pixel_y = self._pixel_to_frac_height(frac_y)

        return (pixel_x, pixel_y)


    def _create_grid_locations(self)->None:
        'Creates a 2D list with tuples of the location for each cell'

        rows = []

        base_width = _GRID_SIZE_VISUALS[0]
        base_height = 0.005
        width_intervals = 0.0297
        cell_width = 0.0415
        cell_height = 0.062
        height_intervals = 0.0139

        for row in range(_GRID_SIZE_LOGIC[0]):
            new_columns = []
            for column in range(_GRID_SIZE_LOGIC[1]):
                width = base_width + width_intervals*(column+1) + cell_width * column
                height = base_height + height_intervals * (row+1) + cell_height * row
                new_columns.append((width, height))
            rows.append(new_columns)


        self._position_grid = rows


    def _get_random_color(self)->str:
        'Returns a random color for a gem'

        random_color = random.randint(0, len(self._gem_colors)-1)

        return self._gem_colors[random_color]
        

    def _get_gem_asset(self, gem: Gem)-> visuals.ImageAsset:
        'Takes a gem and returns the right asset to use'

        color = gem.get_color()

        color_name = self._gem_color_map[color]

        state = gem.get_state()

        state_name = ""

        match state:
            case GemState.FALLER:
                state_name = "faller"
            case GemState.FALLER_LANDED:
                state_name = "landed"
            case GemState.FROZEN:
                state_name = "frozen"
            case GemState.MATCH:
                state_name = "match"

        return self._visual_assets[f"{state_name}_{color_name}"]
    

    def _draw_gems(self)->None:
        'Draws the gems in their location based on the game state'

        for row in range(_GRID_SIZE_LOGIC[0]):
            for column in range(_GRID_SIZE_LOGIC[1]):
                cell = self._game_logic.get_game_state()[row][column]

                if not cell.contains_gem():
                    continue

                image_asset = self._get_gem_asset(cell.peek_content())
                
                new_width = self._frac_to_pixel_width(image_asset.get_width())
                new_height = self._frac_to_pixel_height(image_asset.get_heigth())
                
                scaled_image_asset = pygame.transform.scale(image_asset.get_image(), (new_width, new_height))
                pos_x, pos_y = self._position_grid[row][column]
                self._surface.blit(scaled_image_asset, self._frac_to_pixel_size(pos_x, pos_y))

    def _draw_game_over(self)->None:
        'Draws the end game textbox'

        new_height = self._frac_to_pixel_height(.3)
        new_width = self._frac_to_pixel_width(.3)

        scaled_game_over_image = pygame.transform.scale(self._visual_assets["game_over"].get_image(), (new_width, new_height))

        self._surface.blit(scaled_game_over_image, (self._frac_to_pixel_size(0, .35)))
        self._surface.blit(scaled_game_over_image, (self._frac_to_pixel_size(0, 0)))
        self._surface.blit(scaled_game_over_image, (self._frac_to_pixel_size(0, .7)))


    def _redraw_screen(self)-> None:
        'Calls the events for updating visuals based on the game state'

        self._surface = pygame.display.get_surface()

        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_grid()
        self._draw_gems()

        if self._running == False:
            self._draw_game_over()

        pygame.display.flip()


    def _draw_grid(self)-> None:
        'Draws the grid of the game'
        
        new_height = self._frac_to_pixel_height(1)
        new_width = self._frac_to_pixel_width(1/2.29)

        scaled_grid_image = pygame.transform.scale(self._visual_assets["game_grid"].get_image(), (new_width, new_height))
        frac_x, frac_y = _GRID_SIZE_VISUALS
        self._surface.blit(scaled_grid_image, (self._frac_to_pixel_size(frac_x, frac_y)))


    def _resize_surface(self, size: tuple[int, int]) -> None:
        'Resizes the screen'
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _stop_game(self)-> None:
        'Closes up the game'
        self._running = not self._running

    def _cleaning_gems(self)->None:
        'Cleans the board form matched gems'

        if len(self._matches) > 2:
            self._game_logic._eliminate_cells(self._matches)
            self._game_logic.drop_frozen_gems()
            self._matches = []
            return
        else:
            self._matches = self._game_logic.check_field_matches()
            if len(self._matches) > 2:
                self._game_logic._update_matching_gems(self._matches)
                return

    def _get_random_column(self)-> int:
        'Returns the index of a column that is not full unless all columns are full'

        possible_columns = []
        
        for index in range(_GRID_SIZE_LOGIC[1]):
            if self._game_logic.is_column_full(index):
                possible_columns.append(index)

        if len(possible_columns) < 1:
            return random.randint(0,_GRID_SIZE_LOGIC[1]-1)
        else:
            return random.choice(possible_columns)

    def _dropping_faller(self)->None:
        'Drops in a faller in the designated column'

        valid = self._game_logic.drop_in_faller(Location(0,self._game_logic.get_faller_column()),
                                                self._game_logic.get_faller_index())

        self._game_logic.set_faller_index(self._game_logic.get_faller_index()-1)
                    
        if not valid:
            self._game_logic.turn_to_fallen()
            self._game_logic.fallen_to_frozen()
            self._redraw_screen()
            self._stop_game()
            

    def _spawn_faller(self)->None:
        'Creates a faller and drops it in'

        top = self._get_random_color()
        middle = self._get_random_color()
        bottom = self._get_random_color()
        self._game_logic._create_faller(top, middle, bottom)

        column = self._get_random_column()
        
        self._game_logic.set_faller_column(column)
        self._game_logic.set_faller_index(2)
                    
        self._dropping_faller()


    def _time_events(self)-> None:
        'Contains the logic for events that should happen every interval of time'
        
        if self._game_logic.is_there_faller():
            self._game_logic.turn_to_fallen()
            return


    def _game_input(self, event: pygame.event)-> None:
        'Takes in all the game input and manages it'

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            faller = self._game_logic.get_faller()
            if faller != None:
                if self._game_logic.move_left():
                    self._game_logic.set_faller_column(self._game_logic.get_faller_column()-1)
                    self._game_logic.turn_from_fallen_to_faller()

        if keys[pygame.K_RIGHT]:
            faller = self._game_logic.get_faller()
            if faller != None:
                if self._game_logic.move_right():
                    self._game_logic.set_faller_column(self._game_logic.get_faller_column()+1)
                    self._game_logic.turn_from_fallen_to_faller()

        if keys[pygame.K_SPACE]:
            self._game_logic.rotate_faller()
            self._game_logic.turn_from_fallen_to_faller()
            

    def _game_time(self, event: pygame.event)->None:
        'Keeps track of the time passage of the game and reacts accordingly'

        if event.type == self._timer_event:
            self._timer += 1
            if self._timer >= _TIME_DELTA:
                if not self._game_logic.is_there_faller():
                    if self._game_logic.is_there_fallen():
                        self._game_logic.turn_from_fallen_to_faller()
                        self._game_logic.fallen_to_frozen()
                        self_timer = 0
                        return
                    self._cleaning_gems()
                    if len(self._matches) < 3:
                        self._spawn_faller()
                else:
                    if self._game_logic.get_faller_index() >= 0:
                        self._game_logic.drop_faller_once()
                        self._dropping_faller()
                    else:
                        self._game_logic.drop_faller_once()
                        self._time_events()
                self_timer = 0


    def _game_quit(self, event: pygame.event)->None:
        'Quits the game if the player closes the window'

        if event.type == pygame.QUIT:
            self._stop_game()
            

    def _handle_events(self)-> None:
        'Calls the handlers for input, time, and game state'

        for event in pygame.event.get():
            self._game_quit(event)
            self._game_time(event)
            self._game_input(event)


    def _game_set_up(self)->None:
        'Sets up pre-requisites for the game to run'

        self._resize_surface(_INITIAL_WINDOW_SIZE)

        self.clock = pygame.time.Clock()
            
        self._surface = pygame.display.get_surface()
        self._load_images()
        self._create_grid_locations()

        self._timer_event = pygame.USEREVENT + 1

        pygame.time.set_timer(self._timer_event, _GAME_SPEED)

        self._timer = 0


    def run(self) -> None:
        'Initializes pygames and runs the gameloop of the game'
        pygame.init()

        try:

            self._game_set_up()

            while self._running:
                self.clock.tick(_FRAME_RATE)
                self._handle_events()
                self._redraw_screen()

            while not self._running:
                self.clock.tick(5)
                for event in pygame.event.get():
                    self._game_quit(event)
                self._redraw_screen()

        finally:
            
            pygame.quit()

