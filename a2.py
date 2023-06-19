
from __future__ import annotations
from a2_support import *


class Card():
    """
    Describes and initialises the card. Sets base variables. 
    Contains constructor of just self.

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
         'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        """Sets default damage, block and energy costs.

        Returns:
            None
        """
        self._damage = 0
        self._block = 0
        self._energy_cost = 1
        self._status = {}
        self._description = 'A card.'
       

    def get_damage_amount(self) -> int:
        """Returns the amount of damage this card done to its target.
        
        Default damage done by a card is 0

        Returns:
            the damage amount

        Examples: 
            >>> card.get_damage_amount()
            0
        """
        return self._damage
    
    def get_block(self) -> int:
        """Returns the amount of block this card adds to its user. 
        
        Default block amount is 0
        
        Returns:
            The block amount

        Examples: 
            >>> card.get_block()
            0
        """
        return self._block
    
    def get_energy_cost(self) -> int:
        """Returns the amount of energy this card costs to play.
        
        Default energy cost is 1. 
         
        Returns:
            The energy cost

        Examples: 
            >>> card.get_energy_cost()
            1
        """
        return self._energy_cost

    
    def get_status_modifiers(self) -> dict[str, int]:
        """Returns a dictionary describing each status modifier applied.

        Default is no status modifiers applied, an empty dictionary. 
        
        Returns:
            The status modifiers

        Examples: 
            >>> card.get_status_modifiers()
            {}
        """
        return self._status

    
    def get_name(self) -> str:
        """Returns the name of the card.
        
        Returns:
            The name of the card

        Examples: 
            >>> card.get_card_name()
            'Card'
        """
        return self.__class__.__name__

    
    def get_description(self) -> str:
        """Returns the description of the card. 
        
        Returns:
            The description of the card.
        
        Examples: 
            >>> card.get_description()
            'A card.'
        """
        return self._description
    
    def requires_target(self) -> bool:
        """Returns True is this card requires a target, and False
        if it does not. 
        
        Returns: 
            True or False

        Examples: 
            >>> card.requires_target()
            True
        """
        return True
    
    def __str__(self) -> str:
        """Returns the string representation of the card.
        
        Returns:
            Returns the Card Name: Description

        Examples: 
            >>> str(card)
            'Card: A card.'
        """
        return f"{self.__class__.__name__}: {self._description}"
    
    def __repr__(self) -> str:
        """Returns the text that would be required to create
        a new instance of this class identical to self.
        
        Returns:
            The name of the card with any parameters that are used to create it.
        
        Examples: 
            >>> card
            Card()
        """
        return f"{self.__class__.__name__}()"


class Strike(Card):
    """Strike deals 6 damage to its target.

    It costs 1 energy point to play. 
    
    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._damage = 6
        self._description = 'Deal 6 damage.'


class Defend(Card):
    """Defend adds 5 block to its user. 
    
    Defend does not require a target. It costs 1 energy point to play. 
    
    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._block = 5
        self._description = 'Gain 5 block.'
    
    def requires_target(self) -> bool:
        return False


class Bash(Card):
    """Bash adds 5 block to its user and causes 7 damage to its target. 
    
    It costs 2 energy points to play. 

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._block = 5
        self._damage = 7
        self._energy_cost = 2
        self._description = 'Deal 7 damage. Gain 5 block.'


class Neutralize(Card):
    """Neutralize deals 3 damage to its target. 
    
    It applies status modifiers to its target: 1 weak and 2 vulnerable.
    Neutralize does not cost any energy points to play. 

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._damage = 3
        self._energy_cost = 0
        self._status = {'weak': 1, 'vulnerable': 2}
        self._description = 'Deal 3 damage. Apply 1 weak. Apply 2 vulnerable.'


class Survivor(Card):
    """Survivor adds 8 block and applies 1 strength to its user. 
    
    Survivor does not require a target.

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._block = 8
        self._strength = 1
        self._status = {'strength': 1}
        self._description = 'Gain 8 block and 1 strength.'

    def requires_target(self) -> bool:
        return False


