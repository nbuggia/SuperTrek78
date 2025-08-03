# ascii_rend.py
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ #
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ #
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                                                          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ #
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    █████╗ ███████╗ ██████╗██╗██╗    ██████╗ ███████╗███╗   ██╗██████╗    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ #
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ██╔══██╗██╔════╝██╔════╝██║██║    ██╔══██╗██╔════╝████╗  ██║██╔══██╗   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ #
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ███████║███████╗██║     ██║██║    ██████╔╝█████╗  ██╔██╗ ██║██║  ██║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ #
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ██╔══██║╚════██║██║     ██║██║    ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ #
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ██║  ██║███████║╚██████╗██║██║    ██║  ██║███████╗██║ ╚████║██████╔╝   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ #
# █████████████████████████   ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝    █████████████████ #
# ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ #
# ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ #
# MiniWi font: https://patorjk.com/software/taag/#p=display&v=3&f=miniwi&t=__build_char_map

import pygame
from typing import Dict, List, Tuple


class AsciiRend:
    COLOR_RED = (255, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_FG1 = (150, 150, 150)
    COLOR_FG2 = (50, 50, 50)
    COLOR_FG3 = (25, 25, 25)
    COLOR_BG = (0, 0, 0)

    # ---------------------------------------------------------------------------------------------------------------- #
    #     ▘  ▘▗     ▗▘▝▖
    #     ▌▛▌▌▜▘    ▐  ▌
    # ▄▖▄▖▌▌▌▌▐▖▄▖▄▖▐  ▌
    #               ▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

    def __init__(self, tile_size: int, tileset_path: str) -> None:
        self.tile_size = tile_size
        self.char_to_tile: Dict[str, pygame.Surface] = {}
        self.tile_set: List[pygame.Surface] = self.__load_tileset(tile_size=tile_size, tileset_path=tileset_path)

    # ---------------------------------------------------------------------------------------------------------------- #
    #     ▌   ▘▜  ▌    ▌              ▗▘▝▖
    #     ▛▌▌▌▌▐ ▛▌  ▛▘▛▌▀▌▛▘  ▛▛▌▀▌▛▌▐  ▌
    # ▄▖▄▖▙▌▙▌▌▐▖▙▌▄▖▙▖▌▌█▌▌ ▄▖▌▌▌█▌▙▌▐  ▌
    #                               ▌ ▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

    # CP437 includes 256 characters: map byte index (0–255) to surface
    def __build_char_map(self, tile_set: List[pygame.Surface]) -> Dict[int, pygame.Surface]:
        return {i: tile_set[i] for i in range(256)}

    # ---------------------------------------------------------------------------------------------------------------- #
    #     ▜      ▌  ▗ ▘▜       ▗ ▗▘▝▖
    #     ▐ ▛▌▀▌▛▌  ▜▘▌▐ █▌▛▘█▌▜▘▐  ▌
    # ▄▖▄▖▐▖▙▌█▌▙▌▄▖▐▖▌▐▖▙▖▄▌▙▖▐▖▐  ▌
    #                            ▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

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
    
    # ---------------------------------------------------------------------------------------------------------------- #
    #      ▌ ▌   ▌    ▗   ▘    ▗▘▝▖
    # ▛▌▀▌▛▌▛▌█▌▛▌  ▛▘▜▘▛▘▌▛▌▛▌▐  ▌
    # ▙▌█▌▙▌▙▌▙▖▙▌▄▖▄▌▐▖▌ ▌▌▌▙▌▐  ▌
    # ▌                      ▄▌▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

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
        
    # ---------------------------------------------------------------------------------------------------------------- #
    #      ▌ ▌   ▌    ▗   ▘    ▗▘▝▖
    # ▛▌▀▌▛▌▛▌█▌▛▌  ▛▘▜▘▛▘▌▛▌▛▌▐  ▌
    # ▙▌█▌▙▌▙▌▙▖▙▌▄▖▄▌▐▖▌ ▌▌▌▙▌▐  ▌
    # ▌                      ▄▌▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

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

    # ---------------------------------------------------------------------------------------------------------------- #
    #      ▌ ▌   ▌    ▗   ▘    ▗▘▝▖
    # ▛▌▀▌▛▌▛▌█▌▛▌  ▛▘▜▘▛▘▌▛▌▛▌▐  ▌
    # ▙▌█▌▙▌▙▌▙▖▙▌▄▖▄▌▐▖▌ ▌▌▌▙▌▐  ▌
    # ▌                      ▄▌▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #

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


    # ---------------------------------------------------------------------------------------------------------------- #
    #      ▌ ▌   ▌    ▗   ▘    ▗▘▝▖
    # ▛▌▀▌▛▌▛▌█▌▛▌  ▛▘▜▘▛▘▌▛▌▛▌▐  ▌
    # ▙▌█▌▙▌▙▌▙▖▙▌▄▖▄▌▐▖▌ ▌▌▌▙▌▐  ▌
    # ▌                      ▄▌▝▖▗▘
    # ---------------------------------------------------------------------------------------------------------------- #
