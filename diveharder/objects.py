from datetime import datetime
import re
from typing import Any, List, Optional
from diveharder.enums import (
    CampaignTypes,
    Faction,
    MajorOrderTypes,
    RewardTypes,
    ValueTypes,
)
from diveharder.utils import hdml_to_md


class BaseObject:
    """
    Base class for all other DiveHarder API objects.
    """

    def __init__(self, client) -> None:
        """
        Initializes a new instance of the BaseObject class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
        """
        from diveharder import DiveHarderApiClient

        self.client: DiveHarderApiClient = client

    @classmethod
    def from_json(cls, client, json):
        """
        Creates a new instance of the class based on the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json: The JSON data used to create the object.

        Returns:
            The newly created object.
        """
        return cls(client, **json)

    def __getitem__(self, item):
        """
        Gets the value of the specified attribute.

        Args:
            item: The name of the attribute.

        Returns:
            The value of the specified attribute.
        """
        return getattr(self, item)

    def __delitem__(self, item):
        """
        Deletes the specified attribute.

        Args:
            item: The name of the attribute to delete.
        """
        delattr(self, item)

    def __setitem__(self, item, value):
        """
        Sets the value of the specified attribute.

        Args:
            item: The name of the attribute.
            value: The value to set.
        """
        setattr(self, item, value)

    def __iter__(self):
        """
        Returns an iterator over the attributes of the object.

        Returns:
            An iterator over the attributes of the object.
        """
        return iter(self.__dict__)

    def __len__(self):
        """
        Returns the number of attributes of the object.

        Returns:
            The number of attributes of the object.
        """
        return len(self.__dict__)

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            The string representation of the object.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class HDMLString(BaseObject):
    def __init__(self, client, text: str) -> None:
        """
        Initializes a new instance of the HDMLString class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            text: The HDML string.
        """
        super().__init__(client)
        self.text = text

    @property
    def as_plaintext(self) -> str:
        """
        Returns the plain text content of the HDML string.

        Returns:
            str: The plain text content of the HDML string.
        """
        return re.sub(r"<.*?>", "", self.text)

    @property
    def as_md(self) -> str:
        """
        Returns the Markdown content of the HDML string.

        Returns:
            str: The Markdown content of the HDML string.
        """
        return hdml_to_md(self.text)

    def __str__(self) -> str:
        return self.as_plaintext


class PlanetStatistics(BaseObject):
    def __init__(
        self,
        client,
        missions_won: int,
        missions_lost: int,
        mission_time: int,
        bug_kills: int,
        automaton_kills: int,
        illuminate_kills: int,
        bullets_fired: int,
        bullets_hit: int,
        time_played: int,
        deaths: int,
        revives: int,
        friendlies: int,
        mission_success_rate: int,
        accurracy: int,
        planet_index: int,
    ) -> None:
        """
        A class used to represent the statistics of a planet.

        Args:
            client (DiveHarderApiClient): The client object used to make API requests.
            missions_won (int): The number of missions won.
            missions_lost (int): The number of missions lost.
            mission_time (int): The total time spent on missions.
            bug_kills (int): The number of bug kills.
            automaton_kills (int): The number of automaton kills.
            illuminate_kills (int): The number of illuminate kills.
            bullets_fired (int): The number of bullets fired.
            bullets_hit (int): The number of bullets hit.
            time_played (int): The total time played.
            deaths (int): The number of deaths.
            revives (int): The number of revives.
            friendlies (int): The number of friendly kills.
            mission_success_rate (int): The success rate of missions.
            accuracy (int): The accuracy of bullets.
            planet_index (int): The index of the planet.

        Returns:
            None
        """
        super().__init__(client)

        self.missions_won = missions_won
        self.missions_lost = missions_lost
        self.mission_time = mission_time
        self.bug_kills = bug_kills
        self.automaton_kills = automaton_kills
        self.illuminate_kills = illuminate_kills
        self.bullets_fired = bullets_fired
        self.bullets_hit = bullets_hit
        self.time_played = time_played
        self.deaths = deaths
        self.revives = revives
        self.friendlies = friendlies
        self.mission_success_rate = mission_success_rate
        self.accurracy = accurracy
        self._planet_index = planet_index

    @property
    def planet(self) -> "Planet":
        return self.client.planets[self._planet_index]

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client,
            json["missionsWon"],
            json["missionsLost"],
            json["missionTime"],
            json["bugKills"],
            json["automatonKills"],
            json["illuminateKills"],
            json["bulletsFired"],
            json["bulletsHit"],
            json["timePlayed"],
            json["deaths"],
            json["revives"],
            json["friendlies"],
            json["missionSuccessRate"],
            json["accurracy"],
            json["planetIndex"],
        )


