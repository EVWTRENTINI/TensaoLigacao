from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure




class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.canvas.figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        self.canvas.axes = self.canvas.figure.add_subplot(projection="3d")
        self.canvas.axes.set_box_aspect([1, 1, 1])


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)


        self.setLayout(vertical_layout)