class Eruption(Card):
    """Eruption deals 9 damage to its target.

    Eruption costs 2 energy points to play.

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._damage = 9
        self._energy_cost = 2
        self._description = 'Deal 9 damage.'


class Vigilance(Card):
    """Vigilance adds 8 block and 1 strength to its user.

    Vigilance 2 energy points to play
    It does not require a target. 

    Attributes:
        _damage: an integer indicating the damage this card deals
        _block: an integer indicating the block amount this card provides
        _energy_cost: an integer indicating how much energy this card costs to
            play
        _status: a dictionary showing the status modifications, in the format 
            'str': int
        _description: a string that describes the card.
    """

    def __init__(self):
        super().__init__()
        self._block = 8
        self._energy_cost = 2
        self._status = {'strength': 1}
        self._description = 'Gain 8 block and 1 strength.'

    def requires_target(self) -> bool:
        return False


class Entity():
    """A type of entity in the game. 

    Can be either a player or a monster. 

    Attributes:
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    def __init__(self, max_hp: int) -> None:
        """Initialises the entity with a given max health.

        Args:
            max_hp: the max amount of health points for an entity

        Returns:
            None
        """
        self._max_hp = max_hp
        self._block = 0
        self._strength = 0
        self._weak = 0
        self._vulnerable = 0
        self._hp = self._max_hp
    
    def get_hp(self) -> int:
        """Returns the current HP for this entity

        Returns:
            The current health points of the entity

        Examples:
            >>> entity.get_hp()
            10
        """
        return self._hp
        
    def get_max_hp(self) -> int:
        """Returns the maximum hp possible for this entity.

        Returns:
            The maximum health points of the entity

        Examples:
            >>> entity.get_max_hp()
            10
        """
        return self._max_hp

    def get_block(self) -> int:
        """Returns the amount of block for this entity.

        Returns:
            The current block amount of the entity

        Examples:
            >>> entity.get_block()
            5
        """
        return self._block
    
    def get_strength(self) -> int:
        """Returns the amount of strength for this entity.
        
        Returns:
            The current strength amount of the entity

        Examples:
            entity.get_strength()
            4
        """
        return self._strength
    
    def get_weak(self) -> int:
        """Returns the number of turns for which this entity is weak.
        
        Returns:
            How many turns left that the entity is weak
        
        Examples: 
            entity.get_weak()
            5
        """
        return self._weak

    def get_vulnerable(self) -> int:
        """Returns the number of turns for which this entity is vulnerable.

        Returns:
            How many turns left that the entity is vulnerable

        Examples: 
            entity.get_vulnerable()
            5
        """
        return self._vulnerable
    
    def get_name(self) -> str:
        """Returns the name of the entity. 
        
        Returns:
            The name of the entity

        Examples:
            >>>entity.get_name()
            'Silent'
        """
        return self.__class__.__name__
    
    def reduce_hp(self, amount: int) -> None:
        """Reduces the health points of the target.
        
        Attacks the entity with a damage of amount.
        This involves reducing block until the amount of damage has been done
        or until block has reduced to zero, in which case the HP is reduced by
        the remaining amount. 
        
        Args:
            amount: the amount of damage that the entity is taking

        Returns:
            None

        Example:
            >>> entity.reduce_hp(12)
            58
        """
        # Loop through range to subtract one block or one hp at a time
        for x in range(0, amount):
            if self._hp == 0:
                break
            else:
                if self._block > 0:
                    self._block -= 1
                else:
                    self._hp -= 1
        return
    
    def is_defeated(self) -> bool:
        """Returns whether the entity is defeated or not.
        
        An entity is defeated if it has no HP remaining. 

        Returns:
            True or False

        Example:
            >>>entity.is_defeated()
            True
        """
        if self._hp == 0: 
            return True
        else:
            return False


    def add_block(self, amount: int) -> None:
        """Adds the given amount to the amount of block this entity has.
        
        Args:
            amount: the amount of block that the entity is adding

        Returns:
            None

        Example:
            >>> entity.add_block(12)
        """
        self._block += amount
        return
    
    def add_strength(self, amount: int) -> None:
        """Adds the given amount to the amount of strength this entity has.

        Args:
            amount: the amount of strength that the entity is adding

        Returns:
            None

        Example:
            >>>entity.add_strength(3)

        """
        self._strength += amount
        return
    
    def add_weak(self, amount: int) -> None:
        """Adds the given amount to the number of turns the entity is weak

        Args:
            amount: the number of turns of being weak that's being added

        Returns:
            None

        Example:
            >>>entity.add_weak(4)
        """
        self._weak += amount
        return
    
    def add_vulnerable(self, amount: int) -> None:
        """Adds the given amount to the amount of vulnerable this entity has.

        Args:
            amount: the number of turns of being vulnerable that's being added

        Returns:
            None

        Example:
            >>>entity.add_vulnerable(4)
        """
        self._vulnerable += amount
        return
    
    def new_turn(self) -> None:
        """Applies any status changes that occur when a new turn begins. 

        For the base Entity class, this involves setting block back to 0, 
        and reducing weak and vulnerable each by 1 if they are greater than 0.

        Returns:
            None
        
        Example:
            >>>entity.new_turn()
        """
        # Reduce variable values if they are greater than 0
        self._block = 0
        if self._weak > 0:
            self._weak -= 1
        if self._vulnerable > 0:
            self._vulnerable -= 1

        return
    
    def __str__(self) -> str:
        """Returns that string representation for the entity.

        Returns:
            The string representation for the entity.
        """
        return (f"{self.__class__.__name__}: {self.get_hp()}/"
                f"{self.get_max_hp()} HP")
    
    def __repr__(self) -> str:
        """Returns the text that would be required to create a new instance of 
        this class identical to self.

        Returns:
            The text that is required to create a new instance of this class
        """
        return f"{self.__class__.__name__}({self._max_hp})"


