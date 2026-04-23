import random

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


def wait_for_space(prompt_text: str) -> None:
    """Require a space bar + Enter input before continuing."""
    while True:
        entered = input(prompt_text)
        if entered == " ":
            return
        print("Please press the space bar, then Enter.")


def get_player_count() -> int:
    while True:
        raw = input("How many players (1, 2, 3): ").strip()
        if raw in {"1", "2", "3"}:
            return int(raw)
        print("Please enter 1, 2, or 3.")


def get_player_names(count: int) -> list[str]:
    names: list[str] = []
    for idx in range(1, count + 1):
        while True:
            name = input(f"Player {idx} name: ").strip()
            if name:
                names.append(name)
                break
            print("Name cannot be empty.")
    return names


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def main() -> None:
    print("Welcome to Pythons & Ladders!")

    player_count = get_player_count()
    players = get_player_names(player_count)

    wait_for_space("Press space bar to begin: ")

    positions = {name: 0 for name in players}
    rolls = {name: 0 for name in players}
    finish_order: list[str] = []

    current_index = 0
    while not finish_order:
        player = players[current_index]

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

        if finish_order:
            break

        wait_for_space("Press space bar to continue: ")

        current_index = (current_index + 1) % player_count

    winner = finish_order[0]
    print("\nGame Over")
    print(f"Winner: {winner} (rolls: {rolls[winner]})")

    others = [name for name in players if name != winner]
    others_sorted = sorted(others, key=lambda name: (-positions[name], rolls[name], name.lower()))

    place = 2
    for name in others_sorted:
        print(
            f"{ordinal(place)} place: {name} | position: {positions[name]} | rolls: {rolls[name]}"
        )
        place += 1


if __name__ == "__main__":
    main()
