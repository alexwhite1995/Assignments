"""
CSSE1001 Assignment 1
Semester 1, 2023
"""

# Fill these in with your details
__author__ = "Alex White"
__email__ = "s4321830@student.uq.edu.au"
__date__ = "16/03/2023"

from constants import *


# Write your functions here

def num_hours() -> float:
    """
    Returns the estimated number of hours spent on the assignment, as a float.

    >>> num_hours()
    8.2
    """
    return float(8.2)


def get_recipe_name(recipe: tuple[str, str]) -> str:
    """Return recipe name... First string in the tuple 
    
    >>> get_recipe_name('cheesecake', 'cheese and cake')
    'cheesecake'

    """


    return recipe[0]


def parse_ingredient(raw_ingredient_detail: str) -> tuple[float, str, str]:
    """
    Returns the ingredient breakdown from the details amount, measure
    and ingredient.


    >>> parse_ingredient('0.5 tsp coffee granules')
    (0.5, 'tsp', 'coffee granules')
    """
    split_ingredients = raw_ingredient_detail.split(' ')
    amount = float(split_ingredients[0])
    measure = split_ingredients[1]
    ingredient = ' '.join(split_ingredients[2:])
    return  (amount, measure, ingredient)


def create_recipe() -> tuple[str, str]:
    """
    Return a recipe in the tuple[str, str] format after a series of prompting.
    The recipe name is prompted first followed by continuous ingredient
    prompting until an empty string is entered
    (enter or return key press with no text).

    >>> def create_recipe()
    Please enter the recipe name: peanut butter
    Please enter an ingredient: 300 g peanuts
    Please enter an ingredient: 0.5 tsp salt
    Please enter an ingredient: 2 tsp oil
    Please enter an ingredient:
    ('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')
    """
    recipe_name = input('Please enter the recipe name: ')
    ingredient_list = ''
    while True:
        ingredient = input('Please enter an ingredient: ')
        if ingredient == '':
            break

        elif ingredient_list != '':
            ingredient_list += ',' + ingredient
        
        elif ingredient_list == '':
            ingredient_list = ingredient
        
    return (recipe_name, ingredient_list)


def recipe_ingredients(recipe: tuple[str, str]) -> tuple[tuple[float, str, str]]:
    """
    Return the ingredients of a recipe amount, measure, and ingredient.
    This transforms a given recipe from the string form into the tuples form.
    Example:
    >>> recipe_ingredients(('peanut butter',
    '300 g peanuts,0.5 tsp salt,2 tsp oil'))
    ((300.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'))

    """
    
    recipe_list = ()
    ingredients = tuple(recipe[1].split(','))
    for x in ingredients:
        recipe_list += (parse_ingredient(x),)
    
    return recipe_list


def add_recipe(new_recipe: tuple[str, str], recipes: list[tuple[str, str]]) -> None:
    """
    Add a given recipe, new_recipe, into the list of recipes.
    Hint: This function doesn’t return
    anything. Recall list mutability.
    Example:
    4
    >>> recipes = []
    >>> recipe = ('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')
    >>> add_recipe(recipe, recipes)
    >>> recipes
    [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')]
    >>> add_recipe(recipe, recipes)
    >>> recipes
    [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil'), ('peanut butter',
    '300 g peanuts,0.5 tsp salt,2 tsp oil')]
    """
    recipes.append(new_recipe)
    
    
    return

def find_recipe(recipe_name: str,
                recipes: list[tuple[str, str]]) -> tuple[str, str] | None:
    """
    Return a recipe or None. This function should attempt to
    find the recipe by the given recipe name
    within the list of recipes. If the recipe can not be found
    then this function should return None.
    Example:
    >>> recipes = [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')]
    >>> find_recipe('peanut butter', recipes)
    ('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')
    >>> find_recipe('cinnamon rolls', recipes)
    >>> print(find_recipe('cinnamon rolls', recipes))
    None
    """
    for x in recipes:
        if recipe_name == x[0]:
            return x