class GalaxyStatistics(BaseObject):
    def __init__(
        self,
        client,
        missions_won: int,
        missions_lost: int,
        mission_time: int,
        bug_kills: int,
        automaton_kills: int,
        illuminate_kills: int,
        bullets_fired: int,
        bullets_hit: int,
        time_played: int,
        deaths: int,
        revives: int,
        friendlies: int,
        mission_success_rate: int,
        accuracy: int,
    ) -> None:
        """
        A class used to represent the statistics of the galaxy (global statistics).

        Args:
            client (DiveHarderApiClient): The client object used to make API requests.
            missions_won (int): The number of missions won.
            missions_lost (int): The number of missions lost.
            mission_time (int): The total time spent on missions.
            bug_kills (int): The number of bug kills.
            automaton_kills (int): The number of automaton kills.
            illuminate_kills (int): The number of illuminate kills.
            bullets_fired (int): The number of bullets fired.
            bullets_hit (int): The number of bullets hit.
            time_played (int): The total time played.
            deaths (int): The number of deaths.
            revives (int): The number of revives.
            friendlies (int): The number of friendly kills.
            mission_success_rate (int): The success rate of missions.
            accuracy (int): The accuracy of bullets.

        Returns:
            None
        """

        super().__init__(client)

        self.missions_won = missions_won
        self.missions_lost = missions_lost
        self.mission_time = mission_time
        self.bug_kills = bug_kills
        self.automaton_kills = automaton_kills
        self.illuminate_kills = illuminate_kills
        self.bullets_fired = bullets_fired
        self.bullets_hit = bullets_hit
        self.time_played = time_played
        self.deaths = deaths
        self.revives = revives
        self.friendlies = friendlies
        self.mission_success_rate = mission_success_rate
        self.accurracy = accuracy

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client,
            json["missionsWon"],
            json["missionsLost"],
            json["missionTime"],
            json["bugKills"],
            json["automatonKills"],
            json["illuminateKills"],
            json["bulletsFired"],
            json["bulletsHit"],
            json["timePlayed"],
            json["deaths"],
            json["revives"],
            json["friendlies"],
            json["missionSuccessRate"],
            json["accurracy"],
        )


class GlobalStatistics(BaseObject):
    def __init__(
        self,
        client,
        galaxy_statistics: GalaxyStatistics,
        planet_statistics: List[PlanetStatistics],
    ) -> None:
        """
        Initializes a new instance of the GlobalStatistics class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            galaxy_statistics (GalaxyStatistics): The statistics of the galaxy.
            planet_statistics (List[PlanetStatistics]): The statistics of the planets.

        Returns:
            None
        """
        super().__init__(client)
        self.galaxy_statistics = galaxy_statistics
        self.planet_statistics = planet_statistics


class PlanetInfo(BaseObject):
    """
    Represents a planet's information.
    """

    def __init__(
        self,
        client,
        index: int,
        settings_hash: int,
        position: dict,
        waypoints: list[int],
        sector: int,
        max_health: int,
        disabled: bool,
        initial_owner: int,
    ) -> None:
        """
        Initializes a new instance of the PlanetInfo class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            index (int): The index of the planet.
            settings_hash (int): The settings hash of the planet.
            position (dict): The position of the planet.
            waypoints (List[int]): The waypoints of the planet.
            sector (int): The sector of the planet.
            max_health (int): The maximum health of the planet.
            disabled (bool): Whether the planet is disabled.
            initial_owner (int): The initial owner of the planet.

        Returns:
            None
        """
        super().__init__(client)

        self._index = index
        self.settings_hash = settings_hash
        self.position = position
        self.waypoints = waypoints
        self.sector = sector
        self.max_health = max_health
        self.disabled = disabled
        self.initial_owner = Faction.parse(initial_owner)

    @property
    def planet(self) -> "Planet":
        """
        Returns the planet associated with this planet info.

        Returns:
            Planet: The planet associated with this planet info.
        """
        return self.client.planets[self._index]

    @classmethod
    def from_json(cls, client, json) -> "PlanetInfo":
        """
        Creates a new PlanetInfo instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict[str, Any]): The JSON data representing the planet info.

        Returns:
            PlanetInfo: The created PlanetInfo instance.
        """
        return cls(
            client,
            index=json["index"],
            settings_hash=json["settingsHash"],
            position=json["position"],
            waypoints=json["waypoints"],
            sector=json["sector"],
            max_health=json["maxHealth"],
            disabled=json["disabled"],
            initial_owner=json["initialOwner"],
        )


