from models import Team

with open("uil_5a_team_rankings_10_31_26.txt", "r") as f:
    team_blocks = f.read().split("\n\n")

state_teams = [
    "Mansfield Legacy", "Fort Worth Paschal", "Wolfforth Frenship", "Burleson Centennial",
    "Dallas Wilson", "Grapevine", "Lucas Lovejoy", "Midlothian Heritage",
    "Austin LASA", "College Station", "Georgetown High", "College Station A&M Cons",
    "Weslaco East", "Boerne Champion", "Corpus Christi Veterans Memorial", "McAllen"
]

def initialize_objects ():
    for team in team_blocks:
        new_team = Team(team)
        if new_team.name in state_teams:
            teams.append(new_team)
            runners.extend(new_team.runners)
    runners.sort(key=lambda x: x.pr_s)

teams = []
runners = []
initialize_objects()

def display_teams (limit=None, verbose=False):
    print("\n\nTEAMS--------------------------------------------------------------------------")
    print("\n".join([(i.display_short() if not verbose else str(i)) for i in teams[:(limit if limit else len(teams))]]))
    print()

def display_individuals (limit=None):
    print("\nINDIVIDUALS--------------------------------------------------------------------")
    print("\n".join([f"{i+1}.\t" + str(runners[i]) for i in range(len(runners) if not limit else limit)]))
    print()

def display_scores (limit=None):
    scores = {team: 0 for team in state_teams}
    runner_scores = {team: [] for team in state_teams}
    for i in range(len(runners)):
        team = runners[i].team_name
        if len(runner_scores[team]) < 5:
            scores[team] += i+1
        runner_scores[team].append(i+1)
    scores = dict(sorted(scores.items(), key=lambda item: item[1])[:(limit if limit else len(scores))])

    print("\n\nTEAM SCORES--------------------------------------------------------------------")
    for [team, score] in scores.items():
        print(f"{score:<3} {team:<32} ({' '.join([str(i) for i in runner_scores[team]])})")
    print()

def display_team_runners (name):
    print()
    for team in teams:
        if team.name == name:
            print(team)
    print()

def change_time (name, time):
    runner = None
    for r in runners:
        if r.name == name:
            runner = r
            break
    if not runner:
        return

    runner.change_time(time)
    runners.sort(key=lambda x: x.pr_s)

print("\n-----------------UIL 5A STATE XC CHAMPIONSHIPS 2026 SIMULATION-----------------")
print("This simulation allows you to view individual and team scores and tweak times.\n")
print("NOTE: Because this is just about team scores, individual quafiers have been")
print("      removed. Therefore, places are not accurate for individual awards.\n")
print("Type \"help\" or \"h\" to view commands.\n")

while (True):
    command = input("STATE 2026--->")
    args = command.split(" ")

    if command == "exit":
        break
    elif command == "help" or command == "h":
        print()
        print("ind [limit*]          Displays the first [limit] individuals.")
        print("team [limit*]         Displays the first [limit] teams.")
        print("score [limit*]        Displays the first [limit] team scores.")
        print("runners [team]        Displays the runners on team [team].")
        print("chtm [runner] [time]  Changes [runner]'s time to [time]. If [time] is negative, adds [time] to [runner]'s time.")
        print("\n* denotes an optional argument")
        print()
    elif args[0] == "ind":
        if len(args) > 1:
            display_individuals(int(args[1]))
        else:
            display_individuals()
    elif args[0] == "team":
        if len(args) > 1:
            display_teams(int(args[1]) if args[1].isnumeric() else None, "-v" in args)
        else:
            display_teams(None, "-v" in args)
    elif args[0] == "score":
        if len(args) > 1:
            display_scores(int(args[1]))
        else:
            display_scores()
    elif args[0] == "runners":
        display_team_runners(" ".join(args[1:]))
    elif args[0] == "chtm":
        change_time(" ".join(args[1:-1]), args[-1])