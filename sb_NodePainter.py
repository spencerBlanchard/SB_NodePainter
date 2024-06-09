import math

from PySide2.QtWidgets import QApplication, QWidget, QCheckBox, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel
import sys
import nuke

class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        self.label = QLabel("Welcome to Spencer's Nuke node drawing tool.\nClick and drag IN THIS WINDOW to make nodes appear in the node graph! \n\n\n"
                            "Press the following keys to change colors:\n"
                            "R = Red\nO = Orange\nY = Yellow\nG = Green\nB = Blue\nP = Purple\nC = Cyan\nM = Magenta\nX = Brown\nK = Black\nZ = Grey\nW = White\n\n\n"
                            "Press the following keys to change brush types:\n"
                            "1 = Single Dot\n2 = Big Dot\n3 = Spread out Diagonal\n4 = Rainbow\n5 = Small spinning Rainbow")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(600, 400)

        self.color = 'r'
        self.old_color = 'r'
        self.brush = '1'
        self.old_brush = '1'
        self.rainbow_index = 0
        self.frame = 0

    def mouseMoveEvent(self, event):
        node_color = {
            'r': 0xFF0000FF,
            'o': 0xFFA500FF,
            'y': 0xFFFF00FF,
            'g': 0x00FF00FF,
            'b': 0x0000FFFF,
            'p': 0x800080FF,
            'c': 0x00FFFFFF,
            'm': 0xFF00FFFF, #Magenta
            'x': 0xA52A2AFF, #Brown
            'k': 0x000000FF, #Black
            'z': 0x808080FF, #Grey
            'w': 0xFFFFFFFF, #White
        }

        brush_types = {
            '1': 'Dot',
            '2': 'Scene',
            '3': 'Dot', #X Shape
            '4': 'Scene', #Rainbow!!!!!!!
            '5': 'Dot'  # Orbitting
        }

        rainbow_colors = [0xFF0000FF, 0xFF9900FF,0xCBFF00FF, 0x33FF00FF, 0x00FF66FF, 0x00FFFFFF, 0x0066FFFF, 0x3200FFFF,
                          0xCC00FFFF]



        if self.color not in node_color:
            self.color = self.old_color
        if self.brush not in brush_types:
                self.brush = self.old_brush

        #create the node
        def create_node(x_offset, y_offset, rainbow = False, spinning = False):
            node_color_value  = node_color[self.color]
            node_brush_type = brush_types[self.brush]
            b = nuke.createNode(node_brush_type, inpanel = False)
            b.setXYpos(event.pos().x() + x_offset, event.pos().y() + y_offset)
            b['note_font_color'].setValue(node_color_value) #color of the text on the node in the node graph
            b['hide_input'].setValue(True)


            if rainbow:
                b['tile_color'].setValue(rainbow_colors[self.rainbow_index % 9])  # RAINBOW COLOR
                self.rainbow_index += 1

            else:
                b['tile_color'].setValue(node_color_value ) #Color of the node




        #1 and 2 are caught at the end.
        #X Shape
        if(self.brush == '3'):
            create_node(0, 40, )
            create_node(0, -40, )
            create_node(40, 0, )
            create_node(-40, 0, )
        #rainbow
        elif(self.brush == '4'):
            create_node(0, 0, True)
        #Orbiting
        elif(self.brush == '5'):
            #Spinning 1
            xpos1 = int(math.sin(self.frame / 10) * 50)
            ypos1 = int(math.sin((self.frame + 10) / 10) * 50)
            #print(f"x is {xpos1} and y is {ypos1}")
            create_node(xpos1, ypos1, True)
            self.frame += 1



        #for normal and big brushes
        else:
            create_node(0, 0 )

    def keyPressEvent(self, event):
        if(event.text().lower()).isalpha():
            self.old_color = self.color
            self.color = event.text().lower()
        else:
            self.old_brush = self.brush
            self.brush = event.text()

    def mousePressEvent(self, event):
        pass #TODO


panel = Panel()
panel.show()


#TODO Make buttons for the colors instead?
#TODO make a clear Canvas Button