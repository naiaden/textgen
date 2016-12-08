from django.db import models
import random

# Create your models here.
class SomeClass:
    def __init__(self):
        self.x = random.randrange(10)

    def getX(self):
        return self.x


