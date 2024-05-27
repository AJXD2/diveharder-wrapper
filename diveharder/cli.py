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


def main() -> None:
    fire.Fire({"campaigns": campaigns})


if __name__ == "__main__":
    main()
