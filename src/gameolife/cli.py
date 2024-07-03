"""This is the entry point of the gameolife package and implements a CLI."""

import sys
import time
import argparse

import curses

from gameolife.grid import LifeGrid

from gameolife import __version__, __project__


class GridView:
    """A view for a LifeGrid."""

    def __init__(self, window: curses.window, grid: LifeGrid):
        self._window = window
        self._grid = grid

        self.window.move(0, 0)
        self.draw()

    def draw(self):
        """Draw the grid on the window."""
        window_size_y, window_size_x = self.window.getmaxyx()
        original_y, original_x = self.window.getyx()
        self.window.move(0, 0)
        for row in range(window_size_y):
            for col in range(window_size_x):
                try:
                    self.window.addch(str(self.grid[(row, col)]))
                except curses.error as e:
                    # Writting to the lower right corner of the window will raise an error
                    # after the last character is written
                    if not (col == window_size_x - 1 and row == window_size_y - 1):
                        raise e
        self.window.move(original_y, original_x)
        self.window.refresh()

    @property
    def window(self) -> curses.window:
        """curses.window: The window."""
        return self._window

    @property
    def grid(self) -> LifeGrid:
        """LifeGrid: The life grid."""
        return self._grid


def grid_interact(view: GridView, help_print_func):
    """Interact with the grid."""

    try:
        curses.curs_set(2)
        view.window.keypad(1)

        view.window.move(0, 0)

        help_print_func(
            "Use the arrow keys to navigate the grid, <space> toggles the state of the cell, <enter> starts the simulation, <ctrl+c> will exit the program.\n"
        )

        while True:
            keypress = view.window.getch()
            if keypress == curses.KEY_UP:  # UP
                cursor_y, cursor_x = view.window.getyx()
                if cursor_y > 0:
                    view.window.move(cursor_y - 1, cursor_x)
                    view.window.refresh()
            elif keypress == curses.KEY_DOWN:  # DOWN
                cursor_y, cursor_x = view.window.getyx()
                if cursor_y < view.window.getmaxyx()[0] - 1:
                    view.window.move(cursor_y + 1, cursor_x)
                    view.window.refresh()
            elif keypress == curses.KEY_LEFT:  # LEFT
                cursor_y, cursor_x = view.window.getyx()
                if cursor_x > 0:
                    view.window.move(cursor_y, cursor_x - 1)
                    view.window.refresh()
            elif keypress == curses.KEY_RIGHT:  # RIGHT
                cursor_y, cursor_x = view.window.getyx()
                if cursor_x < view.window.getmaxyx()[1] - 1:
                    view.window.move(cursor_y, cursor_x + 1)
                    view.window.refresh()
            elif keypress in [curses.KEY_ENTER, 10, 13]:  # ENTER
                break
            elif keypress == 32:  # SPACE
                view.grid[view.window.getyx()].toggle()
                view.draw()

    finally:
        view.window.keypad(0)


def grid_simulate(view: GridView, help_print_func, period: float = 0.1):
    """Simulate the grid."""

    try:
        curses.curs_set(0)

        help_print_func("Press <ctrl+c> to stop the simulation.\n")

        while True:
            view.draw()
            time.sleep(period)
            view.grid.evolve()

    except KeyboardInterrupt:
        pass

    finally:
        curses.curs_set(2)


def run(screen: curses.window, **kwargs):
    try:

        def help_writer(screen: curses.window):
            def writer(help_text: str):
                screen.move(1, 0)
                screen.addstr(help_text)
                screen.refresh()

            return writer

        screen.clear()
        screen.addstr("Welcome to the Game of Life!\n")
        screen.addstr("placeholder_help_string\n")

        game_window = screen.subwin(screen.getyx()[0], 0)
        grid = LifeGrid(*game_window.getmaxyx())
        grid_view = GridView(game_window, grid)

        while True:
            grid_interact(grid_view, help_writer(screen))
            grid_simulate(grid_view, help_writer(screen))

    except KeyboardInterrupt:
        return


def parse_args(args) -> argparse.Namespace:
    """Parse the command line arguments and return the parsed arguments."""
    parser = argparse.ArgumentParser(
        prog=__project__,
        description="Game of life running on a terminal.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    parser.add_argument(
        "-y",
        "--height",
        type=int,
        help="The height of the game grid.",
    )
    parser.add_argument(
        "-x",
        "--width",
        type=int,
        help="The width of the game grid.",
    )

    parser.add_argument(
        "-p",
        "--period",
        type=float,
        help="The period of the simulation in seconds.",
    )

    return parser.parse_args(args)


def main() -> None:
    """This is the main entry point for the command line interface (CLI)"""
    args = parse_args(sys.argv[1:])
    curses.wrapper(run, **vars(args))


if __name__ == "__main__":
    # Users can also run the modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #     python -m gameolife.cli --help
    sys.exit(main())