class Player(Entity):
    """An entity that the user controls. 
    
    In addition to a regular entity, a player also has energy and cards. 
    Players have the deck, their hand and a discard pile.

    Attributes:
        _energy: The player's energy
        _deck: The cards in the chosen player's deck
        _hand: The current cards in the player's hand
        _discard_pile: The current cards in the discard pile
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        """Initialises the player. 
        
        Initialise the player's energy - starting at 3 and 
        3 lists of cards (deck, hand and discard pile). 

        Args:
            max_hp: the amount used to initialise the player's max health
            cards: the cards the player has
        
        Returns:
            None

        Examples: 
            >>> player = Player()
        """
        super().__init__(max_hp)
        self._energy = 3
        if cards is None:
            self._deck = []
        else:
            self._deck = cards
        self._hand = []
        self._discard_pile = []
    
    def get_energy(self) -> int:
        """Returns the amount of energy the user has remaining
        
        Returns:
            The energy the user has remaining
        
        Examples: 
            >>> player.get_energy()
            4
        """
        return self._energy
    
    def get_hand(self) -> list[Card]:
        """Returns the player's current hand.

        Returns:
            The current cards in the player's hand

        Examples:
            >>> player.get_hand()
            ['bash', 'block']
        """
        return self._hand
    
    def get_deck(self) -> list[Card]:
        """Returns the players current deck.

        Returns:
            The current cards in the player's deck

        Examples:
            >>> player.get_deck()
            ['bash', 'block']
        """
        return self._deck
    
    def get_discarded(self) -> list[Card]:
        """Returns the players current discard pile.

        Returns:
            The current cards in the player's discard pile

        Examples:
            >>> player.get_discarded()
            ['bash', 'block']
        """
        return self._discard_pile
    
    def start_new_encounter(self) -> None:
        """Starts a new encounter, and empties the player's discard pile.
        
        Adds all cards from the player's disard pile to the end of their deck, 
        and sets the discard pile to be an empty list. 

        Returns: 
            None

        Examples:
            >>> player.start_new_encounter()
        """
        if self._hand ==[]:
            self._deck.extend(self._discard_pile)
            self._discard_pile = []

        return

    def end_turn(self) -> None:
        """Resets the player's hand. 
        
        Adds all remaining cards from the player's hand to the end
        of their disard pile and sets their hand back to an empty list.

        Returns:
            None

        Examples:
            >>> player.end_turn()
        """
        self._discard_pile.extend(self._hand)
        self._hand = []
        return
    
    def new_turn(self) -> None:
        """Sets the player up for a new turn.

        Player is dealt a new hand of 5 cards
        Energy is reset to 3
        
        Returns:
            None
        
        Examples: 
            >>> player.new_turn()
        """
        super().new_turn()
        draw_cards(self._deck, self._hand, self._discard_pile)
        self._energy = 3
        return
    
    def play_card(self, card_name: str) -> Card | None:
        """Attempts to play a card from the player's hand. 

        If a card with the given name exists in the player's hand and the
        player has enough energy to play said card, the card is removed from 
        the player's hand and added to discard pile, required energy deducted 
        and card returned. 
        If no card with given name exists in hand, or player doesn't have 
        enough energy to play, this function returns none. 

        Args:
            The name of the card to be played

        Returns:
            The card that has been played, or None.
        """
        # Check if card is in hand, and complete actions
        if self._hand:
            for card in self._hand:
                if card.__class__.__name__ == card_name:
                    if card.get_energy_cost() > self._energy:
                        break
                    else:
                        self._energy -= card.get_energy_cost()
                        self._discard_pile.append(card)
                        self._hand.remove(card)
                        return card
                else:
                    pass
        return
    

    def __repr__(self) -> str:
        # Include cards if there are any.
        if self._deck == []:
            return f"{self.__class__.__name__}({self._max_hp})"
        else:
            return f"{self.__class__.__name__}({self._max_hp}, {self._deck})"


class IronClad(Player):
    """A Player that starts with 80HP.

    IronClad's deck contains 5 Strike cards, 4 Defend cards and 1 Bash card.

    Attributes:
        _energy: The player's energy
        _deck: The cards in the chosen player's deck
        _hand: The current cards in the player's hand
        _discard_pile: The current cards in the discard pile
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    def __init__(self):
        """
        Initialises IronClad with max HP of 80. 
        """
        super().__init__(80)
        self._deck = [
            Strike(), 
            Strike(), 
            Strike(), 
            Strike(), 
            Strike(),
            Defend(), 
            Defend(), 
            Defend(), 
            Defend(), 
            Bash()
            ]
        
    def __repr__(self) -> str:
        # Return name of class without hp
        return f"{self.__class__.__name__}()"


