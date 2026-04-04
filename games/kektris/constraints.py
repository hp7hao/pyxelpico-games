from enum import Enum, auto


class BaseEnum(Enum):
    """Base class for enumeration"""

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[int]:
        return [e.value for e in cls]

    @classmethod
    def get_includes(cls) -> list["BaseEnum"]:
        """This used for random figure generation"""
        return [i for i in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return cls._member_names_


class Direction(BaseEnum):
    """Move or rotation directions"""

    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class Orientation(BaseEnum):
    """Block orientation"""

    U = auto()
    L = auto()
    D = auto()
    R = auto()


class CellState(BaseEnum):
    """Possible state of item"""

    CLEAR = auto()
    BLOCK = auto()
    FR0ZEN = auto()


class FigureOrientation(BaseEnum):
    """All figures orientation (by longest flat side faces)"""

    # all orientations of figure I
    I_U = (
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
        (False, False, False, False),
    )
    I_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
    )
    I_D = (
        (False, False, False, False),
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
    )
    I_R = (
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
    )

    # all orientations of figure O
    O = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
    )

    # all orientations of figure J
    J_U = (
        (True, False, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
    )
    J_L = (
        (False, True, True, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
    )
    J_D = (
        (False, False, False, False),
        (True, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
    )
    J_R = (
        (False, True, False, False),
        (False, True, False, False),
        (True, True, False, False),
        (False, False, False, False),
    )

    # all orientations of figure L
    L_U = (
        (False, False, True, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
    )
    L_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
    )
    L_D = (
        (False, False, False, False),
        (True, True, True, False),
        (True, False, False, False),
        (False, False, False, False),
    )
    L_R = (
        (True, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
    )

    # all orientations of figure S
    S_U = (
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
        (False, False, False, False),
    )
    S_L = (
        (False, True, False, False),
        (False, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
    )
    S_D = (
        (False, False, False, False),
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
    )
    S_R = (
        (True, False, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
    )

    # all orientations of figure Z
    Z_U = (
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
    )
    Z_L = (
        (False, False, True, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
    )
    Z_D = (
        (False, False, False, False),
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
    )
    Z_R = (
        (False, True, False, False),
        (True, True, False, False),
        (True, False, False, False),
        (False, False, False, False),
    )

    # all orientations of figure T
    T_U = (
        (False, False, False, False),
        (True, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
    )
    T_L = (
        (False, True, False, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
    )
    T_D = (
        (False, True, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
    )
    T_R = (
        (False, True, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
    )

    @classmethod
    def get_includes(cls) -> list["FigureOrientation"]:
        """This used for random figure generation"""
        includes = [i for i in cls]
        for _ in range(3):
            includes.append(cls.O)
        return includes

    def get_figure_color(self) -> int:
        """Color of figure"""
        match self.name[0]:
            case "I":
                return 8
            case "O":
                return 9
            case "J":
                return 14
            case "L":
                return 11
            case "S":
                return 12
            case "Z":
                return 15
            case "T":
                return 2


# --- Layout constants for 240x240 ---
# Cell: 4px block + 1px gap = 5px stride
# Grid: 34 cells * 5px = 170px + 2px border = 172px
# Grid origin: (4, 4), grid inner: (5, 5) to (174, 174)
# Sidebar: x=178 to 239 (62px wide)

GRID_ORIGIN_X = 4
GRID_ORIGIN_Y = 4
GRID_SIZE = 172  # 34*5 + 2 border
CELL_PX = 4
CELL_STRIDE = 5
GRID_CELLS = 34

# Sidebar positions
SIDEBAR_X = 180

# Next figure preview grid (in sidebar)
NEXT_FIG_GRID_X = list(range(SIDEBAR_X, SIDEBAR_X + 24, 6))
NEXT_FIG_GRID_Y = list(range(115, 139, 6))


GRID_HALF = GRID_CELLS // 2  # 17

# Pre-compute quarter regions at module level (list comprehensions can't see class attrs)
_ARRIVE_TOP = [(x, -4) for x in range(GRID_CELLS)]
_ARRIVE_BOTTOM = [(x, GRID_CELLS) for x in range(GRID_CELLS)]
_ARRIVE_LEFT = [(-4, y) for y in range(GRID_CELLS)]
_ARRIVE_RIGHT = [(GRID_CELLS, y) for y in range(GRID_CELLS)]
_ARRIVE = _ARRIVE_TOP + _ARRIVE_BOTTOM + _ARRIVE_LEFT + _ARRIVE_RIGHT

_LEFT_QUARTER = [(x, y) for x in range(-4, GRID_HALF) for y in range(0, GRID_CELLS)]
_RIGHT_QUARTER = [(x, y) for x in range(GRID_HALF, GRID_CELLS + 3) for y in range(0, GRID_CELLS)]
_BOTTOM_QUARTER = [(x, y) for x in range(0, GRID_CELLS) for y in range(GRID_HALF, GRID_CELLS + 3)]
_TOP_QUARTER = [(x, y) for x in range(0, GRID_CELLS) for y in range(-4, GRID_HALF)]


def get_next_figure_grid_pos() -> list[list[tuple[int, int]]]:
    return [
        [(x + 1, y + 1) for x in NEXT_FIG_GRID_X]
        for y in NEXT_FIG_GRID_Y
    ]


class GameConst:
    """Game constants"""

    ARRIVE_TOP = _ARRIVE_TOP
    ARRIVE_BOTTOM = _ARRIVE_BOTTOM
    ARRIVE_LEFT = _ARRIVE_LEFT
    ARRIVE_RIGHT = _ARRIVE_RIGHT
    ARRIVE = _ARRIVE

    HALF = GRID_HALF
    LEFT_QUARTER = _LEFT_QUARTER
    RIGHT_QUARTER = _RIGHT_QUARTER
    BOTTOM_QUARTER = _BOTTOM_QUARTER
    TOP_QUARTER = _TOP_QUARTER

    NEXT_FIGURE_GRID: tuple[list[int], list[int]] = (
        NEXT_FIG_GRID_X,
        NEXT_FIG_GRID_Y,
    )
    NEXT_FIGURE_GRID_POS: list[list[tuple[int, int]]] = get_next_figure_grid_pos()

    START_FRAME_COUNT: int = 5
    COLOR_TIMOUT: int = 60

    PRIZE_BY_CLEAR: int = 60
    START_CLEAR_LENGTH: int = 6
    MAX_CLEAR_LENGHT: int = 10
    LENGHT_MODIFICATOR: int = 7000
    MAX_GAME_SPEED: int = 22
    GAME_SPEED_LIMIT: int = 30
    SPEED_MODIFICATOR: int = 1000
