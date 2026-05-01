import random
import sys

FINAL_SQUARE = 100

# Classic Snakes & Ladders style board map.
# Ladders move forward (low -> high), pythons move backward (high -> low).
JUMPS = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100,
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
}


def wait_for_space(prompt_text: str) -> bool:
    """Wait for SPACE, Q, or A. Returns True if autoplay was requested."""
    print(prompt_text, end="", flush=True)
    if sys.platform == "win32":
        import msvcrt
        while True:
            ch = msvcrt.getwch()
            if ch == " ":
                print()
                return False
            elif ch.lower() == "q":
                print("\nThanks for playing!")
                sys.exit(0)
            elif ch.lower() == "a":
                print("\nAutoplay enabled — sit back and watch!")
                return True
            else:
                # Invalid key, loop and ask again
                pass
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == " ":
                    print()
                    return False
                elif ch.lower() == "q":
                    print("\nThanks for playing!")
                    sys.exit(0)
                elif ch.lower() == "a":
                    print("\nAutoplay enabled — sit back and watch!")
                    return True
                else:
                    # Invalid key, loop and ask again
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_player_count() -> int:
    while True:
        raw = input("How many players (1, 2, 3): ").strip()
        if raw in {"1", "2", "3"}:
            return int(raw)
        print("Please enter 1, 2, or 3.")


def get_player_names(count: int) -> list[str]:
    names: list[str] = []
    for idx in range(1, count + 1):
        name = input(f"Player {idx} name (Enter to use 'Player {idx}'): ").strip()
        names.append(name if name else f"Player {idx}")
    return names


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def main() -> None:
    print("Welcome to Pythons & Ladders!")
    print("Press SPACE to roll. Press A to autoplay. Press Q at any prompt to quit.")
    print()

    player_count = get_player_count()
    players = get_player_names(player_count)

    autoplay = wait_for_space("Press space bar to begin: ")

    positions = {name: 0 for name in players}
    rolls = {name: 0 for name in players}
    finish_order: list[str] = []

    current_index = 0
    while len(finish_order) < player_count:
        player = players[current_index]

        if player not in finish_order:
            die = random.randint(1, 6)
            rolls[player] += 1

            print(f"{player} rolls a {die}")

            attempted = positions[player] + die
            if attempted > FINAL_SQUARE:
                print(
                    f"{player} needs an exact roll to reach space {FINAL_SQUARE} and stays on space {positions[player]}"
                )
            else:
                positions[player] = attempted
                print(f"{player} lands on space {positions[player]}")

                if positions[player] in JUMPS:
                    destination = JUMPS[positions[player]]
                    if destination > positions[player]:
                        print(
                            f"Ladder! {player} climbs from space {positions[player]} to space {destination}"
                        )
                    else:
                        print(
                            f"Python! {player} slides from space {positions[player]} to space {destination}"
                        )
                    positions[player] = destination

                if positions[player] == FINAL_SQUARE:
                    finish_order.append(player)
                    print(f"{player} has finished in {ordinal(len(finish_order))} place!")

        current_index = (current_index + 1) % player_count

        if len(finish_order) < player_count:
            if not autoplay:
                autoplay = wait_for_space("Press space bar to continue: ")

    print("\nGame Over")
    print(f"Winner: {finish_order[0]} (rolls: {rolls[finish_order[0]]})")

    for place, name in enumerate(finish_order[1:], start=2):
        print(
            f"{ordinal(place)} place: {name} | rolls: {rolls[name]}"
        )


if __name__ == "__main__":
    main()
