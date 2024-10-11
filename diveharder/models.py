from pydantic import BaseModel, Field
from datetime import datetime
import typing


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
