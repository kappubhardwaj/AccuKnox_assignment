'''
Description: You are tasked with creating a Rectangle class with the following requirements:

An instance of the Rectangle class requires length:int and width:int to be initialized.
We can iterate over an instance of the Rectangle class 
When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}

'''


class Rectangle:
    def __init__(self,length: int, width: int ):
        self.length=length
        self.width= width

    def __iter__(self):
        yield{"length": self.length}
        yield{"width": self.width}


rectangle =  Rectangle(10,5)     

for attributes in rectangle:
    print(attributes)
