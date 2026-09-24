from __future__ import annotations


class Maze:
    """Represent a maze as a grid of cells."""
    def __init__(
                self,
                height: int = 7, width: int = 9,
                start: tuple[int, int] | None = None,
                end: tuple[int, int] | None = None) -> None:

        """Initialize an empty maze grid with all walls closed.

        Args:
            height: Number of rows in the maze
            width: Number of columns in the maze
            start: coordinates of the entry cell (row, col)
            end: coordinates of the exit cell (row, col)
        """
        self._errors = []

        if (height <= 0 or width <= 0 or (height <= 1 and width <= 1)):
            height = 5
            width = 5
            error = "Warning, invalid maze size"
            error += ", defaulting width to 5"
            error += " and height to 5"
            self._errors.append(error)

        start = start or (0, 0)
        end = end or (height - 1, width - 1)
        if (start[0] < 0 or start[1] < 0 or
                start[0] >= height or start[1] >= width):
            error = f"Warning, entry {start}"
            start = (0, 0)
            end = (height - 1, width - 1)
            error += f" is out of bounds, defaulting start to {start}"
            error += f" and end to {end}"
            self._errors.append(error)
        if (end[0] < 0 or end[1] < 0 or
                end[0] >= height or end[1] >= width):
            error = f"Warning, entry {end}"
            start = (0, 0)
            end = (height - 1, width - 1)
            error += f" is out of bounds, defaulting start to {start}"
            error += f" and end to {end}"
            self._errors.append(error)

        if (start == end):
            error = f"Warning, both entry and exit on {start}"
            start = (0, 0)
            end = (height - 1, width - 1)
            error += f", defaulting start to {start}"
            error += f" and end to {end}"
            self._errors.append(error)

        self._height = height
        self._width = width
        self._maze = [
            [
                Maze.Cell(row, col)
                for col in range(width)
            ]
            for row in range(height)
        ]
        self._42 = set()
        if self._height >= 7 and self._width >= 9:
            (r, c) = (self._height//2, self._width//2)
            self._42 = {(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2),
                        (r + 2, c + 3)}
            for coords in self._42:
                self._maze[coords[0]][coords[1]].lock()
        else:
            error = "Warning, maze not big enough "
            error += "to fit 42 symbol, needs to be at least "
            error += "7 cells high and 9 cells wide"
            self._errors.append(error)
        if (start in self._42):
            error = f"Warning, entry {start}"
            start = (0, 0)
            end = (height - 1, width - 1)
            error += f" is inside 42, defaulting start to {start}"
            error += f" and end to {end}"
            self._errors.append(error)
        if (end in self._42):
            error = f"Warning, exit {end}"
            start = (0, 0)
            end = (height - 1, width - 1)
            error += f" is inside 42, defaulting start to {start}"
            error += f" and end to {end}"
            self._errors.append(error)
        self._start = {"Y": start[0], "X": start[1]}
        self._end = {"Y": end[0], "X": end[1]}
        self._maze[self._start["Y"]][self._start["X"]].set_start()
        self._maze[self._end["Y"]][self._end["X"]].set_end()

        self._renderer = self.Renderer(self._maze, height, width)

    def get_maze(self) -> list[list["Maze.Cell"]]:
        """Return the maze grid."""
        return (self._maze)

    def get_cell(self, row: int, col: int) -> "Maze.Cell":
        """Return the cell at the given coordinates.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            The cell at the specified coordinates
        """
        return (self._maze[row][col])

    def get_cell_neighbours(self,
                            row: int, col: int
                            ) -> dict[str, "Maze.Cell"]:
        """Return all valid neighbouring cells.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            A dictionary mapping directions to neighbouring cells
        """
        ret: dict[str, "Maze.Cell"] = {}
        for x in "NSEW":
            cell = self.get_neighbour_cell(row, col, x)
            if (cell is not None):
                ret.update({x: cell})
        return (ret)

    def get_neighbour_cell(
                        self, row: int,
                        col: int, direction: str) -> "Maze.Cell" | None:
        """Return the neighbouring cell in a given direction.

        Args:
            row: Row index of the cell
            col: Column index of the cell
            direction: Direction of the neighbour: N, S, E, or W

        Returns:
            The neighbouring cell, or None if it is outside the maze
        """
        if (direction == "N"):
            if (row - 1 < 0):
                return (None)
            else:
                return (self.get_cell(row - 1, col))
        if (direction == "S"):
            if (row + 1 >= self._height):
                return (None)
            else:
                return (self.get_cell(row + 1, col))
        if (direction == "E"):
            if (col + 1 >= self._width):
                return (None)
            else:
                return (self.get_cell(row, col + 1))
        if (direction == "W"):
            if (col - 1 < 0):
                return (None)
            else:
                return (self.get_cell(row, col - 1))
        return (None)

    def get_start(self) -> dict[str, int]:
        """Return the maze entry coordinates."""
        return (self._start)

    def get_end(self) -> dict[str, int]:
        """Return the maze exit coordinates."""
        return (self._end)

    def get_42(self) -> set[tuple[int, int]]:
        """Return the coordinates occupied by the 42 pattern."""
        return (self._42)

    def get_width(self) -> int:
        """Return the maze width."""
        return (self._width)

    def get_height(self) -> int:
        """Return the maze height."""
        return (self._height)

    def open_cell_north(self, row: int, col: int) -> None:
        """Open the northern wall of a cell and its neighbour."""
        self._maze[row][col].open_north()
        if (row - 1 >= 0):
            self._maze[row - 1][col].open_south()

    def open_cell_south(self, row: int, col: int) -> None:
        """Open the southern wall of a cell and its neighbour."""
        self._maze[row][col].open_south()
        if (row + 1 < self._height):
            self._maze[row + 1][col].open_north()

    def open_cell_east(self, row: int, col: int) -> None:
        """Open the eastern wall of a cell and its neighbour."""
        self._maze[row][col].open_east()
        if (col + 1 < self._width):
            self._maze[row][col + 1].open_west()

    def open_cell_west(self, row: int, col: int) -> None:
        """Open the western wall of a cell and its neighbour."""
        self._maze[row][col].open_west()
        if (col - 1 >= 0):
            self._maze[row][col - 1].open_east()

    def open_cell_wall(self, row: int, col: int, direction: str) -> None:
        """Open a wall in the specified direction.

        Args:
            row: Row index of the cell
            col: Column index of the cell
            direction: Direction of the wall: N, S, E, or W
        """
        if (direction == "N"):
            self.open_cell_north(row, col)
        if (direction == "S"):
            self.open_cell_south(row, col)
        if (direction == "E"):
            self.open_cell_east(row, col)
        if (direction == "W"):
            self.open_cell_west(row, col)

    def close_cell_north(self, row: int, col: int) -> None:
        """Close the northern wall of a cell and its neighbour."""
        self._maze[row][col].close_north()
        if (row - 1 >= 0):
            self._maze[row - 1][col].close_south()

    def close_cell_south(self, row: int, col: int) -> None:
        """Close the southern wall of a cell and its neighbour."""
        self._maze[row][col].close_south()
        if (row + 1 < self._height):
            self._maze[row + 1][col].close_north()

    def close_cell_east(self, row: int, col: int) -> None:
        """Close the eastern wall of a cell and its neighbour."""
        self._maze[row][col].close_east()
        if (col + 1 < self._width):
            self._maze[row][col + 1].close_west()

    def close_cell_west(self, row: int, col: int) -> None:
        """Close the western wall of a cell and its neighbour."""
        self._maze[row][col].close_west()
        if (col - 1 >= 0):
            self._maze[row][col - 1].close_east()

    def close_cell_wall(self, row: int, col: int, direction: str) -> None:
        """Close a wall in the specified direction.

        Args:
            row: Row index of the cell
            col: Column index of the cell
            direction: Direction of the wall: N, S, E, or W
        """
        if (direction == "N"):
            self.close_cell_north(row, col)
        if (direction == "S"):
            self.close_cell_south(row, col)
        if (direction == "E"):
            self.close_cell_east(row, col)
        if (direction == "W"):
            self.close_cell_west(row, col)

    def cell_to_int(self, row: int, col: int) -> int:
        """Encode a cell's wall configuration as an integer (0-15).

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            An integer from 0 to 15 representing the cell's walls
        """
        return (self._maze[row][col].walls_to_int())

    def maze_to_hex(self) -> str:
        """Convert the entire maze into a hexadecimal string.

        Returns:
            A hexadecimal representation of the maze, with one row
            per line
        """
        return (
            "\n".join(
                [
                    "".join(
                        [
                            f"{self.cell_to_int(r, c):x}"
                            for c in range(self._width)
                        ]
                    )
                    for r in range(self._height)
                ]
            )
        )

    def render_maze(
            self, show_path: bool = False,
            R: int = 0, G: int = 150, B: int = 225) -> str:
        """Render the maze as a coloured string.

        Args:
            show_path: Whether to display the calculated path
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour

        Returns:
            The rendered maze as a string
        """
        return (self._renderer.render_simple(R, G, B, show_path))

    def reset_cells(self) -> None:
        """Reset all cells to their initial closed-wall state."""
        for row in self._maze:
            for cell in row:
                cell.close_north()
                cell.close_east()
                cell.close_south()
                cell.close_west()
                cell.set_path(0)
        self.reset_42()

    def reset_42(self) -> None:
        """Restore the 42 pattern and lock its cells."""
        self._42 = set()
        if self._height >= 7 and self._width >= 9:
            (r, c) = (self._height//2, self._width//2)
            self._42 = {(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2),
                        (r + 2, c + 3)}
            for coords in self._42:
                self._maze[coords[0]][coords[1]].lock()

    def get_errors(self) -> list[str]:
        """Return all warnings generated during maze initialization."""
        return (self._errors)

    class Cell:
        """Represent a single cell in the maze."""
        def __init__(
                    self, row: int, col: int,
                    n_wall: bool = True, e_wall: bool = True,
                    s_wall: bool = True, w_wall: bool = True) -> None:
            """Initialize a maze cell.

            Args:
                row: Row index of the cell
                col: Column index of the cell
                n_wall: Whether the northern wall is closed
                e_wall: Whether the eastern wall is closed
                s_wall: Whether the southern wall is closed
                w_wall: Whether the western wall is closed
            """
            self._north = n_wall
            self._east = e_wall
            self._south = s_wall
            self._west = w_wall
            self._coords = {"Y": row, "X": col}
            self._start = False
            self._end = False
            self._locked = False
            self._path = 0

        def get_north(self) -> bool:
            """Return whether the northern wall is closed."""
            return (self._north)

        def get_east(self) -> bool:
            """Return whether the eastern wall is closed."""
            return (self._east)

        def get_south(self) -> bool:
            """Return whether the southern wall is closed."""
            return (self._south)

        def get_west(self) -> bool:
            """Return whether the western wall is closed."""
            return (self._west)

        def get_wall(self, direction: str) -> bool:
            """Return whether the specified wall is closed.

            Args:
                direction: Wall direction: N, S, E, or W

            Returns:
                True if the wall is closed, otherwise False
            """
            if (direction == "N"):
                return (self._north)
            elif (direction == "S"):
                return (self._south)
            elif (direction == "E"):
                return (self._east)
            elif (direction == "W"):
                return (self._west)
            return (True)

        def get_x(self) -> int:
            """Return the column coordinate of the cell."""
            return (self._coords["X"])

        def get_y(self) -> int:
            """Return the row coordinate of the cell."""
            return (self._coords["Y"])

        def get_walls(self) -> dict[str, bool]:
            """Return the closed-wall states for all directions."""
            return ({
                    "N": self._north, "E": self._east,
                    "S": self._south, "W": self._west
                    })

        def get_coords(self) -> dict[str, int]:
            """Return the cell coordinates."""
            return (self._coords)

        def open_north(self) -> None:
            """Open the northern wall."""
            self._north = False

        def open_east(self) -> None:
            """Open the eastern wall."""
            self._east = False

        def open_south(self) -> None:
            """Open the southern wall."""
            self._south = False

        def open_west(self) -> None:
            """Open the western wall."""
            self._west = False

        def close_north(self) -> None:
            """Close the northern wall."""
            self._north = True

        def close_east(self) -> None:
            """Close the eastern wall."""
            self._east = True

        def close_south(self) -> None:
            """Close the southern wall."""
            self._south = True

        def close_west(self) -> None:
            """Close the western wall."""
            self._west = True

        def set_start(self) -> None:
            """Mark the cell as the maze entry."""
            self._start = True

        def set_end(self) -> None:
            """Mark the cell as the maze exit."""
            self._end = True

        def is_start(self) -> bool:
            """Return whether the cell is the maze entry."""
            return (self._start)

        def is_end(self) -> bool:
            """Return whether the cell is the maze exit."""
            return (self._end)

        def lock(self) -> None:
            """Lock the cell to prevent maze generation from modifying it."""
            self._locked = True

        def unlock(self) -> None:
            """Unlock the cell."""
            self._locked = False

        def is_locked(self) -> bool:
            """Return whether the cell is locked."""
            return (self._locked)

        def get_path(self) -> int:
            """Return the path state of the cell."""
            return (self._path)

        def set_path(self, num: int) -> None:
            """Set the path state of the cell.

            Args:
                num: Path state to assign to the cell
            """
            self._path = num

        def confirm_path(self) -> None:
            """Mark the cell as part of the confirmed shortest path."""
            self._path = -1

        def walls_to_int(self) -> int:
            """Convert the cell's walls into a four-bit integer.

            Returns:
                An integer from 0 to 15 using the mapping
                N=1, E=2, S=4, and W=8
            """
            cell = self.get_walls()
            num = 0
            num = num | (cell["N"] * 1)
            num = num | (cell["E"] * 2)
            num = num | (cell["S"] * 4)
            num = num | (cell["W"] * 8)
            return (num)

    class Renderer:
        """Render a maze as a coloured terminal string."""
        def __init__(
                self, maze: list[list["Maze.Cell"]],
                height: int, width: int) -> None:
            """Initialize the maze renderer.

            Args:
                maze: Maze grid to render
                height: Number of rows in the maze
                width: Number of columns in the maze
            """
            self._maze = maze
            self._height = height
            self._width = width

        def set_maze(self, maze: list[list["Maze.Cell"]]) -> None:
            """Set the maze grid used by the renderer.

            Args:
                maze: Maze grid to render
            """
            self._maze = maze

        def set_height(self, height: int) -> None:
            """Set the maze height.

            Args:
                height: Number of rows in the maze
            """
            self._height = height

        def set_width(self, width: int) -> None:
            """Set the maze width.

            Args:
                width: Number of columns in the maze
            """
            self._width = width

        def render_simple(
                self, R: int = 0, G: int = 150, B: int = 225,
                show_path: bool = True) -> str:
            """Render the maze using terminal colours.

            Args:
                R: Red component of the maze colour
                G: Green component of the maze colour
                B: Blue component of the maze colour
                show_path: Whether to display path information

            Returns:
                The rendered maze as a coloured string
            """
            maze_color = f"\033[38;2;{R};{G};{B}m"
            start_color = f"\033[38;2;{0};{255};{0}m"
            end_color = f"\033[38;2;{255};{0};{0}m"
            unsure_color = f"\033[38;2;{255};{140};{0}m"
            path_color = "\033[95m"
            color_reset = "\033[0m"
            maze = self._maze
            line = ""
            for cell in self._maze[0]:
                if (cell.walls_to_int() == 0b1111 and
                        not cell.is_end() and
                        not cell.is_start()):
                    line += "████"
                    continue
                if (cell.get_x() == 0 or cell.get_west()):
                    line += "█"
                else:
                    line += "▀"
                if (cell.get_north()):
                    line += "▀▀▀"
                else:
                    line += "   "
            line += "█\n"

            for row in maze:
                mid = ""
                end = ""
                for cell in row:
                    x = cell.get_x()
                    y = cell.get_y()
                    if (cell.get_west()):
                        mid += "█"
                    else:
                        mid += " "

                    if (cell.is_start()):
                        mid += start_color + " ▀ " + maze_color
                    elif (cell.is_end()):
                        mid += end_color + " ▀ " + maze_color
                    elif (cell.is_locked()):
                        mid += "███"
                    elif (show_path and cell.get_path() == -1):
                        mid += path_color + " ▀ " + maze_color
                    elif (show_path and cell.get_path() != 0):
                        mid += unsure_color + " ▀ " + maze_color
                    else:
                        if (cell.walls_to_int() == 0b1111):
                            mid += "███"
                        else:
                            mid += "   "

                    if (y != self._height - 1 and
                            (maze[y + 1][x].get_west() or
                                (x == 0))):
                        end += "█"
                    else:
                        end += "▀"
                    if (y != self._height - 1 and
                            (maze[y + 1][x].walls_to_int() == 0b1111) and
                            not maze[y + 1][x].is_end() and
                            not maze[y + 1][x].is_start()):
                        end += "███"
                    elif (cell.get_south()):
                        end += "▀▀▀"
                    else:
                        end += "   "
                if (row[-1].get_east()):
                    mid += "█"
                else:
                    mid += " "
                if (cell.get_y() != self._height - 1):
                    end += "█"
                else:
                    end += "▀"
                line += f"{mid}\n{end}\n"
            return (maze_color + line + color_reset)
