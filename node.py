from typing import Tuple, List, Dict


class Node:
    def __init__(self, attr_dict: dict):
        """
        :param attr_dict: Dictionary containing Node attributes as values
        """

        self._label = str(attr_dict.get('label'))
        self._successive = {}  # dictionary of lines
        self.lenght

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def lenght(self):
        return self._label

    @label.setter
    def lenght(self, lenght):
        self.lenght = lenght

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive: dict):
        self._successive = dict(successive)

    def propagate(self, lightpath, occupation=False):
        path = lightpath.path

    if len(path) > 1:
        line_label = path[:2]
    line = self.successive[line_label]
    lightpath.next()
    lightpath = line.propagate(lightpath, occupation)
    return lightpath