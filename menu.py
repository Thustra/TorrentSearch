__author__ = 'Peter'

#import search


class Menu:

    def __init__(self, label, options):
        self.label = label
        self.options = options

    def __repr__(self):

        option_list = '\n'.join([str(self.options.index(option) + 1) + '. ' + option[0] for option in self.options])

        label_string = '{} \n=====================\n'.format(self.label)
        return label_string + option_list

    def evaluate(self, choice):
        if isinstance(self.options[int(choice) - 1][1],Menu):
            print('this is a menu')
            #print(self.options[int(choice) - 1][1])
            #search.set_current_menu(self.options[int(choice) - 1][1])
        else:
            print('This is a function')
            self.options[int(choice) - 1][1]()
