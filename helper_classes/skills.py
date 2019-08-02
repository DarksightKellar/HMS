class Skill():
    def __init__(self, skill: str, shorthand=''):
        self.skill = skill
        self.shorthand = shorthand

        if shorthand == '':
            words = skill.split(' ')
            for w in words:
                self.shorthand += w[0]

class SkillRequired():
    def __init__(self, skill: Skill, required):
        self.skill = skill
        self.required = required