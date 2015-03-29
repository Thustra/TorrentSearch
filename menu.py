__author__ = 'Peter'

import sys


class Menu:

    def __init__(self, label, options):
        self.label = label
        #Options is a list of tuples
        #('option', function or menu, arguments for the function )
        self.options = options
        self.previous = None

    def __repr__(self):

        menu_options = '\n'.join([str(self.options.index(option) + 1) + '. ' + option[0] for option in self.options])

        menu_header = '{} \n=====================\n'.format(self.label)

        if self.previous == None:
            menu_footer ='\nx. Exit'
        else:
            menu_footer ='\nb. Back\nx. Exit'

        return menu_header + menu_options + menu_footer

    def show(self):
        print(self)

    def return_func(self):
        None

    def set_previous(self,previous_menu):
        self.previous = previous_menu

    def evaluate(self, choice):
        if choice == 'b':
            return self.previous
        elif choice == 'x':
            sys.exit()
        elif isinstance(self.options[int(choice) - 1][1],Menu):
            print('this is a menu')
            # Set the previous menu to this menu
            self.options[int(choice) - 1][1].set_previous(self)
            # Return the new menu
            return self.options[int(choice) - 1][1]
            # t_current_menu(self.options[int(choice) - 1][1])
        else:
            print('This is a function')
            #Generate response

            #Check if the funtion has arguments and generate a response
            if len(self.options[int(choice) - 1])>2:
                argument = self.options[int(choice) - 1][2]
                response = self.options[int(choice) - 1][1](argument)
            else:
                response = self.options[int(choice) - 1][1]()
            # Set the previous menu to this menu
            response.set_previous(self)
            # Functions will do something and return a menu
            return response