class HomeWorldInfo(BaseObject):
    """
    Represents information about a home world.

    Attributes:
        race (Faction): The race of the home world.
        planets (List[Planet]): The planets associated with the home world.
    """

    def __init__(self, client, race: int, planets: List[int]) -> None:
        """
        Initializes a HomeWorldInfo object with the given parameters.

        Args:
            client: The client object.
            race (int): The race of the home world.
            planets (List[int]): The indices of the planets associated with the home world.
        """
        super().__init__(client)

        self.race = Faction.parse(race)
        self._planet_ids = planets

    @property
    def planets(self) -> List["Planet"]:
        """
        Returns the planets associated with the home world.

        Returns:
            List[Planet]: The planets associated with the home world.
        """
        return [self.client.planets[id] for id in self._planet_ids]

    @classmethod
    def from_json(cls, client, json) -> "HomeWorldInfo":
        """
        Creates a new HomeWorldInfo instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict[str, Any]): The JSON data representing the home world info.

        Returns:
            HomeWorldInfo: The created HomeWorldInfo instance.
        """
        return cls(
            client,
            race=json["race"],
            planets=json["planetIndices"],
        )


class WarInfo(BaseObject):
    """
    Represents information about a war.

    Args:
        client: The client object.
        war_id (int): The ID of the war.
        start_date (datetime): The start date of the war.
        end_date (datetime): The end date of the war.
        layout_version (int): The version of the layout.
        minimum_client_version (str): The minimum client version required.
        planet_infos (List[PlanetInfo]): A list of PlanetInfo objects.
        home_worlds (List[HomeWorldInfo]): A list of HomeWorldInfo objects.
        capital_infos (List[Any]): A list of capital information.
        planet_permanent_effects (List[Any]): A list of permanent effects on planets.
    """

    def __init__(
        self,
        client,
        war_id: int,
        start_date: datetime,
        end_date: datetime,
        layout_version: int,
        minimum_client_version: str,
        planet_infos: List[PlanetInfo],
        home_worlds: List[HomeWorldInfo],
        capital_infos: List[Any],
        planet_permanent_effects: List[Any],
    ) -> None:
        super().__init__(client)
        self.war_id = war_id
        self._start_date = start_date
        self._end_date = end_date
        self.layout_version = layout_version
        self.minimum_client_version = minimum_client_version
        self.planet_infos = planet_infos
        self.home_worlds = home_worlds
        self.capital_infos = capital_infos
        self.planet_permanent_effects = planet_permanent_effects

    @property
    def start_date(self) -> datetime:
        """
        Gets the start date of the war.

        Returns:
            datetime: The start date of the war.
        """
        return datetime.fromtimestamp(self._start_date)

    @property
    def end_date(self) -> datetime:
        """
        Gets the end date of the war.

        Returns:
            datetime: The end date of the war.
        """
        return datetime.fromtimestamp(self._end_date)

    @classmethod
    def from_json(cls, client, json) -> "WarInfo":
        """
        Creates a new WarInfo instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict[str, Any]): The JSON data representing the war info.

        Returns:
            WarInfo: The created WarInfo instance.
        """
        planets_info = [
            PlanetInfo.from_json(client, info) for info in json["planetInfos"]
        ]
        home_worlds_info = [
            HomeWorldInfo.from_json(client, info) for info in json["homeWorlds"]
        ]

        return cls(
            client,
            json["warId"],
            json["startDate"],
            json["endDate"],
            json["layoutVersion"],
            json["minimumClientVersion"],
            planets_info,
            home_worlds_info,
            json["capitalInfos"],
            json["planetPermanentEffects"],
        )


