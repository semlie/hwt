from pydantic import BaseModel, Field
from typing import List


class MenuItem(BaseModel):
    '''Represents a menu item in a restaurant, including its name, price, ingredients, category, and correction score.'''
    name: str = Field(..., description="The name of the menu item")
    price: float = Field(..., description="The price of the menu item")
    ingredients: List[str] = Field(
        default_factory=list, description="A list of ingredients for the menu item")
    category: str = Field(default="Uncategorized",
                          description="The category of the menu item (e.g., appetizer, main dish, dessert)")
    correction_score: float = Field(
        default=0.0, description="The correction score indicating how accurate or corrected the item information is between 0 and 1")


class RestaurantMenu(BaseModel):
    '''Represents a restaurant menu with its name and a list of menu items, each item having a name, price, ingredients, category, and correction score.'''
    restaurant_name: str = Field(
        default="", description="The name of the restaurant")
    menu_items: List[MenuItem] = Field(
        default_factory=list, description="A list of menu items offered by the restaurant")


class RestaurantMenuExtractionResult(RestaurantMenu):
    file_name: str