class Silent(Player):
    """A Player that starts with 70 HP. 

    Silent's deck contains 5 Strike cards, 5 Defend cards, 1 Neutralise and
    1 Survivor card. 

    Attributes:
        _energy: The player's energy
        _deck: The cards in the chosen player's deck
        _hand: The current cards in the player's hand
        _discard_pile: The current cards in the discard pile
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    def __init__(self):
        super().__init__(70)
        self._deck = [
            Strike(), 
            Strike(), 
            Strike(), 
            Strike(), 
            Strike(), 
            Defend(), 
            Defend(), 
            Defend(), 
            Defend(), 
            Defend(), 
            Neutralize(), 
            Survivor()
            ]

    def __repr__(self) -> str:
        # Return name of class without hp
        return f"{self.__class__.__name__}()"


class Watcher(Player):
    """A Player that starts with 72 HP. 
    
    Watcher's deck contains 5 Strike cards, 5 Defend cards, 1 Neutralise and
    1 Survivor card. 

    Attributes:
        _energy: The player's energy
        _deck: The cards in the chosen player's deck
        _hand: The current cards in the player's hand
        _discard_pile: The current cards in the discard pile
    """

    def __init__(self):
        super().__init__(72)
        self._deck = [
            Strike(), 
            Strike(), 
            Strike(), 
            Strike(),
            Defend(), 
            Defend(), 
            Defend(), 
            Defend(), 
            Eruption(), 
            Vigilance()
            ]

    def __repr__(self) -> str:
        # Return name of class without hp
        return f"{self.__class__.__name__}()"


class Monster(Entity):
    """A entity that the user battles during encounters. 

    Each monster has a unique id, and an action method that handles effects of 
    the monster's action on itself, and desribes the effect the monster's 
    action would have on its target.
    Each monster takes one action per turn. 

    Attributes:
        _id: the unique id of the monster
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    # Create class variable for monster counter
    monster_counter = 0

    def __init__(self, max_hp: int):
        super().__init__(max_hp)
        self._id = Monster.monster_counter
        Monster.monster_counter += 1

    
    def get_id(self) -> int:
        """Returns the unique ID for this monster

        Returns:
            The unique ID for the monster

        Examples:
        >>> monster.get_id()
        2
        """
        return self._id
    
    def action(self) -> dict[str, int]:
        """Performs the current action for this monster.
         
        Returns:
            Returns a dict describing the effects this monster's action should 
            cause to its target.

        Examples:
            >>> monster.action()
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            ...
            raise NotImplementedError
            NotImplementedError

            >>> louse.action()
            {'damage': 6}
        """
        raise NotImplementedError


