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
            "Please enter the names of the champion you want to click, separated by commas"
        )

    for champion_name in champion_names.split(","):
        # Cleaning up the champion name to have the exact Riot nomenclature
        champion_name = lol_id_tools.get_translation(
            champion_name, object_type="champion"
        )

        # Selecting the LoL window then scrolling very far up to make sure we’re at the beginning of the champion select
        select_lol_window()
        pyautogui.scroll(120 * 5 * 10)

        tries = 0
        result = None  # To not get weak warnings
        start_time = datetime.now()

        while tries < 7:
            img = get_champion_select_image()
            result = find_champion_in_picture(champion_name, img)

            if result is not None:
                click_champion_select(result)
                typer.secho(
                    f"\t{champion_name} was found in {(datetime.now()-start_time).total_seconds()}s",
                    fg=typer.colors.GREEN,
                )
                break

            else:
                # We scroll down
                pyautogui.scroll(-120 * 5)
                tries += 1

        # If we existed and result is still None, something went wrong
        if result is None:
            typer.secho(
                f"{champion_name} not found, were you properly in champion select?",
                fg=typer.colors.RED,
            )


# Simple testing by running the file
if __name__ == "__main__":
    select_champion("Zilean")
