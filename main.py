#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=306s
# best ascii tile repositories: https://dwarffortresswiki.org/Tileset_repository#16x16_sb_ascii.png

import pygame
from sys import exit
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Constants
GRID_COLS = 98
GRID_ROWS = 50
TILE_SIZE = 12
SCREEN_WIDTH = GRID_COLS * TILE_SIZE
SCREEN_HEIGHT = GRID_ROWS * TILE_SIZE

GALAXY_WIDTH = 10
GALAXY_HEIGHT = 10


########################################################
# Class Sector()
########################################################


@dataclass
class Sector:
    starbases: int = 0
    enemies: int = 0
    planets: int = 0


########################################################
# Class GameState()
########################################################


class GameState:
    def __init__(self, galaxy_width: int, galaxy_height: int) -> None:
        self.current_sector: Tuple[int, int] = (0, 0)
        self.player_position: Tuple[int, int] = (5, 5)
        self.klingons_remaining: int = 3
        self.star_date: int = 0
        self.time_left: int = 0
        self.energy: int = 1000
        self.shields: int = 500
        self.galaxy_width: int = galaxy_width
        self.galaxy_height: int = galaxy_height
        self.sectors: List[List[Sector]] = self.init_sectors()
        self.game_over: bool = True

    def init_sectors(self) -> List[List[Sector]]:
        return [[Sector() for _ in range(self.galaxy_width)] for _ in range(self.galaxy_height)]

    def reset(self) -> None:
        self.__init__()  # Simple reset

    def is_game_over(self) -> bool:
        return self.game_over or self.energy <= 0

    # Add methods to update state safely:
    def move_player(self, dx: int, dy: int) -> None:
        x, y = self.player_position
        self.player_position = (x + dx, y + dy)

    def consume_energy(self, amount: int) -> None:
        self.energy = max(0, self.energy - amount)
        if self.energy == 0:
            self.game_over = True


########################################################
# Class RenderUtils()
########################################################


class RenderUtils:
    COLOR_RED = (255, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_FG1 = (150, 150, 150)
    COLOR_FG2 = (50, 50, 50)
    COLOR_FG3 = (25, 25, 25)
    COLOR_BG = (0, 0, 0)

    def __init__(self, tile_size: int, tileset_path: str) -> None:
        self.tile_size = tile_size
        self.char_to_tile: Dict[str, pygame.Surface] = {}
        self.tile_set: List[pygame.Surface] = self.__load_tileset(tile_size=tile_size, tileset_path=tileset_path)

    # CP437 includes 256 characters: map byte index (0–255) to surface
    def __build_char_map(self, tile_set: List[pygame.Surface]) -> Dict[int, pygame.Surface]:
        return {i: tile_set[i] for i in range(256)}

    # Load the tileset asset and create a list of tiles
    def __load_tileset(self, tile_size: int, tileset_path: str) -> List[pygame.Surface]:
        tileset_image = pygame.image.load(tileset_path).convert_alpha()
        rows = tileset_image.get_height() // tile_size
        cols = tileset_image.get_width() // tile_size
        tiles = []

        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                tile = tileset_image.subsurface(rect)
                tiles.append(tile)

        self.char_to_tile = self.__build_char_map(tiles)
        return tiles

    # Convert an int to a string with padding to fill a bounding box.
    # Ex. padded_string(25, 5, '0', True) = "00025"
    # Ex. padded_string(125, 5, ' ', False) = "125  "
    # Ex. error padded_string(55555, 3, ' ', True) = "999" (the number is too big to fit the space)
    def padded_string(self, number: int, fixed_length: int, padding_chr: str, is_right_aligned: bool) -> str:
        number_str: str = str(number)
        padding_str: str = ""
        padding_len: int = fixed_length - len(number_str)

        # if the padding length is negative, the number is longer than our fixed_length, then return the error string
        # Otherwise, create a padding string for the amount of space we have left
        if padding_len < 0:
            return "9" * fixed_length
        else:
            padding_str = padding_chr * padding_len

        # if right aligned, put the number string last, otherwise, put it first.
        if is_right_aligned:
            return padding_str + number_str
        else:
            return number_str + padding_str

    # Draw a single tile on the screen at the specified column and row
    def draw_tile(
        self,
        screen: pygame.Surface,
        tile: pygame.Surface,
        col: int,
        row: int,
        fg: Tuple[int, int, int],
        bg: Tuple[int, int, int],
    ) -> None:
        x = col * self.tile_size
        y = row * self.tile_size
        screen.fill(bg, pygame.Rect(x, y, self.tile_size, self.tile_size))
        tinted = tile.copy()
        tinted.fill(fg, special_flags=pygame.BLEND_MULT)
        screen.blit(tinted, (x, y))

    # Draw a string of text starting at the specified column and row
    def draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        col: int,
        row: int,
        fg: Tuple[int, int, int],
        bg: Tuple[int, int, int],
    ) -> None:
        try:
            encoded = text.encode("cp437")
        except UnicodeEncodeError as e:
            print(f"Unsupported character: {e}")
            return

        for i, byte in enumerate(encoded):
            tile = self.char_to_tile.get(byte)
            if tile:
                x = (col + i) * self.tile_size
                y = row * self.tile_size

                # Create a surface for the tile with background color
                char_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                char_surface.fill(bg)

                # Tint the character tile with the foreground color
                tinted_tile = tile.copy()
                tinted_tile.fill(fg, special_flags=pygame.BLEND_RGBA_MULT)

                # Blit tinted tile onto char_surface, then onto the main surface
                char_surface.blit(tinted_tile, (0, 0))
                screen.blit(char_surface, (x, y))


