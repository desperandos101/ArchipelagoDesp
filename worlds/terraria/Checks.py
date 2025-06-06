from BaseClasses import Item, Location
from typing import Tuple, Union, Set, List, Dict
import string
import pkgutil


class TerrariaItem(Item):
    game = "Terraria"


class TerrariaLocation(Location):
    game = "Terraria"


def add_token(
        tokens: List[Tuple[int, int, Union[str, int, None]]],
        token: Union[str, int],
        token_index: int,
):
    if token == "":
        return
    if type(token) == str:
        tokens.append((token_index, 0, token.rstrip()))
    elif type(token) == int:
        tokens.append((token_index, 1, token))


IDENT = 0
NUM = 1
SEMI = 2
HASH = 3
AT = 4
NOT = 5
AND = 6
OR = 7
LPAREN = 8
RPAREN = 9
END_OF_LINE = 10

CHAR_TO_TOKEN_ID = {
    ";": SEMI,
    "#": HASH,
    "@": AT,
    "~": NOT,
    "&": AND,
    "|": OR,
    "(": LPAREN,
    ")": RPAREN,
}

TOKEN_ID_TO_CHAR = {id: char for char, id in CHAR_TO_TOKEN_ID.items()}


def tokens(rule: str) -> List[Tuple[int, int, Union[str, int, None]]]:
    token_list = []
    token = ""
    token_index = 0
    escaped = False
    for index, char in enumerate(rule):
        if escaped:
            if token == "":
                token_index = index
            token += char
            escaped = False
        elif char == "\\":
            if type(token) == int:
                add_token(token_list, token, token_index)
                token = ""
            escaped = True
        elif char == "/" and token.endswith("/"):
            add_token(token_list, token[:-1], token_index)
            return token_list
        elif token == "" and char.isspace():
            pass
        elif token == "" and char.isdigit():
            token_index = index
            token = int(char)
        elif type(token) == int and char.isdigit():
            token = token * 10 + int(char)
        elif (id := CHAR_TO_TOKEN_ID.get(char)) != None:
            add_token(token_list, token, token_index)
            token_list.append((index, id, None))
            token = ""
        else:
            if token == "":
                token_index = index
            token += char

    add_token(token_list, token, token_index)
    return token_list


NAME = 0
NAME_SEMI = 1
FLAG_OR_SEMI = 2
POST_FLAG = 3
FLAG = 4
FLAG_ARG = 5
FLAG_ARG_END = 6
COND_OR_SEMI = 7
POST_COND = 8
COND = 9
LOC = 10
FN = 11
POST_FN = 12
FN_ARG = 13
FN_ARG_END = 14
END = 15
GOAL = 16

PRE_ITEM_COUNT = 17
POST_ITEM_COUNT = 18

POS_FMT = [
    "name or `#`",
    "`;`",
    "flag or `;`",
    "`;`, `|`, or `(`",
    "flag",
    "text or number",
    "`)`",
    "name, `#`, `@`, `~`, `(`, or `;`",
    "`;`, `&`, `|`, or `)`",
    "name, `#`, `@`, `~`, or `(`",
    "name",
    "name",
    "`(`, `;`, `&`, `|`, or `)`",
    "text or number",
    "`)`",
    "end of line",
    "goal",
    "pre item count",
    "post item count"
]

RWD_NAME = 0
RWD_NAME_SEMI = 1
RWD_FLAG = 2
RWD_FLAG_SEMI = 3
RWD_END = 4
RWD_LABEL = 5

RWD_POS_FMT = ["name or `#`", "`;`", "flag", "`;`", "end of line", "name"]


def unexpected(line: int, char: int, id: int, token, pos, pos_fmt, file):
    if id == IDENT or id == NUM:
        token_fmt = f"`{token}`"
    elif id == END_OF_LINE:
        token_fmt = "end of line"
    else:
        token_fmt = f"`{TOKEN_ID_TO_CHAR[id]}`"

    raise Exception(
        f"in `{file}`, found {token_fmt} at {line + 1}:{char + 1}; expected {pos_fmt[pos]}"
    )


COND_ITEM = 0
COND_LOC = 1
COND_FN = 2
COND_GROUP = 3

quant_locs = [
    "Chest",
    "Orb",
    "Common Enemy",
    "Rare Enemy",
    "Invasion Enemy",
    "Miniboss Enemy"
]


