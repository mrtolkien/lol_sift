import PIL
import numpy
import pyautogui

# Very barbaric, works well enough for a single window though
lol_window = pyautogui.getWindowsWithTitle("League of Legends")[0]


def select_lol_window():
    """
    Clicks the LoL window in the center (gets focus)
    """
    pyautogui.click(lol_window.center.x, lol_window.center.y)


def click_champion_select(champion_select_coordinates):
    pyautogui.click(
        lol_window.left + 1280 / 2 - 590 / 2 + champion_select_coordinates[0],
        lol_window.top + 720 / 2 - 480 / 2 + champion_select_coordinates[1],
    )


def get_champion_select_image() -> numpy.ndarray:
    """
    Returns a numpy array representing the champion portraits in champion select

    On a 1280*720 client, champion select is 590*470, centered
    """
    # Screenshot the LoL window only
    pyautogui.hotkey("alt", "prtscr")

    # Read the screenshot from memory
    lol_screenshot = PIL.ImageGrab.grabclipboard()

    # TODO Ideally this should be dynamic, with everything being defined as percents of the total client size
    # Crop around the center
    lol_screenshot = lol_screenshot.crop(
        (1280 / 2 - 590 / 2, 720 / 2 - 470 / 2, 1280 / 2 + 590 / 2, 720 / 2 + 470 / 2)
    )

    # Transform into into a numpy array
    lol_screenshot_array = numpy.array(lol_screenshot)

    # Finally, we revert the array as it’s read in RGB but cv2 wants BGR
    return lol_screenshot_array[:, :, ::-1]

##

