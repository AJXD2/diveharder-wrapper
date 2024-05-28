from datetime import datetime
from functools import lru_cache
import re
from typing import Any, List


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
        start_date: int,
        end_date: int,
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


class Dispatch(BaseObject):
    """
    Represents a dispatch message from the DiveHarder API.

    Attributes:
        id (int): The ID of the dispatch message.
        published (datetime): The date and time the message was published.
        type (int): The type of the dispatch message.
        tagIds (list): A list of tag IDs associated with the message.
        message (str): The content of the message.
    """

    def __init__(
        self, client, id: int, published: int, type: int, tagIds: list, message: str
    ):
        """
        Initializes a new instance of the Dispatch class.

        Args:
            client: The DiveHarderApiClient instance used to interact with the API.
            id (int): The ID of the dispatch message.
            published (int): The timestamp of when the message was published.
            type (int): The type of the dispatch message.
            tagIds (list): A list of tag IDs associated with the message.
            message (str): The content of the message.
        """
        super().__init__(client)

        self.id = id
        self.published = datetime.fromtimestamp(self.client.fix_timestamp(published))
        self.type = type
        self.tagIds = tagIds
        self.message = message

    @property
    def as_plaintext(self):
        """
        Returns the plain text content of the message.

        Returns:
            str: The plain text content of the message.
        """
        return re.sub(r"<.*?>", "", self.message)

    @property
    def as_markdown(self):
        """
        Returns the Markdown version of the message.

        Returns:
            str: The Markdown version of the message.
        """
        return hdml_to_md(self.message)


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
        self.title = title
        self.brief = brief
        self.description = description
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


class MajorOrder(BaseObject):
    """
    Represents a Major Order.
    """

    def __init__(
        self,
        client,
        id: int,
        progress: int,
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
        self.progress = progress
        if not isinstance(expires, datetime):
            expires = datetime.fromtimestamp(expires)
        self.expires = expires
        self.settings = settings
        self.tasks = tasks

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

        for i in json["setting"]["tasks"]:

            vals = {}
            for j, k in enumerate(i["values"]):

                try:
                    val = ValueTypes(i["valueTypes"][j])
                except ValueError:
                    val = ValueTypes.UNKNOWN
                if val == ValueTypes.PLANET_INDEX:
                    if vals.get(ValueTypes.PLANET_INDEX) is None:
                        vals[ValueTypes.PLANET_INDEX] = []
                    vals[ValueTypes.PLANET_INDEX].append(k)
                    continue
                vals[val] = k

            tasks.append(MajorOrderTask(client, type=i["type"], values=vals))

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
            expires=datetime.fromtimestamp(client.current_time + json["expiresIn"]),
            settings=settings,
            tasks=tasks,
        )


class Biome(BaseObject):
    """
    Represents a Biome on DiveHarder.
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
    Represents an Environmental on DiveHarder.
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
