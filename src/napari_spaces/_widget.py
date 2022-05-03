"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
import napari
import numpy as np
from magicgui import magic_factory
from napari.layers import Image, Points
from qtpy.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget


class SpaceWidget(QWidget):
    def __init__(self, viewer: napari.viewer.Viewer):
        super().__init__()
        self.viewer = viewer
        checkerboard = np.zeros((10, 10))
        checkerboard[::2, ::2] = 1
        points = np.random.uniform(0, 5, (5, 2))
        self.spaces = {
            "first": [Image(checkerboard), Points(points)],
            "second": [
                Image(checkerboard * -1),
                Points(points * 2, face_color="blue"),
            ],
        }

        explanation = QLabel("write 'first' or 'second' below")
        self.text_box = QLineEdit("space name")
        self.text_box.textChanged.connect(self._on_text_change)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(explanation)
        self.layout().addWidget(self.text_box)

    @property
    def active_space(self):
        return self.text_box.text()

    @active_space.setter
    def active_space(self, value: str):
        self.text_box.setText(value)

    def _on_text_change(self):
        if self.active_space in self.spaces:
            self.viewer.layers.clear()
            self.viewer.layers.extend(self.spaces[self.active_space])


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
