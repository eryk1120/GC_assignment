import argparse
import curses

from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

from tqdm import tqdm

from slot_machine import SlotMachine


def game(stdscr) -> None:
    # setup slot machine
    slot_machine = SlotMachine()
    # Set up the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.clear()  # clear TUI screen

    stdscr.addstr(0, 0, "Press space to roll!")
    stdscr.addstr(1, 0, "Press q to quit! :(")

    # Main loop
    while True:
        # display rolls
        stdscr.addstr(5, 0, slot_machine.get_screen())
        stdscr.addstr(10, 0, 50 * " ")
        stdscr.addstr(10, 0, f"Balance: {slot_machine.balance}")
        # Get user input
        key = stdscr.getch()

        if key == ord(" "):
            points = slot_machine.play()
            stdscr.addstr(9, 0, 50 * " ")  # clear line
            stdscr.addstr(9, 0, f"You won {sum(points)} points!")

        elif key == ord("q"):
            break

        # Refresh the screen
        stdscr.refresh()

    # Cleanup
    curses.endwin()


def simulate(revolutions: int = 1000, number_of_workers: int = None) -> None:
    number_of_workers = number_of_workers or cpu_count()
    print("Running test...")
    results = 0
    with tqdm(total=revolutions, desc="generating data...   ") as pbar:
        # tqdm supplies nice looking progress bars
        with ThreadPoolExecutor(max_workers=number_of_workers) as ex:
            futures = [
                ex.submit(
                    lambda _: [pbar.update(1), SlotMachine().play()],
                    pbar,
                )
                for _ in range(revolutions)
            ]

        for feature in as_completed(futures):
            results += sum(feature.result()[1]) - 5

    print(f"Sum of results: {results}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Run test function")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--revolutions",
        type=int,
        help="Number of revolutions (only valid with --simulate)",
    )

    args = parser.parse_args()

    if args.simulate:
        simulate(revolutions=args.revolutions)
    else:
        curses.wrapper(game)


if __name__ == "__main__":
    main()
