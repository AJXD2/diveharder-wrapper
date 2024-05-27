from functools import lru_cache
import json
from pathlib import Path
from typing import Generator, List, Optional
from diveharder.api.base import ApiBase
from diveharder.objects import Biome, Enviromental, Planet


class Planets(ApiBase):

    def get_planets(self):
        data = self._api_request("planets")
        for i in data:
            yield Planet.from_json(self._client, i, data[i])

    def get_planet(self, id: int) -> Optional[Planet]:
        for i in self.get_planets():
            if i.id == id:
                return i

        return None

    def get_planets_by_enviromental(
        self, enviromental: Enviromental
    ) -> Generator[Planet, None, None]:
        for i in self.get_planets():
            for j in i.enviromentals:
                if enviromental == j:
                    yield i

    def get_planets_by_biome(self, biome: Biome) -> Generator[Planet, None, None]:
        for i in self.get_planets():
            if biome == i.biome:
                yield i

    def __getitem__(self, item):
        return self.get_planet(item)
