import heapq
import os
import random

import matplotlib.pyplot as plt
import numpy as np


class CityGrid:
    def __init__(self, lines, columns, probability=30):
        self.lines = lines
        self.columns = columns
        self.grid = [[0] * columns for _ in range(lines)]
        self.tower_positions = set()

        count_blocked_blocks = int((probability / 100) * lines * columns)
        for _ in range(count_blocked_blocks):
            line, column = random.randint(0, lines - 1), random.randint(
                0, columns - 1
            )
            self.grid[line][column] = 1

    def __str__(self):
        grid_str = os.linesep.join(
            " ".join(map(str, line)) for line in self.grid
        )
        return grid_str

    def place_tower(self, line, column, radius):
        for l in range(line - radius - 1, line + radius):
            for c in range(column - radius - 1, column + radius):
                if (
                    0 <= l < len(self.grid)
                    and 0 <= c < len(self.grid[0])
                    and self.grid[l][c] != 1
                ):
                    self.grid[l][c] = 2
        self.grid[line - 1][column - 1] = 3
        self.tower_positions.add((line - 1, column - 1))

    def optimization_place_tower(self, radius):
        while True:
            max_uncovered = 0
            best_position = None

            for l in range(self.lines):
                for c in range(self.columns):
                    if self.grid[l][c] == 0:
                        uncovered_blocks = self.count_uncovered_blocks(
                            l, c, radius
                        )
                        if uncovered_blocks > max_uncovered:
                            max_uncovered = uncovered_blocks
                            best_position = (l + 1, c + 1)

            if best_position:
                self.place_tower(*best_position, radius)
            else:
                break

    def count_uncovered_blocks(self, line, column, radius):
        count = 0
        for l in range(line - radius, line + radius + 1):
            for c in range(column - radius, column + radius + 1):
                if (
                    0 <= l < self.lines
                    and 0 <= c < self.columns
                    and self.grid[l][c] == 0
                ):
                    count += 1
        return count

    def find_path(self, tower1, tower2):
        heap = [(0, tower1)]
        g_values = {tower1: 0}
        f_values = {tower1: self.distance(tower1, tower2)}
        path = {tower1: []}

        while heap:
            current_f, current = heapq.heappop(heap)

            if current == tower2:
                return path[current]

            for neighbor in self.get_neighbors(current):
                new_g = g_values[current] + self.calculate_reliability(
                    current, neighbor
                )

                if neighbor not in g_values or new_g < g_values[neighbor]:
                    g_values[neighbor] = new_g
                    f_values[neighbor] = new_g + self.distance(
                        neighbor, tower2
                    )
                    path[neighbor] = path[current] + [neighbor]
                    heapq.heappush(heap, (f_values[neighbor], neighbor))

        return []

    def get_neighbors(self, current):
        line, column = current
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_line, new_column = line + i, column + j
                if (
                    0 <= new_line < self.lines
                    and 0 <= new_column < self.columns
                ):
                    neighbors.append((new_line, new_column))
        return neighbors

    def calculate_reliability(self, tower1, tower2):
        distance_value = self.distance(tower1, tower2)
        return 1 / distance_value if distance_value != 0 else float("inf")

    def distance(self, tower1, tower2):
        line1, column1 = tower1
        line2, column2 = tower2
        return abs(line1 - line2) + abs(column1 - column2)

    def visualize_city(self):
        plt.imshow(
            np.array(self.grid), cmap="coolwarm", interpolation="nearest"
        )
        plt.title("City Grid")
        plt.show()

    def visualize_blocked_blocks(self):
        blocked_blocks = np.array(self.grid) == 1
        plt.imshow(blocked_blocks, cmap="Greys", interpolation="nearest")
        plt.title("Blocked Blocks")
        plt.show()

    def visualize_towers(self):
        towers = np.array(self.grid) == 3
        plt.imshow(towers, cmap="Blues", interpolation="nearest")
        plt.title("Towers")
        plt.show()

    def visualize_coverage(self, tower, radius):
        coverage = np.zeros((self.lines, self.columns))
        line, column = tower
        for l in range(
            max(0, line - radius), min(self.lines, line + radius + 1)
        ):
            for c in range(
                max(0, column - radius), min(self.columns, column + radius + 1)
            ):
                if self.grid[l][c] == 2:
                    coverage[l][c] = 1
        plt.imshow(coverage, cmap="Greens", interpolation="nearest")
        plt.title(f"Coverage of Tower at {tower} with Radius {radius}")
        plt.show()

    def visualize_path(self, tower1, tower2):
        path = self.find_path(tower1, tower2)
        if path:
            path_arr = np.zeros((self.lines, self.columns))
            for point in path:
                path_arr[point[0]][point[1]] = 1
            plt.imshow(path_arr, cmap="Reds", interpolation="nearest")
            plt.title(f"Path from {tower1} to {tower2}")
            plt.show()
        else:
            print(f"No path found between {tower1} and {tower2}.")


city = CityGrid(9, 20)
print("Initial City:")
print(city)

city.optimization_place_tower(radius=1)
print("City after Optimization:")
print(city)

print("Tower Positions:", city.tower_positions)

tower1 = random.choice(list(city.tower_positions))
tower2 = random.choice(list(city.tower_positions))

path = city.find_path(tower1, tower2)
if path:
    print(f"Path from {tower1} to {tower2}: {path}")
    reliability = len(path)
    print(f"Reliability between {tower1} and {tower2}: {reliability}")
else:
    print(f"No path found between {tower1} and {tower2}.")

city.visualize_city()
city.visualize_blocked_blocks()
city.visualize_towers()
tower_position = next(iter(city.tower_positions))
city.visualize_coverage(tower_position, radius=1)
city.visualize_path(tower1, tower2)
