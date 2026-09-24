from .maze import Maze
import os
import time


class UserInterface:
    """Provide terminal display utilities for the maze."""

    @staticmethod
    def clear_display() -> None:
        """Clear the terminal display."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display(
        maze: "Maze", delay: float = 0,
        show_path: bool = False,
        R: int = 0, G: int = 150, B: int = 225
    ) -> None:
        """Render one generation frame to the terminal."""
        frame = maze.render_maze(show_path, R, G, B)
        print(frame, end="")

        if delay > 0:
            time.sleep(delay)

    @staticmethod
    def go_to_maze_start(maze: "Maze") -> None:
        """Move the terminal cursor to the start of the maze display."""
        print(f"\033[{maze.get_height() * 2 + 1}A", end="")
