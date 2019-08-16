class Skill():
    def __init__(self, skill: str, shorthand=''):
        self.skill = skill
        self.shorthand = shorthand

        if shorthand == '':
            words = skill.split(' ')
            for w in words:
                self.shorthand += w[0]

class SkillRequired():
    def __init__(self, skill: Skill, required, cost = 2):
        self.skill = skill
        self.required = required
        self.cost = cost

def count_skills(nurses, skills_required):
    count = 0
    for nurse in nurses:
        invalid = False
        for req_skill in skills_required:
            if req_skill.skill in nurse.skills:
                continue
            else:
                invalid = True
                break
        
        if not invalid:
            count += 1

    return count