class Louse(Monster):
    """A type of monster. 

    Has a random amount of damage between 5 and 7 (inclusive).

    Attributes:
        _id: the unique id of the monster
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
    """

    def __init__(self, max_hp: int):
        super().__init__(max_hp)
        self._action = {'damage': random_louse_amount()}


    def action(self) -> dict[str, int]:
        return self._action


class Cultist(Monster):
    """Cultist is a type of Monster. 

    Attributes:
        _id: the unique id of the monster
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
        num_calls: number of times the action method has been called on this 
        specific Cultist instance
        damage_amount: the amount of damage this monster does
        weak_amount: the number of turns that the action of this monster causes 
        the player to be weak for
    """

    def __init__(self, max_hp: int):
        super().__init__(max_hp)
        self.num_calls = 0
        self.damage_amount = 0
        self.weak_amount = 0
    
    def action(self) -> dict[str, int]:
        """Returns the damage or status modifications

        Returns:
            A dictionary describing how much damage or weak has been applied.
        """
        self._action = {'damage': self.damage_amount, 'weak': self.weak_amount}

        # Re-define damage amount for new number of calls
        self.num_calls += 1
        self.damage_amount = 6 + self.num_calls

        # Alternate weak amount
        if self.weak_amount == 0:
            self.weak_amount = 1
        else:
            self.weak_amount = 0
        return self._action


