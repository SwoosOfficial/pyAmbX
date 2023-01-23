#!./pyambx/bin/python
import sys
import time

import matplotlib.colors as mcolor

from pyAMBX import set_color

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
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

class Color(QWidget):

    def __init__(self, qColor):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        self.setColor(qColor)

    def setColor(self, qColor):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, qColor)
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.colors = ['Red', 'Green', 'Blue']
        self.hsv_specs = ['Hue', 'Saturation', 'Value']
        self.color_modes = ['RGB','HSV']
        self.setWindowTitle("pyAmbX")
        outer_layout = QVBoxLayout()
        self.color_sc_chooser = QComboBox()
        self.color_sc_chooser.addItems(self.color_modes)
        self.color_sc_chooser.currentIndexChanged.connect(self.color_mode_changed)
        outer_layout.addWidget(self.color_sc_chooser)
        self.slider_busy = False
        self.color_mode = self.color_modes[0]
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
        self.color_indicator = Color(QColor.fromRgb(0,0,0,1))
        outer_layout.addWidget(self.color_indicator)
        self.setFixedSize(QSize(300, 300))

        # Set the central widget of the Window.
        c_widget = QWidget()
        c_widget.setLayout(outer_layout)
        self.setCentralWidget(c_widget)
    
    def closeEvent(self, event):
        set_color((0,0,0,0))
        event.accept() # let the window close

    def color_mode_changed(self):
        current_index = self.color_sc_chooser.currentIndex()
        prev_colors = self.get_color_sliders()
        self.color_mode = self.color_modes[current_index]
        if self.color_mode == self.color_modes[0]:
            new_colors = prev_colors
            for label in self.colors:
                self.sliders[label]['qlabel'].setText(label)
        elif self.color_mode == self.color_modes[1]:
            new_colors = mcolor.rgb_to_hsv(prev_colors)
            for label, hsv in zip(self.colors, self.hsv_specs):
                self.sliders[label]['qlabel'].setText(hsv)
        else:
            raise RuntimeError(f"Undefined Color Mode {self.color_mode}")
        self.set_color_sliders(new_colors)
        self.value_changed()
        return self.color_mode

    def value_changed(self):
        if self.slider_busy:
            return
        color_list = self.get_color_sliders()
        color_list.append(1)
        color_tup = tuple(color_list)
        return self.set_color_GUI(color_tup)
        
    def slider_pressed(self):
        self.slider_busy = True
        return True

    def slider_released(self):
        self.slider_busy = False
        self.value_changed()
        
    def get_color_sliders(self):
        color_list =[]
        for label in self.colors:
            color = self.sliders[label]['slider'].value()
            color_list.append(color/255)
        if self.color_mode == self.color_modes[1]:
            color_list = list(mcolor.hsv_to_rgb(color_list))
        return color_list
    
    def set_color_sliders(self, rgb_tuple):
        self.slider_busy = True
        for label, channel in zip(self.colors, rgb_tuple):
            self.sliders[label]['slider'].setValue(int(255*channel))
        self.slider_busy = False
        return rgb_tuple
    
    def set_color_GUI(self, rgba_tup):
        c_ind = self.color_indicator
        adj_col_tup = [int(255*channel) for channel in rgba_tup]
        c_ind.setColor(QColor.fromRgb(*adj_col_tup))
        return set_color(rgba_tup)

window = MainWindow()
window.show()

# Start the event loop.
app.exec()
