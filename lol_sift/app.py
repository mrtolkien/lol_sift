import time

import typer
import pyautogui
import lol_id_tools
from datetime import datetime

from lol_sift import (
    find_champion_in_picture,
    select_lol_window,
    get_champion_select_image,
    click_champion_select,
)

app = typer.Typer()


@app.command()
def select_champion(
    champion_names: str = typer.Argument(
        None,
        help="Champion or list of champions you want to pick separated by commas",
    )
):
    """
    Selects the specified champion from an open League of Legends champion select.

    The LoL client must be open and visible on your desktop for it to work.
    """

    if not champion_names:
        champion_names = typer.prompt(
            "Please enter the names of the champions you want to click, separated by commas"
        )

    # Selecting the LoL window then scrolling very far up to make sure we’re at the beginning of the champion select
    select_lol_window()
    pyautogui.scroll(120 * 5 * 10)

    clean_champion_names = set()

    for champion_name in champion_names.split(","):
        # Cleaning up the champion name to have the exact Riot nomenclature
        champion_id = lol_id_tools.get_id(champion_name, object_type="champion")
        clean_champion_names.add(
            lol_id_tools.get_name(champion_id, object_type="champion")
        )

    start_time = datetime.now()

    tries = 0
    champions_found = set()

    while clean_champion_names and tries < 7:

        for champion_name in clean_champion_names:
            if champion_name in champions_found:
                continue

            img = get_champion_select_image()
            result = find_champion_in_picture(champion_name, img)

            if result is not None:
                champions_found.add(champion_name)
                click_champion_select(result)
                typer.secho(
                    f"\t{champion_name} found",
                    fg=typer.colors.GREEN,
                )
                time.sleep(1/60)  # To reduce bugs when we move too fast

        # We scroll down roughly 1 screen
        pyautogui.scroll(-100 * 5)

        # Ensures we stop when at the bottom of the champion select
        tries += 1

    # If we exited and result is still None, something went wrong
    if len(champions_found) != len(clean_champion_names):
        typer.secho(
            f"{', '.join([c for c in clean_champion_names if c not in champions_found])} not found",
            fg=typer.colors.RED,
        )

    typer.secho(
        f"Search finished in {(datetime.now()-start_time).total_seconds()}s",
        fg=typer.colors.GREEN,
    )


# Simple testing by running the file
if __name__ == "__main__":
    select_champion("Zilean")
