"""Implements the Game of Life grid."""

from gameolife.cell import Cell


class LifeGrid:
    """The Game of Life grid."""

    def __init__(self, height: int, width: int):
        self._width = width
        self._height = height
        self._grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def evolve(self) -> None:
        """Evolve the grid to the next generation."""

        death_note = []
        life_note = []

        # Iterate over all cells in the grid and gather cells that change state
        for cell in self.__cells():
            alive_neighbors = self.__alive_neighbors(cell)
            if self[cell].alive:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    death_note.append(cell)
            else:
                if alive_neighbors == 3:
                    life_note.append(cell)

        # kill and enliven cells
        for cell in death_note:
            self[cell].kill()
        for cell in life_note:
            self[cell].enliven()

    def __cells(self) -> list[tuple[int, int]]:
        """Return the index for all cells in the grid."""
        for row in range(self._height):
            for col in range(self._width):
                yield (row, col)

    def __neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        """Return the index of neighboring cells of a cell in the grid."""
        DELTAS = [-1, 0, 1]
        x, y = cell
        for dx in DELTAS:
            for dy in DELTAS:
                # Skip the cell itself
                if dx == 0 and dy == 0:
                    continue

                # Offset the index by the deltas
                nx = x + dx
                ny = y + dy

                # Skip if the index is out of bounds
                if not (0 <= nx < self._height) or not (0 <= ny < self._width):
                    continue

                yield (nx, ny)

    def __alive_count(self, cells: list[tuple[int, int]]) -> int:
        """Return the number of alive cells in a list of cells."""
        return sum([1 for cell in cells if self[cell].alive])

    def __alive_neighbors(self, cell: tuple[int, int]) -> int:
        """Return the number of alive neighbors of a cell in the grid."""
        return self.__alive_count(self.__neighbors(cell))

    def __getitem__(self, index) -> Cell:
        """Return the cell at the given index."""
        x, y = index
        return self._grid[x][y]

    def __repr__(self) -> str:
        """Return the string representation of the grid."""
        return repr(self._grid)

    def __str__(self) -> str:
        """Return the pretty string representation of the grid."""
        return "\n".join([" ".join([str(self[(row, col)]) for col in range(self._width)]) for row in range(self._height)])
