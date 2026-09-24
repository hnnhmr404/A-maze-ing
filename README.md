*This project has been created as part of the 42 curriculum by \<hbinti-d\> and \<thdexmun\>*

# A-Maze-ing

## Description
A-Maze-ing is a configurable maze generator and solver developed in Python. The project reads maze settings from a configuration file and uses a Depth-First Search (DFS) algorithm with backtracking to generate the maze. It can generate both perfect and imperfect mazes, depending on the selected configuration.

The project also includes a Breadth-First Search (BFS) algorithm to find the shortest path between the maze entrance and exit. The generated maze can be displayed directly in the terminal, with options to visualize the generation process and highlight the solution path.

The project also supports additional features such as a centered 42 pattern when the maze dimensions are large enough, configurable maze colours, regeneration, shortest-path display, and an interactive command-line menu. Finally, the maze is exported in the required hexadecimal format for submission.

## Instructions
### Create virtual environment

```bash
make venv
```

### Install dependencies

```bash
make install
```

### Run

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Build reusable package

```bash
make build
```

## Configuration File

Configuration file format：
```text
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=0, 0
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
ANIMATION=TRUE
SHOW_PATH=false
DELAY=0.01
```

### Configuration Keys

- `WIDTH`: number of columns in the maze
- `HEIGHT`: number of rows in the maze
- `ENTRY`: entry coordinate in `(x,y)` format
- `EXIT`: exit coordinate in `(x,y)` format
- `OUTPUT_FILE`: file path where the generated maze and solution are saved
- `PERFECT`: Whether the maze is perfect (`true` or `false`)
- `SEED`: integer used to reproduce maze
- `ANIMATION`: Whether animation is enabled
- `SHOW_PATH`: Togle the shortest path
- `DELAY`: delays in between animation frames when animation is enabled


## Maze Algorithm

### Maze Generation

The maze generator uses a randomized Depth-First Search (DFS) algorithm with backtracking.

DFS was chosen because it naturally produces a connected maze while being relatively simple to implement and understand. It is also well suited to generating a perfect maze because the algorithm initially creates a spanning tree of the maze.

#### How It Works
1. Start from the selected entry cell.
2. Mark the current cell as visited.
3. Find neighbouring cells that have not been visited.
4. Randomly select one of the available neighbours.
5. Remove the wall between the current cell and the selected neighbour.
6. Move to the selected cell.
7. Continue until there are no unvisited neighbours.
8. Backtrack through previously visited cells until an unvisited neighbour is found.
9. Continue until all reachable cells have been visited.

#### Why DFS?
- It is suitable for generating perfect mazes.
- It guarantees that every reachable cell can be connected.
- It is relatively simple to implement using a stack.
- It allows the generation process to be animated.
- It can be extended with additional rules for the non-perfect maze mode.
- It produces different mazes when a different random seed is used.

#### Perfect Maze
Generates a perfect maze where every reachable cell is connected, no isolated cells, no loops, and there is exactly one path between any two cells.

#### Imperfect Maze
Generates a more open and playable maze with full connectivity, multiple independent routes, loops, open corners and centre, no dead ends, no large open area (3x3), and a playable layout suitable for Pac-Man-like movement.

### Path Solver

The shortest path between the entrance and exit is calculated using Breadth-First Search (BFS).

BFS was chosen because every movement between neighbouring cells has the same cost. Therefore, the first time BFS reaches the exit, the path found is a shortest path.

#### How It Works:
1. Start from the entry cell.
2. Add the entry to a queue.
3. Visit neighbouring cells that can be reached without crossing a wall.
4. Record the previous cell used to reach each new cell.
5. Continue until the exit is reached.
6. Follow the recorded previous cells backwards from the exit to the entry.
7. Convert the result into the required N, E, S, and W movement directions.

The shortest path can then be displayed in the terminal and written to the output file.

## Code Reusability

The maze generation logic was designed to be reusable independently from the main application.

The main reusable component is the `MazeGenerator` class.

It is responsible for generating the maze structure and can be instantiated with custom parameters such as:
- Maze width and height
- Maze entry and exit
- Maze output file name
- Perfect/Imperfect mode
- Seed number
- Animation mode
- Show path
- Animation rate

The generated maze structure and solution can then be accessed by other parts of the project.

This separation allows the generator to be reused in another Python project without depending on the command-line interface.

Basic Example
```bash
from mazegen import MazeGenerator

generator = MazeGenerator(
	WIDTH=20
	HEIGHT=20
	ENTRY=0,0
	EXIT=0,0
	OUTPUT_FILE=maze.txt
	PERFECT=False
	SEED=42
	ANIMATION=TRUE
	SHOW_PATH=false
	DELAY=0.01
)

generator.generate()

maze = generator.maze
solution = generator.solve()

print(maze)
print(solution)
```

