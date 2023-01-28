from character import Character
import Constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.character_list = []


    def process_data(self, data, tile_list, mob_animations):
        self.level_length = len(data)
        # go through level data file
        for y, row in enumerate(data):
            for x, tile in  enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * Constants.TILE_SIZE
                image_y = y * Constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile ==  5:
                    self.obstacle_tiles.append(tile_data)
                if tile == 9:
                    enemy = Character(image_x, image_y, 30, mob_animations, 3)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                if tile == 10:
                    enemy = Character(image_x, image_y, 70, mob_animations, 2)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]

            #image data
                if tile >= 0:
                    self.map_tiles.append(tile_data)
    
    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])