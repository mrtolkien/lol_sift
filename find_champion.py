import pyautogui

from lol_surf.features_utils import find_champion_in_picture
from lol_surf.lol_window_utils import (
    select_lol_window,
    get_champion_select_image,
    click_champion_select,
)

champion_name = "Zilean"

select_lol_window()
pyautogui.scroll(120*5*10)

while True:
    img = get_champion_select_image()
    result = find_champion_in_picture(champion_name, img)

    if result is not None:
        click_champion_select(result)
        break
    else:
        # We scroll down
        pyautogui.scroll(-120*5)

##