class Update(BaseObject):
    """
    Represents a steam update.

    Attributes:
        title (str): The title of the update.
        url (str): The URL of the update.
        contents (HDMLString): The contents of the update.
        date (datetime): The date and time the update was published.
    """

    def __init__(self, client, title: str, url: str, contents: str, date: str) -> None:
        super().__init__(client)
        self.title = title
        self.url = url
        self.contents = HDMLString(self.client, contents)
        self.date = datetime.strptime(date, "%d-%b-%Y %H:%M")


class Dispatch(BaseObject):
    """
    Represents a dispatch (news feed).

    Attributes:
        id (int): The ID of the dispatch message.
        published (datetime): The date and time the message was published.
        type (int): The type of the dispatch message.
        tagIds (list[int]): A list of tag IDs associated with the message.
        message (str): The content of the message.
    """

    def __init__(
        self,
        client,
        id: int,
        published: int,
        type: int,
        tagIds: list[int],
        message: str,
    ):
        """
        Initializes a new instance of the Dispatch class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the dispatch message.
            published (datetime): The time of when the message was published.
            type (int): The type of the dispatch message.
            tagIds (list): A list of tag IDs associated with the message.
            message (str): The content of the message.
        """
        super().__init__(client)

        self.id = id
        self.published = datetime.fromtimestamp(self.client.fix_timestamp(published))
        self.type = type
        self.tagIds = tagIds
        self.message = HDMLString(self.client, message)


class MajorOrderReward(BaseObject):
    """
    Represents a reward for a Major Order.
    """

    def __init__(
        self,
        client,
        id: int,
        type: int,
        amount: int,
    ):
        """
        Initializes a new instance of the MajorOrderReward class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the reward.
            type (int): The type of the reward.
            amount (int): The amount of the reward.
        """
        super().__init__(client)

        self.id = id
        self.type = RewardTypes(type)
        self.amount = amount

    def __str__(self) -> str:
        return f"MajorOrderReward({self.amount} {self.type.name})"


class MajorOrderSettings(BaseObject):
    """
    Represents the settings of a Major Order.
    """

    def __init__(
        self,
        client,
        type: int,
        title: str,
        brief: str,
        description: str,
        reward: MajorOrderReward,
    ):
        """
        Initializes a new instance of the MajorOrderSettings class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            type (int): The type of the Major Order.
            title (str): The title of the Major Order.
            brief (str): The brief description of the Major Order.
            description (str): The full description of the Major Order.
            reward (MajorOrderReward): The reward for completing the Major Order.
        """
        super().__init__(client)

        self.type = type
        self.title = HDMLString(self.client, title)
        self.brief = HDMLString(self.client, brief)
        self.description = HDMLString(self.client, description)
        self.reward = reward


class MajorOrderTask(BaseObject):
    """
    Represents a task in a Major Order.
    """

    def __init__(
        self,
        client,
        type: int,
        values: dict,
    ):
        """
        Initializes a new instance of the MajorOrderTask class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            type (int): The type of the task.
            values (dict): The values of the task.
        """
        super().__init__(client)
        self.type = MajorOrderTypes(type)
        self.values = values

    @property
    def completed(self) -> bool:
        """
        Returns whether the task is completed or not.

        Returns:
            bool: True if the task is completed, False otherwise.
        """
        return self.major_order.progress.is_complete(self)

    @property
    def planet(self) -> Optional["Planet"]:
        """
        Returns the planet associated with the task.

        Returns:
            Optional[Planet]: The planet associated with the task.
        """
        if self.type == MajorOrderTypes.ERADICATE:
            return None

        if self.values.get(ValueTypes.PLANET_INDEX) is not None:
            return self.client.planets.get_planet(
                self.values.get(ValueTypes.PLANET_INDEX)
            )

        return None

    @property
    def goal(self) -> int:
        """
        Returns the goal of the task.

        Returns:
            int: The goal of the task.
        """
        return self.values.get(ValueTypes.GOAL)

    @property
    def race(self) -> Optional["Faction"]:
        """
        Returns the race associated with the task.

        Returns:
            Optional[Faction]: The race associated with the task.
        """

        return Faction.parse(self.values.get(ValueTypes.RACE))

    # Dont want to have to do it this way but it works :P
    @property
    def major_order(self) -> "MajorOrder":
        """
        Returns the Major Order associated with the task.

        Returns:
            MajorOrder: The Major Order associated with the task.
        """
        return self._major_order

    @major_order.setter
    def major_order(self, value: "MajorOrder"):
        """
        Sets the Major Order associated with the task.

        Args:
            value (MajorOrder): The Major Order associated with the task.
        """
        self._major_order = value