class Condition:
    def __init__(
            self,
            # True = positive, False = negative
            sign: bool,
            # See the `COND_*` constants
            type: int,
            # Condition name or list
            condition: Union[str, Tuple[Union[bool, None], List["Condition"]], Tuple[str, int]],
            argument: Union[str, int, None],
    ):
        self.sign = sign
        self.type = type
        self.condition = condition
        self.argument = argument


class Rule:
    def __init__(
            self,
            name: str,
            # Name to arg
            flags: Dict[str, Union[str, int, None]],
            # True = or, False = and, None = N/A
            operator: Union[bool, None],
            conditions: List[Condition],
    ):
        self.name = name
        self.flags = flags
        self.operator = operator
        self.conditions = conditions


def get_default_item_name(name, flags):
    return flags.get("Item") or name


def get_cond_name(condition):
    if isinstance(condition.condition, tuple):
        return condition.condition[0]
    else:
        return condition.condition





def validate_conditions(
        rule: str,
        rule_indices: dict,
        conditions: List[Condition],
):
    for condition in conditions:
        if condition.type == COND_ITEM:
            cond_name = get_cond_name(condition)
            if cond_name not in rule_indices:
                raise Exception(
                    f"item `{cond_name}` in `{rule}` is not defined"
                )
        elif condition.type == COND_LOC:
            if condition.condition not in rule_indices:
                raise Exception(
                    f"location `{condition.condition}` in `{rule}` is not defined"
                )
        elif condition.type == COND_FN:
            if condition.condition not in {
                "npc",
                "calamity",
                "biome_locks",
                "extra_checks",
                "grindy",
                "pickaxe",
                "hammer",
                "mech_boss",
                "minions",
                "getfixedboi",
                "gear_power",
                "require_boots_jump_hook",
                "require_wings"
            }:
                raise Exception(
                    f"function `{condition.condition}` in `{rule}` is not defined"
                )
        elif condition.type == COND_GROUP:
            _, conditions = condition.condition
            validate_conditions(rule, rule_indices, conditions)


