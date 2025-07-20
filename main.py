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
# Class RenderUtils()
########################################################


class RenderUtils:
    COLOR_RED = (255, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_FG1 = (75, 75, 75)
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
# Class Sector()
########################################################


@dataclass
class Sector:
    starbases: int = 0
    enemies: int = 0
    planets: int = 0


########################################################
# Class GalaxyMap()
########################################################


# Represents the galaxy map in the Super Trek 78 game
class GalaxyMap:

    def __init__(self, cols: int, rows: int, renderer: RenderUtils):
        self.rows = cols
        self.cols = rows
        self.renderer = renderer
        # Initialize a 2D grid of sectors
        self.sectors = [[Sector() for _ in range(self.cols)] for _ in range(self.rows)]

    # Placeholder for map generation logic
    def generate_map(self):
        pass

    # Placeholder for drawing the map on the screen
    def draw(self, screen):
        self.renderer.draw_text(
            screen,
            "╔══════════════════════════════════════ SUPER TREK 78 ═════════════════════════════════════════╗",
            1,
            1,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "║                                                                                              ║",
            1,
            2,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "║       Star date: XXXXX.X           Time left: XXX days             Klingons: XX              ║",
            1,
            3,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "║                                                                                              ║",
            1,
            4,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )
        self.renderer.draw_text(
            screen,
            "╠═══════════════════════════════════════ Galaxy [M]ap ═════════════════════════════════════════╣",
            1,
            5,
            self.renderer.COLOR_FG1,
            self.renderer.COLOR_BG,
        )



#╔═══════════════════════════════════════ SUPER TREK 78 ════════════════════════════════════════╗
#║                                                                                              ║
#║       Star date: XXXXX.X           Time left: XXX days             Klingons: XX              ║
#║                                                                                              ║
#╠═══════════════════════════════════════ Galaxy [M]ap ═════════════════════════════════════════╣


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
        self.screen = pygame.display.set_mode((width, height))
        self.renderer = RenderUtils(tile_size, "assets/Nice_curses_12x12.png")
        self.tile_size = tile_size
        self.galaxy_map = GalaxyMap(GALAXY_WIDTH, GALAXY_HEIGHT, self.renderer)

    def __draw_game(self):
        self.screen.fill((0, 0, 0))
        self.galaxy_map.draw(self.screen)

        # TODO: Delete this, just to show what all the tiles look like
        # Draw all 256 tiles in a 16x16 grid starting at top-left
        # for i in range(256):
        #    tile = self.tile_set[i]
        #    row = i // 16
        #    col = i % 16
        #    self.renderer.draw_tile(self.screen, tile, self.tile_size, col, row, (0, 255, 0), (0, 0, 0))

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
