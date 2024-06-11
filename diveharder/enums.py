from enum import Enum

# {"1": "race", "2": "unknown", "3": "goal", "11": "liberate", "12": "planet_index"}


class BetterEnum(Enum):
    @classmethod
    def parse(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class CampaignTypes(BetterEnum):

    LIBERATION_DEFENSE = 0
    RECON = 1
    STORY = 2


class ValueTypes(BetterEnum):
    RACE = 1
    UNKNOWN = 2
    GOAL = 3
    LIBERATE = 11
    PLANET_INDEX = 12


# {
#     "2": "Planet Index"
# }
class Values(BetterEnum):
    PLANET_INDEX = 2


class RewardTypes(BetterEnum):
    MEDALS = 1


# {"3": "Eradicate", "11": "Liberation", "12": "Defense", "13": "Control"}


class MajorOrderTypes(BetterEnum):
    ERADICATE = 3
    LIBERATION = 11
    DEFENSE = 12
    CONTROL = 13


# {"1": "Humans", "2": "Terminids", "3": "Automaton", "4": "Illuminate"}


class Faction(BetterEnum):
    ANY = 0
    HUMANS = 1
    TERMINIDS = 2
    AUTOMATON = 3
    ILLUMINATE = 4
