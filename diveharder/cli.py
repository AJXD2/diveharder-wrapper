import fire
from diveharder import DiveHarderApiClient
from diveharder.constants import __version__
from rich.console import Console
from diveharder.enums import MajorOrderTypes
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.markdown import Markdown

api = DiveHarderApiClient(f"DiveHarderApiWrapper/{__version__}/CLI")
con = Console(markup=True)


def pretty_print_number(num):
    num = int(num)

    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


def campaigns() -> None:
    """
    Show a table of all campaigns.
    """
    table = Table("Planet", "Sector", "Liberation", "Is Major Order", title="Campaigns")
    for i in api.campaigns.get_campaigns():
        table.add_row(
            i.planet.name,
            i.planet.sector,
            f"{i.liberation_percentage}%",
            "[green]:heavy_check_mark:[/]"
            if i.planet.is_part_of_major_order
            else "[red]:x:[/]",
        )

    con.print(table)


def news(latest: bool = False) -> None:
    """
    Show news from the news feed. -l for latest
    """
    if latest:
        news = api.dispatches.get_latest_dispatch()
        con.print(Panel(f"{news.published.strftime('%Y-%m-%d')}\n{news.message.as_md}"))
        return

    for i in api.dispatches.get_dispatches():
        con.print(Panel(f"{i.published.strftime('%Y-%m-%d')}\n{i.message.as_md}"))


def major_order() -> None:
    """
    Show major order
    """
    mo = api.dispatches.get_major_order()
    if mo is None:
        con.print(Panel("There is not major order at this time."))
    for i in mo.tasks:
        if i.type == MajorOrderTypes.ERADICATE:
            con.print(
                Panel(
                    f"Eradicate {i.goal} {i.race} ({'[green]:heavy_check_mark:[/]' if i.completed else '[red]:x:[/]'})"
                )
            )
        else:
            campaign = api.campaigns.get_campaign_by_planet(i.planet)
            liberation_string = (
                f"{campaign.liberation_percentage}%" if campaign is not None else "0%"
            )
            con.print(
                Panel(
                    f"Liberate {i.planet.name} in the {i.planet.sector} sector. ({'green]:heavy_check_mark:[/]' if i.completed else liberation_string})"
                )
            )


def planets(id: int = None):
    """
    Show a table of all planets.
    -id for specific planet
    """
    table = Table(
        "ID",
        "Name",
        "Sector",
        "Biome",
        "Enviromentals",
        "Players",
        "Part of Major Order",
        title="Planets",
    )
    if id is None:
        con.print("[bold red blink]WARNING[/bold red blink]: This may take a while.")

        with Progress() as prog:
            task1 = prog.add_task("Getting planets", total=260, start=True)
            for i in api.planets.get_planets():
                prog.update(task1, description=f"Getting {i.name}")
                table.add_row(
                    str(i.id),
                    i.name,
                    i.sector,
                    i.biome.name if i.biome is not None else "None",
                    ", ".join([j.name for j in i.enviromentals]),
                    str(i.status.players),
                    f"[green]:heavy_check_mark:[/] {i.campaign.liberation_percentage}%"
                    if i.is_part_of_major_order
                    else "[red]:x:[/]",
                )
                prog.update(task1, advance=1, description=f"Got {i.name}")
        con.print(table)
    else:
        table.title = f"Planet {id}"
        planet = api.planets.get_planet(id)
        if planet is None:
            con.print("[red bold]ERROR[/red bold]: No planet found with that ID.")
        else:
            table.add_row(
                str(planet.id),
                planet.name,
                planet.sector,
                planet.biome.name if planet.biome is not None else "None",
                ", ".join([j.name for j in planet.enviromentals]),
                str(planet.status.players),
                f"[green]:heavy_check_mark:[/] {planet.campaign.liberation_percentage}% Liberated"
                if planet.is_part_of_major_order
                else "[red]:x:[/]",
            )

    con.print(table)


def statistics(planet: int = None) -> None:
    """
    Show global statistics.
    -p for specific planet
    """

    stats = api.statistics.get_galaxy_statistics()
    table = Table("Statistic", "Value", title="Global Statistics")
    if planet is not None:
        stats = api.statistics.get_planet_statistics(planet)
        if stats is None:
            con.print("[red bold]ERROR[/red bold]: No planet found with that ID.")
            return
        table.title = f"Statistics for {api.planets.get_planet(planet).name}"

    for k, v in stats.__dict__.items():
        if k == "client":
            continue
        match k:
            case "missions_won":
                table.add_row("Missions Won", str(pretty_print_number(v)))
            case "missions_lost":
                table.add_row("Missions Lost", str(pretty_print_number(v)))
            case "mission_time":
                table.add_row("Mission Time", str(pretty_print_number(v)))
            case "bug_kills":
                table.add_row("Bug Kills", str(pretty_print_number(v)))
            case "automaton_kills":
                table.add_row("Automaton Kills", str(pretty_print_number(v)))
            case "illuminate_kills":
                table.add_row("Illuminate Kills", str(pretty_print_number(v)))
            case "bullets_fired":
                table.add_row("Bullets Fired", str(pretty_print_number(v)))
            case "bullets_hit":
                table.add_row("Bullets Hit", str(pretty_print_number(v)))
            case "time_played":
                table.add_row("Time Played", str(pretty_print_number(v)))
            case "deaths":
                table.add_row("Deaths", str(pretty_print_number(v)))
            case "revives":
                table.add_row("Revives", str(pretty_print_number(v)))
            case "friendlies":
                table.add_row("Friendlies", str(pretty_print_number(v)))
            case "mission_success_rate":
                table.add_row("Mission Success Rate", f"{v}%")
            case "accurracy":
                table.add_row("Accurracy", f"{v}%")
    con.print(table)


def updates(latest: bool = False) -> None:
    """
    Show updates.
    -l for latest
    """
    if latest:
        update = api.updates.get_latest_update()
        con.print(
            Panel(
                Markdown(update.contents.as_plaintext + f"\n[URL]({update.url})"),
                title=f"{update.title} ({update.date.strftime('%Y-%m-%d %H:%M %Z')})",
            )
        )
        return
    for update in api.updates.get_updates():
        con.print(
            Panel(
                Markdown(update.contents.as_plaintext + f"\n[URL]({update.url})"),
                title=f"{update.title} ({update.date.strftime('%Y-%m-%d %H:%M %Z')})",
            )
        )


cli_map = {
    "campaigns": campaigns,
    "news": news,
    "mo": major_order,
    "planets": planets,
    "stats": statistics,
    "updates": updates,
}


def main() -> None:
    fire.Fire(cli_map)


if __name__ == "__main__":
    main()
