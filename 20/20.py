import argparse
from collections import namedtuple
from math import sqrt


Tile = namedtuple("Tile", ["id", "contents", "borders"])
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def main():
    tiles = parse_args()

    # Part 1
    arranged_tiles = arrange_tiles(tiles)
    corner_value = multiply_corner_values(arranged_tiles)
    print(f"Corner value: {corner_value}")

    # Part 2
    image = image_from_tiles(arranged_tiles)
    water_roughness = calculate_water_roughness(image)
    print(f"Roughness level: {water_roughness}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    tiles = parse_tiles(open(args.input_file).read().strip().split("\n\n"))
    return tiles


def parse_tiles(lines):
    tiles = dict()
    for l in lines:
        tile = parse_tile(l)
        tiles[tile.id] = tile
    return tiles


def parse_tile(s):
    id_line, raw_contents = s.split(":\n")
    id = int(id_line.split(" ")[1])
    content_lines = raw_contents.split("\n")
    contents = ["".join(c for c in l[1:-1]) for l in content_lines[1:-1]]
    # Following the border clockwise allows easier manipulation and comparison later
    north_border = content_lines[0]
    south_border = rev_str(content_lines[-1])
    east_border = "".join(content_lines[i][-1] for i in range(len(content_lines)))
    west_border = "".join(content_lines[i][0] for i in reversed(range(len(content_lines))))
    return Tile(id, contents, [north_border, east_border, south_border, west_border])


# Use this to verify the input has unique borders between correct tile pairs
def count_borders(tiles):
    borders = dict()
    for t in tiles.values():
        for b in t.borders:
            b_reverse = rev_str(reversed(b))
            if b_reverse in borders:
                borders[b_reverse] += 1
            elif b in borders:
                borders[b] += 1
            else:
                borders[b] = 1
    return borders


def arrange_tiles(tiles):
    image = []
    remaining_tiles = dict(tiles)
    image_width = int(sqrt(len(tiles)))

    next_tile_down = find_top_left_corner_piece(tiles)
    first_column = []
    for _ in range(image_width):
        first_column.append(next_tile_down)
        remaining_tiles.pop(next_tile_down.id)
        next_tile_down = find_tile_with_border(rev_str(next_tile_down.borders[SOUTH]), NORTH, remaining_tiles.values())
    for first_tile in first_column:
        row = [first_tile]
        for x in range(1, image_width):
            next_tile_across = find_tile_with_border(rev_str(row[x - 1].borders[EAST]), WEST, remaining_tiles.values())
            remaining_tiles.pop(next_tile_across.id)
            row.append(next_tile_across)
        image.append(row)
    return image


def find_top_left_corner_piece(tiles):
    for tile in tiles.values():
        get_other_tiles = lambda: (tiles[id] for id in tiles if id != tile.id)
        missing_north = find_tile_with_border(tile.borders[NORTH], SOUTH, get_other_tiles()) is None
        missing_east = find_tile_with_border(tile.borders[EAST], WEST, get_other_tiles()) is None
        missing_south = find_tile_with_border(tile.borders[SOUTH], NORTH, get_other_tiles()) is None
        missing_west = find_tile_with_border(tile.borders[WEST], EAST, get_other_tiles()) is None
        if missing_west and missing_north:
            return tile
        if missing_north and missing_east:
            return rotate_anticlockwise(tile)
        if missing_east and missing_south:
            return rotate_180(tile)
        if missing_south and missing_west:
            return rotate_clockwise(tile)
    raise Exception(f"Couldn't find a potential top-left corner piece")


def find_tile_with_border(target_border, target_direction, tiles_list):
    for tile in tiles_list:
        for border_direction, border in enumerate(tile.borders):
            direction_difference = (target_direction - border_direction) % 4
            if border == target_border:
                if direction_difference == 0:
                    return tile
                elif direction_difference == 1:
                    return rotate_clockwise(tile)
                elif direction_difference == 2:
                    return rotate_180(tile)
                elif direction_difference == 3:
                    return rotate_anticlockwise(tile)
            elif border == rev_str(target_border):
                rotated_tile = tile
                if direction_difference == 1:
                    rotated_tile = rotate_clockwise(tile)
                elif direction_difference == 2:
                    rotated_tile = rotate_180(tile)
                elif direction_difference == 3:
                    rotated_tile = rotate_anticlockwise(tile)
                if target_direction == NORTH or target_direction == SOUTH:
                    return flip_vertical(rotated_tile)
                else:
                    return flip_horizontal(rotated_tile)
    return None


def image_from_tiles(arranged_tiles):
    image = []
    for tile_row in arranged_tiles:
        for y in range(len(tile_row[0].contents)):
            image.append("".join(t.contents[y] for t in tile_row))
    return image


def calculate_water_roughness(image):
    sea_monster_count = count_sea_monsters_with_transforms(image)
    # Assume that there won't ever be 2 overlapping sea monsters
    return sum(1 if c == "#" else 0 for l in image for c in l) - 15 * sea_monster_count


def count_sea_monsters_with_transforms(image):
    return max(count_sea_monsters(image),
               count_sea_monsters(rotate_image_clockwise(image)),
               count_sea_monsters(rotate_image_anticlockwise(image)),
               count_sea_monsters(rotate_image_180(image)),
               count_sea_monsters(flip_image_horizontal(image)),
               count_sea_monsters(rotate_image_clockwise(flip_image_horizontal(image))),
               count_sea_monsters(rotate_image_anticlockwise(flip_image_horizontal(image))),
               count_sea_monsters(rotate_image_180(flip_image_horizontal(image))),
               count_sea_monsters(flip_image_vertical(image)),
               count_sea_monsters(rotate_image_clockwise(flip_image_vertical(image))),
               count_sea_monsters(rotate_image_anticlockwise(flip_image_vertical(image))),
               count_sea_monsters(rotate_image_180(flip_image_vertical(image))))


"""
Sea Monster:
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
01234567890123456789
"""
def count_sea_monsters(image):
    count = 0
    for y in range(len(image) - 2):
        for x in range(len(image[y]) - 19):
            if image[x][y + 1] == '#' \
                    and image[x + 1][y + 2] == '#' \
                    and image[x + 4][y + 2] == '#' \
                    and image[x + 5][y + 1] == '#' \
                    and image[x + 6][y + 1] == '#' \
                    and image[x + 7][y + 2] == '#' \
                    and image[x + 10][y + 2] == '#' \
                    and image[x + 11][y + 1] == '#' \
                    and image[x + 12][y + 1] == '#' \
                    and image[x + 13][y + 2] == '#' \
                    and image[x + 16][y + 2] == '#' \
                    and image[x + 17][y + 1] == '#' \
                    and image[x + 18][y] == '#' \
                    and image[x + 18][y + 1] == '#' \
                    and image[x + 19][y + 1] == '#':
                count += 1
    return count


def rotate_clockwise(tile):
    contents = rotate_image_clockwise(tile.contents)
    borders = [tile.borders[WEST], tile.borders[NORTH], tile.borders[EAST], tile.borders[SOUTH]]
    return Tile(tile.id, contents, borders)


def rotate_image_clockwise(image):
    return ["".join(image[y][x] for y in reversed(range(len(image)))) for x in range(len(image[0]))]


def rotate_anticlockwise(tile):
    contents = rotate_image_anticlockwise(tile.contents)
    borders = [tile.borders[EAST], tile.borders[SOUTH], tile.borders[WEST], tile.borders[NORTH]]
    return Tile(tile.id, contents, borders)


def rotate_image_anticlockwise(image):
    return ["".join(image[y][x] for y in range(len(image))) for x in reversed(range(len(image[0])))]


def rotate_180(tile):
    contents = rotate_image_180(tile.contents)
    borders = [tile.borders[SOUTH], tile.borders[WEST], tile.borders[NORTH], tile.borders[EAST]]
    return Tile(tile.id, contents, borders)


def rotate_image_180(image):
    return ["".join(image[y][x] for x in reversed(range(len(image[0])))) for y in reversed(range(len(image)))]


def flip_horizontal(tile):
    contents = flip_image_horizontal(tile.contents)
    borders = [rev_str(tile.borders[SOUTH]), rev_str(tile.borders[EAST]), rev_str(tile.borders[NORTH]), rev_str(tile.borders[WEST])]
    return Tile(tile.id, contents, borders)


def flip_image_horizontal(image):
    return ["".join(image[y][x] for x in range(len(image[y]))) for y in reversed(range(len(image)))]


def flip_vertical(tile):
    contents = flip_image_vertical(tile.contents)
    borders = [rev_str(tile.borders[NORTH]), rev_str(tile.borders[WEST]), rev_str(tile.borders[SOUTH]), rev_str(tile.borders[EAST])]
    return Tile(tile.id, contents, borders)


def flip_image_vertical(image):
    return ["".join(image[y][x] for x in reversed(range(len(image[y])))) for y in range(len(image))]


def multiply_corner_values(tiles):
    return tiles[0][0].id * tiles[0][-1].id * tiles[-1][0].id * tiles[-1][-1].id


def rev_str(s):
    return "".join(reversed(s))


if __name__ == "__main__":
    main()
