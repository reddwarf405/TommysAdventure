from components.ai import HostileEnemy
from components.fighter import Fighter
from components import consumable
from components.inventory import Inventory
from Entity import Item, Actor

player = Actor(char="@", color=(255, 255, 255), name="Tommy", ai_cls=HostileEnemy, fighter=Fighter(hp=30, defense=2, power=5), inventory=Inventory(capacity=26),)

bot = Actor(char="b", color=(63, 127, 63), name="Security Bot", ai_cls=HostileEnemy, fighter=Fighter(hp=8, defense=2, power=2), inventory=Inventory(capacity=0),)
employee = Actor(char="E", color=(0, 127, 0), name="Employee", ai_cls=HostileEnemy, fighter=Fighter(hp=14, defense=1, power=4), inventory=Inventory(capacity=0),)
bandage = Item(char= "!", color=(127, 0, 255), name="Nanotech Bandage", consumable=consumable.HealingConsumable(amount=4))
onetimehack = Item(char= "~", color=(255, 255, 0), name="System Disruptor", consumable=consumable.LightningDmgConsumable(damage=10, max_range=5))
emp = Item(char= "~", color=(207, 63, 255), name="Short-Range EMP", consumable=consumable.ConfusionConsumable(number_of_turns=3))
bomb = Item(char= "~", color=(255, 0, 0), name="Tubbo's Bomb", consumable=consumable.BombDamageConsumable(damage=8, radius=3))