from dataclasses import dataclass
from enum import Enum
from rich.table import Table


############################################
# ENUMS
############################################


class Properties(Enum):
    MEDITERRANEAN_AVENUE = "Mediterranean Avenue"
    BALTIC_AVENUE = "Baltic Avenue"
    ORIENTAL_AVENUE = "Oriental Avenue"
    VERMONT_AVENUE = "Vermont Avenue"
    CONNECTICUT_AVENUE = "Connecticut Avenue"
    ST_CHARLES_PLACE = "St. Charles Place"
    STATES_AVENUE = "States Avenue"
    VIRGINIA_AVENUE = "Virginia Avenue"
    ST_JAMES_PLACE = "St. James Place"
    TENNESSEE_AVENUE = "Tennessee Avenue"
    NEW_YORK_AVENUE = "New York Avenue"
    KENTUCY_AVENUE = "Kentucy Avenue"
    INDIANA_AVENUE = "Indiana Avenue"
    ILLINOIS_AVENUE = "Illinois Avenue"
    ATLANTIC_AVENUE = "Atlantic Avenue"
    VENTNOR_AVENUE = "Ventnor Avenue"
    MARVIN_GARDENS = "Marvin Gardens"
    PACIFIC_AVENUE = "Pacific Avenue"
    NORTH_CAROLINA_AVENUE = "North Carolina Avenue"
    PENNSYLVANIA_AVENUE = "Pennsylvania Avenue"
    PARK_PLACE = "Park Place"
    BOARDWALK = "Board Walk"


class Colors(Enum):
    BROWN = "Brown"
    LIGHTBLUE = "Light blue"
    PURPLE = "Purple"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"


############################################
# PROPERTY
############################################


@dataclass
class Property:
    """One of the 28 properties in Monopoly"""

    name: Properties
    color: Colors
    price: int
    house_price: int
    rent: list
    mortgage: int

    def __repr__(self):
        return f"{self.name.value}"

    def table(self):
        table = Table()

        table.add_column("Rent", style="cyan")
        table.add_column("Price", style="red")

        table.add_row("base", f"${self.rent[0]}")
        table.add_row("1 house", f"${self.rent[1]}")
        table.add_row("2 houses", f"${self.rent[2]}")
        table.add_row("3 houses", f"${self.rent[3]}")
        table.add_row("4 houses", f"${self.rent[4]}")
        table.add_row("hotel", f"${self.rent[5]}")

        return table


############################################
# PROPERTIES
############################################


properties = [
    Property(
        Properties.MEDITERRANEAN_AVENUE,
        Colors.BROWN,
        60,
        50,
        [2, 10, 30, 90, 160, 250],
        30,
    ),
    Property(
        Properties.BALTIC_AVENUE,
        Colors.BROWN,
        60,
        50,
        [4, 20, 60, 180, 320, 450],
        30,
    ),
    Property(
        Properties.ORIENTAL_AVENUE,
        Colors.LIGHTBLUE,
        100,
        50,
        [6, 30, 90, 270, 400, 550],
        50,
    ),
    Property(
        Properties.VERMONT_AVENUE,
        Colors.LIGHTBLUE,
        100,
        50,
        [6, 30, 90, 270, 400, 550],
        50,
    ),
    Property(
        Properties.CONNECTICUT_AVENUE,
        Colors.LIGHTBLUE,
        120,
        50,
        [8, 40, 100, 300, 450, 600],
        60,
    ),
    Property(
        Properties.ST_CHARLES_PLACE,
        Colors.PURPLE,
        140,
        100,
        [10, 50, 150, 450, 625, 750],
        70,
    ),
    Property(
        Properties.STATES_AVENUE,
        Colors.PURPLE,
        140,
        100,
        [10, 50, 150, 450, 625, 750],
        70,
    ),
    Property(
        Properties.VIRGINIA_AVENUE,
        Colors.PURPLE,
        160,
        100,
        [12, 60, 180, 500, 700, 900],
        80,
    ),
    Property(
        Properties.ST_JAMES_PLACE,
        Colors.ORANGE,
        180,
        100,
        [14, 70, 200, 550, 750, 950],
        90,
    ),
    Property(
        Properties.TENNESSEE_AVENUE,
        Colors.ORANGE,
        180,
        100,
        [14, 70, 200, 550, 750, 950],
        90,
    ),
    Property(
        Properties.NEW_YORK_AVENUE,
        Colors.ORANGE,
        200,
        100,
        [16, 80, 220, 600, 800, 1000],
        100,
    ),
    Property(
        Properties.KENTUCY_AVENUE,
        Colors.RED,
        220,
        150,
        [18, 90, 250, 700, 875, 1050],
        110,
    ),
    Property(
        Properties.INDIANA_AVENUE,
        Colors.RED,
        220,
        150,
        [18, 90, 250, 700, 875, 1050],
        110,
    ),
    Property(
        Properties.ILLINOIS_AVENUE,
        Colors.RED,
        240,
        150,
        [20, 100, 300, 750, 925, 1100],
        120,
    ),
    Property(
        Properties.ATLANTIC_AVENUE,
        Colors.YELLOW,
        260,
        150,
        [22, 110, 330, 800, 975, 1150],
        130,
    ),
    Property(
        Properties.VENTNOR_AVENUE,
        Colors.YELLOW,
        260,
        150,
        [22, 110, 330, 800, 975, 1150],
        130,
    ),
    Property(
        Properties.MARVIN_GARDENS,
        Colors.YELLOW,
        280,
        150,
        [24, 120, 360, 850, 1025, 1200],
        140,
    ),
    Property(
        Properties.PACIFIC_AVENUE,
        Colors.GREEN,
        300,
        200,
        [26, 130, 390, 900, 1100, 1275],
        150,
    ),
    Property(
        Properties.NORTH_CAROLINA_AVENUE,
        Colors.GREEN,
        300,
        200,
        [26, 130, 390, 900, 1100, 1275],
        150,
    ),
    Property(
        Properties.PENNSYLVANIA_AVENUE,
        Colors.GREEN,
        320,
        200,
        [28, 150, 450, 1000, 1200, 1400],
        160,
    ),
    Property(
        Properties.PARK_PLACE,
        Colors.BLUE,
        350,
        200,
        [35, 175, 500, 1100, 1300, 1500],
        175,
    ),
    Property(
        Properties.BOARDWALK,
        Colors.BLUE,
        400,
        200,
        [50, 200, 600, 1400, 1700, 2000],
        200,
    ),
]
