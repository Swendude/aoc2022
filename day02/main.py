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

loses = {wins[k]: k for k in wins}


def choice_points(choice):
    if choice == "rock":
        return 1
    if choice == "paper":
        return 2
    if choice == "scissors":
        return 3


def rps_points(opp, you):
    if opp == you:
        return 3
    if wins[you] == opp:
        return 6
    else:
        return 0


def select_choice(opp, outcome):
    if outcome == "X":
        return wins[opp]  # lose
    if outcome == "Y":
        return opp  # draw
    if outcome == "Z":
        return loses[opp]  # win


with open("input.txt", "r") as inp:
    total = 0
    for line in inp:
        opp, outcome = line.strip().split(" ")
        opp = choices[opp]
        you = select_choice(opp, outcome)
        # print(opp, you)
        total += rps_points(opp, you) + choice_points(you)
    print(total)
