import os


class OutputMaze:
    """Store and write the generated maze output."""

    def __init__(
            self, maze_hex: str = "",
            start: tuple[int, int] = (0, 0),
            end: tuple[int, int] = (0, 0),
            solution: str = ""):
        """Initialize the maze output data.

        Args:
            maze_hex: Hexadecimal representation of the maze.
            start: Coordinates of the maze entry.
            end: Coordinates of the maze exit.
            solution: Shortest solution path.
        """
        self._maze_hex = maze_hex
        self._entry = start
        self._exit = end
        self._solution = solution

    def set_maze_hex(self, maze_hex: str) -> None:
        """Set the hexadecimal representation of the maze.

        Args:
            maze_hex: Hexadecimal representation of the maze.
        """
        self._maze_hex = maze_hex

    def set_entry(self, start: tuple[int, int]) -> None:
        """Set the maze entry coordinates.

        Args:
            start: Coordinates of the maze entry.
        """
        self._entry = start

    def set_exit(self, end: tuple[int, int]) -> None:
        """Set the maze exit coordinates.

        Args:
            end: Coordinates of the maze exit.
        """
        self._exit = end

    def set_solution(self, solution: str) -> None:
        """Set the shortest solution path.

        Args:
            solution: Shortest solution path.
        """
        self._solution = solution

    def create_output(self, file_name: str = "output_maze.txt") -> None:
        """Write the maze data and solution to an output file.

        Args:
            file_name: Name of the output file.
        """
        self._errors = []
        try:
            file = open(file_name, "w")
        except Exception:
            error = f"OutputWarning: failed to open {file}"
            error += " with write permission"
            self._errors.append(error)
            try:
                file = open(file_name, "x")
            except Exception:
                try:
                    error = f"OutputWarning: failed to create {file_name}"
                    error += ", removing and retrying"
                    self._errors.append(error)
                    os.remove(file_name)
                finally:
                    file = open(file_name, "x")

        line = f"{self._maze_hex}\n"
        line += "\n"
        line += f"{self._entry[1]},{self._entry[0]}\n"
        line += f"{self._exit[1]},{self._exit[0]}\n\n"
        line += "#entry: (x, y)\n"
        line += "#exit: (x, y)\n"
        line += "\n"
        line += f"{self._solution}     #shortest solution\n"

        file.write(line)
        file.close()
