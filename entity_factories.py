from Entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

bot = Entity(char="b", color=(63, 127, 63), name="Security Bot", blocks_movement=True)
employee = Entity(char="E", color=(0, 127, 0), name="Employee", blocks_movement=True)