def remove_recipe(name: str, recipes: list[tuple[str, str]]) -> None:
    """
    Remove a recipe from the list of recipes given the name of a recipe.
    If the recipe name does not match any of the recipes within the list
    of recipes then nothing happens.
    Example:
    >>> recipes = [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil'),
    ('cinnamon rolls', '480 ml almond milk,115 g Nuttelex,50 g sugar,7 g
    active dry yeast,5.5 cup flour,1 tsp salt,170 g Nuttelex,165 g brown
    sugar,2 tbsp cinnamon,160 g powdered sugar,30 ml almond milk,0.5 tsp
    vanilla extract')]
    >>> remove_recipe('brownie', recipes)
    >>> recipes
    [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil'), ('cinnamon
    rolls', '480 ml almond milk,115 g Nuttelex,50 g sugar,7 g active dry
    yeast,5.5 cup flour,1 tsp salt,170 g Nuttelex,165 g brown sugar,2 tbsp
    cinnamon,160 g powdered sugar,30 ml almond milk,0.5 tsp vanilla
    extract')]
    >>> remove_recipe('cinnamon rolls', recipes)
    >>> recipes
    [('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')]
    """
    for x in recipes:
        if name == x[0]:
          recipes.remove(x)
          break
    return


def get_ingredient_amount(ingredient: str,
                          recipe: tuple[str, str]) -> tuple[float, str] | None:
    """
    Return the amount and measure of a certain ingredient as a tuple[float, str]
    given the ingredient name as a str and a recipe. If the ingredient doesn’t
    exist then nothing happens.
    Example:
    >>> recipe = ('peanut butter', '300 g peanuts,0.5 tsp salt,2 tsp oil')
    >>> get_ingredient_amount('peanuts', recipe)
    (300.0, 'g')
    >>> get_ingredient_amount('soy beans', recipe)
    """
    
    for x in recipe_ingredients(recipe):
        if x[2] == ingredient:
            return x[:2]

    
def add_to_shopping_list(ingredient_details: tuple[float, str, str],
                         shopping_list: list[tuple[float, str, str]| None]) -> None:
    """
    Add an ingredient to the shopping list which could be empty
    or could contain tuples of ingredient
    details. If the ingredient being added already exist within
    the shopping list then the amount should be combined.
    If the ingredient does not exist then it can be added without any calculations.
    Note: It can be assumed that the measure is consistent
    for all ingredients of the same name.
    In addition, ingredient_details contains all the information
    about the ingredient being added to
    the shopping list. Also, the order does not matter.
    Example:
    >>> shopping_list = [(300.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'),
    (2.0, 'tsp', 'oil')]
    >>> add_to_shopping_list((1000.0, 'g', 'tofu'), shopping_list)
    >>> shopping_list
    [(300.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (1000.0, 'g', 'tofu')]
    >>> add_to_shopping_list((1200.0, 'g', 'peanuts'), shopping_list)
    >>> shopping_list
    [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (1000.0, 'g', 'tofu')]
    >>> add_to_shopping_list((8000.0, 'g', 'tofu'), shopping_list)
    >>> shopping_list
    [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (9000.0, 'g', 'tofu')]
    
    """
    if shopping_list == []:
        shopping_list.insert(0,ingredient_details)
    else:
        for x in shopping_list:
            if x[2] == ingredient_details[2]:
                y = list(x)
                y[0] += ingredient_details[0]
                shopping_list.remove(x)
                x = tuple(y)
                shopping_list.insert(0,x)
                break
            elif x == shopping_list[-1]:
                shopping_list.append(ingredient_details)
                break
            else:
                pass
    return



def remove_from_shopping_list(ingredient_name: str, amount: float, shopping_list: list) -> None:
    """
    Remove a certain amount of an ingredient, with the given ingredient_name, from the shopping_list.
    If the ingredient exists in the shopping_list then the amount given as the parameter of this func6
    tion should be subtracted from the amount that exists in the shopping_list. The ingredient
    should be removed from the shopping list altogether if the amount goes below 0.
    Example:
    >>> shopping_list = [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'),
    (2.0, 'tsp', 'oil'), (9000.0, 'g', 'tofu'), (100.0, 'g', 'sugar'),
    (50.0, 'g', 'tomato sauce'), (120.0, 'g', 'rice'),
    (920.0, 'g', 'ice cream')]
    >>> remove_from_shopping_list('ice cream', 500.0, shopping_list)
    >>> shopping_list
    [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (9000.0, 'g', 'tofu'), (100.0, 'g', 'sugar'), (50.0, 'g', 'tomato
    sauce'), (120.0, 'g', 'rice'), (420.0, 'g', 'ice cream')]
    >>> remove_from_shopping_list('sugar', 500.0, shopping_list)
    >>> shopping_list
    [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (9000.0, 'g', 'tofu'), (50.0, 'g', 'tomato sauce'), (120.0, 'g',
    'rice'), (420.0, 'g', 'ice cream')]
    >>> remove_from_shopping_list('ice cream', 9000.0, shopping_list)
    >>> shopping_list
    [(1500.0, 'g', 'peanuts'), (0.5, 'tsp', 'salt'), (2.0, 'tsp', 'oil'),
    (9000.0, 'g', 'tofu'), (50.0, 'g', 'tomato sauce'), (120.0, 'g',
    'rice')]
    """
    ingredient = [ingredient_name, amount]
    for x in shopping_list:
        if x[2] == ingredient[0]:
            y = list(x)
            y[0] -= ingredient[1]
            shopping_list.remove(x)
            x = tuple(y)
            shopping_list.insert(0,x)
            if x[0] < 0.0:
                shopping_list.remove(x)
                break
            else:
                break
        else:
            pass
    return


