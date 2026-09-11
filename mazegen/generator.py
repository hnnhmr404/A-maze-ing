"""Randomized maze generation via DFS backtracking."""

from __future__ import annotations

import os
import random
import time

from .directions import DIRECTIONS
from .maze import Maze


class MazeGenerator:
    """Generate perfect or imperfect mazes using randomized DFS.

    A perfect maze contains no cycles. When ``perfect`` is False, the
    generated maze is loosened into a Pac-Man-style board by opening
    selected dead ends, corners, the centre, and additional walls until
    at least two independent cycles exist.

    The existing Maze and DIRECTIONS APIs are intentionally preserved.
    """

    def __init__(
        self, maze: Maze, perfect: bool = True,
        rng: random.Random | None = None
    ) -> None:
        self.maze = maze
        self.perfect = perfect
        self.rng = rng or random.Random()

    def _in_bounds(self, row: int, col: int) -> bool:
        """Return True if a cell is inside the maze."""
        return (
            0 <= row < self.maze.height
            and 0 <= col < self.maze.width
        )

    def _neighbour(
        self, row: int, col: int, direction: str
    ) -> tuple[int, int]:
        """Return the cell reached by moving in ``direction``."""
        info = DIRECTIONS[direction]

        return (row + int(info["dr"]), col + int(info["dc"]))

    def _opposite(self, direction: str) -> str:
        """Return the opposite direction."""
        return str(DIRECTIONS[direction]["opposite"])

    def _remove_wall(self, row: int, col: int, direction: str) -> None:
        """Remove a wall between a cell and its neighbour."""
        neighbour_row, neighbour_col = self._neighbour(row, col, direction)
        opposite = self._opposite(direction)

        self.maze.maze[row][col][direction] = False
        self.maze.maze[neighbour_row][neighbour_col][opposite] = False

    def _display(
        self, R: int, G: int, B: int, delay: float,
        stack: list[tuple[int, int]] | None = None
    ) -> None:
        """Render one generation frame to the terminal."""
        frame = self.maze.render_maze(stack or [], R, G, B)

        os.system("cls" if os.name == "nt" else "clear")
        print(frame)

        if delay > 0:
            time.sleep(delay)

    def _unvisited_neighbours(
        self, row: int, col: int, visited: set[tuple[int, int]]
    ) -> list[tuple[tuple[int, int], str]]:
        """Return unvisited neighbouring cells and their directions."""
        neighbours = []

        for direction in DIRECTIONS:
            neighbour_row, neighbour_col = self._neighbour(row, col, direction)

            if not self._in_bounds(neighbour_row, neighbour_col):
                continue

            if (neighbour_row, neighbour_col) in visited:
                continue

            neighbours.append(((neighbour_row, neighbour_col), direction))

        return neighbours

    def _generate_perfect_maze(
        self, R: int, G: int, B: int, delay: float, display_generation: bool
    ) -> None:
        """Generate a perfect maze using iterative DFS."""
        start = self.maze.start
        stack: list[tuple[int, int]] = [start]

        # Cells belonging to the 42 pattern are never visited by DFS.
        visited: set[tuple[int, int]] = set(self.maze._42)
        visited.add(start)

        while stack:
            if display_generation:
                self._display(R, G, B, delay, stack)

            row, col = stack[-1]
            neighbours = self._unvisited_neighbours(row, col, visited)

            if not neighbours:
                stack.pop()
                continue

            next_cell, direction = self.rng.choice(neighbours)
            self._remove_wall(row, col, direction)

            visited.add(next_cell)
            stack.append(next_cell)

    def cycle_count(self) -> int:
        """Return the number of independent cycles in the maze graph.

        Uses the cyclomatic-number formula:

            cycles = edges - vertices + connected_components

        The maze generator assumes all playable cells form one connected
        component, so connected_components is one.
        """
        playable_vertices = (
            self.maze.height * self.maze.width - len(self.maze._42)
        )

        open_walls = sum(
            not self.maze.maze[row][col][direction]
            for row in range(self.maze.height)
            for col in range(self.maze.width)
            for direction in DIRECTIONS
        )

        # Every edge is represented twice: once from each cell.
        edges = open_walls // 2
        connected_components = 1

        return (edges - playable_vertices + connected_components)

    def _is_dead_end(self, row: int, col: int) -> bool:
        """Return True if the cell currently has exactly one opening."""
        cell = self.maze.cell_to_int(row, col)
        all_walls = (1 << 4) - 1

        return (
            cell != all_walls
            and (cell | (cell + 1)) == all_walls
        )

    def _dead_end_cells(self) -> list[tuple[int, int]]:
        """Return all current dead-end cells."""
        return [
            (row, col)
            for row in range(self.maze.height)
            for col in range(self.maze.width)
            if self._is_dead_end(row, col)
        ]

    def large_open_region(
        self, row: int, col: int, direction: str | None
    ) -> bool:
        """Check whether opening a wall creates an oversized open area.

        The existing geometry rules are preserved from the original
        implementation.
        """
        maze = self.maze

        # Top edge
        if row == 0 and maze.height > 2:
            if direction is None:
                return False

            neighbour_row, neighbour_col = self._neighbour(row, col, direction)
            opposite = self._opposite(direction)

            maze.maze[row][col][direction] = False
            maze.maze[neighbour_row][neighbour_col][opposite] = False

            result = any(
                self.large_open_region(row + 1, col - 1 + offset, None)
                for offset in range(3)
            )

            maze.maze[row][col][direction] = True
            maze.maze[neighbour_row][neighbour_col][opposite] = True

            return result

        # Bottom edge
        if row == maze.height - 1 and maze.height > 2:
            if direction is None:
                return False

            neighbour_row, neighbour_col = self._neighbour(row, col, direction)
            opposite = self._opposite(direction)

            maze.maze[row][col][direction] = False
            maze.maze[neighbour_row][neighbour_col][opposite] = False

            result = any(
                self.large_open_region(row - 1, col - 1 + offset, None)
                for offset in range(3)
            )

            maze.maze[row][col][direction] = True
            maze.maze[neighbour_row][neighbour_col][opposite] = True

            return result

        # Left edge
        if col == 0 and maze.width > 2:
            if direction is None:
                return False

            neighbour_row, neighbour_col = self._neighbour(row, col, direction)
            opposite = self._opposite(direction)

            maze.maze[row][col][direction] = False
            maze.maze[neighbour_row][neighbour_col][opposite] = False

            result = any(
                self.large_open_region(row - 1 + offset, col + 1, None)
                for offset in range(3)
            )

            maze.maze[row][col][direction] = True
            maze.maze[neighbour_row][neighbour_col][opposite] = True

            return result

        # Right edge
        if col == maze.width - 1 and maze.width > 2:
            if direction is None:
                return False

            neighbour_row, neighbour_col = self._neighbour(row, col, direction)
            opposite = self._opposite(direction)

            maze.maze[row][col][direction] = False
            maze.maze[neighbour_row][neighbour_col][opposite] = False

            result = any(
                self.large_open_region(row - 1 + offset, col - 1, None)
                for offset in range(3)
            )

            maze.maze[row][col][direction] = True
            maze.maze[neighbour_row][neighbour_col][opposite] = True

            return result

        # Ignore outer boundary cases not covered above.
        if not (
            0 < col < maze.width - 1
            and 0 < row < maze.height - 1
        ):
            return False

        left = maze.maze[row][col - 1]
        bottom_left = maze.maze[row + 1][col - 1]
        bottom = maze.maze[row + 1][col]
        bottom_right = maze.maze[row + 1][col + 1]
        right = maze.maze[row][col + 1]
        top_right = maze.maze[row - 1][col + 1]
        top = maze.maze[row - 1][col]
        top_left = maze.maze[row - 1][col - 1]

        if direction is not None:
            neighbour_row, neighbour_col = self._neighbour(row, col, direction)

            opposite = self._opposite(direction)

            maze.maze[row][col][direction] = False
            maze.maze[neighbour_row][neighbour_col][opposite] = False

        is_center_open = (maze.cell_to_int(row, col) == 0)

        result = (
            is_center_open
            and not any(left[d] for d in "NES")
            and not any(bottom_left[d] for d in "NE")
            and not any(bottom[d] for d in "WNE")
            and not any(bottom_right[d] for d in "WN")
            and not any(right[d] for d in "SWN")
            and not any(top_right[d] for d in "SW")
            and not any(top[d] for d in "ESW")
            and not any(top_left[d] for d in "ES")
        )

        if direction is not None:
            maze.maze[row][col][direction] = True
            maze.maze[neighbour_row][neighbour_col][opposite] = True

        return result

    def valid_wall_removal(
        self, row: int, col: int, direction: str
    ) -> bool:
        """Return True if removing a wall is allowed."""
        neighbour_row, neighbour_col = self._neighbour(row, col, direction)

        if not self._in_bounds(neighbour_row, neighbour_col):
            return False

        if not self.maze.maze[row][col][direction]:
            return False

        if (
            (row, col) in self.maze._42
            or
            (neighbour_row, neighbour_col)
            in self.maze._42
        ):
            return False

        if self.large_open_region(row, col, direction):
            return False

        if self.large_open_region(
            neighbour_row, neighbour_col, self._opposite(direction)
        ):
            return False

        return True

    def _valid_directions(self, row: int, col: int) -> list[str]:
        """Return directions whose walls can safely be removed."""
        return [
            direction
            for direction in DIRECTIONS
            if self.valid_wall_removal(row, col, direction)
        ]

    def _open_dead_end(self, row: int, col: int) -> bool:
        """Open one valid wall from a dead-end cell."""
        directions = self._valid_directions(row, col)

        if not directions:
            return False

        direction = self.rng.choice(directions)
        self._remove_wall(row, col, direction)

        return True

    def _process_dead_ends(
        self, R: int, G: int, B: int, delay: float, display_generation: bool
    ) -> None:
        """Open selected dead ends."""
        special_cells = [
            (0, 0),
            (0, self.maze.width - 1),
            (self.maze.height - 1, 0),
            (
                self.maze.height - 1,
                self.maze.width - 1
            ),
            (
                self.maze.height // 2,
                self.maze.width // 2
            )
        ]

        cells = (special_cells + self._dead_end_cells())

        for row, col in cells:
            if display_generation:
                self._display(R, G, B, delay)

            if not self._is_dead_end(row, col):
                continue

            self._open_dead_end(row, col)

    def _add_loops(
        self, R: int, G: int, B: int,
        delay: float, display_generation: bool
    ) -> None:
        """Remove additional valid walls until two cycles exist."""
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                if self.cycle_count() >= 2:
                    return

                if display_generation:
                    self._display(R, G, B, delay)

                directions = self._valid_directions(row, col)

                if not directions:
                    continue

                direction = self.rng.choice(directions)
                self._remove_wall(row, col, direction)

    def make_imperfect(
        self, R: int = 0, G: int = 150, B: int = 225,
        delay: float = 0.01, display_generation: bool = False
    ) -> None:
        """Convert a perfect maze into a Pac-Man-style maze.

        Opens selected dead ends, corners, and centre cells, then removes
        additional valid walls until at least two independent cycles
        exist.
        """
        self._process_dead_ends(R, G, B, delay, display_generation)
        self._add_loops(R, G, B, delay, display_generation)

    def generate_maze(
        self, R: int = 0, G: int = 150, B: int = 225,
        delay: float = 0.1, display_generation: bool = False
    ) -> None:
        """Generate the maze in place.

        When ``perfect`` is True, a perfect maze is generated.

        When ``perfect`` is False, a perfect maze is generated first and
        then converted into a maze containing loops and Pac-Man-style
        open areas.
        """
        self._generate_perfect_maze(R, G, B, delay, display_generation)

        if not self.perfect:
            self.make_imperfect(R, G, B, delay, display_generation)
