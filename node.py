from typing import Tuple, List, Dict


class Node:
    def __init__(self, attr_dict: dict):
        """
        :param attr_dict: Dictionary containing Node attributes as values
        """

        self._label = str(attr_dict.get('label'))
        self._successive = {}  # dictionary of lines
        self._switching_matrix = None
        self.lenght
        self._transceiver = attr_dict.get('transceiver', 'fixed-rate')

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def lenght(self):
        return self._label

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

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
    def update_switching_matrix(self, channel: int, src: str, dst: str, state: int):
        """
        Updates the switching matrix

        :param channel: Number of the channel
        :param src: Source node label
        :param dst: Destination node label
        :param state: 0 is occupied, 1 is free
        """
