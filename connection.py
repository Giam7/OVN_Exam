class Connection ( object ):
    def __init__ (self , input_node , output_node , signal_power ):
        self._input_node = input_node
        self_ouput_node = ouput_node
        self._signal_power = signal_power
        self . _latency = 0
        self . _snr = 0
        self._bit_rate = 0.0
    @property
    def input_node ( self ):
        return self . _input_node
    @property
    def ouput_node ( self ):
        return self . _ouput_node
    @property
    def signal_power ( self ):
        return self . _signal_power
    @property
    def latency ( self ):
        return self . _latency

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self, snr):
        self._snr = snr
        return self.snr
    @property
    def bitrate(self):
        return self.bitrate
