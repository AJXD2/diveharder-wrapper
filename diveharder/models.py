from pydantic import BaseModel, Field
from datetime import datetime
import typing
import diveharder.enums as enums


class APIURLConfiguration(BaseModel):
    diveharder: str
    community: str


class Statistics(BaseModel):
    """The statistics of a player."""

    missions_won: int = Field(alias="missionsWon")
    missions_lost: int = Field(alias="missionsLost")
    mission_time: int = Field(alias="missionTime")
    terminid_kills: int = Field(alias="terminidKills")
    automaton_kills: int = Field(alias="automatonKills")
    illuminate_kills: int = Field(alias="illuminateKills")
    bullets_fired: int = Field(alias="bulletsFired")
    bullets_hit: int = Field(alias="bulletsHit")
    time_played: int = Field(alias="timePlayed")
    deaths: int
    revives: int
    friendlies: int
    mission_success_rate: int = Field(alias="missionSuccessRate")
    accuracy: int
    player_count: int = Field(alias="playerCount")


class WarInfo(BaseModel):
    """The information about the current war."""

    started: datetime
    ended: datetime
    now: datetime
    client_version: str = Field(alias="clientVersion")
    factions: list[typing.Literal["Humans", "Terminids", "Automaton", "Illuminate"]]
    impact_multiplier: float = Field(alias="impactMultiplier")
    statistics: Statistics


class Dispatch(BaseModel):
    """The information about the current war."""

    id: int
    published: datetime
    type: typing.Literal[0]
    message: str


class SteamNews(BaseModel):
    """Steam patchh notes."""

    id: str
    title: str
    url: str
    author: str
    content: str
    published_at: datetime = Field(alias="publishedAt")


# TODO: make better docstrings
class AssignmentTaskData(typing.TypedDict):
    """task data"""

    race: enums.FactionType | None
    target_count: int | None
    # TODO: implement the actual planet
    planet: int | None
    liberate: bool | None


class AssignmentTask(BaseModel):
    """A task in an assignment"""

    type: enums.AssignmentTypes
    values: list[int]
    value_types: list[enums.ValueTypes] = Field(alias="valueTypes")
    data: AssignmentTaskData = AssignmentTaskData(
        liberate=None, planet=None, target_count=None, race=None
    )

    def model_post_init(self, __context: typing.Any) -> None:
        for k, v in zip(self.value_types, self.values):
            if k == enums.ValueTypes.LIBERATE:
                self.data["liberate"] = bool(v)
            else:
                self.data[k.name.lower()] = v  # type: ignore


class AssignmentReward(BaseModel):
    """A reward in an assignment"""

    type: int
    amount: int


class Assignment(BaseModel):
    """An assignment (Major Order)"""

    id: int
    progress: list[int]
    title: str | None = None
    briefing: str | None = None
    description: str | None = None
    tasks: list[AssignmentTask]
    reward: AssignmentReward
    expiration: datetime

    @property
    def is_complete(self) -> bool:
        return self.progress == [1] * len(self.tasks)

    def __str__(self) -> str:
        return f"{self.title} - {self.briefing}"


"""
[
  {
    "index": 0,
    "name": "string",
    "sector": "string",
    "biome": {
      "name": "string",
      "description": "string"
    },
    "hazards": [
      {
        "name": "string",
        "description": "string"
      }
    ],
    "hash": 0,
    "position": {
      "x": 0,
      "y": 0
    },
    "waypoints": [
      0
    ],
    "maxHealth": 0,
    "health": 0,
    "disabled": true,
    "initialOwner": "string",
    "currentOwner": "string",
    "regenPerSecond": 0,
    "event": {
      "id": 0,
      "eventType": 0,
      "faction": "string",
      "health": 0,
      "maxHealth": 0,
      "startTime": "2024-10-12T02:39:12.326Z",
      "endTime": "2024-10-12T02:39:12.326Z",
      "campaignId": 0,
      "jointOperationIds": [
        0
      ]
    },
    "statistics": {
      "missionsWon": 0,
      "missionsLost": 0,
      "missionTime": 0,
      "terminidKills": 0,
      "automatonKills": 0,
      "illuminateKills": 0,
      "bulletsFired": 0,
      "bulletsHit": 0,
      "timePlayed": 0,
      "deaths": 0,
      "revives": 0,
      "friendlies": 0,
      "missionSuccessRate": 0,
      "accuracy": 0,
      "playerCount": 0
    },
    "attacking": [
      0
    ]
  }
]
"""


class Position(BaseModel):
    """A position in the game."""

    x: float
    y: float


class PlanetEvent(BaseModel):
    """An event on a planet."""

    id: int
    event_type: typing.Literal[1]
    faction: enums.FactionType
    health: int
    max_health: int = Field(alias="maxHealth")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    campaign_id: int = Field(alias="campaignId")
    joint_operation_ids: list[int] = Field(alias="jointOperationIds")


class PlanetaryHazard(BaseModel):
    """A hazard on a planet."""

    name: str
    description: str


class Biome(BaseModel):
    """A biome on a planet."""

    name: str
    description: str


class Planet(BaseModel):
    """A planet in the game."""

    index: int
    name: str
    sector: str
    biome: Biome
    hazards: list[PlanetaryHazard]
    hash: int
    position: Position
    waypoints: list[int]
    max_health: int = Field(alias="maxHealth")
    health: int
    disabled: bool
    initial_owner: enums.FactionType = Field(
        alias="initialOwner",
    )
    current_owner: enums.FactionType = Field(alias="currentOwner")
    regen_per_second: float = Field(alias="regenPerSecond")
    event: PlanetEvent | None
    statistics: Statistics
    attacking: list[int]
