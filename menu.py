__author__ = 'Peter'


class Menu:

    def __init__(self, label, options):
        self.label = label
        self.options = options

    def __repr__(self):

        option_list = '\n'.join([str(self.options.index(option) + 1) + '. ' + option for option in self.options])

        result_string = '{} \n=====================\n'.format(self.label)
        return result_string + option_list