def generate_shopping_list(recipes: list[tuple[str, str]]) -> list[tuple[float, str, str]]:
    """
    Return a list of ingredients, (amount, measure, ingredient_name), given a list of recipes.
    Example:
    >>> shopping_list = generate_shopping_list([PEANUT_BUTTER,
    MUNG_BEAN_OMELETTE])
    >>> shopping_list
    [(300.0, 'g', 'peanuts'), (1.0, 'tsp', 'salt'), (3.0, 'tsp', 'oil'),
    (1.0, 'cup', 'mung bean'), (0.75, 'tsp', 'pink salt'), (0.25, 'tsp',
    'garlic powder'), (0.25, 'tsp', 'onion powder'), (0.125, 'tsp',
    'pepper'), (0.25, 'tsp', 'turmeric'), (1.0, 'cup', 'soy milk')]
    >>> shopping_list = generate_shopping_list([PEANUT_BUTTER, PEANUT_BUTTER,
    MUNG_BEAN_OMELETTE])
    >>> shopping_list
    [(600.0, 'g', 'peanuts'), (1.5, 'tsp', 'salt'), (5.0, 'tsp', 'oil'),
    7
    (1.0, 'cup', 'mung bean'), (0.75, 'tsp', 'pink salt'), (0.25, 'tsp',
    'garlic powder'), (0.25, 'tsp', 'onion powder'), (0.125, 'tsp',
    'pepper'), (0.25, 'tsp', 'turmeric'), (1.0, 'cup', 'soy milk')]
    """
    list_of_ingredients = []

    for x in recipes:
        ingredients = list(recipe_ingredients(x))
        for y in ingredients:
            add_to_shopping_list(y, list_of_ingredients)
    return list_of_ingredients


