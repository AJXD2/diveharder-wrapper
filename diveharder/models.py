from pydantic import BaseModel, Field
from datetime import datetime
import typing
import diveharder.enums as enums


class APIURLConfiguration(BaseModel):
    diveharder: str
    community: str


class GlobalStatistics(BaseModel):
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
    statistics: GlobalStatistics


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

    race: enums.Faction | None
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