def read_data() -> Tuple[
    # Goal to rule index that ends that goal's range and the locations required
    List[Tuple[int, Set[str]]],
        # Rules
    List[Rule],
        # Rule to rule index
    Dict[str, int],
        # Label to rewards
    Dict[str, List[str]],
        # Reward to flags
    Dict[str, Set[str]],
        # Item name to ID
    Dict[str, int],
        # Location name to ID
    Dict[str, int],
        # Location name to Item name
    Dict[str, str],
        # NPCs
    List[str],
        # Pickaxe to pick power
    Dict[str, int],
        # Hammer to hammer power
    Dict[str, int],
        # Weapon groups to numerical power
    Dict[str, int],
        # Armor groups to numerical power
    Dict[str, int],
        # Accessory groups to numerical power
    Dict[str, int],
        # Mechanical bosses
    List[str],
        # Calamity final bosses
    List[str],
        # Progression rules
    Set[str],
        # Armor to minion count,
    Dict[str, int],
        # Accessory to minion count,
    Dict[str, int],
]:
    next_id = 0x7E0000
    item_name_to_id = {}

    goals = []
    goal_indices = {}
    rules = []
    rule_indices = {}
    loc_to_item = {}

    npcs = []
    pickaxes = {}
    hammers = {}
    weapons = {}
    armor = {}
    accessories = {}
    mech_boss_loc = []
    mech_bosses = []
    final_boss_loc = []
    final_bosses = []
    armor_minions = {}
    accessory_minions = {}

    progression = set()

    for line, rule in enumerate(
            pkgutil.get_data(__name__, "Rules.dsv").decode().splitlines()
    ):
        goal = None
        name = None
        flags = {}

        sign = True
        operator = None
        outer = []
        conditions = []

        pos = NAME
        for char, id, token in tokens(rule):
            if pos == NAME:
                if id == IDENT:
                    name = token
                    pos = NAME_SEMI
                elif id == HASH:
                    pos = GOAL
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == NAME_SEMI:
                if id == SEMI:
                    pos = FLAG_OR_SEMI
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_OR_SEMI:
                if id == IDENT:
                    flag = token
                    pos = POST_FLAG
                elif id == SEMI:
                    pos = COND_OR_SEMI
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_FLAG:
                if id == SEMI:
                    if flag is not None:
                        if flag in flags:
                            raise Exception(
                                f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                            )
                        flags[flag] = None
                        flag = None
                    pos = COND_OR_SEMI
                elif id == OR:
                    pos = FLAG
                elif id == LPAREN:
                    pos = FLAG_ARG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG:
                if id == IDENT:
                    if flag is not None:
                        if flag in flags:
                            raise Exception(
                                f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                            )
                        flags[flag] = None
                        flag = None
                    flag = token
                    pos = POST_FLAG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_ARG:
                if id == IDENT or id == NUM:
                    if flag in flags:
                        raise Exception(
                            f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                        )
                    flags[flag] = token
                    flag = None
                    pos = FLAG_ARG_END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_ARG_END:
                if id == RPAREN:
                    pos = POST_FLAG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == COND_OR_SEMI:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_ITEM, token, None))
                    sign = True
                    pos = POST_COND
                elif id == HASH:
                    pos = LOC
                elif id == AT:
                    pos = FN
                elif id == NOT:
                    sign = not sign
                    pos = COND
                elif id == LPAREN:
                    outer.append((sign, None, conditions))
                    conditions = []
                    sign = True
                    pos = COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_COND:
                if id == SEMI:
                    if outer:
                        raise Exception(
                            f"found `;` at {line + 1}:{char + 1} after unclosed `(`"
                        )
                    pos = END
                elif id == AND:
                    if operator is True:
                        raise Exception(
                            f"found `&` at {line + 1}:{char + 1} in group containing `|`"
                        )
                    operator = False
                    pos = COND
                elif id == OR:
                    if operator is False:
                        raise Exception(
                            f"found `|` at {line + 1}:{char + 1} in group containing `&`"
                        )
                    operator = True
                    pos = COND
                elif id == RPAREN:
                    if not outer:
                        raise Exception(
                            f"found `)` at {line + 1}:{char + 1} without matching `(`"
                        )
                    condition = operator, conditions
                    sign, operator, conditions = outer.pop()
                    conditions.append(Condition(sign, COND_GROUP, condition, None))
                    sign = True
                    pos = POST_COND
                elif id == LPAREN:
                    pos = PRE_ITEM_COUNT
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == PRE_ITEM_COUNT:
                if id == NUM:
                    if token < 1:
                        raise Exception(
                            f"{line + 1}:{char + 1}, '{token}' must be a natural number"
                        )
                    else:
                        temp_cond = conditions.pop(-1)
                        conditions.append(
                            Condition(temp_cond.sign, temp_cond.type, (temp_cond.condition, token), temp_cond.argument))
                        pos = POST_ITEM_COUNT
                else:
                    raise Exception(
                        f"{line + 1}:{char + 1}, non ident token found in parentheses"
                    )
            elif pos == POST_ITEM_COUNT:
                if id == RPAREN:
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == COND:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_ITEM, token, None))
                    sign = True
                    pos = POST_COND
                elif id == HASH:
                    pos = LOC
                elif id == AT:
                    pos = FN
                elif id == NOT:
                    sign = not sign
                elif id == LPAREN:
                    outer.append((sign, operator, conditions))
                    conditions = []
                    sign = True
                    operator = None
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == LOC:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_LOC, token, None))
                    sign = True
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN:
                if id == IDENT:
                    function = token
                    pos = POST_FN
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_FN:
                if id == LPAREN:
                    pos = FN_ARG
                elif id == SEMI:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    pos = END
                elif id == AND:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    sign = True
                    if operator is True:
                        raise Exception(
                            f"found `&` at {line + 1}:{char + 1} in group containing `|`"
                        )
                    operator = False
                    pos = COND
                elif id == OR:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    sign = True
                    if operator is False:
                        raise Exception(
                            f"found `|` at {line + 1}:{char + 1} in group containing `&`"
                        )
                    operator = True
                    pos = COND
                elif id == RPAREN:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    if not outer:
                        raise Exception(
                            f"found `)` at {line + 1}:{char + 1} without matching `(`"
                        )
                    condition = operator, conditions
                    sign, operator, conditions = outer.pop()
                    conditions.append(Condition(sign, COND_GROUP, condition, None))
                    sign = True
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN_ARG:
                if id == IDENT or id == NUM:
                    conditions.append(Condition(sign, COND_FN, function, token))
                    sign = True
                    pos = FN_ARG_END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN_ARG_END:
                if id == RPAREN:
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == END:
                unexpected(line, char, id, token, pos)
            elif pos == GOAL:
                if id == IDENT:
                    goal = token
                    pos = END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")

        if pos != NAME and pos != FLAG_OR_SEMI and pos != COND_OR_SEMI and pos != END:
            unexpected(line, char + 1, END_OF_LINE, None, pos, POS_FMT, "Rules.dsv")

        if name:
            if name in rule_indices:
                raise Exception(
                    f"rule `{name}` on line `{line + 1}` shadows a previous rule"
                )

            def create_new_rule(the_name, the_flags, the_operator, the_conditions):

                rule_indices[the_name] = len(rules)
                new_rule = Rule(the_name, the_flags, the_operator, the_conditions)
                rules.append(new_rule)

            def get_loc_quantity():
                flag_list = flags.keys()
                for loc in quant_locs:
                    if loc in flag_list:
                        return 100
                return 0

            # loc_types_with_quantity = ["Chest", "Orb"]
            # quant_to_return = 0
            # type_found = False
            # for loc_type in loc_types_with_quantity:
            #     if (quantity := flags.get(loc_type)) is not None:
            #         quant_to_return = quantity
            #         if type_found:
            #             raise Exception(f"rule '{name}' on line '{line + 1}' has multiple location flags")
            #         type_found = True
            # return quant_to_return
            quant = get_loc_quantity()
            if quant > 0:
                create_new_rule(name, [], operator, conditions)
                create_new_rule(f"{name} 1", flags, operator, conditions)
                for i in range(1, quant):
                    create_new_rule(f"{name} {i + 1}", flags, operator, conditions)
            else:
                create_new_rule(name, flags, operator, conditions)

            for flag in flags:
                if flag not in {
                    "Location",
                    "Item",
                    "Goal",
                    "Early",
                    "Achievement",
                    "Chest",
                    "Chest Item",
                    "Orb",
                    "Orb Item",
                    "Common Enemy",
                    "Common Enemy Item",
                    "Rare Enemy",
                    "Rare Enemy Item",
                    "Invasion Enemy",
                    "Invasion Enemy Item",
                    "Miniboss Enemy",
                    "Miniboss Enemy Item",
                    "Grindy",
                    "Fishing",
                    "Npc",
                    "Pickaxe",
                    "Hammer",
                    "Minions",
                    "Armor Minions",
                    "Mech Boss",
                    "Final Boss",
                    "Getfixedboi",
                    "Not Getfixedboi",
                    "Calamity",
                    "Not Calamity",
                    "Not Calamity Getfixedboi",
                    "Biome Lock",
                    "Not Biome Lock",
                    "Weather Lock",
                    "Grappling Hook",
                    "Melee",
                    "Ranged",
                    "Magic",
                    "Summoning",
                    "Weapon Power",
                    "Armor Power",
                    "Accessory Power",
                    "Corruption",
                    "Crimson",
                    "Vanity",
                    "Journey",
                }:
                    raise Exception(
                        f"rule `{name}` on line `{line + 1}` has unrecognized flag `{flag}`"
                    )

            if ("Item" in flags
                    or "Chest Item" in flags
                    or "Orb Item" in flags
                    or "Common Enemy Item" in flags
                    or "Rare Enemy Item" in flags
                    or "Invasion Enemy Item" in flags
                    or "Miniboss Enemy Item" in flags
                    or "Biome Lock" in flags
                    or "Not Biome Lock" in flags
                    or "Weather Lock" in flags
                    or "Grappling Hook" in flags):
                item_name = get_default_item_name(name, flags)
                if item_name in item_name_to_id:
                    raise Exception(
                        f"item `{item_name}` on line `{line + 1}` shadows a previous item"
                    )
                item_name_to_id[item_name] = next_id
                next_id += 1
                loc_to_item[name] = item_name
            else:
                loc_to_item[name] = name

            if "Npc" in flags:
                npcs.append(name)

            if (power := flags.get("Pickaxe")) is not None:
                pickaxes[name] = power

            if (power := flags.get("Hammer")) is not None:
                hammers[name] = power

            if (power := flags.get("Weapon Power")) is not None:
                weapons[name] = power

            if (power := flags.get("Armor Power")) is not None:
                armor[name] = power

            if (power := flags.get("Accessory Power")) is not None:
                accessories[name] = power

            if "Mech Boss" in flags:
                item_name_to_id[name] = next_id
                next_id += 1
                mech_bosses.append(name)
                mech_boss_loc.append(name)

            if "Final Boss" in flags:
                final_bosses.append(flags["Item"] or f"Post-{name}")
                final_boss_loc.append(name)

            if (minions := flags.get("Armor Minions")) is not None:
                armor_minions[name] = minions

            if (minions := flags.get("Minions")) is not None:
                accessory_minions[name] = minions

        if goal:
            if goal in goal_indices:
                raise Exception(
                    f"goal `{goal}` on line `{line + 1}` shadows a previous goal"
                )
            goal_indices[goal] = len(goals)
            goals.append((len(rules), set()))

    for rule in rules:
        if "Goal" in rule.flags:
            if (name := rule.flags.get("Goal")) is not None:
                goal_name = name
            else:
                goal_name = (
                    rule.name.translate(str.maketrans("", "", string.punctuation))
                    .replace(" ", "_")
                    .lower()
                )

            _, items = goals[goal_indices[goal_name]]
            items.add(rule.name)

    _, mech_boss_items = goals[goal_indices["mechanical_bosses"]]
    mech_boss_items.update(mech_boss_loc)

    _, final_boss_items = goals[goal_indices["calamity_final_bosses"]]
    final_boss_items.update(final_boss_loc)

    for rule in rules:
        validate_conditions(rule.name, rule_indices, rule.conditions)

    # Will be randomized via `slot_randoms` / `self.multiworld.random`
    label = None
    labels = {}
    rewards = {}

    for line in pkgutil.get_data(__name__, "Rewards.dsv").decode().splitlines():
        reward = None
        flags = set()

        pos = RWD_NAME
        for char, id, token in tokens(line):
            if pos == RWD_NAME:
                if id == IDENT:
                    reward = f"Reward: {token}"
                    pos = RWD_NAME_SEMI
                elif id == HASH:
                    pos = RWD_LABEL
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_NAME_SEMI:
                if id == SEMI:
                    pos = RWD_FLAG
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_FLAG:
                if id == IDENT:
                    if token in flags:
                        raise Exception(
                            f"set flag `{token}` at {line + 1}:{char + 1} that was already set"
                        )
                    flags.add(token)
                    pos = RWD_FLAG_SEMI
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_FLAG_SEMI:
                if id == SEMI:
                    pos = RWD_END
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_END:
                unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_LABEL:
                if id == IDENT:
                    label = token
                    if label in labels:
                        raise Exception(
                            f"started label `{label}` at {line + 1}:{char + 1} that was already used"
                        )
                    labels[label] = []
                    pos = RWD_END
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")

        if pos != RWD_NAME and pos != RWD_FLAG and pos != RWD_END:
            unexpected(line, char + 1, END_OF_LINE, None, pos)

        if reward:
            if reward in rewards:
                raise Exception(
                    f"reward `{reward}` on line `{line + 1}` shadows a previous reward"
                )
            rewards[reward] = flags

            if not label:
                raise Exception(
                    f"reward `{reward}` on line `{line + 1}` is not labeled"
                )
            labels[label].append(reward)

            if reward in item_name_to_id:
                raise Exception(
                    f"item `{reward}` on line `{line + 1}` shadows a previous item"
                )
            item_name_to_id[reward] = next_id
            next_id += 1

    item_name_to_id["Reward: Coins"] = next_id
    next_id += 1

    location_name_to_id = {}

    for rule in rules:
        if ("Location" in rule.flags
                or "Achievement" in rule.flags
                or "Chest" in rule.flags
                or "Orb" in rule.flags
                or "Common Enemy" in rule.flags
                or "Rare Enemy" in rule.flags
                or "Invasion Enemy" in rule.flags
                or "Miniboss Enemy" in rule.flags):
            if rule.name in location_name_to_id:
                raise Exception(f"location `{rule.name}` shadows a previous location")
            location_name_to_id[rule.name] = next_id
            next_id += 1

    return (
        goals,
        rules,
        rule_indices,
        labels,
        rewards,
        item_name_to_id,
        location_name_to_id,
        loc_to_item,
        npcs,
        pickaxes,
        hammers,
        weapons,
        armor,
        accessories,
        mech_bosses,
        final_bosses,
        progression,
        armor_minions,
        accessory_minions,
    )


(
    goals,
    rules,
    rule_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    loc_to_item,
    npcs,
    pickaxes,
    hammers,
    weapons,
    armour,
    accessories,
    mech_bosses,
    final_bosses,
    progression,
    armor_minions,
    accessory_minions,
) = read_data()
