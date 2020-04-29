from data import value

class text():
    def __init__(self,text):
        if not(type(text)==str):
            raise Exception('the given text has to be of type string : given type = '+str(type(text)))
        self.text=str(text)

    def display(self):
        for i in range(value):
            print(self.text)
