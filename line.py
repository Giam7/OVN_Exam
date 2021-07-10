import scipy
from numpy.doc.constants import constants
from numpy.lib import math


class Line ( object ):
    def __init__(self, line_dict):
        self._label = line_dict['label ']
        self._length = line_dict['length ']
        self._state = ['free '] * 10
        self._successive = {}
        self._n_amplifiers = 0
        self._gain = 16  # dB
        self._noise_figure = 3  # dB
        self._alpha_dB = 0.2e-3  # dB/m
        self._beta2 = 2.13e-26  # (m*Hz^2)^(-1)
        # self._beta2 = 0.6e-26  # (m*Hz^2)^(-1)
        self._gamma = 1.27e-3  # (W*m)^(-1)
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
    def alpha_dB(self):
        return self._alpha_dB

    @alpha_dB.setter
    def alpha_dB(self, alpha_dB: float):
        self._alpha_dB = alpha_dB

    @property
    def beta2(self):
        return self.beta2

    @beta2.setter
    def beta2(self, beta2: float):
        self._beta2 = beta2

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, gamma: float):
        self._gamma = gamma

    def is_free(self, channel: int):
        """
        Tells if the selected channel is free or not

        :param channel: Number of the channel
        :return: True or False
        :rtype: bool
        """

        if self._state[channel] == 'free':
            return True
        else:
            return False

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
    def ase_generation(self):
        """
        Evaluates the amount of ASE generated by the amplifiers
        :return: ASE in linear units
        :rtype: float
        """
        N = self._n_amplifiers
        h = constants.h  # Planck constant
        f = 193.414e12  # C-band center
        Bn = 12.5e9  # noise bandwidth
        NF = 10 ** (self._noise_figure / 10)
        G = 10 ** (self._gain / 10)

        x = N * (h * f * Bn * NF * (G - 1))

        return x
    def nli_generation(self, power: float):
        """
        Evaluates the total amount of nonlinear interference noise

        :param power: Signal power
        :return: NLI in linear units
        :rtype: float
        """

        alpha = self._alpha_dB / (20 * math.log10(math.e))
        Rs = 32e9
        df = 50e9
        Nch = 10
        N = self._n_amplifiers  # N span
        eta_nli = 16 / (27 * math.pi) * math.log(
            (math.pi ** 2) / 2 * abs(self._beta2) * (Rs ** 2) / alpha * Nch ** (2 * Rs / df)) * (self._gamma ** 2) / (
                              4 * alpha * self._beta2) * 1 / (Rs ** 3)
        Bn = 12.5e9

        return power ** 3 * eta_nli * N * Bn

