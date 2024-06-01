from datetime import datetime
from functools import lru_cache
import re
from typing import Any, List, Optional

from diveharder.enums import (
    CampaignTypes,
    Factions,
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
    def as_plaintext(self):
        """
        Returns the plain text content of the HDML string.

        Returns:
            str: The plain text content of the HDML string.
        """
        return re.sub(r"<.*?>", "", self.text)

    @property
    def as_md(self):
        """
        Returns the Markdown content of the HDML string.

        Returns:
            str: The Markdown content of the HDML string.
        """
        return hdml_to_md(self.text)

    def __str__(self) -> str:
        return self.as_plaintext

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={self.text})"


class PlanetStatistics(BaseObject):
    def __init__(
        self,
        client,
        missionsWon: int,
        missionsLost: int,
        missionTime: int,
        bugKills: int,
        automatonKills: int,
        illuminateKills: int,
        bulletsFired: int,
        bulletsHit: int,
        timePlayed: int,
        deaths: int,
        revives: int,
        friendlies: int,
        missionSuccessRate: int,
        accurracy: int,
        planetIndex: int,
    ) -> None:
        """
        A class used to represent the statistics of a planet.

        Args:
            client (DiveHarderApiClient): The client object used to make API requests.
            missionsWon (int): The number of missions won.
            missionsLost (int): The number of missions lost.
            missionTime (int): The total time spent on missions.
            bugKills (int): The number of bug kills.
            automatonKills (int): The number of automaton kills.
            illuminateKills (int): The number of illuminate kills.
            bulletsFired (int): The number of bullets fired.
            bulletsHit (int): The number of bullets hit.
            timePlayed (int): The total time played.
            deaths (int): The number of deaths.
            revives (int): The number of revives.
            friendlies (int): The number of friendly kills.
            missionSuccessRate (int): The success rate of missions.
            accurracy (int): The accuracy of bullets.
            planetIndex (int): The index of the planet.

        Returns:
            None
        """
        super().__init__(client)

        self.missionsWon = missionsWon
        self.missionsLost = missionsLost
        self.missionTime = missionTime
        self.bugKills = bugKills
        self.automatonKills = automatonKills
        self.illuminateKills = illuminateKills
        self.bulletsFired = bulletsFired
        self.bulletsHit = bulletsHit
        self.timePlayed = timePlayed
        self.deaths = deaths
        self.revives = revives
        self.friendlies = friendlies
        self.missionSuccessRate = missionSuccessRate
        self.accurracy = accurracy
        self._planet_index = planetIndex

    @property
    def planet(self):
        return self.client.planets[self._planet_index]


class GalaxyStatistics(BaseObject):

    def __init__(
        self,
        client,
        missionsWon: int,
        missionsLost: int,
        missionTime: int,
        bugKills: int,
        automatonKills: int,
        illuminateKills: int,
        bulletsFired: int,
        bulletsHit: int,
        timePlayed: int,
        deaths: int,
        revives: int,
        friendlies: int,
        missionSuccessRate: int,
        accurracy: int,
    ) -> None:
        """
        A class used to represent the statistics of the galaxy (global statistics).

        Args:
            client (DiveHarderApiClient): The client object used to make API requests.
            missionsWon (int): The number of missions won.
            missionsLost (int): The number of missions lost.
            missionTime (int): The total time spent on missions.
            bugKills (int): The number of bug kills.
            automatonKills (int): The number of automaton kills.
            illuminateKills (int): The number of illuminate kills.
            bulletsFired (int): The number of bullets fired.
            bulletsHit (int): The number of bullets hit.
            timePlayed (int): The total time played.
            deaths (int): The number of deaths.
            revives (int): The number of revives.
            friendlies (int): The number of friendly kills.
            missionSuccessRate (int): The success rate of missions.
            accuracy (int): The accuracy of bullets.

        Returns:
            None
        """

        super().__init__(client)

        self.missions_won = missionsWon
        self.missions_lost = missionsLost
        self.mission_time = missionTime
        self.bug_kills = bugKills
        self.automaton_kills = automatonKills
        self.illuminate_kills = illuminateKills
        self.bullets_fired = bulletsFired
        self.bullets_hit = bulletsHit
        self.time_played = timePlayed
        self.deaths = deaths
        self.revives = revives
        self.friendlies = friendlies
        self.mission_success_rate = missionSuccessRate
        self.accurracy = accurracy


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
        super().__init__(client)

        self._index = index
        self.settings_hash = settings_hash
        self.position = position
        self.waypoints = waypoints
        self.sector = sector
        self.max_health = max_health
        self.disabled = disabled
        self.initial_owner = initial_owner

    @property
    def planet(self):
        return self.client.planets[self._index]

    @classmethod
    def from_json(cls, client, json):
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
    def __init__(self, client, race: int, planets: List[int]) -> None:
        super().__init__(client)

        self.race = Factions.parse(race)
        self._planet_ids = planets

    @property
    def planets(self):
        return [self.client.planets[id] for id in self._planet_ids]

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client,
            race=json["race"],
            planets=json["planetIndices"],
        )


