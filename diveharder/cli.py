import fire
from diveharder import DiveHarderApiClient
from rich.table import Table
from rich import print
from rich.status import Status

api = DiveHarderApiClient()


def campaigns():
    table = Table(
        "ID",
        "Planet",
        "Sector",
        "Biome",
        "Enviromentals",
        "Battles",
        "Health",
        "Players",
        title="Campaigns",
    )

    with Status("Loading campaigns...") as status:
        camps = list(api.campaigns.get_campaigns())

        for i in camps:
            status.update(
                f"Loading {i.planet.name}({camps.index(i)/len(camps):.2%})..."
            )
            table.add_row(
                str(i.id),
                i.planet.name,
                i.planet.sector,
                i.planet.biome.name,
                ", ".join([i.name for i in i.planet.enviromentals]),
                str(i.count),
                str(i.planet.status.health),
                str(i.planet.status.players),
            )

    print(table)


def planet(id: int = None):
    if id is None:
        with Status("Loading planets...") as status:
            planets = list(api.planets.get_planets())
            table = Table(
                "ID",
                "Name",
                "Sector",
                "Biome",
                "Enviromentals",
                "Faction",
                "Players",
                title="Planets",
            )
            for i in planets:
                status.update(
                    f"Loading {i.name}({planets.index(i)/len(planets):.2%})..."
                )
                table.add_row(
                    str(i.id),
                    i.name,
                    i.sector,
                    i.biome.name,
                    ", ".join([i.name for i in i.enviromentals]),
                    i.status.faction.name,
                    str(i.status.players),
                )

        print(table)
        return
    print(id)
    planet = api.planets.get_planet(id)

    table = Table(
        "ID",
        "Name",
        "Sector",
        "Biome",
        "Enviromentals",
        "Faction",
        "Players",
        title="Planets",
    )
    table.add_row(
        str(planet.id),
        planet.name,
        planet.sector,
        planet.biome.name,
        ", ".join([i.name for i in planet.enviromentals]),
        planet.status.faction.name,
        str(planet.status.players),
    )

    print(table)


cli = {"campaigns": campaigns, "planets": planet}


def main() -> None:
    fire.Fire(cli)


if __name__ == "__main__":
    main()
