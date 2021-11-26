'''
https://adventofcode.com/2020/day/20
'''

from collections import namedtuple
import re
from textwrap import dedent


def main():
    tiles = load_tiles_from_file('20_input.txt')
    tiles[0].position = Position(0, 0)
    print('Start')
    while not all(tile.position for tile in tiles):
        for tile in tiles:
            if not tile.position:
                tile.find_place(tiles)
    tile_by_pos = {tile.position: tile for tile in tiles}
    for tile in tiles:
        tile.validate(tile_by_pos)
    corner_tiles = [tile.ident for tile in tiles if tile.is_corner(tile_by_pos)]
    assert len(corner_tiles) == 4
    print('Corner tiles:', corner_tiles, product(corner_tiles))

    big_picture = create_big_picture(tiles)

    print('Big picture:')
    for line in big_picture:
        print(''.join(line))

    for i in range(4):
        big_picture = rotated(big_picture)
        big_picture = mark_monster(big_picture)
        big_picture = flipped_horizontally(big_picture)
        big_picture = mark_monster(big_picture)
        big_picture = flipped_vertically(big_picture)
        big_picture = mark_monster(big_picture)
        big_picture = flipped_horizontally(big_picture)
        big_picture = mark_monster(big_picture)
        big_picture = flipped_vertically(big_picture)

    print('Big picture after marking monsters:')
    for line in big_picture:
        print(''.join(line))

    print('Roughness:', str(big_picture).count('#'))

    print('Done')


def mark_monster(big_picture):
    pattern = dedent('''\
                          #
        #    ##    ##    ###
         #  #  #  #  #  #
    ''')
    pattern = pattern.splitlines()
    for line_offset in range(0, len(big_picture)):
        for column_offset in range(0, len(big_picture[0])):
            found = True
            try:
                for pattern_line_number, pattern_line in enumerate(pattern):
                    for pattern_column_number, pattern_cell in enumerate(pattern_line):
                        if pattern_cell == '#':
                            bp_line = line_offset + pattern_line_number
                            bp_column = column_offset + pattern_column_number
                            if big_picture[bp_line][bp_column] != '#':
                                found = False
                                break
                    if not found:
                        break
            except IndexError:
                continue
            if found:
                for pattern_line_number, pattern_line in enumerate(pattern):
                    for pattern_column_number, pattern_cell in enumerate(pattern_line):
                        if pattern_cell == '#':
                            bp_line = line_offset + pattern_line_number
                            bp_column = column_offset + pattern_column_number
                            assert big_picture[bp_line][bp_column] == '#'
                            assert isinstance(big_picture[bp_line], tuple)
                            big_picture[bp_line] = list(big_picture[bp_line])
                            big_picture[bp_line][bp_column] = 'O'
                            big_picture[bp_line] = tuple(big_picture[bp_line])



    return big_picture


def create_big_picture(tiles):
    min_tile_line = min(tile.position.line for tile in tiles)
    min_tile_column = min(tile.position.column for tile in tiles)
    big_picture = []
    for tile in tiles:
        assert len(tile.lines) == 10
        for line_number, line in enumerate(tile.lines[1:-1]):
            assert len(line) == 10
            for column_number, cell in enumerate(line[1:-1]):
                big_picture_line = (-min_tile_line + tile.position.line) * 8 + line_number
                big_picture_column = (-min_tile_column + tile.position.column) * 8 + column_number
                while len(big_picture) <= big_picture_line:
                    big_picture.append([])
                while len(big_picture[big_picture_line]) <= big_picture_column:
                    big_picture[big_picture_line].append(None)
                big_picture[big_picture_line][big_picture_column] = cell
    return big_picture


def product(numbers):
    prod = 1
    for n in numbers:
        prod *= n
    return prod


def transposed(square):
    assert len(set(len(line) for line in square)) == 1
    return [tuple(x) for x in zip(*square)]


def rotated(lines):
    return flipped_horizontally(transposed(lines))


def flipped_horizontally(lines):
    return [tuple(reversed(line)) for line in lines]


def flipped_vertically(lines):
    return list(reversed(lines))


class Position (namedtuple('_Position', 'line column')):

    __slots__ = ()

    def add(self, line=0, column=0):
        return Position(self.line + line, self.column + column)


class Tile:

    def __init__(self, ident, lines):
        self.ident = ident
        self.lines = [tuple(line) for line in lines]
        self.position = None

    def __repr__(self):
        return f"{self.ident}:{'|'.join(''.join(line) for line in self.lines)}"

    def top_border(self): return self.lines[0]
    def bottom_border(self): return self.lines[-1]
    def left_border(self): return transposed(self.lines)[0]
    def right_border(self): return transposed(self.lines)[-1]


    def find_place(self, all_tiles):
        assert self.position is None
        def try_find_place():
            for tile in all_tiles:
                if tile.position:
                    if self.top_border() == tile.bottom_border():
                        self.position = tile.position.add(line=1)
                    elif self.bottom_border() == tile.top_border():
                        self.position = tile.position.add(line=-1)
                    if self.left_border() == tile.right_border():
                        self.position = tile.position.add(column=1)
                    elif self.right_border() == tile.left_border():
                        self.position = tile.position.add(column=-1)
        orig_lines = self.lines
        for i in range(4):
            self.lines = rotated(self.lines)
            try_find_place()
            if self.position:
                return
            self.lines = flipped_horizontally(self.lines)
            try_find_place()
            if self.position:
                return
            self.lines = flipped_vertically(self.lines)
            try_find_place()
            if self.position:
                return
            self.lines = flipped_horizontally(self.lines)
            try_find_place()
            if self.position:
                return
            self.lines = flipped_vertically(self.lines)
        assert self.lines == orig_lines

    def validate(self, tile_by_pos):
        top_neighbor = tile_by_pos.get(self.position.add(line=-1))
        bottom_neighbor = tile_by_pos.get(self.position.add(line=1))
        left_neighbor = tile_by_pos.get(self.position.add(column=-1))
        right_neighbor = tile_by_pos.get(self.position.add(column=1))
        assert not top_neighbor or self.top_border() == top_neighbor.bottom_border()
        assert not bottom_neighbor or self.bottom_border() == bottom_neighbor.top_border()
        assert not left_neighbor or self.left_border() == left_neighbor.right_border()
        assert not right_neighbor or self.right_border() == right_neighbor.left_border()

    def is_corner(self, tile_by_pos):
        neighbor_count = sum([
            self.position.add(line=-1) in tile_by_pos,
            self.position.add(line=1) in tile_by_pos,
            self.position.add(column=-1) in tile_by_pos,
            self.position.add(column=1) in tile_by_pos,
        ])
        assert neighbor_count in (2, 3, 4)
        return neighbor_count == 2


def load_tiles_from_file(path):
    data = open(path).read().splitlines()
    assert len(data) % 12 == 11
    tiles = []
    it = iter(data)
    while True:
        ident, = re.match(r'^Tile ([0-9]+):$', next(it)).groups()
        tiles.append(Tile(int(ident), [next(it) for i in range(10)]))
        try:
            assert next(it) == ''
        except StopIteration:
            break
    return tiles


if __name__ == '__main__':
    main()
