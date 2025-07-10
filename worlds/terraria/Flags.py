import abc
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty
from .Options import TerrariaOptions


class RuleCode(Enum):
    ITEM = 1  # Archipelago Item
    LOCATION = 2  # Archipelago Location
    LOCATION_MULTI = 3  # Multiple Archipelago Locations
    DISPOSE = 4  # Illegal rule
    FORCE_EVENT = 5  # Override other rulecodes and make event
    BUCKET_LIST = 6  # Categorize rule into unique list
    BUCKET_DICT = 7  # Categorize rule into unique dict


def get_flag_dict(options: TerrariaOptions) -> dict[str, None | RuleCode | tuple[RuleCode]]:
    return {"Location": RuleCode.LOCATION,
            "Item": RuleCode.ITEM,
            "Goal": RuleCode.BUCKET_LIST,
            "Achievement": RuleCode.LOCATION if options.normal_achievements.value else RuleCode.DISPOSE,
            "Early": RuleCode.LOCATION if options.early_achievements.value else RuleCode.DISPOSE,
            "Grindy": RuleCode.LOCATION if options.grindy_achievements.value else RuleCode.DISPOSE,
            "Fishing": RuleCode.LOCATION if options.fishing_achievements.value else RuleCode.DISPOSE,
            "Chest": RuleCode.LOCATION_MULTI if options.chest_loot.value else None,
            "Chest Item": RuleCode.ITEM if options.chest_loot.value else None,
            "Orb": RuleCode.LOCATION_MULTI if options.orb_loot.value else None,
            "Orb Item": RuleCode.ITEM if options.orb_loot.value else None,
            "Common Enemy": RuleCode.LOCATION_MULTI if options.enemy_common_drops.value else None,
            "Common Enemy Item": RuleCode.ITEM if options.enemy_common_drops.value else None,
            "Rare Enemy": RuleCode.LOCATION_MULTI if options.enemy_rare_drops.value else None,
            "Rare Enemy Item": RuleCode.ITEM if options.enemy_rare_drops.value else None,
            "Invasion Enemy": RuleCode.LOCATION_MULTI if options.enemy_invasion_drops.value else None,
            "Invasion Enemy Item": RuleCode.ITEM if options.enemy_invasion_drops.value else None,
            "Miniboss Enemy": RuleCode.LOCATION_MULTI if options.enemy_miniboss_drops.value else None,
            "Miniboss Enemy Item": RuleCode.ITEM if options.enemy_miniboss_drops.value else None,
            "Shop": RuleCode.LOCATION_MULTI if options.shop_loot.value else None,
            "Shop Item": RuleCode.ITEM if options.shop_loot.value else None,
            "Npc": {RuleCode.LOCATION, RuleCode.ITEM, RuleCode.BUCKET_LIST} if options.randomize_npcs.value else
            RuleCode.BUCKET_LIST,
            "Guide": {RuleCode.ITEM, RuleCode.BUCKET_LIST} if options.randomize_guide.value else RuleCode.BUCKET_LIST,
            "Slime": RuleCode.BUCKET_LIST,
            "Pet": RuleCode.BUCKET_LIST,
            "Pickaxe": RuleCode.BUCKET_DICT,
            "Hammer": RuleCode.BUCKET_DICT,
            "Minions": RuleCode.BUCKET_DICT,
            "Armor Minions": RuleCode.BUCKET_DICT,
            "Mech Boss": RuleCode.BUCKET_LIST,
            "Final Boss": RuleCode.BUCKET_LIST,
            "Getfixedboi": None if options.getfixedboi.value else RuleCode.DISPOSE,
            "Not Getfixedboi": RuleCode.DISPOSE if options.getfixedboi.value else None,
            "Calamity": None if options.calamity.value else RuleCode.DISPOSE,
            "Not Calamity": RuleCode.DISPOSE if options.calamity.value else None,
            "Not Calamity Getfixedboi": None if not options.calamity.value and options.getfixedboi.value else
            RuleCode.DISPOSE,
            "Biome Lock": RuleCode.ITEM if options.biome_locks.value else None,
            "Not Biome Lock": None if options.biome_locks.value else RuleCode.ITEM,
            "Weather Lock": RuleCode.ITEM if options.weather_locks.value else None,
            "Grappling Hook": RuleCode.ITEM if options.grappling_hook.value else None,
            "Melee": None,
            "Ranged": None,
            "Magic": None,
            "Summoning": None,
            "Weapon Power": None,
            "Armor Power": None,
            "Accessory Power": None,
            "Corruption": RuleCode.DISPOSE if options.toggle_evil.value == 1 else None,
            "Crimson": RuleCode.DISPOSE if options.toggle_evil.value == 0 else None,
            "Vanity": RuleCode.BUCKET_LIST,
            "Journey": RuleCode.ITEM if not options.journey_mode.value else None
            }