class MajorOrderProgress(BaseObject):
    """
    Represents the progress of a Major Order.
    """

    def __init__(
        self,
        client,
        progress: List[int],
        tasks: List[MajorOrderTask],
        major_order: "MajorOrder",
    ):
        """
        Initializes a new instance of the MajorOrderProgress class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            progress (List[int]): The progress of the Major Order.
        """
        super().__init__(client)
        self.progress = progress
        self.tasks = tasks
        self._major_order = major_order

    @property
    def major_order(self) -> "MajorOrder":
        """
        Returns the Major Order associated with the progress.

        Returns:
            MajorOrder: The Major Order associated with the progress.
        """
        return self._major_order

    def is_complete(self, task: "MajorOrderTask") -> bool:
        if task.type in (
            MajorOrderTypes.CONTROL,
            MajorOrderTypes.DEFENSE,
            MajorOrderTypes.LIBERATION,
        ):
            return self.progress[self.tasks.index(task)] == 1
        elif task.type == MajorOrderTypes.ERADICATE:
            return self.progress[self.tasks.index(task)] == task.values.get(
                ValueTypes.GOAL
            )

        return False

    def get_progress(self, task: "MajorOrderTask") -> int:
        return self.progress[self.tasks.index(task)]

    @property
    def completed(self) -> bool:
        """
        Returns whether the Major Order is completed or not.

        Returns:
            bool: True if the Major Order is completed, False otherwise.
        """
        return all(i.completed for i in self.tasks)

    @property
    def total(self) -> int:
        """
        Returns the total number of tasks in the Major Order.

        Returns:
            int: The total number of tasks in the Major Order.
        """

        return len(self.tasks)

    @property
    def remaining_tasks(self) -> List["MajorOrderTask"]:
        """
        Returns the remaining tasks in the Major Order.

        Returns:
            List["MajorOrderTask"]: The remaining tasks in the Major Order.
        """
        return [i for i in self.tasks if not i.completed]

    @property
    def remaining(self) -> int:
        """
        Returns the remaining number of tasks in the Major Order.

        Returns:
            int: The remaining number of tasks in the Major Order.
        """
        return len(self.remaining_tasks)

    @property
    def percent(self) -> float:
        """
        Returns the percentage of completed tasks in the Major Order.

        Returns:
            float: The percentage of completed tasks in the Major Order.
        """
        return self.current / self.total * 100

    @property
    def completed_tasks(self) -> List["MajorOrderTask"]:
        """
        Returns the completed tasks in the Major Order.

        Returns:
            List["MajorOrderTask"]: The completed tasks in the Major Order.
        """
        completed = []
        for i in self.tasks:
            if i.completed:
                completed.append(i)
        return completed

    @property
    def current(self) -> int:
        """
        Returns the current number of completed tasks in the Major Order.

        Returns:
            int: The current number of completed tasks in the Major Order.
        """

        return len(self.completed_tasks)

    def __getitem__(self, item):
        try:
            return self.tasks[item]
        except ValueError:
            return None