class JawWorm(Monster):
    """A type of Monster. 

    Attributes:
        _id: the unique id of the monster
        _max_hp: the max amount of health points for an entity
        _block: the current block amount of the entity
        _strength: the current strength amount of the entity
        _weak: how many turns left that the entity is weak
        _vulnerable: how many turns left that the entity is vulnerable
        _hp: the current health points of the entity
        _damage_amount: the amount of damage this monster does
        _damage_taken: the amount of damage this monster has taken
    """

    def __init__(self, max_hp: int):
        super().__init__(max_hp)
        self.damage_amount = 0
        self.damage_taken = 0

    def action(self) -> dict[str, int]:
        self.damage_taken = self._max_hp - self._hp
        self._block += -(-self.damage_taken//2)    # Dbl negative to round up
        self.damage_amount = int(self.damage_taken/2)   # Damage rounding down
        self._action = {'damage': self.damage_amount}
        return self._action


class Encounter():
    """An interaction between a player and monsters. 

    Manages one player and a set of 1 to 3 monsters, and facilitates
    interactions between the player and monsters. 

    Attributes:
        _player: the chosen player entity
        _monsters: the given list of monsters and their health
        _encounter_monsters: a list of initialised monster entities
    """

    def __init__(self, player: Player, monsters: list[tuple[str, int]]) -> None:
        """Initilises the interaction between player and monsters.

        Args:
            player: the chosen player entity
            monsters: the given list of monsters and their health

        Returns:
            None
        """
        self._player = player
        self._monsters = monsters
        self._encounter_monsters = []

        # Construct all monster instances required
        for monster in self._monsters:
            if monster[0] == 'Louse':
                self._encounter_monsters.append(Louse(monster[1]))
            if monster[0] == 'Cultist':
                self._encounter_monsters.append(Cultist(monster[1]))
            if monster[0] == 'JawWorm':
                self._encounter_monsters.append(JawWorm(monster[1]))
        
        self._player.start_new_encounter()
        self.start_new_turn()


    def start_new_turn(self) -> None:
        """Sets it to be the player's turn and calls the new turn on the player.

        Returns:
            None

        Example:
            >>>encounter.start_new_turn()
        """
        self._players_turn = True
        self._player.new_turn()
        return
    
    def end_player_turn(self) -> None:
        """Sets it to not be the player's turn.

        Ensures all remaining cards in player's hand are moved to discard pile.
        Calls new turn method on all monster instances. 

        Returns:
            None
        """
        self._players_turn = False
        self._player.end_turn()

        for monster in self._encounter_monsters:
            monster.new_turn()
        
        return
    
    def get_player(self) -> Player:
        """Returns the player in this encounter

        Returns:
            The player instance
        """
        return self._player
    
    def get_monsters(self) -> list[Monster]:
        """Returns the monsters remaining in this encounter

        Returns:
            A list of the monster instances
        """
        return self._encounter_monsters
    
    def is_active(self) -> bool:
        """Returns True if there are monsters remaining in this encounter.

        Returns:
            True or False if there are monsters remaining
        """
        if self._encounter_monsters == []:
            return False
        else:
            return True
    
    def player_apply_card(self, card_name: str, 
                          target_id: int | None = None) -> bool:
        """Attempts to apply the first card with the given name from the 
        player's hand.

        Returns:
            True or False if the action was successful
        """
        card_played = self._player.play_card(card_name)

        if card_played is None:
            return False
        
        # Only offensive cards require target
        if (card_name in ['Strike', 'Bash', 'Neutralize', 'Eruption'] and 
         target_id is None):
            return False
        
        if not self._players_turn:
            return False
        
        # Check if target id is correct
        self._target_monster = None
        if target_id is not None:
            for monster in self._encounter_monsters:
                if target_id == monster.get_id():
                    self._target_monster = monster
                    break
            
            if not self._target_monster:
                return False
            
        self._player.add_block(card_played.get_block())

        status_modifiers = card_played.get_status_modifiers()
        if 'strength' in status_modifiers:
            self._player.add_strength(status_modifiers['strength'])
            
        if self._target_monster:
            if 'vulnerable' in status_modifiers:
                self._target_monster.add_vulnerable(status_modifiers
                                                    ['vulnerable'])
            if 'weak' in status_modifiers:
                self._target_monster.add_weak(status_modifiers['weak'])
                
            card_damage = (card_played.get_damage_amount()
                           + self._player.get_strength())
            if self._target_monster.get_vulnerable() > 0:
                card_damage *= 1.5
            if self._player.get_weak() > 0: 
                card_damage *= 0.75
                
            card_damage = int(card_damage)
            self._target_monster.reduce_hp(card_damage)
            
            if self._target_monster.is_defeated():
                self._encounter_monsters.remove(self._target_monster)
        
        
        return True

    def enemy_turn(self) -> None:
        """Allows remaining monsters in the encounter to take an action. 
        
        Returns:
            None
        """
        if self._players_turn:
            return
        
        for monster in self._encounter_monsters:
            monster_action = monster.action()
            if 'weak' in monster_action:
                self._player.add_weak(monster_action['weak'])
            if 'vulnerable' in monster_action:
                self._player.add_vulnerable(monster_action['vulnerable'])
            if 'strength' in monster_action:
                monster.add_strength(monster_action['strength'])

            # Set base damage
            base_monster_damage = (monster.get_strength() 
                                   + monster_action['damage'])
            
            # Determine actual damage amount
            monster_damage = base_monster_damage
            if self._player.get_vulnerable() > 0:
                monster_damage = base_monster_damage * 1.5
            if monster.get_weak() > 0:
                monster_damage *= 0.75
            monster_damage = int(monster_damage)

            self._player.reduce_hp(monster_damage)
        self.start_new_turn()
        return



def main():
    """Starts the game

    End turn: End user's turn and allow the monsters to perform their actions.
    Inspect {deck | disard}: Inspect the deck or discard pile.
    Describe {card_name}: Describe what the given card does.
    Play {card_name}{target_id}: Play the given card name and, if relevant, 
    against the target with the given id. 
    """
    # Initialise player entities using user input
    player = input("Enter a player type: ")
    game_file = input("Enter a game file: ")
    
    if player == "ironclad":
        player = IronClad()
    if player == "silent":
        player = Silent()
    if player == "watcher":
        player = Watcher()

    # Set up dictionary of descriptions to avoiding looping
    card_descriptions = {
        "Bash": Bash().get_description(),
        "Strike": Strike().get_description(),
        "Defend": Defend().get_description(),
        "Neutralize": Neutralize().get_description(),
        "Survivor": Survivor().get_description(),
        "Eruption": Eruption().get_description(),
        "Vigilance": Vigilance().get_description()
    }

    encounters = read_game_file(game_file)
    # Set variables to break loops
    game_lost = False
    encounter_end = False

    # Start encounter loop here, break if game lost or encounter is ended
    for encounter in encounters:
        if game_lost:
            break
        current_encounter = Encounter(player, encounter)
        
        monsters = current_encounter.get_monsters()
        if monsters == []:
            encounter_end = True
            break
        else: 
            encounter_end = False
            print("New encounter!\n")
        
        while not encounter_end:
            monster_state = "MONSTERS\n"

            # Set up bar length and assign visuals for monster
            for monster in monsters:
                monster_bar_length = len(f"{str(monster)}")
                monster_state += (
                    f"{'-' * monster_bar_length}\n"
                    f"Monster {monster.get_id()}\n"
                    f"{str(monster)}\n"
                    f"{'-' * monster_bar_length}\n"
                    )
                
            # Set up bar length and assign visuals for player
            player_bar_length = len(f"Hand: {player.get_hand()}")
            player_state = (
                "\n\n\nPLAYER\n"
                f"{'-'*player_bar_length}\n"
                f"{player.get_name()}\n"
                f"HP: {player.get_hp()}/{player.get_max_hp()}\n"
                f"Energy: {player.get_energy()}\n"
                f"Hand: {player.get_hand()}\n"
                f"Block: {player.get_block()} "
                f"Strength: {player.get_strength()} "
                f"Vulnerable: {player.get_vulnerable()} "
                f"Weak: {player.get_weak()}\n"
                f"{'-'*player_bar_length}"
                )

            error_message = ("\nCard application failed.\n")
            print(monster_state,player_state, sep='')
            card_played = False
            

            # Loop for playing cards while encounter or turn hasn't ended.
            while not card_played:
                # If won the encounter
                if monsters == []:
                    print("\nYou have won the encounter!\n")
                    encounter_end = True
                    break
                move = input("Enter a move: ").split(" ")

                # End turn here and check for game lost.
                if move[0] == "end":
                    current_encounter.end_player_turn()
                    current_encounter.enemy_turn()
                    if player.is_defeated():
                        print("\nYou have lost the game!\n")
                        game_lost = True
                        encounter_end = True
                    card_played = True
                        
                # Inspecting the cards in deck or discard
                if move[0] == "inspect":
                    if move[1] == "deck":
                        print(f"\n{player.get_deck()}\n")
                    elif move[1] == "discard":
                        print(f"\n{player.get_discarded()}\n")

                # Use previously initiated dictionary to pull out descriptions.
                if move[0] == "describe":
                    if move[1] in card_descriptions:
                        print(f"\n{card_descriptions[move[1]]}\n")
                    else:
                        print(error_message)
                
                # Offensive cards require target, defensive don't. 
                if move[0] == "play":
                    if (move[1] in ['Strike', 'Bash','Neutralize', 'Eruption'] 
                        and len(move) > 2):
                        card_played = current_encounter.player_apply_card(
                            move[1], int(move[2]))
                    elif (move[1] in ['Defend', 'Survivor', 'Vigilance'] 
                          and len(move) == 2):
                        current_encounter.player_apply_card(move[1])
                        card_played = True
                    else:
                        print(error_message)
    
    # If made it to this point in loop and game hasn't been lost -> print win.
    if not game_lost:
        print("\nYou have won the game!\n")

if __name__ == '__main__':
    main()

