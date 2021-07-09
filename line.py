import scipy
class Line ( object ):
    def __init__ (self , line_dict ):
        self . _label = line_dict ['label ']
        self . _length = line_dict ['length ']
        self . _state = 'free '
        self . _successive = {}
    @property
    def label ( self ):
        return self . _label
    @property
    def length ( self ):
        return self . _length
    @property
    def state ( self ):
        return self . _state
    @state.setter
    def state (self , state ):
        state = state . lower (). strip ()
        if state in ['free ','occupied ']:
            self . _state = state
        else :
            print('ERROR : line state not recognized . Value :', state)

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

    def propagate(self, signal_information, occupation=False):
        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)
        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)
        # Update line state
        if occupation:
            self.state = 'occupied '
        node = self.successive[signal_information.path[0]]
        signal_information = node.propagate(signal_information, occupation)
        return signal_information