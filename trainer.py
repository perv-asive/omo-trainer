import random
import omo_utils


#
# Generic trainer implemented by perv-asive
#
class Trainer(object):
    def __init__(self):
        self.variables = {}

    def has_variable(self, varName):
        return varName in self.variables

    def set_string_variable(self, varName, varValue):
        if(varValue == ""):
            if(varName in self.variables):
                del self.variables[varName]
        else:
            self.variables[varName] = varValue

    @property
    def name(self):
        if(self.has_variable("name")):
            return self.variables["name"]
        else:
            return None

    @name.setter
    def name(self, name):
        self.set_string_variable("name", name)

    def get_permission_message(self, drinker, canGo):
        msg = ""
        if(canGo):
            msg = self.get_affirmative_message()
        else:
            msg = self.get_negative_message()
        return msg

    def get_affirmative_message(self):
        retStr = ""
        if("name" in self.variables):
            retStr = self.replace_variables("You may go pee, {name}.")
        else:
            retStr = "You may go pee."
        return retStr

    def get_negative_message(self):
        retStr = ""
        if("name" in self.variables):
            retStr = self.replace_variables("You may not go pee, {name}.")
        else:
            retStr = "You may not go pee."
        return retStr

    def get_go_pee_message(self, drinker):
        return "You went pee."

    def get_accident_message(self, drinker):
        return "You had an accident."

    # Adds all supported variables to a message.
    def replace_variables(self, message):
        return message.format(**self.variables)

    # Chooses randomly between a list of options
    # If a message contains a variable we do not have a value for, filter it out
    def choose_random_message_with_variables(self, choices):
        def filterFunc(el):
            print("el: " + el)
            print("vars: " + str(self.variables))
            return omo_utils.have_keys_for_template_string(self.variables, el)
        # Filter down to strings we can use
        finalChoices = omo_utils.filter_to_list(filterFunc, choices)
        print("final: " + str(finalChoices))
        return self.replace_variables(random.choice(finalChoices))
