import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *
from tkinter import messagebox


class InfoBar(AbstractGrid):
    """The InfoBar class displays relevant information about the game state.

    It displays information about the current day, player's money, and energy.
    It inherits from the AbstractGrid class and acts as a 2x3 grid of text
    labels and values.

    Attributes:
    - _master: The parent widget of this frame.
    - _day: The current day in the game.
    - _money: The player's current amount of money.
    - _energy: The player's current energy level.
    - _day_label: The label displaying the current day.
    - _money_label: The label displaying the player's current amount of money.
    - _energy_label: The label displaying the player's current energy level.

    Args:
    - master (tk.Tk | tk.Frame): The parent widget of this frame.
    """

    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """Initializes the InfoBar class with the parent widget and dimensions.

        Args:
        - master (tk.Tk | tk.Frame): The parent widget of this frame.
        """
        super().__init__(
            master=master,
            dimensions=(2, 3),
            size=(FARM_WIDTH, INFO_BAR_HEIGHT)
        )

        start_day = 1
        start_money = 0
        start_energy = 100

        # Labels
        self.annotate_position((0, 0), "Day:", font=HEADING_FONT)
        self.annotate_position((0, 1), "Money:", font=HEADING_FONT)
        self.annotate_position((0, 2), "Energy:", font=HEADING_FONT)

        # Draw initial values
        self._day_label = self.create_text(
            self.get_midpoint((1, 0)),
            text=start_day
        )
        self._money_label = self.create_text(
            self.get_midpoint((1, 1)), text=f"${start_money}"
        )
        self._energy_label = self.create_text(
            self.get_midpoint((1, 2)), text=start_energy
        )

    def redraw(self, day: int, money: int, energy: int) -> None:
        """Update and redraw the day, money, and energy labels with new values.

        Args:
            day (int): The new value for the day label.
            money (int): The new value for the money label.
            energy (int): The new value for the energy label.
        """
        # Clear previous values
        self.delete(self._day_label)
        self.delete(self._money_label)
        self.delete(self._energy_label)

        # Redraw new values
        self._day_label = self.create_text(
            self.get_midpoint((1, 0)),
            text=day
        )
        self._money_label = self.create_text(
            self.get_midpoint((1, 1)), text=f"${money}"
        )
        self._energy_label = self.create_text(
            self.get_midpoint((1, 2)), text=energy
        )


class FarmView(AbstractGrid):
    """
    A class that represents a view of the farm.

    Args:
        master (tk.Tk | tk.Frame): The parent widget of the view.
        dimensions (tuple[int, int]): The number of rows and columns in
            the grid.
        size (tuple[int, int]): The size of the grid in pixels.
        **kwargs: Optional keyword arguments.

    Attributes:
        _master (tk.Tk | tk.Frame): The parent widget of the view.
        _dimensions (tuple[int, int]): The number of rows and columns in
            the grid.
        _size (tuple[int, int]): The size of the grid in pixels.
        _cache (dict): A dictionary used to cache images.

    Methods:
        redraw(self, ground: List[str], plants: Dict[Tuple[int, int], Plant],
               player_position: Tuple[int, int], 
                player_direction: str) -> None:
            Redraws the view with the given ground, plants, player position,
                and direction.
    """

    def __init__(
        self,
        master: tk.Tk | tk.Frame,
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs,
    ) -> None:
        """Creates a new FarmView object.

        Args:
            master (tk.Tk | tk.Frame): The parent widget.
            dimensions (tuple[int, int]): The number of rows and columns in
                the grid.
            size (tuple[int, int]): The size of the grid in pixels.
            **kwargs: Additional keyword arguments to be passed to the parent
                class's constructor.
        """
        super().__init__(master, dimensions, size)
        self._master = master
        self._dimensions = dimensions
        self._size = size
        self._cache = {}

    def redraw(
        self,
        ground: list[str],
        plants: dict[tuple[int, int], "Plant"],
        player_position: tuple[int, int],
        player_direction: str,
    ) -> None:
        """Redraws the view with the given ground, plants, player position,
            and direction.

        Args:
            ground (List[str]): A list of strings representing the ground
                tiles.
            plants (Dict[Tuple[int, int], Plant]): A dictionary mapping
                positions to plant objects.
            player_position (Tuple[int, int]): The position of the player on
                the grid.
            player_direction (str): The direction the player is facing.
        """
        self.clear()
        rows, columns = self._dimensions

        # Mapping of cell types to image names
        cell_image_map = {
            GRASS: IMAGES[GRASS],
            SOIL: IMAGES[SOIL],
            UNTILLED: IMAGES[UNTILLED],
        }

        # Display Ground Images
        for row in range(rows):
            for col in range(columns):
                position = row, col
                cell_type = ground[row][col]
                image_name = cell_image_map.get(cell_type)
                if image_name:
                    image = get_image(
                        f"images/{image_name}",
                        self.get_cell_size(),
                        self._cache
                    )
                    self.create_image(self.get_midpoint(position), image=image)

        # Display Plant Images
        for position, plant in plants.items():
            plant_image_name = get_plant_image_name(plant)
            plant_image = get_image(
                f"images/{plant_image_name}",
                self.get_cell_size(),
                self._cache,
            )
            self.create_image(
                self.get_midpoint(position),
                image=plant_image
            )

        # Display Player Image
        player_image = get_image(
            f"images/{IMAGES[player_direction]}",
            self.get_cell_size(),
            self._cache,
        )
        self.create_image(
            self.get_midpoint(player_position), image=player_image
        )