class WarInfo(BaseObject):
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
        """
        Initializes a WarInfo object with the given parameters.

        Args:
            client: The client object.
            war_id (int): The ID of the war.
            start_date (int): The start date of the war.
            end_date (int): The end date of the war.
            layout_version (int): The version of the layout.
            minimum_client_version (str): The minimum client version required.
            planet_infos (List[PlanetInfo]): A list of PlanetInfo objects.
            home_worlds (List[HomeWorldInfo]): A list of HomeWorldInfo objects.
            capital_infos (List[Any]): A list of capital information.
            planet_permanent_effects (List[Any]): A list of permanent effects on planets.

        Returns:
            None
        """

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
        return datetime.fromtimestamp(self._start_date)

    @property
    def end_date(self) -> datetime:
        return datetime.fromtimestamp(self._end_date)

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client,
            json["warId"],
            json["startDate"],
            json["endDate"],
            json["layoutVersion"],
            json["minimumClientVersion"],
            [
                PlanetInfo.from_json(client, planet_info)
                for planet_info in json["planetInfos"]
            ],
            [
                HomeWorldInfo.from_json(client, home_world)
                for home_world in json["homeWorlds"]
            ],
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
            # print("Eradicate task does not have a planet.")
            return None

        if self.values.get(ValueTypes.PLANET_INDEX) is not None:
            # print(f"Planet index: {self.values.get(ValueTypes.PLANET_INDEX)}")
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
    def race(self) -> Optional["Factions"]:
        """
        Returns the race associated with the task.

        Returns:
            Optional[Factions]: The race associated with the task.
        """

        return Factions.parse(self.values.get(ValueTypes.RACE))

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

    def __repr__(self):
        return f"MajorOrderProgress({self.current}/{self.total})"


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
    def from_json(cls: "MajorOrder", client, json):
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

    def __str__(self) -> str:
        return f"MajorOrder(progress={self.progress})"


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

    @classmethod
    def from_json(cls, client, json):
        return cls(
            client=client,
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
        planet: "Planet",
        health: int,
        regen: float,
        players: int,
        faction: Factions,
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
        self.planet = planet
        self.health = health
        self.regen = regen
        self.players = players
        self.faction = faction

    @classmethod
    def from_json(cls, client, planet, json):
        """
        Creates a new PlanetStatus instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            planet: The Planet instance.
            json: The JSON data representing the PlanetStatus.

        Returns:
            PlanetStatus: The created PlanetStatus instance.
        """

        return cls(
            client=client,
            planet=planet,
            health=json["health"],
            regen=json["regenPerSecond"],
            players=json["players"],
            faction=Factions.parse(json["owner"]),
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

        self.id = id
        self.name = name
        self.sector = sector
        self.biome = biome
        self.enviromentals = enviromentals
        self._cache = {}

    @property
    def status(self):
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
    def campaign(self):
        """
        Returns the campaign of the planet.

        Returns:
            Campaign: The campaign of the planet.
        """
        if self._cache.get("campaign") is None:
            self._cache["campaign"] = self.client.campaigns.get_campaign_by_planet(self)

            return self._cache["campaign"]

        return self._cache["campaign"]

    @classmethod
    def from_json(cls, client, id: int, json: dict[str, Any]):
        """
        Creates a new Planet instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the planet.
            json (dict[str, Any]): The JSON data representing the planet.

        Returns:
            Planet: The created Planet instance.
        """

        from diveharder import DiveHarderApiClient

        client: DiveHarderApiClient = client

        return cls(
            client=client,
            id=int(id),
            name=json["name"],
            sector=json["sector"],
            biome=Biome.from_json(client, json["biome"]),
            enviromentals=[
                Enviromental.from_json(client, i) for i in json["environmentals"]
            ],
        )


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
        planetid: int,
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
        self.id = id

        self._planetid = planetid
        if isinstance(type, int):
            type = CampaignTypes.parse(type)
        self._planet = None
        self.type: CampaignTypes = type
        self.count = count

    @property
    @lru_cache(maxsize=1)
    def planet(self):
        """
        Returns the planet the campaign is on.

        Returns:
            Planet: The planet the campaign is on.
        """
        if not self._planet:
            self._planet = self.client.planets.get_planet(self._planetid)
            return self._planet

        return self._planet

    @classmethod
    def from_json(cls, client, json: dict[str, Any]):
        """
        Creates a new Campaign instance from the given JSON data.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            json (dict[str, Any]): The JSON data representing the campaign.

        Returns:
            Campaign: The created Campaign instance.
        """

        campaign = cls(
            client=client,
            id=json["id"],
            planetid=json["planetIndex"],
            type=CampaignTypes(json["type"]),
            count=json["count"],
        )
        return campaign
