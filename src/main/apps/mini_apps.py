import random, string

# Генератор USERNAME
class GenUsername:
    @staticmethod
    def generate_username(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))