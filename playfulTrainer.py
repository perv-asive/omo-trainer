import trainer
import omo_utils
import random


class PlayfulTrainer(trainer.Trainer):
    def __init__(self, onlyNamed=False):
        super().__init__()
        self.onlyNamed = onlyNamed

        # Playful randomly chooses between many different messages.
        # If the user registered a name, it will choose between
        # messages with a name and without
        self.affirmativePermissionMessages = [
            #With names
            "Yes my cute little {name}, you can go potty!",
            "Go pee, {name}! c:",
            "Aww, you look like you're about to burst {name}! Go pee <3",
            #Without names
            "Yes sweetie, you can go potty.",
            "Go on to the bathroom honey, you earned it~!",
            "Yes, you can pee cutie~"
        ]

        self.negativePermissionMessages = [
            #With names
            "Oh no, you can't go potty yet {name}. It's too soon!",
            "Tell you what {name}, you can go potty if you hold it a bit longer.",
            "Aww, little {name} has to go potty? Too bad!",
            #Without names
            "No no, you can't go potty now!",
            "Aww sweetie, hold it for just a bit longer, okay?",
            "You have to pee? No no, not yet~"
        ]

        self.goPeeMessages = [
            "I'm so glad you went pee for me, {name}!",
            "You went pee! Good job!"
        ]

        self.accidentMessages = [
            "Little {name} had an accident, oh no~! Hold it in better next time, okay?",
            "Aww, you had an accident? That's okay! Hold it this time, sweetie."
        ]

        self.defaultNames = ["sweetie", "honey", "cutie"]

        if(self.onlyNamed):
            def messageContainsName(el):
                return "name" in omo_utils.keys_from_template_string(el)
            self.affirmativePermissionMessages = omo_utils.filter_to_list(messageContainsName, self.affirmativePermissionMessages)
            self.negativePermissionMessages = omo_utils.filter_to_list(messageContainsName, self.negativePermissionMessages)
            self.goPeeMessages = omo_utils.filter_to_list(messageContainsName, self.goPeeMessages)
            self.accidentMessages = omo_utils.filter_to_list(messageContainsName, self.accidentMessages)

    def get_permission_message(self, drinker, canGo):
        if(canGo):
            return self.choose_random_message_with_variables(self.affirmativePermissionMessages)
        else:
            return self.choose_random_message_with_variables(self.negativePermissionMessages)

    def get_go_pee_message(self, drinker):
        return self.choose_random_message_with_variables(self.goPeeMessages)

    def get_accident_message(self, drinker):
        return self.choose_random_message_with_variables(self.accidentMessages)

    # Parent property override shenanigans
    @property
    def name(self):
        super().name

    @name.setter
    def name(self, n):
        # This sets the property using the parent setter
        # TODO: methodize this maybe?
        trainer.Trainer.name.fset(self, n)
        if(self.onlyNamed and super().name == None):
            n = random.choice(self.defaultNames)
            trainer.Trainer.name.fset(self, n)