The reusable package is provided in the repository and can be built using the standard Python packaging tools.

## Team Roles

### hbinti-d

- Designing and implementing the Maze class.
- Implementing maze generation using DFS.
- Implementing the 42 pattern.
- Setting up the Makefile.
- Implementing hexadecimal maze encoding.
- Managing dependencies.
- Implementing the no-dead-end maze feature.
- Fixing flake8 issues.
- Writing and maintaining the README.

### thdexmun
- Implementing the BFS path finder.
- Optimising parts of the codebase.
- Implementing the configuration system.
- Creating the interactive menu.
- Implementing path-finding animation.
- Implementing maze wall colour selection.
- Fixing mypy issues.
- Implementing the output-file functionality.
- Writing the usage documentation.

## Planning
At the beginning of the project, the main tasks were divided into two major areas:

1. Maze generation.
2. Maze path finder.

This allowed both parts to be developed independently before being integrated.

Separate Git branches were used to develop the maze generator and path finder. Once the individual components were stable, they were merged into the main codebase.

The project was then extended with:

- Configuration handling.
- Terminal rendering.
- Interactive controls.
- Output generation.
- Animation.
- Additional maze constraints.
- Code quality and type checking.

## Evolution

The initial implementation focused on generating a valid perfect maze using DFS.

Once the perfect maze was working, the non-perfect mode required additional work because the subject imposes different requirements for this mode.

The non-perfect maze needed to support multiple routes, loops, open corners and centre, no dead ends, Pac-Man-like gameplay, and restrictions on large open areas (3x3).

Additional wall-removal rules were therefore introduced to modify the initial maze while maintaining its validity.

The project also evolved through several rounds of refactoring as new features were added. This included reorganising class responsibilities, improving configuration management, and fixing type-checking and linting issues.

## What Worked

### Configuration Class
The configuration system provided a central place to store maze parameters and made it easier to add new configuration options.

### 3x3 Open-Area Validation
Checking the surrounding cells before opening additional walls helped prevent the non-perfect maze from creating forbidden 3x3 open areas.

### Separate Git Branches
Developing the maze generator and path finder separately reduced conflicts during the initial development stage and allowed each component to be tested independently.

### Reusable Maze Generation
Keeping the generation logic separate from the CLI made the project easier to extend and allowed the generator to be packaged for reuse.

### Static Type Checking
Using mypy helped identify incorrect assumptions about data types and function return values during development.

### Linting
Using flake8 helped keep the code consistent and identify formatting and style issues before evaluation.

## What Could Be Improved

### Additional Algorithms
The project currently focuses on DFS for maze generation and BFS for path finding. Future versions could support multiple generation algorithms such as Prim's algorithm or other maze-generation approaches.

### Planning
More detailed planning at the beginning would have reduced the amount of refactoring required later, especially when integrating the perfect and non-perfect maze requirements.

### Class Responsibilities
Some responsibilities could be separated more clearly between classes. A clearer design from the beginning would make the code easier to maintain and extend.

### Colour Management
The current colour system could be improved by making colour selection more flexible and easier to configure.

## Bonus

### No Dead Ends
The non-perfect maze was extended to support a maze with no dead ends, creating a more open and continuous board where the player is less likely to become trapped.

### Maze Generation Animation
The generation process can be animated in the terminal, allowing the user to see the DFS algorithm constructing the maze step by step. The animation can be toggled by the user.

### User-Defined Seed
The user can provide a seed through the terminal. Using the same seed and configuration allows the same maze to be reproduced, which is useful for debugging and testing.

### Extended Configuration
Additional configuration options were added beyond the mandatory subject requirements, giving the user more control over the maze generation and display behaviour.

## Tools

- Python 3.10+
- Makefile
- mypy for static type checking
- flake8 for linting and style validation
- Git
- Virtual Environment

## Resources

- Python documentation
- setuptools and packaging documentation
- algorithm references for randomized DFS/backtracking
- algorithm references for breadth-first search
- 42 project subject and evaluation requirements

## AI Usage

AI tools were used as a development support tool during the project.

They were mainly used for:
- Explaining Python concepts and algorithms.
- Understanding DFS, BFS, and maze-generation techniques.
- Debugging error messages and tracebacks.
- Discussing code structure and possible refactoring approaches.
- Reviewing README structure and documentation.
- Clarifying Python type annotations and standard-library behaviour.

AI-generated suggestions were reviewed, tested, and adapted by the team before being incorporated into the project. The final implementation, design decisions, testing, and integration were performed and verified by the project team.

## License

- This project is licensed under the MIT License.
- The license permits the maze generator to be used, modified, and distributed in future projects, provided that the original copyright and license notice are included.
- See `LICENSE.md` for the complete license terms.