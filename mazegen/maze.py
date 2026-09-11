class Maze:

    """Represents a grid-based maze and its wall state.

    Stores the maze dimensions, entry/exit points, the "42" pattern
    cells, and a per-cell dictionary of wall states (True = closed,
    False = open) for each cardinal direction.
    """

    def __init__(
            self, height: int, width: int, start: tuple[int, int],
            end: tuple[int, int]
            ) -> None:
        """Initialize an empty maze grid with all walls closed.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            start: (row, col) coordinates of the entry cell.
            end: (row, col) coordinates of the exit cell.
        """
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self._42 = set()
        if self.height >= 6 and self.width >= 9:
            (r, c) = (self.height//2, self.width//2)
            self._42 = {(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2),
                        (r + 2, c + 3)}
        self.maze = [
            [
                {"N": True, "E": True, "S": True, "W": True}
                for col in range(width)
            ]
            for row in range(height)
        ]

    def cell_to_int(self, r: int, c: int) -> int:
        """Encode a cell's wall configuration as an integer (0-15).

        Args:
            r: Row index of the cell.
            c: Column index of the cell.

        Returns:
            Integer where each bit represents a closed wall
            (N=1, E=2, S=4, W=8), following the direction bit mapping.
        """
        cell = self.maze[r][c]
	return (cell["N"] * 1) | (cell["E"] * 2) | (cell["S"] * 4) | (cell["W"] * 8)

    def maze_to_hex(self) -> str:
        """Encode the entire maze as a hexadecimal grid string.

        Returns:
            A string with one row per line, each cell represented by
            a single hexadecimal digit (0-f) describing its walls.
        """
        return (
            "\n".join(
                [
                    "".join(
                        [
                            f"{self.cell_to_int(r, c):x}"
                            for c in range(self.width)
                        ]
                    )
                    for r in range(self.height)
                ]
            )
        )

    def render_maze(self, stack: list[tuple[int, int]], R: int = 0, G: int = 150, B: int = 225) -> str:
        WALL = f"\033[38;2;{R};{G};{B}m"
        PURPLE = "\033[35m"
        PINK = "\033[95m"
        RESET = "\033[0m"

        stack_index = {cell: i for i, cell in enumerate(stack)}

        lines = ["+" + "---+" * self.width]
        for r in range(self.height):
            row_str, bot_str = "|", "+"
            for c in range(self.width):
                pos = (r, c)
                idx = stack_index.get(pos)
                
                # Determine cell content symbol
                if pos in self._42:
                    char = f"{PURPLE}███"
                elif pos == self.start:
                    char = f"{PURPLE} S "
                elif pos == self.end:
                    char = f"{PURPLE} E "
                elif idx is not None:
                    char = f" {PINK}. "
                else:
                    char = "   "

                # Check East connection
                east_conn = False
                if idx is not None:
                    east_conn = (idx + 1 < len(stack) and stack[idx + 1] == (r, c + 1)) or \
                                (idx - 1 >= 0 and stack[idx - 1] == (r, c + 1))

                e_wall = f"{WALL}|" if self.maze[r][c]["E"] else (f"{PINK}." if east_conn else " ")
                row_str += f"{char}{e_wall}"

                # Check South connection
                south_conn = False
                if idx is not None:
                    south_conn = (idx + 1 < len(stack) and stack[idx + 1] == (r + 1, c)) or \
                                 (idx - 1 >= 0 and stack[idx - 1] == (r + 1, c))

                s_wall = f"{WALL}---" if self.maze[r][c]["S"] else (f" {PINK}. " if south_conn else "   ")
                bot_str += f"{s_wall}{WALL}+"

            lines.extend([row_str, bot_str])

        return WALL + "\n".join(lines) + RESET
