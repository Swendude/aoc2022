choices = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

wins = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}


def choice_points(choice):
    choice = choices[choice]
    if choice == "rock":
        return 1
    if choice == "paper":
        return 2
    if choice == "scissors":
        return 3


def rps_points(opp, you):
    opp, you = choices[opp], choices[you]
    if opp == you:
        return 3
    if wins[you] == opp:
        return 6
    else:
        return 0


with open("input.txt", "r") as inp:
    total = 0
    for line in inp:
        opp, you = line.strip().split(" ")
        total += rps_points(opp, you) + choice_points(you)
    print(total)
