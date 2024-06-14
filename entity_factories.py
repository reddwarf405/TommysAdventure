from Entity import Actor
from components.ai import HostileEnemy
from components.fighter import Fighter

player = Actor(char="@", color=(255, 255, 255), name="Tommy", ai_cls=HostileEnemy, fighter=Fighter(hp=30, defense=2, power=5),)

bot = Actor(char="b", color=(63, 127, 63), name="Security Bot", ai_cls=HostileEnemy, fighter=Fighter(hp=8, defense=2, power=2))
employee = Actor(char="E", color=(0, 127, 0), name="Employee", ai_cls=HostileEnemy, fighter=Fighter(hp=14, defense=1, power=4))