def display_ingredients(shopping_list: list[tuple[float, str, str]]) -> None:
    """
    
    Print the given shopping list in any order you wish. CSSE7030 students must display the shopping
    list alphabetically based on the name of the ingredients. See example in Appendix.
    Note: The amount of spaces changes depending on how long the longest text is. The order
    does not matter.
    Example:
    >>> display_ingredients([(1.0, 'large', 'banana'), (0.5, 'cup', 'ice'),])
    | 1.0 | large | banana |
    | 0.5 | cup | ice |
    >>> display_ingredients([(1.0, 'large', 'banana'),
    (2.0, 'tbsp', 'peanut butter'),
    (2.0, 'pitted', 'dates'),
    (1.0, 'tbsp', 'cacao powder'),
    (240.0, 'ml', 'almond milk'),
    (0.5, 'cup', 'ice'),
    (1.0, 'tbsp', 'cocao nibs'),
    (1.0, 'tbsp', 'flax seed')])
    | 1.0 | large | banana |
    | 2.0 | tbsp | peanut butter |
    | 2.0 | pitted | dates |
    | 1.0 | tbsp | cacao powder |
    | 240.0 | ml | almond milk |
    | 0.5 | cup | ice |
    | 1.0 | tbsp | cocao nibs |
    | 1.0 | tbsp | flax seed |

    """
    longest_amount = 0
    longest_measure = 0
    longest_ingred = 0

    shopping_list.sort(key = lambda x: x[2])
        
    for x in shopping_list: #find width of display
        for no, y in enumerate(x):
            if no == 0:
                if len(str(y)) > longest_amount:
                    longest_amount = len(str(y))
                else:
                    pass
            elif no == 1:
                if len(y) > longest_measure:
                    longest_measure = len(y)
                else:
                    pass
            elif no == 2:
                if len(y) > longest_ingred:
                    longest_ingred = len(y)
                else:
                    pass    
    default_l_buffer = ' '
    default_r_buffer = '  '
    for x in shopping_list: #print display
        for no, y in enumerate(x):
            if no == 0:
                amount = '| ' + str(y).rjust((longest_amount), ' ') + ' |'
            elif no == 1:
                if longest_measure == len(y):
                    measure = default_l_buffer + y + default_r_buffer
                elif (longest_measure - len(y)) % 2 == 0:
                    left_buffer = right_buffer = ((longest_measure - len(y))//2)
                    measure = default_l_buffer + (left_buffer * ' ') + y + (right_buffer * ' ') + default_r_buffer
                else:
                    left_buffer = (((longest_measure - len(y)) // 2) + 1)
                    right_buffer = longest_measure - len(y) - left_buffer
                    measure = default_l_buffer + (left_buffer * ' ') + y + (right_buffer * ' ') + default_r_buffer
            elif no == 2:
                ingred = '| ' + y.ljust((longest_ingred), ' ') + '  |'
        line = [amount, measure, ingred]
        line = ''.join(line)
        print(line)
    return 

def sanitise_command(command: str) -> str:
    """
    
    >>> sanitise_command()
    """
    new_str = ''
    command = command.strip()
    for x in command:
        if 47 < ord(x) < 58:
            pass
        elif 64 < ord(x) < 91:
            new_str += chr(ord(x) + 32)
        elif 96 < ord(x) < 123:
            new_str += x
        else:
            new_str += x
    new_str = new_str.strip()
    return new_str



def main():
    """
    H or h: Help
    mkrec: creates a recipe, add to cook book.
    add {recipe}: adds a recipe to the collection.
    rm {recipe}: removes a recipe from the collection.
    rm -i {ingredient_name} {amount}: removes ingredient from shopping list.
    ls: list all recipes in shopping cart.
    ls -a: list all available recipes in cook book.
    ls -s: display shopping list.
    g or G: generates a shopping list.
    Q or q: Quit.

    """
    # cook book
    recipe_collection = [
        CHOCOLATE_PEANUT_BUTTER_SHAKE, 
        BROWNIE, 
        SEITAN, 
        CINNAMON_ROLLS, 
        PEANUT_BUTTER, 
        MUNG_BEAN_OMELETTE
    ]
    
    # Write the rest of your code here
    #initiating varibles
    command = ''
    list_of_recipes = []
    shopping_list = []
    while command != 'q':
        entry = input('Please enter a command: ')
        command = sanitise_command(entry.split(' ')[0])
        #start commands
        if command == 'h':
            print('    H or h: Help\n'
            '    mkrec: creates a recipe, add to cook book.\n'
            '    add {recipe}: adds a recipe to the collection.\n'
            '    rm {recipe}: removes a recipe from the collection.\n'
            '    rm -i {ingredient_name} {amount}: removes ingredient from shopping list.\n'
            '    ls: list all recipes in shopping cart.\n'
            '    ls -a: list all available recipes in cook book.\n'
            '    ls -s: display shopping list.\n'
            '    g or G: generates a shopping list.\n'
            '    Q or q: Quit.')
        elif command == 'mkrec':
            recipe_collection.append(create_recipe())
            
        elif command == 'add':
            recipe_name = sanitise_command(' '.join(entry.split(' ')[1:]))
            recipe = find_recipe(recipe_name, recipe_collection)
            if recipe == None:
                print('\nRecipe does not exist in the cook book. \n'
                      'Use the mkrec command to create a new recipe.\n')
            else:
                add_recipe(recipe, list_of_recipes)
            
        elif command == 'rm':
            removals = entry.split(' ')[1:]
            if removals[0] != '-i':
                #remove recipe
                recipe_name = ' '.join(removals)
                remove_recipe(recipe_name, list_of_recipes)
            else:
                #remove ingredients
                remove_from_shopping_list(' '.join(removals[1:-1]), float(removals[-1]), shopping_list)
        elif entry == 'ls':
            if list_of_recipes == []:
                print('No recipe in meal plan yet.')
            else:
                print(list_of_recipes)

        elif entry == 'ls -a':
            for x in recipe_collection:
                print(x[0])

        elif entry == 'ls -s':
            display_ingredients(shopping_list)

        elif command == 'g':
            shopping_list = generate_shopping_list(list_of_recipes)
            display_ingredients(shopping_list)

    
if __name__ == "__main__":
    main()
