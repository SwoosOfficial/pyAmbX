#!./pyambx/bin/python
import sys
import time

from pyAMBX import set_color

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
                             QApplication,
                             QMainWindow,
                             QWidget,
                             QLabel,
                             QSlider,
                             QComboBox,
                             QVBoxLayout,
                             QGridLayout,
)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.colors = ['Red', 'Green', 'Blue']
        self.setWindowTitle("pyAmbX")
        outer_layout = QVBoxLayout()
        self.color_sc_chooser = QComboBox()
        self.color_sc_chooser.addItems(['RGB','HSV'])
        outer_layout.addWidget(self.color_sc_chooser)
        self.slider_busy = False
        self.sliders={}
        inner_layout = QGridLayout()
        for i,label in enumerate(self.colors):
            qlabel = QLabel(label)
            inner_layout.addWidget(qlabel, i, 0)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0,255)
            slider.valueChanged.connect(self.value_changed)
            slider.sliderPressed.connect(self.slider_pressed)
            slider.sliderReleased.connect(self.slider_released)
            inner_layout.addWidget(slider, i, 1)
            self.sliders[label] = dict(qlabel = qlabel, slider = slider)
        outer_layout.addLayout(inner_layout)
        self.setFixedSize(QSize(400, 300))
        

        # Set the central widget of the Window.
        c_widget = QWidget()
        c_widget.setLayout(outer_layout)
        self.setCentralWidget(c_widget)

    def value_changed(self):
        if self.slider_busy:
            return
        color_list = []
        for label in self.colors:
            color = self.sliders[label]['slider'].value()
            color_list.append(color/255)
        color_list.append(1)
        color_tup = tuple(color_list)
        return set_color(color_tup)
        
    def slider_pressed(self):
        self.slider_busy = True
        return True

    def slider_released(self):
        self.slider_busy = False
        self.value_changed()
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
