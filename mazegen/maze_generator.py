"""Randomized maze generation via DFS backtracking."""

from __future__ import annotations

import random

from .directions import DIRECTIONS
from .maze import Maze
from .interface import UserInterface


class MazeGenerator:
    """Generate perfect or imperfect mazes using randomized DFS.

    A perfect maze contains no cycles. When ``perfect`` is False, the
    generated maze is converted into a Pac-Man-style maze by opening
    selected walls and creating additional cycles.
    """

    def __init__(
                self,
                perfect: bool = True,
                height: int = 7, width: int = 9,
                seed: str | None = None,
                start: tuple[int, int] | None = None,
                end: tuple[int, int] | None = None
            ) -> None:
        """Initialize the maze generator.

        Args:
            perfect: Whether to generate a perfect maze
            height: Number of rows in the maze
            width: Number of columns in the maze
            seed: Random seed used for maze generation
            start: Coordinates of the maze entry
            end: Coordinates of the maze exit
        """
        self._maze = Maze(height, width, start, end)
        self._perfect = perfect
        self._seed = seed or str(random.randint(1000000000, 9999999999))
        self._rng = random.Random(self._seed)

    def get_maze(self) -> "Maze":
        """Return the generated maze."""
        return (self._maze)

    def get_seed(self) -> str:
        """Return the random seed used by the generator."""
        return (self._seed)

    def set_seed(self, seed: str) -> None:
        """Set the random seed and reset the random number generator.

        Args:
            seed: Random seed to use for maze generation
        """
        self._seed = seed
        self.reset_rng()

    def random_seed(self) -> None:
        """Generate a new random seed and reset the random number generator."""
        self._seed = str(random.randint(1000000000, 9999999999))
        self.reset_rng()

    def reset_rng(self) -> None:
        """Reset the random number generator using the current seed."""
        self._rng = random.Random(self._seed)

    def _in_bounds(self, row: int, col: int) -> bool:
        """Return whether the given coordinates are inside the maze.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            True if the coordinates are inside the maze, otherwise False
        """
        return (
            0 <= row < self._maze.get_height() and
            0 <= col < self._maze.get_width()
        )

    def _neighbour(
        self, row: int, col: int, direction: str
    ) -> tuple[int, int]:
        """Return the coordinates of a neighbouring cell."""
        info = DIRECTIONS[direction]

        return (row + int(info["dr"]), col + int(info["dc"]))

    def _opposite(self, direction: str) -> str:
        """Return the opposite direction."""
        return str(DIRECTIONS[direction]["opposite"])

    def _remove_wall(self, row: int, col: int, direction: str) -> None:
        """Remove a wall between a cell and its neighbour."""
        self._maze.open_cell_wall(row, col, direction)

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
            self, R: int = 0, G: int = 150, B: int = 225,
            delay: float = 0.1, display_generation: bool = False,
            show_path: bool = False) -> None:
        """Generate a perfect maze using iterative depth-first search.

        Args:
            R: Red component of the maze colour.
            G: Green component of the maze colour.
            B: Blue component of the maze colour.
            delay: Delay between generation steps in seconds.
            display_generation: Whether to display the generation process.
            show_path: Whether to display path information.
        """
        maze = self._maze
        start = maze.get_start()
        stack: list[tuple[int, int]] = [(start["Y"], start["X"])]

        # Cells belonging to the 42 pattern are never visited by DFS.
        visited: set[tuple[int, int]] = self._maze.get_42()
        visited.add((start["Y"], start["X"]))

        if (display_generation):
            UserInterface.clear_display()
            UserInterface.display(maze, delay, show_path, R, G, B)

        while stack:
            row, col = stack[-1]
            neighbours = self._unvisited_neighbours(row, col, visited)

            if not neighbours:
                stack.pop()
                continue

            next_cell, direction = self._rng.choice(neighbours)
            self._remove_wall(row, col, direction)

            visited.add(next_cell)
            stack.append(next_cell)
            if display_generation and neighbours:
                UserInterface.go_to_maze_start(maze)
                UserInterface.display(maze, delay, show_path, R, G, B)

    def cycle_count(self) -> int:
        """Return the number of independent cycles in the maze graph.

        Uses the cyclomatic-number formula:

            cycles = edges - vertices + connected_components

        The maze generator assumes all playable cells form one connected
        component, so connected_components is one.
        """
        grid_42 = self._maze.get_42()
        if (grid_42 is None):
            grid_42 = set()
        playable_vertices = (
            self._maze.get_height() * self._maze.get_width() - len(grid_42)
        )

        open_walls = sum(
            not self._maze.get_cell(row, col).get_wall(direction)
            for row in range(self._maze.get_height())
            for col in range(self._maze.get_width())
            for direction in DIRECTIONS
        )

        # Every edge is represented twice: once from each cell.
        edges = open_walls // 2
        connected_components = 1

        return (edges - playable_vertices + connected_components)

    def _is_dead_end(self, row: int, col: int) -> bool:
        """Return whether a cell has exactly one open wall."""
        cell = self._maze.cell_to_int(row, col)
        all_walls = 0b1111

        return (
            cell != all_walls
            and (cell | (cell + 1)) == all_walls
        )

    def _dead_end_cells(self) -> list[tuple[int, int]]:
        """Return the coordinates of all current dead-end cells."""
        return [
            (row, col)
            for row in range(self._maze.get_height())
            for col in range(self._maze.get_width())
            if self._is_dead_end(row, col)
        ]

    def large_open_region(
        self, row: int, col: int, direction: str | None
    ) -> bool:
        """Check whether opening a wall creates an oversized open region.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.
            direction: Wall direction to test, or None when checking
                an existing configuration.

        Returns:
            True if opening the wall creates an oversized open region,
            otherwise False.
        """
        maze = self._maze
        height = maze.get_height()
        width = maze.get_width()

        # Top edge
        if row == 0 and height > 2:
            if direction is None:
                return False

            maze.open_cell_wall(row, col, direction)

            result = any(
                self.large_open_region(row + 1, col - 1 + offset, None)
                for offset in range(3)
            )

            maze.close_cell_wall(row, col, direction)

            return result

        # Bottom edge
        if row == height - 1 and height > 2:
            if direction is None:
                return False

            maze.open_cell_wall(row, col, direction)

            result = any(
                self.large_open_region(row - 1, col - 1 + offset, None)
                for offset in range(3)
            )

            maze.close_cell_wall(row, col, direction)

            return result

        # Left edge
        if col == 0 and width > 2:
            if direction is None:
                return False

            maze.open_cell_wall(row, col, direction)

            result = any(
                self.large_open_region(row - 1 + offset, col + 1, None)
                for offset in range(3)
            )

            maze.close_cell_wall(row, col, direction)

            return result

        # Right edge
        if col == width - 1 and width > 2:
            if direction is None:
                return False

            maze.open_cell_wall(row, col, direction)

            result = any(
                self.large_open_region(row - 1 + offset, col - 1, None)
                for offset in range(3)
            )

            maze.close_cell_wall(row, col, direction)

            return result

        # Ignore outer boundary cases not covered above.
        if not (
            0 < col < width - 1
            and 0 < row < height - 1
        ):
            return False

        left = maze.get_cell(row, col - 1)
        bottom_left = maze.get_cell(row + 1, col - 1)
        bottom = maze.get_cell(row + 1, col)
        bottom_right = maze.get_cell(row + 1, col + 1)
        right = maze.get_cell(row, col + 1)
        top_right = maze.get_cell(row - 1, col + 1)
        top = maze.get_cell(row - 1, col)
        top_left = maze.get_cell(row - 1, col - 1)

        if direction is not None:
            maze.open_cell_wall(row, col, direction)

        is_center_open = (maze.cell_to_int(row, col) == 0)

        result = (
            is_center_open
            and not any(left.get_wall(d) for d in "NES")
            and not any(bottom_left.get_wall(d) for d in "NE")
            and not any(bottom.get_wall(d) for d in "WNE")
            and not any(bottom_right.get_wall(d) for d in "WN")
            and not any(right.get_wall(d) for d in "SWN")
            and not any(top_right.get_wall(d) for d in "SW")
            and not any(top.get_wall(d) for d in "ESW")
            and not any(top_left.get_wall(d) for d in "ES")
        )

        if direction is not None:
            maze.close_cell_wall(row, col, direction)

        return result

    def valid_wall_removal(
        self, row: int, col: int, direction: str
    ) -> bool:
        """Return whether a wall can safely be removed.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.
            direction: Direction of the wall to remove.

        Returns:
            True if the wall can be removed, otherwise False.
        """
        neighbour_row, neighbour_col = self._neighbour(row, col, direction)

        if not self._in_bounds(neighbour_row, neighbour_col):
            return False

        if not self._maze.get_cell(row, col).get_wall(direction):
            return False

        if (
            self._maze.get_cell(row, col).is_locked()
            or
            self._maze.get_cell(neighbour_row, neighbour_col).is_locked()
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

        direction = self._rng.choice(directions)
        self._remove_wall(row, col, direction)

        return True

    def _process_dead_ends(
            self, R: int, G: int, B: int,
            delay: float, display_generation: bool,
            show_path: bool) -> None:
        """Open selected dead ends to make the maze more open.

        Args:
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour
            delay: Delay between generation steps in seconds
            display_generation: Whether to display the generation process
            show_path: Whether to display path information
        """
        maze = self._maze
        height = self._maze.get_height()
        width = self._maze.get_width()
        special_cells = [
            (0, 0),
            (0, width - 1),
            (height - 1, 0),
            (
                height - 1,
                width - 1
            ),
            (
                height // 2,
                width // 2
            )
        ]

        cells = (special_cells + self._dead_end_cells())

        for row, col in cells:

            if not self._is_dead_end(row, col):
                continue

            self._open_dead_end(row, col)

            if display_generation:
                UserInterface.go_to_maze_start(maze)
                UserInterface.display(maze, delay, show_path, R, G, B)

    def _add_loops(
        self, R: int, G: int, B: int,
        delay: float, display_generation: bool, show_path: bool
    ) -> None:
        """Remove valid walls until the maze contains at least two cycles.

        Args:
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour
            delay: Delay between generation steps in seconds
            display_generation: Whether to display the generation process
            show_path: Whether to display path information
        """
        maze = self._maze
        for row in range(self._maze.get_height()):
            for col in range(self._maze.get_width()):
                if self.cycle_count() >= 2:
                    return

                directions = self._valid_directions(row, col)

                if not directions:
                    continue

                direction = self._rng.choice(directions)
                self._remove_wall(row, col, direction)

                if display_generation:
                    UserInterface.go_to_maze_start(maze)
                    UserInterface.display(maze, delay, show_path, R, G, B)

    def make_imperfect(
            self, R: int = 0, G: int = 150, B: int = 225,
            delay: float = 0.01, display_generation: bool = False,
            show_path: bool = False) -> None:
        """Convert a perfect maze into a Pac-Man-style maze.

        Selected dead ends and walls are opened to create larger open areas
        and additional cycles.

        Args:
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour
            delay: Delay between generation steps in seconds
            display_generation: Whether to display the generation process
            show_path: Whether to display path information
        """
        self._process_dead_ends(R, G, B, delay, display_generation, show_path)
        self._add_loops(R, G, B, delay, display_generation, show_path)

    def generate_maze(
            self, display_generation: bool = False, delay: float = 0.1,
            show_path: bool = False,
            R: int = 0, G: int = 150, B: int = 225) -> None:
        """Generate the maze in place

        A perfect maze is generated first. If ``perfect`` is False, the
        maze is then converted into a Pac-Man-style maze with additional
        open areas and cycles.

        Args:
            display_generation: Whether to display the generation process
            delay: Delay between generation steps in seconds
            show_path: Whether to display path information
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour
        """
        self._maze.reset_cells()
        self._generate_perfect_maze(
            R, G, B, delay,
            display_generation, show_path)

        if not self._perfect:
            self.make_imperfect(R, G, B, delay, display_generation, show_path)