class MajorOrder(BaseObject):
    """
    Represents a Major Order.
    """

    def __init__(
        self,
        client,
        id: int,
        progress: List[int],
        expires: int,
        settings: MajorOrderSettings,
        tasks: List[MajorOrderTask],
    ):
        """
        Initializes a new instance of the MajorOrder class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the Major Order.
            progress (int): The progress of the Major Order.
            expires (int): The timestamp when the Major Order expires.
            settings (MajorOrderSettings): The settings of the Major Order.
            tasks (List[MajorOrderTask]): The tasks in the Major Order.
        """
        super().__init__(client)

        self.id = id
        self.progress = MajorOrderProgress(self.client, progress, tasks, self)
        self.expires = self.client.fix_timestamp(expires, True)
        self.settings = settings
        self.tasks = tasks
        for i in self.tasks:
            i.major_order = self

    @classmethod
    def from_json(cls: "MajorOrder", client, json) -> "MajorOrder":
        """
        Creates a MajorOrder instance from a JSON object.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict): The JSON object representing the Major Order.

        Returns:
            MajorOrder: The MajorOrder instance created from the JSON object.
        """
        if isinstance(json, list):
            json = json[0]

        tasks = []

        for task in json["setting"]["tasks"]:
            vals = {}

            for j, value in enumerate(task["values"]):
                try:
                    val_type = ValueTypes(task["valueTypes"][j])
                except ValueError:
                    val_type = ValueTypes.UNKNOWN

                if val_type == ValueTypes.PLANET_INDEX:
                    if vals.get(ValueTypes.PLANET_INDEX) is None:
                        vals[ValueTypes.PLANET_INDEX] = []
                    vals[ValueTypes.PLANET_INDEX].append(value)
                else:
                    vals[val_type] = value

            if len(vals.get(ValueTypes.PLANET_INDEX)) == 1:
                vals[ValueTypes.PLANET_INDEX] = vals[ValueTypes.PLANET_INDEX][0]
            tasks.append(MajorOrderTask(client, type=task["type"], values=vals))

        settings = MajorOrderSettings(
            client,
            type=json["setting"]["type"],
            title=json["setting"]["overrideTitle"],
            brief=json["setting"]["overrideBrief"],
            description=json["setting"]["taskDescription"],
            reward=MajorOrderReward(
                client,
                id=json["setting"]["reward"]["id32"],
                type=json["setting"]["reward"]["type"],
                amount=json["setting"]["reward"]["amount"],
            ),
        )

        return cls(
            client=client,
            id=json["id32"],
            progress=json["progress"],
            expires=json["expiresIn"],
            settings=settings,
            tasks=tasks,
        )


class Biome(BaseObject):
    """
    Represents a Biome.
    """

    def __init__(self, client, name: str, description: str) -> None:
        """
        Initializes a new instance of the Biome class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            name (str): The name of the Biome.
            description (str): The description of the Biome.
        """
        super().__init__(client)
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, client, json) -> Optional["Biome"]:
        if not isinstance(json, dict):
            return None
        return cls(client, name=json["name"], description=json["description"])

    def __eq__(self, value: object) -> bool:
        """
        Determines if the current instance is equal to the given value.

        Args:
            value (object): The value to compare to the current instance.

        Returns:
            bool: True if the current instance is equal to the given value, False otherwise.
        """
        if not isinstance(value, Biome):
            return False
        return all(self.name == value.name, self.description == value.description)


class Enviromental(BaseObject):
    """
    Represents an Environmental.
    """

    def __init__(self, client, name: str, description: str) -> None:
        """
        Initializes a new instance of the Enviromental class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            name (str): The name of the Environmental.
            description (str): The description of the Environmental.
        """
        super().__init__(client)
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, client, json) -> Optional["Enviromental"]:
        if not isinstance(json, dict):
            return None
        return cls(client, name=json["name"], description=json["description"])

    def __eq__(self, value: object) -> bool:
        """
        Determines if the current instance is equal to the given value.

        Args:
            value (object): The value to compare to the current instance.

        Returns:
            bool: True if the current instance is equal to the given value, False otherwise.
        """
        if not isinstance(value, Biome):
            return False
        return all(self.name == value.name, self.description == value.description)


class JointOperation(BaseObject):
    def __init__(
        self,
        client,
    ) -> None:
        super().__init__(client)


