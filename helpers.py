import random
import string


class Generate:

    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))

        return random_string

    @staticmethod
    def generate_mail(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))

        return random_string + '@mail.com'
