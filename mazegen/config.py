class Config:
    """Read and store maze configuration from a configuration file."""

    def __init__(self, file: str = "config.txt", mode: str = "r") -> None:
        """Initialize the configuration from a file.

        Args:
            file: Name of the configuration file
            mode: File opening mode
        """
        self._errors: list[str] = []
        self._content: dict[str, str] = {}
        self._open_success = False
        self._seed: str | None = None

        try:
            self._file = open(file, mode)
            self._open_success = True
        except Exception as e:
            self._errors.append(str(e))

        if (self._open_success):
            try:
                while (True):
                    line = self._file.readline()
                    if (line == ""):
                        break
                    line = line.strip().split("=")
                    if (len(line) != 2 or line[0][0] == "#"):
                        continue
                    self._content.update({line[0]: line[1]})
            except Exception as e:
                self._errors.append(str(e))
            self._file.close()

        try:
            self._width = int(self._content["WIDTH"])
        except Exception:
            self._errors.append(
                "Warning, failed to extract WIDTH, defaulting to 10")
            self._width = 10

        try:
            self._height = int(self._content["HEIGHT"])
        except Exception:
            self._errors.append(
                "Warning, failed to extract HEIGHT, defaulting to 10")
            self._height = 10

        try:
            entry = self._content["ENTRY"].strip().split(",")
            if (len(entry) != 2):
                raise Exception()
            self._entry = (int(entry[0].strip()), int(entry[1].strip()))
        except Exception:
            self._errors.append(
                "Warning, failed to extract ENTRY, defaulting to (0, 0)")
            self._entry = (0, 0)

        try:
            ex = self._content["EXIT"].strip().split(",")
            if (len(ex) != 2):
                raise Exception()
            self._exit = (int(ex[0].strip()), int(ex[1].strip()))
        except Exception:
            error = "Warning, failed to extract EXIT,"
            error += f"defaulting to ({self._height - 1}, {self._width - 1})"
            self._errors.append(error)
            self._exit = (self._height - 1, self._width - 1)

        try:
            self._output = self._content["OUTPUT_FILE"]
        except Exception:
            error = "Warning, failed to extract OUTPUT_FILE"
            error = ", defaulting to output_maze.txt"
            self._errors.append(error)
            self._output = "output_maze.txt"

        try:
            perfect = self._content["PERFECT"].strip().lower()
            if (perfect == "true"):
                self._perfect = True
            elif (perfect == "false"):
                self._perfect = False
            else:
                raise Exception()
        except Exception:
            self._errors.append(
                "Warning, failed to extract PERFECT, defaulting to False")
            self._perfect = False

        try:
            seed = self._content["SEED"].strip()
            if (seed == ""):
                raise Exception()
            self._seed = seed
        except Exception:
            self._errors.append(
                "Warning, failed to extract SEED, defaulting to None")

        try:
            animation = self._content["ANIMATION"].strip().lower()
            if (animation == "true"):
                self._animation = True
            elif (animation == "false"):
                self._animation = False
            else:
                raise Exception()
        except Exception:
            self._errors.append(
                "Warning, failed to extract ANIMATION, defaulting to True")
            self._animation = True

        try:
            show_path = self._content["SHOW_PATH"].strip().lower()
            if (show_path == "true"):
                self._show_path = True
            elif (show_path == "false"):
                self._show_path = False
            else:
                raise Exception()
        except Exception:
            self._errors.append(
                "Warning, failed to extract SHOW_PATH, defaulting to True")
            self._show_path = True

        try:
            self._delay = float(self._content["DELAY"])
        except Exception:
            self._errors.append(
                "Warning, failed to extract DELAY, defaulting to 0.01")
            self._delay = 0.01

    def get_width(self) -> int:
        """Return the configured maze width."""
        return (self._width)

    def get_height(self) -> int:
        """Return the configured maze height."""
        return (self._height)

    def get_entry(self) -> tuple[int, int]:
        """Return the configured maze entry coordinates."""
        return (self._entry)

    def get_exit(self) -> tuple[int, int]:
        """Return the configured maze exit coordinates."""
        return (self._exit)

    def get_output(self) -> str:
        """Return the configured output file name."""
        return (self._output)

    def get_perfect(self) -> bool:
        """Return whether perfect maze generation is enabled."""
        return (self._perfect)

    def get_seed(self) -> str | None:
        """Return the configured seed."""
        return (self._seed)

    def get_animation(self) -> bool:
        """Return whether maze generation animation is enabled."""
        return (self._animation)

    def get_show_path(self) -> bool:
        """Return whether the solution path should be displayed."""
        return (self._show_path)

    def get_delay(self) -> float:
        """Return the configured animation delay."""
        return (self._delay)

    def get_errors(self) -> list[str]:
        """Return the configuration errors and warnings."""
        return (self._errors)