class Status(BaseObject):
    def __init__(
        self,
        client,
        planet_status: list[dict],
        war_id: int,
        time: int,
        impact_multiplier: float,
        story_beat_id: int,
        community_targets: list,
        joint_operations: list,
        planet_events: list,
        planet_active_effects: list,
        active_election_policy_effects: list,
        global_events: list,
        war_results: list,
        layout_version: int,
    ) -> None:
        super().__init__(client)
        self._planet_status = planet_status
        self.war_id = war_id
        self.time = time
        self.impact_multiplier = impact_multiplier
        self.story_beat_id = story_beat_id
        self.community_targets = community_targets
        self.joint_operations = joint_operations
        self.planet_events = planet_events
        self.planet_active_effects = planet_active_effects
        self.active_election_policy_effects = active_election_policy_effects
        self.global_events = global_events
        self.war_results = war_results
        self.layout_version = layout_version

    @property
    def planet_status(self) -> list["PlanetStatus"]:
        if not isinstance(self._planet_status[0], PlanetStatus):
            self._planet_status = [
                PlanetStatus.from_json(self.client, i) for i in self._planet_status
            ]
        return self._planet_status

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client=client,
            planet_status=json["planetStatus"],
            war_id=json["warId"],
            time=json["time"],
            impact_multiplier=json["impactMultiplier"],
            story_beat_id=json["storyBeatId32"],
            community_targets=json["communityTargets"],
            joint_operations=json["jointOperations"],
            planet_events=json["planetEvents"],
            planet_active_effects=json["planetActiveEffects"],
            active_election_policy_effects=json["activeElectionPolicyEffects"],
            global_events=json["globalEvents"],
            war_results=json["superEarthWarResults"],
            layout_version=json["layoutVersion"],
        )


class PlanetStatus(BaseObject):
    """
    Represents the status of a Planet on DiveHarder.
    """

    def __init__(
        self,
        client,
        planet: int,
        health: int,
        regen: float,
        players: int,
        faction: Faction,
    ) -> None:
        """
        Initializes a new instance of the PlanetStatus class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            planet: The Planet instance.
            health: The current health of the planet.
            regen: The rate of regeneration for the planet.
            players: The number of players on the planet.
        """
        super().__init__(client)
        self._planet = planet
        self.health = health
        self.regen = regen
        self.players = players
        self.faction = faction

    @property
    def planet(self) -> "Planet":
        """
        Returns the planet the campaign is on.

        Returns:
            Planet: The planet the campaign is on.
        """
        print(f"Getting planet: {self._planet}")
        if not isinstance(self._planet, Planet):
            self._planet = self.client.planets.get_planet(self._planet)
            return self._planet
        return self._planet

    @classmethod
    def from_json(cls, client, json) -> "PlanetStatus":
        """
        Creates a new PlanetStatus instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json: The JSON data representing the PlanetStatus.

        Returns:
            PlanetStatus: The created PlanetStatus instance.
        """

        return cls(
            client=client,
            planet=json["index"],
            health=json["health"],
            regen=json["regenPerSecond"],
            players=json["players"],
            faction=Faction.parse(json["owner"]),
        )


