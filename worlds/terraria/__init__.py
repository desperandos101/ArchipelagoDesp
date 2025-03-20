# Look at `Rules.dsv` first to get an idea for how this works
import copy
import logging
from typing import Union, Tuple, List, Dict, Set
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, Tutorial, CollectionState
from .Checks import (
    TerrariaItem,
    TerrariaLocation,
    Condition,
    goals,
    rules,
    rule_indices,
    labels,
    rewards,
    item_names,
    location_names,
    loc_to_item,
    get_cond_name,
    COND_ITEM,
    COND_LOC,
    COND_FN,
    COND_GROUP,
    npcs,
    pickaxes,
    hammers,
    weapons,
    armour,
    accessories,
    mech_bosses,
    progression,
    armor_minions,
    accessory_minions,
)
from .Options import TerrariaOptions, Goal


class TerrariaWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Terraria randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Seldom"],
        )
    ]


class TerrariaWorld(World):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """

    game = "Terraria"
    web = TerrariaWeb()
    options_dataclass = TerrariaOptions
    options: TerrariaOptions

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 3

    item_names = item_names
    location_names = location_names
    item_name_to_id = {}
    location_name_to_id = {}
    mult_loc_to_rule = {}

    calamity = False
    getfixedboi = False
    require_optimal_gear = False

    ter_items: List[str]
    ter_locations: List[str]

    ter_goals: Dict[str, str]
    goal_items: Set[str]
    goal_locations: Set[str]

    def is_location(self, flags):
        return ("Location" in flags
                or ("Achievement" in flags and self.any_achievements_enabled)
                or ("Chest" in flags and self.options.chest_loot)
                or ("Orb" in flags and self.options.orb_loot))

    def is_mult_location(self, flags):
        return "Chest" in flags or "Orb" in flags

    def is_item(self, flags):
        allowed_as_rule = ("Item" in flags
                           or ("Chest Item" in flags and self.options.chest_loot)
                           or ("Orb Item" in flags and self.options.orb_loot)
                           or ("Biome Lock" in flags and self.options.biome_locks)
                           or ("Not Biome Lock" in flags and not self.options.biome_locks)
                           or ("Grappling Hook" in flags and self.options.grappling_hook))
        allowed_as_class_item = self.class_acceptable(flags)
        return allowed_as_rule and allowed_as_class_item

    def is_disallowed_enumerable_location(self, flags):
        return (("Orb" in flags and not self.options.orb_loot)
                or ("Chest" in flags and not self.options.chest_loot))

    def class_acceptable(self, flags):
        if ("Melee" not in flags
                and "Ranged" not in flags
                and "Magic" not in flags
                and "Summoning" not in flags):
            return True
        return (self.options.class_preference.value == 0
                or ("Melee" in flags and self.options.class_preference.value == 1)
                or ("Ranged" in flags and self.options.class_preference.value == 2)
                or ("Magic" in flags and self.options.class_preference.value == 3)
                or ("Summoning" in flags and self.options.class_preference.value == 4))

    def is_event(self, flags):
        return not self.is_disallowed_enumerable_location(flags) and not self.is_location(flags) and not self.is_item(
            flags)

    def get_rule(self, rule_name):
        if (base_loc_name := self.mult_loc_to_rule.get(rule_name)) is not None:
            index = rule_indices.get(base_loc_name)
        else:
            index = rule_indices.get(rule_name)
        return rules[index] if index is not None else None

    def any_achievements_enabled(self):
        return (self.options.normal_achievements.value
                or self.options.early_achievements.value
                or self.options.fishing_achievements.value
                or self.options.grindy_achievements.value)

    def extra_checks_enabled(self):
        return (self.options.grindy_achievements
                or self.options.fishing_achievements
                or self.options.normal_achievements
                or self.options.early_achievements
                or self.options.chest_loot)

    def generate_early(self) -> None:
        self.options.goal
        goal_id = self.options.goal.value
        goal, goal_locations = goals[goal_id]
        ter_goals = {}
        goal_items = set()
        for location in goal_locations:
            flags = self.get_rule(location).flags
            if not self.options.calamity.value and "Calamity" in flags:
                logging.warning(
                    f"Terraria goal `{Goal.name_lookup[goal_id]}`, which requires Calamity, was selected with Calamity disabled; enabling Calamity"
                )
                self.options.calamity.value = True

            item = Checks.get_default_item_name(location, flags)
            ter_goals[item] = location
            goal_items.add(item)

        self.calamity = self.options.calamity.value
        self.getfixedboi = self.options.getfixedboi.value

        location_count = 0
        locations = []
        item_count = 0
        items = []
        for rule in rules[:goal]:
            if "Item" in rule.flags:
                name = Checks.get_default_item_name(rule.name, rule.flags)
            else:
                name = rule.name
            prog = False
            if (
                    "Goal" in rule.flags
                    or "Pickaxe" in rule.flags
                    or "Hammer" in rule.flags
                    or "Mech Boss" in rule.flags
                    or "Final Boss" in rule.flags
                    or (self.any_achievements_enabled
                        and ("Npc" in rule.flags
                             or "Minions" in rule.flags
                             or "Armor Minions" in rule.flags))
            ):
                progression.add(name)
                prog = True
            if prog or self.is_location(rule.flags):
                self.mark_progression(
                    rule.conditions
                )

        next_id = 0x7E0000

        for rule in rules[:goal]:
            early = "Early" in rule.flags
            grindy = "Grindy" in rule.flags
            fishing = "Fishing" in rule.flags

            if (
                    (not self.getfixedboi and "Getfixedboi" in rule.flags)
                    or (self.getfixedboi and "Not Getfixedboi" in rule.flags)
                    or (not self.calamity and "Calamity" in rule.flags)
                    or (self.calamity and "Not Calamity" in rule.flags)
                    or (
                            self.getfixedboi
                            and self.calamity
                            and "Not Calamity Getfixedboi" in rule.flags
                    )
                    or (not self.options.early_achievements.value and early)
                    or (
                            not self.options.normal_achievements.value
                            and "Achievement" in rule.flags
                            and not early
                            and not grindy
                            and not fishing
                    )
                    or (not self.options.grindy_achievements.value and grindy)
                    or (not self.options.fishing_achievements.value and fishing)
            ) and rule.name not in goal_locations:
                continue

            for condition in rule.conditions:
                if isinstance(condition.condition, tuple) and type(condition.condition[0]) is str:
                    progressive_item = condition.condition[0]
                    item_count = condition.condition[1]
                    current_item_count = items.count(progressive_item)
                    while current_item_count < item_count:
                        items.append(progressive_item)
                        current_item_count += 1

            if self.is_location(rule.flags):
                # Location
                if self.is_mult_location(rule.flags):
                    counter = 1
                    quant = self.options.epic_number.value
                    while counter <= quant:
                        new_name = f"{rule.name} {counter}"
                        location_count += 1
                        self.location_name_to_id[new_name] = next_id
                        next_id += 1
                        locations.append(new_name)
                        self.mult_loc_to_rule[new_name] = rule.name
                        counter += 1
                else:
                    location_count += 1
                    self.location_name_to_id[rule.name] = next_id
                    next_id += 1
                    locations.append(rule.name)

            if self.is_item(rule.flags) and not (
                    "Achievement" in rule.flags and rule.name not in goal_locations
            ):
                # Item
                item_name = rule.flags.get("Item") or rule.name
                item_count += 1
                self.item_name_to_id[item_name] = next_id
                next_id += 1
                if rule.name not in goal_locations:
                    items.append(item_name)

            if self.is_event(rule.flags):
                # Event
                self.item_name_to_id[rule.name] = next_id
                next_id += 1
                self.location_name_to_id[rule.name] = next_id
                next_id += 1
                items.append(rule.name)
                locations.append(rule.name)

        fill_checks = self.options.fill_extra_checks_with.value
        ordered_rewards = [
            reward
            for reward in labels["ordered"]
            if self.calamity or "Calamity" not in rewards[reward]
        ]
        while fill_checks == 1 and item_count < location_count and ordered_rewards:
            reward = ordered_rewards.pop(0)
            items.append(reward)
            self.item_name_to_id[reward] = next_id
            next_id += 1
            item_count += 1

        random_rewards = [
            reward
            for reward in labels["random"]
            if self.calamity or "Calamity" not in rewards[reward]
        ]
        self.multiworld.random.shuffle(random_rewards)
        while fill_checks == 1 and item_count < location_count and random_rewards:
            reward = (random_rewards.pop(0))
            items.append(reward)
            self.item_name_to_id[reward] = next_id
            next_id += 1
            item_count += 1

        while item_count < location_count:
            reward = "Reward: Coins"
            items.append(reward)
            self.item_name_to_id[reward] = next_id
            next_id += 1
            item_count += 1

        self.ter_items = items
        self.ter_locations = locations

        self.ter_goals = ter_goals
        self.goal_items = goal_items
        self.goal_locations = goal_locations

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)

        for location in self.ter_locations:
            menu.locations.append(
                TerrariaLocation(
                    self.player, location, self.location_name_to_id.get(location), menu
                )
            )

        self.multiworld.regions.append(menu)

    def create_item(self, item: str) -> TerrariaItem:
        if item in progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return TerrariaItem(item, classification, self.item_name_to_id.get(item), self.player)

    def create_items(self) -> None:
        for item in self.ter_items:
            if (rule := self.get_rule(item)) is not None:
                if self.is_item(rule.flags):
                    name = Checks.get_default_item_name(item, rule.flags)
                else:
                    continue
            else:
                name = item

            self.multiworld.itempool.append(self.create_item(name))

        locked_items = {}

        for location in self.ter_locations:
            rule = self.get_rule(location)
            if self.is_event(rule.flags):
                if location in progression:
                    classification = ItemClassification.progression
                else:
                    classification = ItemClassification.useful

                locked_items[location] = TerrariaItem(
                    location, classification, self.location_name_to_id[location], self.player
                )

        for item, location in self.ter_goals.items():
            locked_items[location] = self.create_item(item)
        for location, item in locked_items.items():
            self.multiworld.get_location(location, self.player).place_locked_item(item)

    def check_condition(self, state, condition: Condition) -> bool:
        if condition.type == COND_ITEM:

            item_count = 1
            if isinstance(condition.condition, tuple):
                cond_name = condition.condition[0]
                item_count = condition.condition[1]
            else:
                cond_name = condition.condition

            rule = self.get_rule(cond_name)
            if self.is_item(rule.flags):
                name = Checks.get_default_item_name(cond_name, rule.flags)
            else:
                name = cond_name

            return condition.sign == state.has(name, self.player, item_count)
        elif condition.type == COND_LOC:
            rule = self.get_rule(condition.condition)
            return condition.sign == self.check_conditions(
                state, rule.operator, rule.conditions
            )
        elif condition.type == COND_FN:
            if condition.condition == "npc":
                if type(condition.argument) is not int:
                    raise Exception("@npc requires an integer argument")

                npc_count = 0
                for npc in npcs:
                    if state.has(npc, self.player):
                        npc_count += 1
                        if npc_count >= condition.argument:
                            return condition.sign

                return not condition.sign
            elif condition.condition == "calamity":
                return condition.sign == self.calamity
            elif condition.condition == "biome_locks":
                return condition.sign == self.options.biome_locks.value
            elif condition.condition == "grindy":
                return condition.sign == self.options.grindy_achievements.value
            elif condition.condition == "extra_checks":
                return condition.sign == self.extra_checks_enabled()
            elif condition.condition == "require_boots_jump_hook":
                return condition.sign == self.options.require_boots_jump_hook
            elif condition.condition == "require_wings":
                return condition.sign == self.options.require_wings
            elif condition.condition == "pickaxe":
                if type(condition.argument) is not int:
                    raise Exception("@pickaxe requires an integer argument")

                for pickaxe, power in pickaxes.items():
                    if power >= condition.argument and state.has(pickaxe, self.player):
                        return condition.sign

                return not condition.sign
            elif condition.condition == "hammer":
                if type(condition.argument) is not int:
                    raise Exception("@hammer requires an integer argument")

                for hammer, power in hammers.items():
                    if power >= condition.argument and state.has(hammer, self.player):
                        return condition.sign

                return not condition.sign
            elif condition.condition == "gear_power":
                if not self.require_optimal_gear:
                    return True
                if type(condition.argument) is not int:
                    raise Exception("@gear_power requires an integer argument")

                adequate_weapons = False
                adequate_armor = False
                adequate_accessories = False

                def power_met(group, level):
                    rule = self.get_rule(group)
                    flags = rule.flags
                    if (level >= condition.argument
                            and self.check_conditions(state, True, rule.conditions)
                            and self.class_acceptable(flags)):
                        return True

                for weapon_group, power in weapons.items():
                    if power_met(weapon_group, power):
                        adequate_weapons = True
                        break

                for armor_group, power in armour.items():
                    if power_met(armor_group, power):
                        adequate_armor = True
                        break

                for accessory_group, power in accessories.items():
                    if power_met(accessory_group, power):
                        adequate_accessories = True
                        break

                return adequate_weapons and adequate_armor and adequate_accessories

            elif condition.condition == "mech_boss":
                if type(condition.argument) is not int:
                    raise Exception("@mech_boss requires an integer argument")

                boss_count = 0
                for boss in mech_bosses:
                    if state.has(boss, self.player):
                        boss_count += 1
                        if boss_count >= condition.argument:
                            return condition.sign

                return not condition.sign
            elif condition.condition == "minions":
                if type(condition.argument) is not int:
                    raise Exception("@minions requires an integer argument")

                minion_count = 1
                for armor, minions in armor_minions.items():
                    if state.has(armor, self.player) and minions + 1 > minion_count:
                        minion_count = minions + 1
                        if minion_count >= condition.argument:
                            return condition.sign

                for accessory, minions in accessory_minions.items():
                    if state.has(accessory, self.player):
                        minion_count += minions
                        if minion_count >= condition.argument:
                            return condition.sign

                return not condition.sign
            elif condition.condition == "getfixedboi":
                return condition.sign == self.getfixedboi
            else:
                raise Exception(f"Unknown function {condition.condition}")
        elif condition.type == COND_GROUP:
            operator, conditions = condition.condition
            return condition.sign == self.check_conditions(state, operator, conditions)

    def check_conditions(
            self,
            state,
            operator: Union[bool, None],
            conditions: List[
                Tuple[
                    bool,
                    int,
                    Union[str, Tuple[Union[bool, None], list]],
                    Union[str, int, None],
                ]
            ],
    ) -> bool:
        if operator is None:
            if len(conditions) == 0:
                return True
            if len(conditions) > 1:
                raise Exception("Found multiple conditions without an operator")
            return self.check_condition(state, conditions[0])
        elif operator:
            return any(
                self.check_condition(state, condition) for condition in conditions
            )
        else:
            return all(
                self.check_condition(state, condition) for condition in conditions
            )

    def mark_progression(
            self,
            conditions: List[Condition],
    ):
        for condition in conditions:
            if condition.type == COND_ITEM:
                cond_name = get_cond_name(condition)
                prog = cond_name in progression
                progression.add(loc_to_item[cond_name])
                rule = self.get_rule(cond_name)
                if (
                        not prog
                        and self.is_event(rule.flags)
                ):
                    self.mark_progression(
                        rule.conditions
                    )
            elif condition.type == COND_LOC:
                self.mark_progression(
                    self.get_rule(condition.condition).conditions
                )
            elif condition.type == COND_FN:
                if condition.condition == "gear_power":
                    def minimum_progression_group(item_group_list):  # In truth, it returns the first valid group
                        # in the set.
                        for item_group, level in item_group_list.items():
                            flags = self.get_rule(item_group).flags
                            if (level >= condition.argument
                                    and self.class_acceptable(flags)):
                                return item_group

                    self.mark_progression(self.get_rule(minimum_progression_group(weapons)).conditions)
                    self.mark_progression(self.get_rule(minimum_progression_group(armour)).conditions)
                    self.mark_progression(self.get_rule(minimum_progression_group(accessories)).conditions)
            elif condition.type == COND_GROUP:
                _, conditions = condition.condition
                self.mark_progression(conditions)

    def set_rules(self) -> None:
        for location in self.ter_locations:
            def check(state: CollectionState, location=location):
                rule = self.get_rule(location)
                return self.check_conditions(state, rule.operator, rule.conditions)

            self.multiworld.get_location(location, self.player).access_rule = check

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
            self.goal_items, self.player
        )

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "goal": list(self.goal_locations),
            "deathlink": bool(self.options.death_link),
            # The rest of these are included for trackers
            "calamity": self.options.calamity.value,
            "getfixedboi": self.options.getfixedboi.value,
            "events_as_items": int(self.options.events_as_items.value),
            "biome_locks": bool(self.options.biome_locks.value),
            "chest_loot": bool(self.options.chest_loot.value),
            "grappling_hook_rando": bool(self.options.grappling_hook.value),
            "early_achievements": self.options.early_achievements.value,
            "normal_achievements": self.options.normal_achievements.value,
            "grindy_achievements": self.options.grindy_achievements.value,
            "fishing_achievements": self.options.fishing_achievements.value,
        }
