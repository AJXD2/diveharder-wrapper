import fire
from diveharder import DiveHarderApiClient
from rich.table import Table
from rich import print
from rich.status import Status

from diveharder.enums import Factions, MajorOrderTypes, ValueTypes

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
        print(f"[bold]Loading all planets...[/bold]")
        print(f"[red]Warning: This may take a while![/red]")
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
            dots = 0
            for i in planets:
                status.update(
                    f"{planets.index(i)/len(planets):.2%}{'.'*dots}\nLoading {i.name}"
                )
                dots += 1
                if dots == 4:
                    dots = 0
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


def major_order():
    mo = api.dispatches.get_major_order()
    if mo is None:
        print("There is no major order at the moment.")
        return

    print(f"Title: {mo.settings.title.as_md}")
    print(f"Description: {mo.settings.description.as_md}")
    print(f"Brief: {mo.settings.brief.as_md}")
    print(f"Reward: {mo.settings.reward.amount} {mo.settings.reward.type.name}")
    print(f"Expires: {mo.expires.strftime('%m-%d-%Y %H:%M')}")

    print("== Tasks ==")
    tasks = mo.tasks

    for i in tasks:

        if i.type == MajorOrderTypes.CONTROL:
            completed = ":white_check_mark:" if mo.progress[tasks.index(i)] else ":x:"
            print(
                f"[{completed}] Control: {api.planets.get_planet(i.values.get(ValueTypes.PLANET_INDEX)[0]).name}"
            )
        if i.type == MajorOrderTypes.DEFENSE:
            completed = ":white_check_mark:" if mo.progress[tasks.index(i)] else ":x:"
            print(
                f"[{completed}] Defend: {api.planets.get_planet(i.values.get(ValueTypes.PLANET_INDEX)[0]).name}"
            )
        if i.type == MajorOrderTypes.LIBERATION:
            completed = ":white_check_mark:" if mo.progress[tasks.index(i)] else ":x:"

            print(
                f"[{completed}] Liberate: {api.planets.get_planet(i.values.get(ValueTypes.PLANET_INDEX)[0]).name}"
            )
        if i.type == MajorOrderTypes.ERADICATE:
            print(
                f"Eradicate: {i.values.get(ValueTypes.GOAL)} {Factions.parse(i.values.get(ValueTypes.RACE)).name}"
            )


cli = {"campaigns": campaigns, "planets": planet, "major_order": major_order}


def main() -> None:
    try:
        fire.Fire(cli)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