class Planet(BaseObject):
    """
    Represents a Planet in DiveHarder.

    Attributes:
        id (int): The ID of the planet.
        name (str): The name of the planet.
        sector (str): The sector of the planet.
        biome (Biome): The biome of the planet.
        enviromentals (List[Enviromental]): The environmentals of the planet.
    """

    def __init__(
        self,
        client,
        id: int,
        name: str,
        sector: str,
        biome: Biome,
        enviromentals: List[Enviromental],
    ) -> None:
        """
        Initializes a new instance of the Planet class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the planet.
            name (str): The name of the planet.
            sector (str): The sector of the planet.
            biome (Biome): The biome of the planet.
            enviromentals (List[Enviromental]): The environmentals of the planet.
        """
        super().__init__(client)

        self.id = int(id)
        self.name = name
        self.sector = sector
        self.biome = biome
        self.enviromentals = enviromentals
        self._cache = {}

    def refresh(self) -> "Planet":
        """
        Refreshes the planet data.

        Returns:
            Planet: The refreshed planet.
        """
        return self.client.planets.get_planet(self.id)

    @property
    def planet_info(self) -> PlanetInfo:
        """
        Returns the planet info of the planet.

        Returns:
            PlanetInfo: The planet info of the planet.
        """

        if self._cache.get("planet_info") is None:
            self._cache["planet_info"] = self.client.war_info.get_planet_info(self)
        return self._cache["planet_info"]

    @property
    def max_health(self) -> int:
        """
        Returns the maximum health of the planet.

        Returns:
            int: The maximum health of the planet.
        """
        return self.planet_info.max_health

    @property
    def health(self) -> float:
        """
        Returns the health of the planet.

        Returns:
            float: The health of the planet.
        """
        return self.status.health

    @property
    def initial_owner(self) -> Faction:
        """
        Returns the initial owner of the planet.

        Returns:
            Faction: The initial owner of the planet.
        """
        return self.planet_info.initial_owner

    @property
    def position(self) -> tuple[int, int]:
        """
        Returns the position of the planet.

        Returns:
            tuple: The position of the planet.
        """
        return self.planet_info.position

    @property
    def waypoints(self) -> List[int]:
        """
        Returns the waypoints of the planet.

        Returns:
            List[Waypoint]: The waypoints of the planet.
        """
        return self.planet_info.waypoints

    @property
    def status(self) -> PlanetStatus:
        """
        Returns the status of the planet.

        Returns:
            PlanetStatus: The status of the planet.
        """

        if self._cache.get("status") is None:
            self._cache["status"] = self.client.status.get_planet_status(self)

            return self._cache["status"]
        return self._cache["status"]

    @property
    def campaign(self) -> Optional["Campaign"]:
        """
        Returns the campaign of the planet.

        Returns:
            Campaign: The campaign of the planet.
        """
        if self._cache.get("campaign") is None:
            self._cache["campaign"] = self.client.campaigns.get_campaign_by_planet(self)

            return self._cache["campaign"]

        return self._cache["campaign"]

    @property
    def is_part_of_major_order(self) -> bool:
        mo = self.client.dispatches.get_major_order()
        for i in mo.tasks:
            if i.planet == self:
                return True

        return False

    @classmethod
    def from_json(cls, client, json: dict[str, Any]) -> "Planet":
        """
        Creates a new Planet instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the planet.
            json (dict[str, Any]): The JSON data representing the planet.

        Returns:
            Planet: The created Planet instance.
        """

        return cls(
            client=client,
            id=json["id"],
            name=json["name"],
            sector=json["sector"],
            biome=Biome.from_json(client, json["biome"]),
            enviromentals=[
                Enviromental.from_json(client, i) for i in json["environmentals"]
            ],
        )

    def __eq__(self, value: object) -> bool:
        # We need to offset the id by 1 because the /v1/planets endpoint returns 0 as the first planet while the real starting index is 1
        return isinstance(value, Planet) and self.id + 1 == value.id


class Campaign(BaseObject):
    """
    Represents a Campaign in DiveHarder.

    Attributes:
        id (int): The ID of the campaign.
        planetid (int): The ID of the planet the campaign is on.
        type (CampaignTypes): The type of the campaign.
        count (int): The count of the campaign.
    """

    def __init__(
        self,
        client,
        id: int,
        planet: int,
        type: CampaignTypes | int,
        count: int,
    ) -> None:
        """
        Initializes a new instance of the Campaign class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the campaign.
            planetid (int): The ID of the planet the campaign is on.
            type (CampaignTypes | int): The type of the campaign.
            count (int): The count of the campaign.
        """
        super().__init__(client)
        self.id = int(id)
        self._planet = planet
        self.type = type
        self.count = count

    @property
    def planet(self) -> Planet:
        """
        Returns the planet the campaign is on.

        Returns:
            Planet: The planet the campaign is on.
        """

        if not isinstance(self._planet, Planet):
            self._planet = self.client.planets.get_planet(self._planet)
            return self._planet
        return self._planet

    @property
    def liberation_percentage(self) -> float:
        """
        Returns the liberation percentage of the campaign.

        Returns:
            float: The liberation percentage of the campaign.
        """

        return round(100 - ((self.planet.health / self.planet.max_health) * 100), 2)

    @classmethod
    def from_json(cls, client, json: dict[str, Any]) -> "Campaign":
        """
        Creates a new Campaign instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict[str, Any]): The JSON data representing the campaign.

        Returns:
            Campaign: The created Campaign instance.
        """

        return cls(
            client=client,
            id=json["id"],
            planet=json["planetIndex"],
            type=CampaignTypes.parse(json["type"]),
            count=json["count"],
        )
