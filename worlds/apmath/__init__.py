from BaseClasses import Region, Entrance, Tutorial, ItemClassification, Location, Item
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from Options import PerGameCommonOptions


class APMathWorld(World):
    """
    AP Math is a digital workbook
    """
    game = "AP Math"
    options_dataclass = PerGameCommonOptions

    items = ["Value of a", "Value of b", "Value of c", "Value of d"]
    item_name_to_id = {
        "Value of a": 11,
        "Value of b": 12,
        "Value of c": 13,
        "Value of d": 14,
        "Filler :)": 15,
    }
    location_name_to_id = {
        "Problem 0": 1,
        "Problem 1": 2,
        "Problem 2": 3,
        "Problem 3": 4,
        "Problem 4": 5,
    }
    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        problems = Region("Problems", self.player, self.multiworld)
        problems.locations += [
            Location(self.player, "Problem 0", 1, problems),
            Location(self.player, "Problem 1", 2, problems),
            Location(self.player, "Problem 2", 3, problems),
            Location(self.player, "Problem 3", 4, problems),
            Location(self.player, "Problem 4", 5, problems)
        ]
        connection = Entrance(self.player, "New Problems", menu)
        menu.exits.append(connection)
        connection.connect(problems)
        self.multiworld.regions += [menu, problems]

    def create_items(self):
        self.multiworld.itempool.append(Item("Value of a", ItemClassification.progression, 11, self.player))
        self.multiworld.itempool.append(Item("Value of b", ItemClassification.progression, 12, self.player))
        self.multiworld.itempool.append(Item("Value of c", ItemClassification.progression, 13, self.player))
        self.multiworld.itempool.append(Item("Value of d", ItemClassification.progression, 14, self.player))
        self.multiworld.itempool.append(Item("Filler :)", ItemClassification.filler, 15, self.player))

    def set_rules(self):
        set_rule(self.multiworld.get_location("Problem 1", self.player),
                 lambda state: state.has("Value of a", self.player))
        set_rule(self.multiworld.get_location("Problem 2", self.player),
                 lambda state: state.has("Value of b", self.player))
        set_rule(self.multiworld.get_location("Problem 3", self.player),
                 lambda state: state.has("Value of c", self.player))
        set_rule(self.multiworld.get_location("Problem 4", self.player),
                 lambda state: state.has("Value of d", self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all_counts(
            {
                "Value of a": 1,
                "Value of b": 1,
                "Value of c": 1,
                "Value of d": 1
            }, self.player
        )
