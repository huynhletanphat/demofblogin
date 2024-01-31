# helpers/display_operations.py
from termcolor import colored

def display_message(message, color="yellow"):
    frame_top = "=" * 120
    frame_middle = f"| {message.center(118)} |"
    frame_bottom = "=" * 120
    framed_message = f"\n{frame_top}\n{frame_middle}\n{frame_bottom}"
    print(colored(framed_message, color, attrs=["bold"]))

def prompt_for_restart():
    restart = input("Do you want to restart? (y/n): ").strip().lower()
    return restart == 'y'