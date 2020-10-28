from PIL import ImageGrab
from pynput import mouse
from helpers import runSIFT, saveImg


def main():
    print("Choose the top left and bottom right coordinates of your box.")

    button_presses = []

    # Stream of events
    with mouse.Events() as events:
        for event in events:
            if hasattr(event, "button") and event.pressed:
                print(
                    "The {0} button was {1} at the following coordinates: x:{2}, y:{3}".format(
                        event.button,
                        "pressed" if event.pressed else "released",
                        event.x,
                        event.y,
                    )
                )
                button_presses.append(event)
            if len(button_presses) == 2:
                break

    screen_shot = ImageGrab.grab(
        bbox=(
            button_presses[0].x,
            button_presses[0].y,
            button_presses[1].x,
            button_presses[1].y,
        )
    )

    saveImg(screen_shot, "pre")
    runSIFT(screen_shot)
    saveImg(screen_shot, "post")


if __name__ == "__main__":
    main()
