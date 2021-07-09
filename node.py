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

    def propagate(self, sig_inf, channel: int, connection=False):
        """
        Propagates the signal to the next line and updates the signal path, if the current node is not the last one in the path

        :param sig_inf: SignalInformation or LightPath object
        :param channel: Number of the channel
        :param connection: True if trying to create a Connection over the lines in the path, False by default, optional
        """

        sig_inf.update_path(self)

        if sig_inf.path:
            next_node = sig_inf.path[0]
            for line in self._successive:
                if line.find(next_node) != -1:
                    sig_inf.signal_power = self._successive.get(line).optimized_launch_power()
                    self._successive.get(line).propagate(sig_inf, channel, connection)