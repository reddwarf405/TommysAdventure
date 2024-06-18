from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

from Entity import Actor
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from Entity import Entity, Actor, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine
    
    def perform(self)-> None:
        # 'Engine' is the scope where the action is being performed, entity is the object doing the action
        # This method will be overriden by the action subclasses. 
        raise NotImplementedError()

class PickUpAction(Action):
    # Pick up an item and add it to the inventory, if there's room for it
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self)-> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")
                
                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return
        
        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None) -> None:
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy
    
    @property
    def target_actor(self) -> Optional[Actor]:
        #Return actor at destination of this item
        return self.engine.game_map.get_actor_at(*self.target_xy)

    def perform(self) -> None:
        # Invokes items ability
        self.item.consumable.activate(self)
    
class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)

class WaitAction(Action):
    def perform(self) -> None:
        pass

class TakeStairsAction(Action):
    def perform(self) -> None:
        # Take the stairs, if there are any at the player's location
        if (self.entity.x, self.entity.y) == self.engine.game_map.upstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You ascend the staircase.", color.ascend
            )
        else:
            raise exceptions.Impossible("There are no stairs here.")

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at(*self.dest_xy)
    
    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAttack(ActionWithDirection):
     def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")
        
        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination out of bounds
            raise exceptions.Impossible("The way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination not walkable (wall)
            raise exceptions.Impossible("The way is blocked.")
        if self.engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            # Destination is blocked by an entity (not walkable)
            raise exceptions.Impossible("The way is blocked.")
        
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAttack(self.entity, self.dx, self.dy).perform()
    
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()