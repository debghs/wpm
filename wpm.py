import time
import random
import os

try:
    import curses
except ImportError:
    # Handle ImportError for platforms that don't support curses
    curses = None


def first_msg(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getch()


def display_text(stdscr, target, current, wpm=0, accuracy=0):
    stdscr.addstr(1,0,target)
    stdscr.addstr(2, 0, f"wpm: {wpm}, acc: {round(accuracy,2)} %")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(1, i, char, color)


def load_text():
    # Adjust the file path based on script location
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, "lines.txt")
    with open(file_path, "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def typing_accuracy(current_text, target_text):
    total_characters = min(len(current_text), len(target_text))
    
    if total_characters == 0:
        return 0.0  # If there are no characters, consider accuracy as 100%

    matching_characters = 0

    for current_char, target_char in zip(current_text, target_text):
        if current_char == target_char:
            matching_characters += 1
    
    matching_percentage = (matching_characters / total_characters) * 100
    return matching_percentage

def wpm(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        accuracy = typing_accuracy(current_text, target_text)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        if len("".join(current_text)) == len(target_text):
            stdscr.nodelay(False)
            break

        key = stdscr.getch()
        if key == 27:
            break

        if key in (curses.KEY_BACKSPACE, 127):
            if len(current_text) > 0:
                current_text.pop()
        elif key >= 0 and key <= 255 and len(current_text) < len(target_text):
            current_text.append(chr(key))



def main(stdscr):
    if curses is None:
        # Display a message if curses is not available
        stdscr.addstr("Curses module is not available on this system.")
        stdscr.getch()
        return

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    first_msg(stdscr)
    while True:
        wpm(stdscr)
        stdscr.addstr(3, 0, "Press any key to continue...")
        key = stdscr.getch()

        if key == 27:
            break


if __name__ == "__main__":
    if curses is not None:
        curses.wrapper(main)
    else:
        # Run main without curses wrapper if curses is not available
        main(None)
