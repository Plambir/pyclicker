import random

COLOR0 = (255, 255, 255)
COLOR1 = (178, 60,  60)
COLOR2 = (134, 105, 48)
COLOR3 = (162, 60,  138)
COLOR4 = (56,  125, 101)
COLOR5 = (77,  60,  174)

WIDTH = 6
HEIGHT = 10

class Cell:
    def __init__(self, x, y):
        self.chip = None
        self.x = x
        self.y = y

    def is_life(self):
        return self.chip is not None

    def set_chip(self, chip):
        self.chip = chip

    def get_color(self):
        if not self.is_life():
            return COLOR0
        else:
            return self.chip

    def random(self, luck, neighbors):
        colors = [COLOR1, COLOR2, COLOR3, COLOR4, COLOR5]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor is None or neighbor.chip is None:
                continue
            if random.randint(1, 100) < luck:
                self.chip = neighbor.chip
                return
            if neighbor.chip in colors:
                colors.remove(neighbor.chip)
        random.shuffle(colors)
        self.chip = colors[0]


class Grid:
    def __init__(self):
        self.grid = [[Cell(x, y) for y in range(HEIGHT)] for x in range(WIDTH)]
        self.cells = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.cells.append(self.grid[x][y])

    def get(self, x, y):
        if x < 0 or x >= WIDTH:
            return None
        if y < 0 or y >= HEIGHT:
            return None
        return self.grid[x][y]

    def get_neighbors(self, cell):
        return [
            self.get(cell.x - 1, cell.y),
            self.get(cell.x + 1, cell.y),
            self.get(cell.x, cell.y - 1),
            self.get(cell.x, cell.y + 1)
        ]

    def random(self, luck):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                neighbors = self.get_neighbors(self.grid[x][y])
                self.grid[x][y].random(luck, neighbors)

    def has_move(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if not self.grid[x][y].is_life():
                    continue
                neighbors = self.get_neighbors(self.grid[x][y])
                for neighbor in neighbors:
                    if neighbor is not None \
                        and neighbor.chip == self.grid[x][y].chip:
                        return True
        return False

    def is_pair(self, cell):
        color = cell.get_color()
        x = cell.x
        y = cell.y
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if neighbor is not None and neighbor.get_color() == color:
                return True
        return False

    def destroy(self, cell, score=1):
        color = cell.get_color()
        if not cell.is_life():
            return 0
        cell.set_chip(None)
        x = cell.x
        y = cell.y
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if neighbor is not None and neighbor.get_color() == color:
                score += self.destroy(neighbor, score)

        return score

    def fall(self, view):
        for y in reversed(range(HEIGHT)):
            for x in range(WIDTH):
                if self.grid[x][y].get_color() == COLOR0:
                    for up in reversed(range(y)):
                        if self.grid[x][up].get_color() != COLOR0:
                            self.grid[x][y].chip, self.grid[x][up].chip = self.grid[x][up].chip, self.grid[x][y].chip
                            break

    def respawn(self, luck, view):
        self.fall(view)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.grid[x][y].get_color() != COLOR0:
                    continue
                self.grid[x][y].random(luck, self.get_neighbors(self.grid[x][y]))
