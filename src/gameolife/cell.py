"""Implements a cell in the Game of Life grid."""

class Cell:
    """A cell in the Game of Life grid.

    Attributes:
        alive (bool): Whether the cell is alive.
    """

    def __init__(self):
        self._alive = False

    @property
    def alive(self) -> bool:
        """bool: Whether the cell is alive."""
        return self._alive

    def kill(self) -> None:
        """Kill the cell."""
        self._alive = False

    def enliven(self) -> None:
        """Enliven the cell."""
        self._alive = True

    def toggle(self) -> None:
        """Toggle the cell's alive state."""
        self._alive = not self._alive

    def __repr__(self) -> str:
        """Return the string representation of the cell."""
        return '1' if self.alive else '0'
    
    def __str__(self) -> str:
        """Return the pretty string representation of the cell."""
        return '♥' if self.alive else '‧'
