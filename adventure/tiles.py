import random
import items, enemies, actions, world

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def intro_text(self):
        raise NotImplementedError()
        
    def modify_player(self, player):
        raise NotImplementedError()
        
    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles"""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
            
    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.DisplayInventory())
        moves.append(actions.UsePotion())
        
        return moves
        

class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """
        
    def modify_player(self, player):
        #Room has no action on the player
        pass
        
class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        self.obtained = False
        super().__init__(x, y)
    
    def add_loot(self, player):
        player.inventory.append(self.item)
        self.obtained = True
    
    def modify_player(self, player):
        if self.obtained == False:
            self.add_loot(player)
        
class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
    
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage.".format(self.enemy.damage))
        if not the_player.is_alive():
            print("You have died. \nGame over")
            
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()
            
            
class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
        
    def modify_player(self, player):
        #Room has no action on the player
        pass
        
class WildDogRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.WildDog())
        
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A rabid wild dog lunges towards you!
            """
        else:
            return """
            The corpse of a wild dog rots on the ground.
            """
            
class GiantLizardRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantLizard())
        
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            Thsssss... a giant lizard crawls out from a crack in the cave wall and eyes you hungrily.
            """
        else:
            return """
            The corpse of a giant lizard lies rotting on the ground.
            """
            
class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())
        
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            RAAARGHH! A brutish ogre seeks your bones for dinner!
            """
        else:
            return """
            The dead ogre remains on the cave floor.
            """

class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())
        
    def intro_text(self):
        if self.obtained == False:
            return """
            You notice something shiny in the corner.
            It's a dagger! You pick it up.
            """
        else:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        
class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))
        
    def intro_text(self):
        if self.obtained == False:
            return """
            You come across a 5 gold piece on the floor and pick it up.
            """
        else:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        
class FindPotionRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Potion())
        
    def intro_text(self):
        if self.obtained == False:
            return """
            You find a red potion on the floor and pick it up.
            """
        else:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
            
class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a light and walk closer to it... you must be nearing the exit!
        
        You have escaped the cave!
        """
        
    def modify_player(self, player):
        player.victory = True
        
class DeathTrapRoom(MapTile):
    def intro_text(self):
        return """
        You fall into a spiked pit! You have died.
        """
        
    def modify_player(self, player):
        player.hp = 0
        
class TrapRoom(MapTile):
    def __init__(self, x, y):
        self.traptype = random.randint(0, 3)
        self.triggered = False
        super().__init__(x, y)
        
    def intro_text(self):
        if self.triggered == False:
            match self.traptype:
                case 0:
                    return """
                    You fall into a spiked pit! You have died.
                    """
                case 1:
                    return """
                    You tripped a wire that shoots a bolt towards you. You suffer 5 damage.
                    """
                case 2:
                    return """
                    You step on a pressure plate and flames shoot from the wall at you. You suffer 10 damage.
                    """
                case 3:
                    return """
                    A bunch of venomous snakes bite at your heels. You are able to dispose of them with ease, but suffer 15 damage in the process
                    """
        else:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
            
    def modify_player(self, player):
        if self.triggered == False:
            match self.traptype:
                case 0:
                    player.hp = 0
                case 1:
                    player.hp -= 5
                case 2:
                    player.hp -= 10
                case 3:
                    player.hp -= 15
        if player.is_alive():
            print(f"You have {player.hp} HP remaining")
            self.triggered = True
        else:         
            print("You have died. \nGame over")
        