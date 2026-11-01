def time_to_s (time_str):
    m = int(time_str.split(":")[0])*60
    s = int(time_str.split(":")[1].split(".")[0])
    ms = 0
    if "." in time_str:
        ms = float(f"0.{time_str.split('.')[1]}")
    return m + s + ms
    
def s_to_time (seconds):
    ms = int(round(seconds % 1, 2) * 100)
    seconds -= ms / 100
    s = int(seconds % 60)
    seconds -= s
    print(seconds)
    m = int(seconds/60)
    return f"{m:>2}:{s:02d}.{ms:02d}"

class Runner:
    def __init__ (self, raw_lines, team_name):
        self.name = raw_lines[0]
        self.grade = raw_lines[1][-2:]
        self.pr = raw_lines[2].split("\t")[1]
        self.pr_s = time_to_s(self.pr)
        self.pr_meet = raw_lines[2].split("\t")[2]
        self.team_name = team_name
        
    def team_display (self):
        return f"{self.name[:18]}\t{'\t' if len(self.name)<11 else ''}({self.grade}) {self.pr} @ {self.pr_meet}"

    def html_display (self, place):
        return f"""
            <tr>
                <td>{place}</td>
                <td>{self.grade}</td>
                <td>{self.name}</td>
                <td>{self.pr}</td>
                <td>{self.team_name}</td>
                <td>{self.pr_meet}</td>
            </tr>
        """

    def __str__ (self):
        return f"{self.name[:23]}\t{'\t' if len(self.name)<=15 else ''}({self.grade}) {self.pr}  {self.team_name}"

    def change_time (self, time):
        self.pr = time
        if "." not in time:
            self.pr += ".00"
        self.pr_s = time_to_s(time)
        self.pr_meet = "[custom time]"

class Team:
    def __init__ (self, raw_str):
        lines = raw_str.split("\n")
        self.name = lines[0]
        self.avg = lines[3]
        self.team_split = lines[5]
        self.runners = []
        for i in range(len(lines)):
            if len(lines[i].strip()) == 1:
                self.runners.append(Runner(lines[i+1:i+4], self.name))

    def display_short (self):
        return f"{self.name} ({self.avg} avg, {self.team_split} split)"

    def display_html (self, place, score):
        return f"""
            <tr>
                <td>{place}</td>
                <td>{self.name}</td>
                <td>{score}</td>
                <td>{self.avg}</td>
            </tr>
        """

    def __str__ (self):
        ret = f"{self.name} ({self.avg} avg, {self.team_split} split)\n"
        ret += "\n".join([f"  {i+1}. " + self.runners[i].team_display() for i in range(len(self.runners))])

        return ret