class ItemView(tk.Frame):
    """A frame widget representing a single item in the player's inventory.

    Args:
        master (tk.Frame): The parent widget.
        item_name (str): The name of the item.
        amount (int): The amount of the item.
        select_command (Optional[Callable[[str], None]], optional):
            A function that will be called when the item is selected.
            Defaults to None.
        sell_command (Optional[Callable[[str], None]], optional):
            A function that will be called when the "Sell" button is clicked.
            Defaults to None.
        buy_command (Optional[Callable[[str], None]], optional):
            A function that will be called when the "Buy" button is clicked.
            Defaults to None.
    """

    def __init__(
        self,
        master: tk.Frame,
        item_name: str,
        amount: int,
        select_command: Optional[Callable[[str], None]] = None,
        sell_command: Optional[Callable[[str], None]] = None,
        buy_command: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Initializes a new ItemView object.

        Args:
            master (tk.Frame): The parent widget.
            item_name (str): The name of the item.
            amount (int): The amount of the item.
            select_command (Optional[Callable[[str], None]], optional):
                A function that will be called when the item is selected.
                Defaults to None.
            sell_command (Optional[Callable[[str], None]], optional):
                A function that will be called when the "Sell" button is
                    clicked.
                Defaults to None.
            buy_command (Optional[Callable[[str], None]], optional):
                A function that will be called when the "Buy" button is
                    clicked.
                Defaults to None.
        """
        super().__init__(master)
        self._item_name = item_name

        self.config(bd=2, relief=tk.SUNKEN)  # Set border

        # Item Label
        item_text = (f"{self._item_name}: {amount}\n" +
                     f"Sell price: ${SELL_PRICES[self._item_name]}\n" +
                     "Buy price: $" +
                     f"{BUY_PRICES.get(self._item_name, 'N/A')}")
        self._item_label = tk.Label(self, text=item_text, fg="black")
        self._item_label.pack(side=tk.LEFT)

        # Buttons
        if buy_command:
            self._buy_button = tk.Button(
                self, text="Buy", command=lambda: buy_command(self._item_name)
            )
            self._buy_button.pack(side=tk.LEFT)

        if sell_command:
            self._sell_button = tk.Button(
                self,
                text="Sell",
                command=lambda: sell_command(self._item_name)
            )
            self._sell_button.pack(side=tk.LEFT)

        # Bind click for select
        self.bind("<Button-1>", lambda event: select_command(self._item_name))
        self._item_label.bind(
            "<Button-1>",
            lambda event: select_command(self._item_name)
        )

        # Initial appearance
        self.update(amount=amount, selected=False)

    def get_item_name(self) -> str:
        """Returns the name of the item.

        Returns:
            str: The name of the item.
        """
        return self._item_name

    def update(self, amount: int, selected: bool = False) -> None:
        """Updates the item view with new information.

        Args:
            amount (int): The amount of the item.
            selected (bool, optional): Whether the item is selected. 
                Defaults to False.
        """
        # Set colour of item views
        if amount == 0:
            color = INVENTORY_EMPTY_COLOUR
        elif selected:
            color = INVENTORY_SELECTED_COLOUR
        else:
            color = INVENTORY_COLOUR

        self.config(bg=color)
        self._item_label.config(
            bg=color,
            text=f"{self._item_name}: {amount}\n"
            f"Sell price: ${SELL_PRICES[self._item_name]}\n"
            f"Buy price: ${BUY_PRICES.get(self._item_name, 'N/A')}",
        )
        if hasattr(self, '_buy_button'):
            self._buy_button.config(highlightbackground=color)

        if hasattr(self, '_sell_button'):
            self._sell_button.config(highlightbackground=color)


class FarmGame:
    """Controls the whole game.

    Responsible for maintaining instances of the model, event handling 
    and fascilitating communication between the model and view classes.
    """

    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """Initialize the FarmGame.

        Args:
            master (tk.Tk): The root Tk instance.
            map_file (str): The file path of the map.
        """
        self._master = master
        self._master.title("Farm Game")
        self.reset_game(map_file)

        # Menu
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.quit_game)
        file_menu.add_command(label="Map selection", command=self.open_map)

        # Title Banner initialise and pack
        self._banner_frame = tk.Frame(self._master)
        self._banner = get_image(
            "images/header.png",
            [(FARM_WIDTH + INVENTORY_WIDTH), BANNER_HEIGHT]
        )
        banner_label = tk.Label(
            self._banner_frame,
            image=self._banner,
        )
        banner_label.pack(side=tk.TOP, expand=tk.TRUE)
        self._banner_frame.pack(side=tk.TOP)

        # Initialise Infobar
        self._infobar = InfoBar(self._master)

        def next_day() -> None:
            """ Iterates a new day in the model and redraws the infobar.

            Returns:
                None
            """
            self._model.new_day()
            self.redraw()

        # Next Day Button
        self._nextday_button = tk.Button(
            self._master, text="Next day", command=next_day
        )
        self._nextday_button.pack(side=tk.BOTTOM)

        # Pack infobar
        self._infobar.pack(side=tk.BOTTOM)

        # Initialise and pack Farmview
        self.create_farm()

        # Initialise Itemview
        self._item_views = {}
        self.create_item_views()

        # Redraw Views
        self.redraw()

        # Handle Keypress
        self._master.bind("<KeyPress>", self.handle_keypress)

    def create_farm(self) -> None:
        """Initialise and pack Farmview

        Returns:
            None
        """
        self._farmview = FarmView(
            self._master,
            dimensions=(len(self._map), len(self._map[0])),
            size=(FARM_WIDTH, FARM_WIDTH)
        )
        self._farmview.pack(side=tk.LEFT)

    def create_item_views(self) -> None:
        """Create and initialize the item views.

        This method creates and packs the item views for the game's inventory.

        Returns:
            None
        """
        self._items = tk.Frame(
            self._master, width=INVENTORY_WIDTH, height=FARM_WIDTH
        )
        self._items.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        for item in ITEMS:
            inventory_args = (
                self._items,
                item,
                self._player.get_inventory().get(item, 0),
                self.select_item,
                self.sell_item,
                self.buy_item if item in BUY_PRICES else None
            )
            item_view = ItemView(*inventory_args)
            item_view.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
            self._item_views[item] = item_view
            self.update_item_view(item)

    def update_item_view(self, item: str) -> None:
        """Update the specified ItemView with the current item amount and 
        selected status.

        Args:
            item (str): The name of the item.

        Returns:
            None
        """
        item_view = self._item_views.get(item)
        if item_view:
            amount = self._player.get_inventory().get(item, 0)
            selected = self._player.get_selected_item() == item
            item_view.update(amount=amount, selected=selected)

    def quit_game(self) -> None:
        """Quit the game.

        This method prompts the user for confirmation and closes the game if
        confirmed.

        Returns:
            None
        """
        self._master.destroy()

    def open_map(self) -> None:
        """Open a new map.

        This method allows the user to select a new map file, resets the game
        with the new map, recreates the item views, and redraws the game views.

        Returns:
            None
        """
        new_map = filedialog.askopenfilename()
        if new_map:
            self._items.destroy()
            self._farmview.destroy()
            self.reset_game(new_map)
            self.create_farm()
            self.create_item_views()
            self.redraw()

    def reset_game(self, map_file) -> None:
        """Reset the game.

        This method resets the game by setting up the map, player, 
        player position, player direction, plants, and item views.

        Args:
            map_file (str): The file path of the map.

        Returns:
            None
        """
        self._map_file = map_file
        self._model = FarmModel(self._map_file)
        self._player = self._model.get_player()
        self._map = self._model.get_map()
        self._player_position = (0, 0)  # Starting position of player
        self._player_direction = "UP"  # Starting direction of player
        self._plants = {}   # Will store plant instances
        self._item_views = {}  # Used for storing item views

    def redraw(self) -> None:
        """Redraw the game views.

        This method updates and redraws the farm view, infobar, and item views.

        Returns:
            None
        """
        # Variables
        model = self._model
        player = model.get_player()

        # Redraw Views
        self._farmview.redraw(
            self._map,
            model.get_plants(),
            model.get_player_position(),
            model.get_player_direction(),
        )
        self._infobar.redraw(
            model.get_days_elapsed(), player.get_money(), player.get_energy()
        )

        for item_view in self._item_views.values():
            self.update_item_view(item_view.get_item_name())

    def handle_keypress(self, event: tk.Event) -> None:
        """Handle keypress events.

        This method handles keypress events and performs corresponding actions 
        in the game, such as moving the player, planting seeds, and
        harvesting plants, etc.

        Args:
            event (tk.Event): The keypress event.

        Returns:
            None
        """
        key = event.char.lower()
        model = self._model
        player = self._player
        pos = player.get_position()
        row, col = pos
        selected_item = player.get_selected_item()
        plants = {
            "abstract plant": Plant(),
            "Potato Seed": PotatoPlant(),
            "Kale Seed": KalePlant(),
            "Berry Seed": BerryPlant(),
        }

        if key == UP:   # Move Player
            model.move_player(UP)
        if key == LEFT:
            model.move_player(LEFT)
        if key == DOWN:
            model.move_player(DOWN)
        if key == RIGHT:
            model.move_player(RIGHT)
        if key == "p":  # Plant seeds
            if (
                selected_item in SEEDS
                and selected_item in player.get_inventory()
                and not model.get_plants().get(pos)
                and self._map[row][col] == SOIL
            ):
                model.add_plant(pos, plants.get(selected_item))
                player.remove_item((selected_item, 1))
        if key == "h":  # Harvest plants
            harvested = model.harvest_plant(pos)
            if harvested:
                player.add_item(harvested)
        if key == "r":  # Remove plants without harvesting
            model.remove_plant(pos)
        if key == "t":  # Till soil
            model.till_soil(pos)
        if key == "u":  # Untill soil
            model.untill_soil(pos)

        self.redraw()

    def select_item(self, item_name: str) -> None:
        """Select an item.

        This method sets the selected item in the player's inventory.

        Args:
            item_name (str): The name of the item.

        Returns:
            None
        """
        self._player.select_item(item_name)
        self.redraw()

    def buy_item(self, item_name: str) -> None:
        """Buy an item.

        This method allows the player to buy an item from the shop.

        Args:
            item_name (str): The name of the item.

        Returns:
            None
        """
        self._player.buy(item_name, BUY_PRICES[item_name])
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """Sell an item.

        This method allows the player to sell an item to the shop.

        Args:
            item_name (str): The name of the item.

        Returns:
            None
        """
        self._player.sell(item_name, SELL_PRICES[item_name])
        self.redraw()


def play_game(root: tk.Tk, map_file: str) -> None:
    """Play the farm game.

    Args:
        root (tk.Tk): The root Tk instance.
        map_file (str): The file path of the map.

    Returns:
        None
    """
    FarmGame(root, map_file)
    root.mainloop()


def main() -> None:
    root = tk.Tk()
    play_game(root, "maps/map1.txt")


if __name__ == "__main__":
    main()
