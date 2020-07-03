#!/usr/bin/env python

"""2D Datamatrix barcode encoder

All needed by the user is done via the DataMatrixEncoder class:

>>> encoder = DataMatrixEncoder("JIAMID")
>>> # encoder.get_img().save( "test.png" )
>>> print encoder.get_ascii()
XX  XX  XX  XX  XX  XX  XX  
XX  XX  XX      XXXX  XXXXXX
XX    XX  XXXXXX    XXXX    
XX  XX      XX  XX  XX    XX
XXXX  XX  XX  XXXX          
XXXX      XX  XXXX  XX  XXXX
XX  XX  XX          XXXXXX  
XX      XXXX    XXXXXX  XXXX
XX  XXXXXX  XX      XX      
XXXXXX    XXXX    XXXX  XXXX
XX    XX      XX      XXXX  
XX      XX      XXXXXXXX  XX
XX    XXXX            XX    
XXXXXXXXXXXXXXXXXXXXXXXXXXXX


Implemented by Helen Taylor for HUDORA GmbH.


2020/7/3
JIAMID 
"""



from .textencoder import TextEncoder
from .placement import DataMatrixPlacer
from PIL import Image,ImageDraw

class DataMatrixEncoder:
    """Top-level class which handles the overall process of
    encoding input data, placing it in the matrix and
    outputting the result"""

    def __init__(self, text):
        """Set up the encoder with the input text.
        This will encode the text,
        and create a matrix with the resulting codewords"""

        enc = TextEncoder()
        codewords = enc.encode(text)
        matrix_size = enc.mtx_size
        self.matrix = [[None] * matrix_size for _ in range(0, matrix_size)]
        placer = DataMatrixPlacer()
        placer.place(codewords, self.matrix)
        self.width = len(self.matrix)
        self.height = len(self.matrix[0])
        # grow the matrix in preparation for the handles
        self.add_border(colour=0)
        # add the edge handles
        self.add_handles()
        self.img = self.get_img()

    def refresh(self, text):
        self.__init__(text)
        return self.img

    def get_img(self):
        """Write the matrix out to an image file"""
        #self.add_border(colour=0,width=2)
        
        width = len(self.matrix)
        height = len(self.matrix[0])
        
        img = Image.new('RGB',(width*5,height*5),'#ffffff').convert('RGBA')
        blank = ImageDraw.Draw(img)

        flagX = 0
        flagY = 0
        for row in self.matrix:
            flagX = 0
            for x in row:
                
                if x == 0:
                    blank.rectangle([flagX,flagY,flagX+5,flagY+5],fill='white')
                elif x == 1:
                    blank.rectangle([flagX,flagY,flagX+5,flagY+5],fill='black',outline='black')
                flagX += 5
            flagY += 5
                
            
        img = img.resize((400,400))
        
        
        return img
        

    def put_cell(self, pos, colour=1):
        posx,posy=pos[0],pos[1]
        """Set the contents of the given cell"""

        self.matrix[posy][posx] = colour

    def add_handles(self):
        """Set up the edge handles"""
        # bottom solid border
        for posx in range(0, self.width):
            self.put_cell((posx, self.height - 1))

        # left solid border
        for posy in range(0, self.height):
            self.put_cell((0, posy))

        # top broken border
        for i in range(0, self.width - 1, 2):
            self.put_cell((i, 0))

        # right broken border
        for i in range(self.height - 1, 0, -2):
            self.put_cell((self.width - 1, i))

    def add_border(self, colour=1, width=1):
        """Wrap the matrix in a border of given width
            and colour"""

        self.width += (width * 2)
        self.height += (width * 2)

        self.matrix = \
            [[colour] * self.width] * width + \
            [[colour] * width + self.matrix[i] + [colour] * width
                for i in range(0, self.height - (width * 2))] + \
            [[colour] * self.width] * width
    def get_ascii(self):
        """Write an ascii version of the matrix out to screen"""

        def symbol(value):
            """return ascii representation of matrix value"""
            if value == 0:
                return '  '
            elif value == 1:
                return 'XX'

        return '\n'.join([''.join([symbol(cell) for cell in row]) for row in self.matrix]) + '\n'

    
