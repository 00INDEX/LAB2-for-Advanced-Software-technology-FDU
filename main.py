from consolemenu import *
from consolemenu.items import *

from src.Entity.User.Client import Client
from src.Entity.User.Worker import Worker
from src.Entity.User.Manager import Manager
from src.Entity.User.Dispatcher import Dispatcher

def main(choice: int):
    if choice == 0:
        client = Client()
        client.login()
    elif choice == 1:
        worker = Worker()
        worker.login()
    elif choice == 2:
        dispatcher = Dispatcher()
        dispatcher.login()
    elif choice == 3:
        manager = Manager()
        manager.login()

# Create the menu
menu = ConsoleMenu("物业维修管理系统")
menu.append_item(FunctionItem("客户登陆", main, [0]))
menu.append_item(FunctionItem("维修工登陆", main, [1]))
menu.append_item(FunctionItem("调度员登陆", main, [2]))
menu.append_item(FunctionItem("物业经理登陆", main, [3]))

# # Create some items
#
# # MenuItem is the base class for all items, it doesn't do anything when selected
# menu_item = MenuItem("Menu Item")
#
# # A FunctionItem runs a Python function when selected
# function_item = FunctionItem("Call a Python function", input, ["Enter an input"])
#
# # A CommandItem runs a console command
# command_item = CommandItem("Run a console command",  "touch hello.txt")
#
# # A SelectionMenu constructs a menu from a list of strings
# selection_menu = SelectionMenu(["item1", "item2", "item3"])
#
# # A SubmenuItem lets you add a menu (the selection_menu above, for example)
# # as a submenu of another menu
# submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
#
# # Once we're done creating them, we just add the items to the menu
# menu.append_item(menu_item)
# menu.append_item(function_item)
# menu.append_item(command_item)
# menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()