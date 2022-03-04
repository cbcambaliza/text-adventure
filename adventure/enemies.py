class Enemy():
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
        
    def is_alive(self):
        return self.hp > 0
        
class WildDog(Enemy):
    def __init__(self):
        super().__init__(name="Wild Dog", hp=10, damage=2)

class GiantLizard(Enemy):
    def __init__(self):
        super().__init__(name="Giant Lizard", hp=20, damage=7)
        
class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", hp=30, damage=15)