arch_id_dict = {"Location": RuleCode.LOCATION,
                "Item": RuleCode.ITEM,
                "Goal": None,
                "Achievement": RuleCode.LOCATION,
                "Early": RuleCode.LOCATION,
                "Grindy": RuleCode.LOCATION,
                "Fishing": RuleCode.LOCATION,
                "Chest": RuleCode.LOCATION_MULTI,
                "Chest Item": RuleCode.ITEM,
                "Orb": RuleCode.LOCATION_MULTI,
                "Orb Item": RuleCode.ITEM,
                "Common Enemy": RuleCode.LOCATION_MULTI,
                "Common Enemy Item": RuleCode.ITEM,
                "Rare Enemy": RuleCode.LOCATION_MULTI,
                "Rare Enemy Item": RuleCode.ITEM,
                "Invasion Enemy": RuleCode.LOCATION_MULTI,
                "Invasion Enemy Item": RuleCode.ITEM,
                "Miniboss Enemy": RuleCode.LOCATION_MULTI,
                "Miniboss Enemy Item": RuleCode.ITEM,
                "Shop": RuleCode.LOCATION_MULTI,
                "Shop Item": RuleCode.ITEM,
                "Npc": {RuleCode.LOCATION, RuleCode.ITEM},
                "Guide": RuleCode.ITEM,
                "Slime": None,
                "Pet": None,
                "Pickaxe": None,
                "Hammer": None,
                "Minions": None,
                "Armor Minions": None,
                "Mech Boss": None,
                "Final Boss": None,
                "Getfixedboi": None,
                "Not Getfixedboi": None,
                "Calamity": None,
                "Not Calamity": None,
                "Not Calamity Getfixedboi": None,
                "Biome Lock": RuleCode.ITEM,
                "Not Biome Lock": RuleCode.ITEM,
                "Weather Lock": RuleCode.ITEM,
                "Grappling Hook": RuleCode.ITEM,
                "Melee": None,
                "Ranged": None,
                "Magic": None,
                "Summoning": None,
                "Weapon Power": None,
                "Armor Power": None,
                "Accessory Power": None,
                "Corruption": None,
                "Crimson": None,
                "Vanity": None,
                "Journey": None
                }


def get_id_code_set(flags: list[str]) -> set[RuleCode]:
    if not isinstance(flags, list):
        raise Exception(f"{type(flags)} passed into get_id_code_set")
    code_set = set()
    for flag in flags:
        if flag not in arch_id_dict.keys():
            raise Exception(f"{flag} not present in arch_id_dict")
        rule_id = arch_id_dict[flag]
        if rule_id is None:
            continue
        elif rule_id in RuleCode.__members__.values():
            if rule_id in code_set:
                raise Exception(f"Attempted to reapply {flag} to rule")
            code_set.add(rule_id)
        elif isinstance(rule_id, set):
            if not rule_id.isdisjoint(code_set):
                raise Exception(f"Attempted to reapply {flag} to rule")
            code_set = code_set.union(rule_id)
        else:
            raise Exception(f"{rule_id} is {type(rule_id)}????")
    return code_set


def get_code_set(arch_dict: dict[str, None | RuleCode | tuple[RuleCode]], flags: list[str]) -> set[RuleCode]:
    if not isinstance(flags, list):
        raise Exception(f"{type(flags)} passed into get_id_code_set")
    code_set = set()
    for flag in flags:
        if flag not in arch_dict.keys():
            raise Exception(f"{flag} not present in arch_id_dict")
        rule_id = arch_dict[flag]
        if rule_id is None:
            continue
        elif rule_id in RuleCode.__members__.values():
            if rule_id in code_set:
                raise Exception(f"Attempted to reapply {flag} to rule")
            code_set.add(rule_id)
        elif isinstance(rule_id, set):
            if not rule_id.isdisjoint(code_set):
                raise Exception(f"Attempted to reapply {flag} to rule")
            code_set = code_set.union(rule_id)
        else:
            raise Exception(f"{rule_id} is {type(rule_id)}????")
    return code_set
