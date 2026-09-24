from mazegen import (
    Config, MazeGenerator, MazeSolver,
    OutputMaze, UserInterface, Maze
)


def show_options(
        maze_gen: "MazeGenerator", show_path: bool, animation: bool,
        themes: tuple[tuple[int, ...], ...], theme: int) -> None:
    """Display the current maze settings and available menu options."""
    print("Seed: " + maze_gen.get_seed() + "\n")
    print("1. generate a new maze (random seed)")
    print("2. generate a new maze (input seed)")
    print("3. regenerate maze (same seed)")
    print("4. show/unshow shortest path ", end="")
    print(f"({'on' if show_path else 'off'})")
    print("5. show/unshow maze generation animation ", end="")
    print(f"({'on' if animation else 'off'})")
    print("6. change maze color ", end="")
    print(f"(R: {themes[theme][0]}, ", end="")
    print(f"G: {themes[theme][1]}, ", end="")
    print(f"B: {themes[theme][2]})")
    print("Anything else: quit")
    print("\n\033[KWhat would you like to do?: ", end="")


def put_output(
        output: "OutputMaze", maze: "Maze",
        solver: "MazeSolver", out_file: str) -> None:
    """Update and create the maze output file."""
    output.set_maze_hex(maze.maze_to_hex())
    output.set_entry((maze.get_start()["Y"], maze.get_start()["X"]))
    output.set_exit((maze.get_end()["Y"], maze.get_end()["X"]))
    output.set_solution(solver.get_solution())
    output.create_output(out_file)


def main() -> None:
    """Run the maze generator and interactive user interface."""
    config = Config("config.txt", "r")
    perfect_maze = config.get_perfect()
    height = config.get_height()
    width = config.get_width()
    seed = config.get_seed()
    start = config.get_entry()
    end = config.get_exit()
    animation = config.get_animation()
    show_path = config.get_show_path()
    ani_delay = config.get_delay()
    out_file = config.get_output()
    themes: tuple[tuple[int, ...], ...] = (
            (0, 150, 225),
            (239, 159, 118),
            (202, 158, 230),
            (129, 200, 190),
            (220, 224, 232),
            (234, 118, 203),
            (128, 128, 0),
            (205, 133, 63),
            (176, 196, 222),
            (238, 232, 170))
    theme = 0

    maze_gen = MazeGenerator(perfect_maze, height, width, seed, start, end)
    maze_gen.generate_maze(
        animation, ani_delay, show_path,
        themes[theme][0], themes[theme][1], themes[theme][2])
    maze = maze_gen.get_maze()
    solver = MazeSolver(maze_gen.get_maze())
    solver.set_maze(maze_gen.get_maze())
    solver.solve_maze(
        animation, ani_delay, show_path,
        themes[theme][0], themes[theme][1], themes[theme][2])
    UserInterface.clear_display()
    UserInterface.display(
        maze, 0, show_path,
        themes[theme][0], themes[theme][1], themes[theme][2])
    output = OutputMaze()
    while (True):
        lines = 12
        maze = maze_gen.get_maze()
        put_output(output, maze, solver, out_file)
        for error in config.get_errors():
            print(error)
            lines += 1
        for error in maze_gen.get_maze().get_errors():
            print(error)
            lines += 1
        show_options(maze_gen, show_path, animation, themes, theme)
        user_input = input()
        match user_input.strip():
            case "1":
                maze_gen.random_seed()
                maze_gen.generate_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                solver.set_maze(maze_gen.get_maze())
                solver.solve_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case "2":
                while (True):
                    print("seed: ", end="")
                    seed = input().strip()
                    if (len(seed) > 0):
                        break
                    print("Seed is empty, try again")
                maze_gen.set_seed(seed)
                maze_gen.generate_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                solver.set_maze(maze_gen.get_maze())
                solver.solve_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case "3":
                maze_gen.reset_rng()
                maze_gen.generate_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                solver.set_maze(maze_gen.get_maze())
                solver.solve_maze(
                    animation, ani_delay, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case "4":
                if (show_path):
                    show_path = False
                else:
                    show_path = True
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case "5":
                if (animation):
                    animation = False
                else:
                    animation = True
                print(f"\033[{lines}A")
            case "6":
                theme += 1
                if (theme >= len(themes)):
                    theme = 0
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case "":
                UserInterface.clear_display()
                UserInterface.display(
                    maze, 0, show_path,
                    themes[theme][0], themes[theme][1], themes[theme][2])
            case _:
                print("Bye!")
                break


if __name__ == "__main__":
    main()
