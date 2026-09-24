# Mazegen

`mazegen` is a reusable Python module for generating and solving mazes. It
currently uses Depth-First Search (DFS) for maze generation.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

or, from source, at the root of the repository:

```bash
pip install .
```

## Quick start

create virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install flake8
python3 -m pip install mypy
python3 -m pip install build
```

## Basic Usage

import each class

```python
from mazegen import MazeGenerator, MazeSolver, Config, OutputMaze, UserInterface
```

initialize each class

```python
config = Config("config.txt", "r")

maze_gen = MazeGenerator(perfect_maze, height, width, seed, start, end)

solver = MazeSolver(maze_gen.get_maze())

output = OutputMaze(maze_hex, start, end, solution)

#UserInterface does not need initializing
```

generate a maze and display it

```python
maze_gen.generate_maze(
	animation, frame_delay, show_path,
	R, G, B)
maze = maze_gen.get_maze()
UserInterface.display(
	maze, frame_delay, show_path,
	R, G, B)
```

solve the maze

```python
solver.set_maze(maze)
solver.solve_maze(
	animation, ani_delay, show_path,
	R, G, B)
```

## Accessing a solution

```python
solver.solve_maze(
	animation, ani_delay, show_path,
	R, G, B)
solver.get_solution()
```

## License

This module is distributed under the license stated in the repository's
`LICENSE.md` file.
