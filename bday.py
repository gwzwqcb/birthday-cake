import curses
import random
import base64
import bz2
import time


def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)

    encoded_string = "QlpoOTFBWSZTWbQ7eg8AAMr7gH/doChY84AQAATAAAAFMAF5QmDQEaEj00I0AyETaJqA9RoAGgCQkRoQjJoYEycRcmNn8JgkdWl1b9yeX1arHCrZQdpdJIGxJB6aEgzYB7ruc8VmVYsQ9WxWrvWPhlxxEqvBsyvw4iTxZwwNiD5QrmDIxRGKLWGUbmaaXxlps9c8t402JqzLay7FleFPkDSzMQg1thxMocVSOoYGvY3DYqWlms3MrxqgwBwjcJ0rQdy4RfmROTTYlz1Y8fJQ07dGkQ4F/F5dtrSQRxtXR3e4t3o338YtLd9vNYnGs754BlgKMk+bGH9JuYnrtylI7gS0NTGA0IyZmt+u6oiSqmdA1mEhp5IqGAYExHK0HIQaAsXtcyUig5VsziVGAHrbKalM/riEKj+SlgWsVJAy5oYEzxjJDNHH4u5IpwoSFodvQeA="

    decoded_bytes = base64.b64decode(encoded_string)
    decompressed_bytes = bz2.decompress(decoded_bytes)
    bg_frame = decompressed_bytes.decode("utf-8")

    main_dec = []
    minor_decs = []
    for y, bg_line in enumerate(bg_frame.split("\n")):
        for x, bg_char in enumerate(bg_line):
            if bg_char in "~*":
                minor_decs.append([y, x, bg_char])
            if y > 7:
                continue
            if bg_char in "()":
                if bg_char == "(" and bg_line[x + 2] != ")":
                    main_dec.append([y, x, bg_char])
                if bg_char == ")" and bg_line[x - 2] != "(":
                    main_dec.append([y, x, bg_char])

    stdscr.addstr(0, 0, bg_frame)
    stdscr.refresh()

    denominator = 3
    finalized = False
    keyin = stdscr.getch()
    while keyin == -1 or not finalized:
        if keyin != -1:
            finalized = True

        random.shuffle(main_dec)
        random.shuffle(minor_decs)

        slice_amount_main = len(main_dec) // denominator
        slice_amount_minor = len(minor_decs) // denominator

        for dec in main_dec[:slice_amount_main]:
            if not finalized:
                dec[2] = "()".strip(dec[2])
            else:
                dec[2] = ","
            stdscr.addstr(dec[0], dec[1], dec[2])

        for minor_dec in minor_decs[:slice_amount_minor]:
            minor_dec[2] = "*~".strip(minor_dec[2])
            stdscr.addstr(minor_dec[0], minor_dec[1], minor_dec[2])

        stdscr.move(0, 0)
        stdscr.refresh()
        time.sleep(0.1)
        keyin = stdscr.getch()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error as e:
        print(f"There was an error with curses: {e}")
        print("Your terminal window might be too small to display the art.")
