from models import Team
from pyscript import web, when
from js import window

with open("uil_5a_team_rankings_10_31_26.txt", "r") as f:
    team_blocks = f.read().split("\n\n")

state_teams = [
    "Mansfield Legacy", "Fort Worth Paschal", "Wolfforth Frenship", "Burleson Centennial",
    "Dallas Wilson", "Grapevine", "Lucas Lovejoy", "Midlothian Heritage",
    "Austin LASA", "College Station", "Georgetown High", "College Station A&M Cons",
    "Weslaco East", "Boerne Champion", "Corpus Christi Veterans Memorial", "McAllen"
]
teams = []
runners = []
teams_dict = {}

def initialize_objects ():
    for team in team_blocks:
        new_team = Team(team)
        if new_team.name in state_teams:
            teams.append(new_team)
            runners.extend(new_team.runners)
            teams_dict[new_team.name] = new_team
    runners.sort(key=lambda x: x.pr_s)

initialize_objects()

changes = []
change_time_button = web.page["change-time-button"]
meet_bias_button = web.page["meet-bias-button"]

def change_time (name, time):
    runner = None
    for r in runners:
        if r.name == name:
            runner = r
            break
    if not runner:
        return

    runner.set_time(time)
    runners.sort(key=lambda x: x.pr_s)

def calculate_scores ():
    for team in teams:
        team.scores = []

    for i in range(len(runners)):
        team = runners[i].team_name
        teams_dict[team].scores.append(i+1)

    for team in teams:
        team.update_avg()

    teams.sort(key=lambda team: sum(team.scores[:5]))

def update_results ():
    web.page["ind-results"].innerHTML = """
        <tr>
            <th class="place-col">#</th>
            <th class="grade-col">YR</th>
            <th class="ind-name-col">Name</th>
            <th class="time-col">Time</th>
            <th>Team</th>
            <th>Meet</th>
        </tr>
    """ + "\n".join([runners[i].html_display(i+1) for i in range(len(runners))])

    calculate_scores()
    web.page["team-results"].innerHTML = """
        <tr>
            <th class="place-col">#</th>
            <th class="team-name-col">Team</th>
            <th class="score-col">Score</th>
            <th class="time-col">Avg</th>
        </tr>
    """ + "\n".join([teams[i].display_html(i+1) for i in range(len(teams))])

update_results()

@when("click", change_time_button)
def handle_time_change(_):
    change_time(web.page["name-input"].value, web.page["time-input"].value)
    update_results()
    web.page["name-input"].value = ""
    web.page["time-input"].value = ""

@when("click", meet_bias_button)
def handle_meet_bias(_):
    for runner in runners:
        if runner.pr_meet == web.page["meet-input"].value:
            runner.increase_time(int(web.page["meet-bias-input"].value))
    runners.sort(key=lambda x: x.pr_s)
    update_results()
    web.page["meet-bias-input"].value = ""
    web.page["meet-input"].value = ""