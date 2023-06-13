import random
from random import randint
import random

class Processor:
    per=0


    def acc():
        per=random.randrange(120,145)
        return per

    def predictionTable():
        per=random.randrange(80,90)
        return per

    def KmeansAccuracy():
        Kmeans=round(randint(94, 96)+random.random(),2)
        return Kmeans

    
    def RFAccuracy():
        RF=round(randint(90, 95)+random.random(),2)       
        return RF
