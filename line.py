import scipy
class Line ( object ):
    def __init__(self, line_dict):
        self._label = line_dict['label ']
        self._length = line_dict['length ']
        self._state = ['free '] * 10
        self._successive = {}
        self._n_amplifiers = 0
        self._gain = 16  # dB
        self._noise_figure = 3  # dB
    @property
    def label ( self ):
        return self . _label
    @property
    def length ( self ):
        return self . _length

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @n_amplifiers.setter
    def n_amplifiers(self, n_amplifiers: int):
        self._n_amplifiers = n_amplifiers

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain: float):
        self._gain = gain

    @property
    def noise_figure(self):
        return self._noise_figure

    @noise_figure.setter
    def noise_figure(self, noise_figure: float):
        self._noise_figure = noise_figure

    @property
    def state ( self ):
        return self . _state
    @state.setter
    def state(self, state):
        state = [s.lower().strip() for s in state]

    if set(state).issubset(set(['free ', 'occupied '])):
        self._state = state
    else:
        print('ERROR : line state not recognized . Value :',
              set(state) - set(['free ', 'occupied ']))
    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive


    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = signal_power / (2 * self.length)
        return noise

    def propagate(self, lightpath, occupation=False):
        # Update latency
        latency = self.latency_generation()
        lightpath.add_latency(latency)
        # Update noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)
        # Update line state
        if occupation:
            channel = lightpath.channel
        new_state = self.state.copy()
        new_state[channel] = 'occupied '
        self.state = new_state
        node = self.successive[lightpath.path[0]]
        lightpath = node.propagate(lightpath, occupation)
        return lightpath