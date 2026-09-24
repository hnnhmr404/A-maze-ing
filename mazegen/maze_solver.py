from .maze import Maze
from .interface import UserInterface


class MazeSolver:
    """Solve a maze and determine the shortest path."""

    def __init__(self, maze: Maze) -> None:
        """Initialize the solver with a maze.

        Args:
            maze: Maze to solve
        """
        self._maze = maze

    def set_maze(self, maze: Maze) -> None:
        """Set the maze to be solved.

        Args:
            maze: Maze to solve
        """
        self._maze = maze

    def _connected_cells(
                        self, maze: "Maze",
                        paths: list[tuple[str, "Maze.Cell"]],
                        prev: list[tuple[str, "Maze.Cell"]]
                        ) -> list["Maze.Cell"]:
        """Find cells where the search paths become connected.

        Args:
            maze: Maze being solved
            paths: Current search paths from the start and end
            prev: Search paths from the previous step

        Returns:
            Cells where the start and end search paths connect
        """
        for cell in paths:
            neighbours = maze.get_cell_neighbours(
                cell[1].get_y(),
                cell[1].get_x())

            if (cell[0] == "S"):
                opposite = "E"
            else:
                opposite = "S"
            if ((opposite, cell[1]) in paths):
                ret = [cell[1]]
                s_path = False
                e_path = False
                for neighbour in neighbours:
                    if (cell[1].get_wall(neighbour)):
                        continue
                    if (not s_path):
                        if (("S", neighbours[neighbour]) in prev):
                            ret.append(neighbours[neighbour])
                            s_path = True
                    if (not e_path):
                        if (("E", neighbours[neighbour]) in prev):
                            ret.append(neighbours[neighbour])
                            e_path = True

                return (ret)
            for neighbour in neighbours:
                if (
                    not cell[1].get_wall(neighbour) and
                    neighbours[neighbour] is not None and
                    neighbours[neighbour].get_path() == cell[1].get_path() and
                    (opposite, neighbours[neighbour]) in paths
                ):
                    return ([cell[1], neighbours[neighbour]])
        return ([])

    def solve_maze(
            self, animate: bool = False, delay: float = 0.1,
            show_path: bool = False,
            R: int = 0, G: int = 150, B: int = 225) -> None:
        """Solve the maze and mark the shortest path.

        The solver searches from both the start and end cells until
        the two searches connect. It then traces the connected cells
        backwards to determine the shortest path.

        Args:
            animate: Whether to display the solving process
            delay: Delay between animation steps in seconds
            show_path: Whether to display the path during solving
            R: Red component of the maze colour
            G: Green component of the maze colour
            B: Blue component of the maze colour
        """
        maze: "Maze" = self._maze
        start: dict[str, int] = maze.get_start()
        end: dict[str, int] = maze.get_end()
        step = 0

        paths = [
            ("S", maze.get_cell(start["Y"], start["X"])),
            ("E", maze.get_cell(end["Y"], end["X"]))
        ]
        prev: list[tuple[str, "Maze.Cell"]] = []
        connected: list["Maze.Cell"] = []
        while (len(paths) > 0):
            step += 1

            for path in paths:
                path[1].set_path(step)

                if (animate and show_path):
                    UserInterface.go_to_maze_start(maze)
                    UserInterface.display(maze, delay, animate, R, G, B)

            next_steps: list[tuple[str, "Maze.Cell"]] = []

            connected = self._connected_cells(maze, paths, prev)
            if (not len(connected) == 0):
                break

            for path in paths:
                neighbours = maze.get_cell_neighbours(
                                                    path[1].get_y(),
                                                    path[1].get_x())
                for neighbour in neighbours:
                    if (
                        neighbours[neighbour] is not None and
                        not path[1].get_wall(neighbour) and
                        neighbours[neighbour].get_path() == 0 and
                        (path[0], neighbours[neighbour]) not in next_steps
                    ):
                        next_steps.append((path[0], neighbours[neighbour]))
            prev = paths
            paths = next_steps

        if (len(connected) == 3):
            connected[0].confirm_path()
            connected.pop(0)

            if (animate and show_path):
                UserInterface.go_to_maze_start(maze)
                UserInterface.display(maze, delay, animate, R, G, B)

        while (step > 0):
            back_set = []
            for cell in connected:
                neighbours = maze.get_cell_neighbours(
                                                    cell.get_y(),
                                                    cell.get_x())
                for neighbour in neighbours:
                    if (
                        neighbours[neighbour] is not None and
                        not cell.get_wall(neighbour) and
                        neighbours[neighbour].get_path() > 0 and
                        neighbours[neighbour].get_path() < step
                    ):
                        back_set.append(neighbours[neighbour])
                        break
                cell.confirm_path()

                if (animate and show_path):
                    UserInterface.go_to_maze_start(maze)
                    UserInterface.display(maze, delay, animate, R, G, B)
            connected = back_set
            step -= 1

        for row in maze.get_maze():
            for cell in row:
                if (cell.get_path() != 0 and cell.get_path() != -1):
                    cell.set_path(0)

                    if (animate and show_path):
                        UserInterface.go_to_maze_start(maze)
                        UserInterface.display(maze, delay, animate, R, G, B)

    def get_solution(self) -> str:
        """Return the solution path from the maze entry to the exit.

        Returns:
            A string containing the directions needed to travel from
            the entry to the exit, using N, S, E, and W
        """
        maze = self._maze
        if (maze.get_cell(0, 0).get_path() == 0):
            self.solve_maze()

        sol = ""
        start = maze.get_start()
        end = maze.get_end()
        end_cell = maze.get_cell(end["Y"], end["X"])
        cell = maze.get_cell(start["Y"], start["X"])
        direction = ""

        while (cell != end_cell):
            neighbours = maze.get_cell_neighbours(cell.get_y(), cell.get_x())
            if (direction == "N"):
                neighbours.pop("S")
            elif (direction == "S"):
                neighbours.pop("N")
            elif (direction == "E"):
                neighbours.pop("W")
            elif (direction == "W"):
                neighbours.pop("E")
            for neighbour in neighbours:
                if (not cell.get_wall(neighbour) and
                        neighbours[neighbour].get_path() == -1):
                    cell = neighbours[neighbour]
                    sol += neighbour
                    direction = neighbour
                    break
            if (direction == ""):
                break
        return (sol)