########################################################
# Class StatusDisplay()
# Represents the status of the game
########################################################


class StatusDisplay:

    def __init__(self, start_row: int, state: GameState, renderer: RenderUtils):
        self.start_row = start_row
        self.state = state
        self.renderer = renderer

    # Placeholder for drawing the map on the screen
    def draw(self, screen: pygame.Surface):
        self.renderer.draw_text(
            screen,
            "╔══════════════════════════════════════ SUPER TREK 78 ═════════════════════════════════════════╗",
            1,
            self.start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "║                                                                                              ║",
            1,
            self.start_row + 1,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        star_date: str = "░░░░░░░"
        time_left: str = "░░░"
        klingons: str = "░░"
        if self.state.is_game_over() != True:
            star_date = self.renderer.padded_string(self.state.star_date, 7, " ", False)
            time_left = self.renderer.padded_string(self.state.time_left, 3, " ", False)
            klingons = self.renderer.padded_string(self.state.klingons_remaining, 2, " ", False)

        self.renderer.draw_text(
            screen,
            f"║       Star date: {star_date}             Time left: {time_left} days             Klingons: {klingons}            ║",
            1,
            self.start_row + 2,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "║                                                                                              ║",
            1,
            self.start_row + 3,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )


########################################################
# Class GalaxyMap()
# Represents the galaxy map in the Super Trek 78 game
########################################################


class GalaxyMap:

    def __init__(self, start_row: int, galaxy_width: int, galaxy_height: int, state: GameState, renderer: RenderUtils):
        self.start_row = start_row
        self.galaxy_width = galaxy_width
        self.galaxy_height = galaxy_height
        self.state = state
        self.renderer = renderer

    # Placeholder for map generation logic
    def generate_map(self):
        pass

    # Draw a single sector in the map
    def __draw_sector(self, screen: pygame.Surface, start_row: int, start_col: int, sector: Sector):
        self.renderer.draw_text(
            screen,
            "░░░░░",
            start_col,
            start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

    # Placeholder for drawing the map on the screen
    # We use "start_row" to keep track of which row we are drawing
    def draw(self, screen: pygame.Surface):
        self.renderer.draw_text(
            screen,
            "╠═══════════════════════════════════════ Galaxy [M]ap ═════════════════════════════════════════╣",
            1,
            self.start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "║        1        2        3        4        5        6        7        8        9       10    ║",
            1,
            self.start_row + 1,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        # Iterate through the sectors, one row at a time. y = row number
        for y in range(self.state.galaxy_height):
            if y + 1 < 10:
                # right justify numbers less than 10
                self.renderer.draw_text(
                    screen,
                    f"║   {y+1}                                                                                          ║",
                    1,
                    self.start_row + y + 2,
                    self.renderer.COLOR_FG1,
                    self.renderer.COLOR_BG,
                )
            else:
                self.renderer.draw_text(
                    screen,
                    f"║  {y+1}                                                                                          ║",
                    1,
                    self.start_row + y + 2,
                    self.renderer.COLOR_FG1,
                    self.renderer.COLOR_BG,
                )

            # Within the row, draw the state of each sector
            row = self.start_row + y + 2
            for x in range(self.state.galaxy_width):
                sector = self.state.sectors[y][x]
                col = 8 + (x * 9)
                self.__draw_sector(screen, row, col, sector)

        self.renderer.draw_text(
            screen,
            "╚══════════════════════════════════════════════════════════════════════════════════════════════╝",
            1,
            self.start_row + 11,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )



########################################################
# Class ShipStatus()
########################################################


# Represents the status of the game
class ShipStatus:

    def __init__(self, start_row: int, state: GameState, renderer: RenderUtils):
        self.start_row = start_row
        self.state = state
        self.renderer = renderer

    # Placeholder for drawing the map on the screen
    def draw(self, screen: pygame.Surface):
        self.renderer.draw_text(
            screen,
            "Condition: [Green]",
            1,
            self.start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "Energy: 1,000 Units",
            1,
            self.start_row + 2,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "||||||||||||||||||||",
            1,
            self.start_row + 3,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "Shields: <84%>",
            1,
            self.start_row + 5,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "F:|||| A:|||| P:|||| S:||||",
            1,
            self.start_row + 6,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "[C]loak: [OFF] <100%>",
            1,
            self.start_row + 8,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "[W]arp drive: 5  <100%>",
            1,
            self.start_row + 10,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "Computer: <100%>",
            1,
            self.start_row + 12,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "Life support: <100%>",
            1,
            self.start_row + 13,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        self.renderer.draw_text(
            screen,
            "Subspace radio: <100%>",
            1,
            self.start_row + 14,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )


########################################################
# Class SectorMap()
# Represents the sector map
########################################################


class SectorMap:

    def __init__(self, start_row: int, state: GameState, renderer: RenderUtils):
        self.start_row = start_row
        self.state = state
        self.renderer = renderer

    # Draw a single sector in the map
    def __draw_location(self, screen: pygame.Surface, start_row: int, start_col: int):
        self.renderer.draw_text(
            screen,
            "░░░░░",
            start_col,
            start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
 
    # Placeholder for drawing the map on the screen
    # We use "start_row" to keep track of which row we are drawing
    def draw(self, screen: pygame.Surface):
        self.renderer.draw_text(
            screen,
            "   1   2   3   4   5   6   7   8   9  10",
            29,
            self.start_row,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )

        # Iterate through the sectors, one row at a time. y = row number
        for y in range(self.state.galaxy_height):
            if y + 1 < 10:
                # right justify numbers less than 10
                self.renderer.draw_text(
                    screen,
                    f"║   {y+1}                                                                                          ║",
                    1,
                    self.start_row + y + 2,
                    self.renderer.COLOR_FG1,
                    self.renderer.COLOR_BG,
                )
            else:
                self.renderer.draw_text(
                    screen,
                    f"║  {y+1}                                                                                          ║",
                    1,
                    self.start_row + y + 2,
                    self.renderer.COLOR_FG1,
                    self.renderer.COLOR_BG,
                )

            # Within the row, draw the state of each sector
            row = self.start_row + y + 2
            for x in range(self.state.galaxy_width):
                sector = self.state.sectors[y][x]
                col = 8 + (x * 9)
                #self.__draw_sector(screen, row, col, sector)

        self.renderer.draw_text(
            screen,
            "╚══════════════════════════════════════════════════════════════════════════════════════════════╝",
            1,
            self.start_row + 11,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )


########################################################
# Class SuperTrek78()
#
# Main logic for the Super Trek 78 game
########################################################


class SuperTrek78:

    def __init__(self, tile_size: int, width: int, height: int):
        pygame.init()
        pygame.display.set_caption("Super Trek 78")
        pygame.display.set_icon(pygame.image.load("assets/app_icon.png"))
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode((width, height))
        self.game_state = GameState(GALAXY_WIDTH, GALAXY_HEIGHT)
        self.renderer = RenderUtils(tile_size, "assets/Nice_curses_12x12.png")
        self.status_display = StatusDisplay(1, self.game_state, self.renderer)
        self.galaxy_map = GalaxyMap(5, GALAXY_WIDTH, GALAXY_HEIGHT, self.game_state, self.renderer)
        self.ship_status = ShipStatus(19, self.game_state, self.renderer)
        self.sector_map = SectorMap(19, self.game_state, self.renderer)

    def __draw_game(self):
        self.screen.fill((0, 0, 0))
        self.status_display.draw(self.screen)
        self.galaxy_map.draw(self.screen)
        self.ship_status.draw(self.screen)
        self.sector_map.draw(self.screen)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.__draw_game()


########################################################
# main()
########################################################


def main():
    game = SuperTrek78(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()


########################################################
# run main
########################################################

if __name__ == "__main__":
    main()
