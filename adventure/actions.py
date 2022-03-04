from player import Player

class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.name = name
        self.hotkey = hotkey
        self.kwargs = kwargs
        
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)
        
class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name="Move north", hotkey="w")
        
class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name="Move south", hotkey="s")
        
class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name="Move east", hotkey="d")
        
class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name="Move west", hotkey="a")
        
class DisplayInventory(Action):
    def __init__(self):
        super().__init__(method=Player.print_inventory, name="Display inventory", hotkey="i")
        
class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey="x", enemy=enemy)
        
class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey="f", tile=tile)
        
class UsePotion(Action):
    def __init__(self):
        super().__init__(method=Player.use_potion, name="Use Potion", hotkey="q")