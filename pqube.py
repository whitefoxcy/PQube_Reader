"""Module containing the PQube object to communicate with a PQube device
via TCP/IP protocol.

Author: Yan Chen

Changelog:
    10/2/2018:
        Add a new class for 3 phase wye configuration.

Example: 
    $ from gridstart.pqube import PQube
    $ p = PQube(hostname="10.60.36.5", power_config="split_single_phase",
                meas_line1=True, meas_line2=False)
    
    $ p.measurements.update_measurements()
    $ p.pqube_log()
"""

from pyModbusTCP import utils
from pyModbusTCP.client import ModbusClient


def convert_to_long(input):
    long_32 = utils.word_list_to_long(input,True)
    return utils.decode_ieee(long_32[0])

    
class LinePQube(ModbusClient):
    """Class for line measurements in pQube device.
    
    A subclass of ModbusClient, denoting one line on a split-single phase
    distribution line. The measurements are collected by the pQube device
    using the PQube class.
    
    Attributes:
        |  v_rms: RMS voltage of the line (V)
        |  v_mag_fundamental: Fundamental RMS voltage (V)
        |  v_angle_fundamental: Fundamental voltage phase angle (degrees)
        |  i_rms: RMS current in the line (A)
        |  i_mag_fundamental: Fundamental RMS current (A)
        |  i_angle_fundamental: Fundamental current phase angle (degrees)
        |  apparent_power: Apparent power consumption of the line (VA)
        |  real_power: Real power consumption of the line (W)
        |  reactive_power: Reactive power consumtion of the line (VAR)
        |  v_thd: Voltage Total Harmonic Distortion (%)
        |  i_tdd:Current Total Demand Distortion (%)
        |  v_register_id: Register address holding RMS voltage measurement
        |  i_register_id: Register address holding RMS current measurement
        
    Methods: 
        |  update_line_measurements: read all the data from the registers
           addresses specified.
    """
    
    # constructors
    def __init__(self, hostname="10.60.36.5" , port=502 ,auto_open=True, debug=False,
                 v_rms_register_id=7008, v_mag_fundamental_register_id=7098,
                 v_angle_fundamental_register_id=7100, i_rms_register_id=7028, 
                 i_mag_fundamental_register_id=7110, 
                 i_angle_fundamental_register_id=7112, 
                 s_register_id = 7210, p_register_id=7204,
                 q_register_id=7216, v_thd_register_id=7192, i_tdd_register_id=7198):
        ModbusClient.__init__(self, host=hostname, port=port, auto_open=auto_open, debug=debug)
        self.v_rms = float('nan')
        self.v_mag_fundamental = float('nan')
        self.v_angle_funamental = float('nan')
        self.i_rms = float('nan')
        self.i_mag_funamental = float('nan')
        self.i_angle_fundamental = float('nan')
        self.apparent_power = float('nan')
        self.real_power = float('nan')
        self.reactive_power = float('nan')
        self.v_thd = float('nan')
        self.i_tdd = float('nan')
        self.v_rms_register_id = v_rms_register_id
        self.v_mag_fundamental_register_id = v_mag_fundamental_register_id
        self.v_angle_fundamental_register_id = v_angle_fundamental_register_id
        self.i_rms_register_id = i_rms_register_id
        self.i_mag_fundamental_register_id = i_mag_fundamental_register_id
        self.i_angle_fundamental_register_id = i_angle_fundamental_register_id
        self.s_register_id = s_register_id
        self.p_register_id = p_register_id
        self.q_register_id = q_register_id
        self.v_thd_register_id = v_thd_register_id
        self.i_tdd_register_id = i_tdd_register_id
        
        if auto_open:
            self.open()
        
    def __str__(self):
        rep = ("V_RMS: " + str(self.v_rms) + " V\n" + \
               "I_RMS: " + str(self.i_rms) + " A\n" + \
               "Apparent Power: " + str(self.apparent_power) + " VA\n" + \
               "Real Power: " + str(self.real_power) + " W\n" + \
               "Reactive Power: " + str(self.reactive_power) + " VAR\n" + \
               "Voltage THD: " + str(self.v_thd) + "%\n" + \
               "Current TDD: " + str(self.i_tdd)) + "%"
        return rep
        
    # methods
    def __meas_v_rms(self):
        """Private method: Returns RMS voltage for the line."""
        return convert_to_long(
                self.read_input_registers(self.v_rms_register_id, 2))
    
    def __meas_v_mag_fundamental(self):
        """Private method: Returns RMS voltage at fundamental frequency."""
        return convert_to_long(
                self.read_input_registers(self.v_mag_fundamental_register_id, 2))
        
    def __meas_v_angle_fundamental(self):
        """Private: Returns Voltage phase angle at fundamental frequency."""
        return convert_to_long(
                self.read_input_registers(self.v_angle_fundamental_register_id, 2))
        
    def __meas_i_rms(self):
        """Private method: Returns RMS Current for the line."""
        return convert_to_long(
                self.read_input_registers(self.i_rms_register_id, 2))
    
    def __meas_i_mag_fundamental(self):
        return convert_to_long(
                self.read_input_registers(self.i_mag_fundamental_register_id, 2))
        
    def __meas_i_angle_fundamental(self):
        return convert_to_long(
                self.read_input_registers(self.i_angle_fundamental_register_id, 2))
        
    def __meas_apparent_power(self):
        """Private mehtod: Returns apparent power measurements for the line."""
        return convert_to_long(
                self.read_input_registers(self.s_register_id, 2))
        
    def __meas_real_power(self):
        """Private method: Returns real power measurements for the line."""
        return convert_to_long(
                self.read_input_registers(self.p_register_id, 2))
        
    def __meas_reactive_power(self):
        """Private: Returns the reactive power measurement for the line."""
        return convert_to_long(
                self.read_input_registers(self.q_register_id, 2))
        
    def __meas_v_thd(self):
        """Private method: Returns voltage THD value for the line"""
        return convert_to_long(
                self.read_input_registers(self.v_thd_register_id, 2))
        
    def __meas_i_tdd(self):
        """Private_method: Returns current TDD value for the line."""
        return convert_to_long(
                self.read_input_registers(self.i_tdd_register_id, 2))
        
    def update_line_measurements(self):
        """Update all the measurements for the line."""
        self.v_rms = self.__meas_v_rms()
        self.v_mag_fundamental = self.__meas_v_mag_fundamental()
        self.v_angle_funamental = self.__meas_v_angle_fundamental()
        self.i_rms = self.__meas_i_rms()
        self.i_mag_funamental = self.__meas_i_mag_fundamental()
        self.i_angle_fundamental = self.__meas_i_angle_fundamental()
        self.apparent_power = self.__meas_apparent_power()
        self.real_power = self.__meas_real_power()
        self.reactive_power = self.__meas_reactive_power()
        self.v_thd = self.__meas_v_thd()
        self.i_tdd = self.__meas_i_tdd()
        
        
class PQubeSplit1p(ModbusClient):
    """Class for data collection with PQube in Split single phase power
    configuration.
    
    Attributes:
        |  hostname: Host IP address. 
        |  port: Comm port.
        |  auto_open: Default True.
        |  debug: Default False.
        |  meas_line1: Set True if voltage and current is being measured 
           through line1, default False.
        |  meas_line2: Set True if voltage and current is being measured 
           through line2, default False.
        |  line1: LinePQube object containing measurements from line1, 
           if meas_line1=True.
        |  line2: LinePQube object containing measurements from line2, 
           if meas_line2=True.
        
        Line attributes are: v_rms, i_rms, apparent_power, real_power, reactive_power, v_thd, i_tdd
    
    Methods:
        |  freq: measured frequency (Hz), Registers 7026-7027.
        |  update_measurements: update the measured attributes from the lines.
    """
    
    # register addresses as constants
    REG_POWER_CONFIG = 8022
    REG_FREQ = 7026
    REG_V_RMS_L1 = 7008
    REG_V_MAG_FUNDAMENTAL_L1 = 7098
    REG_V_ANGLE_FUNDAMENTAL_L1 = 7100
    REG_V_RMS_L2 = 7010
    REG_V_MAG_FUNDAMENTAL_L2 = 7102
    REG_V_ANGLE_FUNDAMENTAL_L2 = 7104
    REG_I_RMS_L1 = 7028
    REG_I_MAG_FUNDAMENTAL_L1 = 7110
    REG_I_ANGLE_FUNDAMENTAL_L1 = 7112
    REG_I_RMS_L2 = 7030
    REG_I_MAG_FUNDAMENTAL_L2 = 7114
    REG_I_ANGLE_FUNDAMENTAL_L2 = 7116
    REG_V_THD_L1 = 7192
    REG_V_THD_L2 = 7194
    REG_I_TDD_L1 = 7198
    REG_I_TDD_L2 = 7200
    REG_WATT_L1 = 7204
    REG_WATT_L2 = 7206
    REG_VA_L1 = 7210
    REG_VA_L2 = 7212
    REG_VAR_FUNDAMENTAL_L1 = 7216
    REG_VAR_FUNDAMENTAL_L2 = 7218
    READ_2_REG = 2    # read two registers
    
    # Constructors
    def __init__(self, hostname="10.60.36.5" , port=502 ,auto_open=True, 
                 debug=False, meas_line1=False, meas_line2=False):
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        
        self.meas_line1 = meas_line1
        self.meas_line2 = meas_line2
        # check power config on the device
        if self.read_input_registers(self.REG_POWER_CONFIG)[0] != 2:
            print("Make sure the power configuration in the 'Setup.ini' file" +
                  " matches the 'power_config' attribute in device initialization.")
            raise AttributeError
        if self.meas_line1:    # initialize line 1 measurements
            self.line1 = LinePQube(
                    hostname=hostname, port=port,
                    auto_open=auto_open, debug=debug,
                    v_rms_register_id=self.REG_V_RMS_L1,
                    v_mag_fundamental_register_id = self.REG_V_MAG_FUNDAMENTAL_L1,
                    v_angle_fundamental_register_id = self.REG_V_ANGLE_FUNDAMENTAL_L1,
                    i_rms_register_id=self.REG_I_RMS_L1,
                    i_mag_fundamental_register_id = self.REG_I_MAG_FUNDAMENTAL_L1,
                    i_angle_fundamental_register_id = self.REG_I_ANGLE_FUNDAMENTAL_L1,
                    s_register_id=self.REG_VA_L1,
                    p_register_id=self.REG_WATT_L1,
                    q_register_id=self.REG_VAR_FUNDAMENTAL_L1,
                    v_thd_register_id=self.REG_V_THD_L1,
                    i_tdd_register_id=self.REG_I_TDD_L1)
            
        if self.meas_line2:    # initialize line 2 measurements
            self.line2 = LinePQube(
                    hostname=hostname, port=port,
                    auto_open=auto_open, debug=debug,
                    v_rms_register_id=self.REG_V_RMS_L2,
                    v_mag_fundamental_register_id = self.REG_V_MAG_FUNDAMENTAL_L2,
                    v_angle_fundamental_register_id = self.REG_V_ANGLE_FUNDAMENTAL_L2,
                    i_rms_register_id=self.REG_I_RMS_L2,
                    i_mag_fundamental_register_id = self.REG_I_MAG_FUNDAMENTAL_L2,
                    i_angle_fundamental_register_id = self.REG_I_ANGLE_FUNDAMENTAL_L2,
                    s_register_id=self.REG_VA_L2,
                    p_register_id=self.REG_WATT_L2,
                    q_register_id=self.REG_VAR_FUNDAMENTAL_L2,
                    v_thd_register_id=self.REG_V_THD_L2,
                    i_tdd_register_id=self.REG_I_TDD_L2)
            
        if self.meas_line1 or self.meas_line2:
            self.freq = float('nan')
            
        if auto_open:
            self.open()

    def __str__(self):
        if self.meas_line1 and self.meas_line2:
            return "Line 1: \n" + str(self.line1) + "\nLine 2: \n" + str(self.line2)
        elif self.meas_line1:
            return "Line 1: \n" + str(self.line1)
        elif self.meas_line2:
            return "Line 2: \n" + str(self.line2)
        else:
            return "No Line measurements specified."
    
    # Methods    
    def meas_freq(self):
        """Returns the measured frequency."""
        return convert_to_long(
                self.read_input_registers(self.REG_FREQ, self.READ_2_REG))
    
    def update_measurements(self):
        """Update the PQube measurements."""
        if self.meas_line1:
            self.freq = self.meas_freq()
            self.line1.update_line_measurements()
            
        if self.meas_line2:
            self.freq = self.meas_freq()
            self.line2.update_line_measurements()
            
    def pqube_phase_log(self):
        """Returns the attribute values of PQube measurements as a list for 
        data logging purposes.
        """
        self.update_measurements()
        if self.meas_line1 and self.meas_line2:
            values = [self.freq, self.line1.v_rms, 
                      self.line1.v_mag_fundamental,
                      self.line1.v_angle_funamental,
                      self.line1.i_rms, 
                      self.line1.i_mag_funamental,
                      self.line1.i_angle_fundamental,
                      self.line1.apparent_power, self.line1.real_power, 
                      self.line1.reactive_power, self.line1.v_thd, 
                      self.line1.i_tdd, self.line2.v_rms, 
                      self.line2.v_mag_fundamental,
                      self.line2.v_angle_funamental,
                      self.line2.i_rms, 
                      self.line2.i_mag_funamental,
                      self.line2.i_angle_fundamental,
                      self.line2.apparent_power, 
                      self.line2.real_power, self.line2.reactive_power, 
                      self.line2.v_thd, self.line2.i_tdd]
        elif  self.meas_line1:
            values = [self.freq, self.line1.v_rms, 
                      self.line1.v_mag_fundamental,
                      self.line1.v_angle_funamental,
                      self.line1.i_rms, 
                      self.line1.i_mag_funamental,
                      self.line1.i_angle_fundamental,
                      self.line1.apparent_power, self.line1.real_power, 
                      self.line1.reactive_power, 
                      self.line1.v_thd, self.line1.i_tdd]
            values.extend([""]*11)
        elif self.meas_line2:
            values = self.freq
            values.extend(list([""]*11))
            values.extend([self.line2.v_rms, 
                           self.line2.v_mag_fundamental,
                           self.line2.v_angle_funamental,
                           self.line2.i_rms, 
                           self.line2.i_mag_funamental,
                           self.line2.i_angle_fundamental,
                           self.line2.apparent_power, self.line2.real_power, 
                           self.line2.reactive_power, self.line2.v_thd, 
                           self.line2.i_tdd])
        else:
            values = list([""]*23)
        
        return values
    

class LToLPQube(ModbusClient):
    """Class for line measurements in pQube device in 3-phase Delta or
    Single phase L1-L2 config."""
    
    # constructors
    def __init__(self, hostname="10.60.36.6" , port=502,
                 auto_open=True, debug=False,
                 v_rms_register_id=7008):
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        self.v_rms = float('nan')
        self.v_rms_register_id = v_rms_register_id
        if auto_open:
            self.open()
        
    def __str__(self):
        rep = "V_RMS: " + str(self.v_rms) + " V"
        return rep
        
    # methods
    def __meas_v_rms(self):
        """Private method: Returns RMS voltage for the line."""
        return convert_to_long(
                self.read_input_registers(self.v_rms_register_id, 2))
        
    def update_line_measurements(self):
        """Update all the measurements for the line."""
        self.v_rms = self.__meas_v_rms()


class PQube3pDelta(ModbusClient):
    """Class for data collection with PQube in 3 phase delta configuration.
    
    Attributes:
        |  hostname: (str) IP address of the pQube device 
        |  port: (int) port number for TCP/IP communication, default 502
        |  auto_open: (bool) auto TCP connect, default True
        |  debug: (bool) debug state, default False
        |  meas_line1_line2: (bool) collect L1-L2 measurements. Default False
        |  meas_line2_line3: (bool) collect L2-L3 measurements. Default False
        |  meas_line3_line1: (bool) collect L3-L1 measurements. Default False
        |  line1_line2: object containing L1-L2 measurements.
        |  line2_line3: object containing L2-L3 measurements.
        |  line3_line1: object containing L3-L1 measurements.
        
        L-L measurement attributes: v_rms
        
    Methods: 
        |  update_measurements: update all the specified measurements.
        |  pqube_phase_log: updates the measuremens and returns as a list for
           data logging purposes.
    """
    
    # register addresses
    REG_POWER_CONFIG = 8022
    REG_V_L1_L2 = 7014
    REG_V_L2_L3 = 7016
    REG_V_L3_L1 = 7018
    
    # constructors
    def __init__(self, hostname="10.60.36.6" , port=502 ,auto_open=True, 
                 debug=False, meas_line1_line2=False, 
                 meas_line2_line3=False, meas_line3_line1=False):
        """Inits PQube3pDelta."""
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        self.meas_line1_line2 = meas_line1_line2
        self.meas_line2_line3 = meas_line2_line3
        self.meas_line3_line1 = meas_line3_line1
        # check power config on pqube
        if self.read_input_registers(self.REG_POWER_CONFIG)[0] != 4:
            print("Make sure the power configuration in the 'Setup.ini' file" +
                  " matches the 'power_config' attribute in device initialization.")
            raise AttributeError
        if self.meas_line1_line2:
            self.line1_line2 = LToLPQube(hostname=hostname, port=port,
                                                auto_open=auto_open,
                                                debug=debug,
                                                v_rms_register_id=self.REG_V_L1_L2)
        if self.meas_line2_line3:
            self.line2_line3 = LToLPQube(hostname=hostname, port=port,
                                                auto_open=auto_open,
                                                debug=debug,
                                                v_rms_register_id=self.REG_V_L2_L3)
        if self.meas_line3_line1:
            self.line3_line1 = LToLPQube(hostname=hostname, port=port,
                                                auto_open=auto_open,
                                                debug=debug,
                                                v_rms_register_id=self.REG_V_L3_L1)
        if auto_open:
            self.open()
            
    def __str__(self):
        if self.meas_line1_line2 and self.meas_line2_line3 and self.meas_line3_line1:
            return ("L1-L2: \n" + str(self.line1_line2) +
                    "L2-L3: \n" + str(self.line2_line3) +
                    "L3-L1: \n" + str(self.line3_line1))
        elif self.meas_line1_line2 and self.meas_line2_line3:
            return ("L1-L2: \n" + str(self.line1_line2) +
                    "L2-L3: \n" + str(self.line2_line3))
        elif self.meas_line2_line3 and self.meas_line3_line1:
            return ("L2-L3: \n" + str(self.line2_line3) +
                    "L3-L1: \n" + str(self.line3_line1))
        elif self.meas_line3_line1 and self.meas_line1_line2:
            return ("L1-L2: \n" + str(self.line1_line2) +
                    "L3-L1: \n" + str(self.line3_line1))
        elif self.meas_line1_line2:
            return "L1-L2: \n" + str(self.line1_line2)
        elif self.meas_line2_line3:
            return "L2-L3: \n" + str(self.line2_line3)
        elif self.meas_line3_line1:
            return "L3-L1: \n" + str(self.line3_line1)
        else:
            return "No measurements specified."
            
    # methods
    def update_measurements(self):
        """Update all the measurements."""
        if self.meas_line1_line2:
            self.line1_line2.update_line_measurements()
        if self.meas_line2_line3:
            self.line2_line3.update_line_measurements()
        if self.meas_line3_line1:
            self.line3_line1.update_line_measurements()
            
    def pqube_phase_log(self):
        """Returns updated measurements as a list for data logging."""
        self.update_measurements()
        if self.meas_line1_line2 and self.meas_line2_line3 and self.meas_line3_line1:
            values = [self.line1_line2.v_rms, self.line2_line3.v_rms,
                      self.line3_line1.v_rms]
        elif self.meas_line1_line2 and self.meas_line2_line3:
            values = [self.line1_line2.v_rms, self.line2_line3.v_rms, ""]
        elif self.meas_line2_line3 and self.meas_line3_line1:
            values = ["", self.line2_line3.v_rms,self.line3_line1.v_rms]
        elif self.meas_line1_line2 and self.meas_line3_line1:
            values = [self.line1_line2.v_rms, "", self.line3_line1.v_rms]
        elif self.meas_line1_line2:
            values = [self.line1_line2.v_rms]
            values.extend(list([""]*2))
        elif self.meas_line2_line3:
            values = ["", self.line2_line3.v_rms, ""]
        elif self.meas_line3_line1:
            values = list([""]*2)
            values.extend([self.line3_line1.v_rms])
        else:
            values = list([""]*3)
            
        return values
    
    
class PQube1pLL(ModbusClient):
    """Class for data collection with PQube in Single_Phase_L1_L2 configuration.
    
    Attributes:
        |  hostname: (str) IP address of the pQube device 
        |  port: (int) port number for TCP/IP communication, default 502
        |  auto_open: (bool) auto TCP connect, default True
        |  debug: (bool) debug state, default False
        |  meas_line1_line2: (bool) collect L1-L2 measurements. Default False
        |  line1_line2: object containing L1-L2 measurements.
        
        L-L measurement attributes: v_rms
        
    Methods: 
        |  update_measurements: update all the specified measurements.
        |  pqube_phase_log: updates the measuremens and returns as a list for
           data logging purposes.
    """
    
    # register addresses
    REG_POWER_CONFIG = 8022
    REG_V_L1_L2 = 7014
    
    # constructors
    def __init__(self, hostname="10.60.36.6" , port=502 ,auto_open=True, 
                 debug=False, meas_line1_line2=False):
        """Inits PQube3pDelta."""
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        self.meas_line1_line2 = meas_line1_line2
        # check power config on pqube
        if self.read_input_registers(self.REG_POWER_CONFIG)[0] != 1:
            print("Make sure the power configuration in the 'Setup.ini' file" +
                  " matches the 'power_config' attribute in device initialization.")
            raise AttributeError
        if self.meas_line1_line2:
            self.line1_line2 = LToLPQube(hostname=hostname, port=port,
                                                auto_open=auto_open,
                                                debug=debug,
                                                v_rms_register_id=self.REG_V_L1_L2)
        if auto_open:
            self.open()
            
    def __str__(self):
        if self.meas_line1_line2:
            return "L1-L2: \n" + str(self.line1_line2)
        else:
            return "No measurements specified."
        
    # methods
    def update_measurements(self):
        """Update all the measurements."""
        if self.meas_line1_line2:
            self.line1_line2.update_line_measurements()
            
    def pqube_phase_log(self):
        """Returns updated measurements as a list for data logging."""
        self.update_measurements()
        if self.meas_line1_line2:
            values = [self.line1_line2.v_rms]
        else:
            values = list([""])
            
        return values

    
class PQube3pWye(ModbusClient):
    """Class for data collection with PQube in 3 phase Wye/Star configuration.
    
    Added on: 10/02/2018
    
    Attributes:
        |  hostname: (str) IP address of the pQube device 
        |  port: (int) port number for TCP/IP communication, default 502
        |  auto_open: (bool) auto TCP connect, default True
        |  debug: (bool) debug state, default False
        |  meas_line1: (bool) collect L1-N measurements. Default False
        |  meas_line2: (bool) collect L2-N measurements. Default False
        |  meas_line3: (bool) collect L3-N measurements. Default False
        |  line1: object containing L1 measurements.
        |  line2: object containing L2 measurements.
        |  line3: object containing L3 measurements.
        
        
    Methods: 
        |  update_measurements: update all the specified measurements.
        |  pqube_phase_log: updates the measuremens and returns as a list for
           data logging purposes.
    """
    
    # register addresses
    REG_POWER_CONFIG = 8022
    REG_FREQ = 7026
    REG_V_RMS = [7008, 7010, 7012]
    REG_V_MAG_FUNDAMENTAL = [7098, 7102, 7106]
    REG_V_ANGLE_FUNDAMENTAL = [7100, 7104, 7108]
    REG_I_RMS = [7028, 7030, 7032]
    REG_I_MAG_FUNDAMENTAL = [7110, 7114, 7118]
    REG_I_ANGLE_FUNDAMENTAL = [7112, 7116, 7120]
    REG_V_THD = [7192, 7194, 7196]
    REG_I_TDD = [7198, 7200, 7202]
    REG_WATT = [7204, 7206, 7208]
    REG_VA = [7210, 7212, 7214]
    REG_VAR_FUNDAMENTAL = [7216, 7218, 7220]
    READ_2_REG = 2    # read two registers
    
    # constructors
    def __init__(self, hostname="10.60.36.6" , port=502 ,auto_open=True, 
                 debug=False, meas_line1=False, 
                 meas_line2=False, meas_line3=False):
        """Inits PQube3pDelta."""
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        self.meas_line1 = meas_line1
        self.meas_line2 = meas_line2
        self.meas_line3 = meas_line3
        
        # check power config on pqube: star/wye is 3
        if self.read_input_registers(self.REG_POWER_CONFIG)[0] != 3:
            print("Make sure the power configuration in the 'Setup.ini' file" +
                  " matches the 'power_config = 3p_wye' attribute " + 
                  "in device initialization.")
            raise AttributeError
            
        # define line-to-neutral measurement objects    
        if self.meas_line1:
            self.line1 = LinePQube(
                    hostname=hostname, port=port,
                    auto_open=auto_open, debug=debug,
                    v_rms_register_id=self.REG_V_RMS[0],
                    v_mag_fundamental_register_id = self.REG_V_MAG_FUNDAMENTAL[0],
                    v_angle_fundamental_register_id = self.REG_V_ANGLE_FUNDAMENTAL[0],
                    i_rms_register_id=self.REG_I_RMS[0],
                    i_mag_fundamental_register_id = self.REG_I_MAG_FUNDAMENTAL[0],
                    i_angle_fundamental_register_id = self.REG_I_ANGLE_FUNDAMENTAL[0],
                    s_register_id=self.REG_VA[0],
                    p_register_id=self.REG_WATT[0],
                    q_register_id=self.REG_VAR_FUNDAMENTAL[0],
                    v_thd_register_id=self.REG_V_THD[0],
                    i_tdd_register_id=self.REG_I_TDD[0])
        if self.meas_line2:
            self.line2 = LinePQube(
                    hostname=hostname, port=port,
                    auto_open=auto_open, debug=debug,
                    v_rms_register_id=self.REG_V_RMS[1],
                    v_mag_fundamental_register_id = self.REG_V_MAG_FUNDAMENTAL[1],
                    v_angle_fundamental_register_id = self.REG_V_ANGLE_FUNDAMENTAL[1],
                    i_rms_register_id=self.REG_I_RMS[1],
                    i_mag_fundamental_register_id = self.REG_I_MAG_FUNDAMENTAL[1],
                    i_angle_fundamental_register_id = self.REG_I_ANGLE_FUNDAMENTAL[1],
                    s_register_id=self.REG_VA[1],
                    p_register_id=self.REG_WATT[1],
                    q_register_id=self.REG_VAR_FUNDAMENTAL[1],
                    v_thd_register_id=self.REG_V_THD[1],
                    i_tdd_register_id=self.REG_I_TDD[1])
        if self.meas_line3:
            self.line3 = LinePQube(
                    hostname=hostname, port=port,
                    auto_open=auto_open, debug=debug,
                    v_rms_register_id=self.REG_V_RMS[2],
                    v_mag_fundamental_register_id = self.REG_V_MAG_FUNDAMENTAL[2],
                    v_angle_fundamental_register_id = self.REG_V_ANGLE_FUNDAMENTAL[2],
                    i_rms_register_id=self.REG_I_RMS[2],
                    i_mag_fundamental_register_id = self.REG_I_MAG_FUNDAMENTAL[2],
                    i_angle_fundamental_register_id = self.REG_I_ANGLE_FUNDAMENTAL[2],
                    s_register_id=self.REG_VA[2],
                    p_register_id=self.REG_WATT[0],
                    q_register_id=self.REG_VAR_FUNDAMENTAL[2],
                    v_thd_register_id=self.REG_V_THD[2],
                    i_tdd_register_id=self.REG_I_TDD[2])
        if auto_open:
            self.open()
            
    def __str__(self):
        if self.meas_line1 and self.meas_line2 and self.meas_line3:
            return ("Line 1: \n" + str(self.line1) + 
                    "\nLine 2: \n" + str(self.line2) + 
                    "\nLine 3: \n" + str(self.line3))
        elif self.meas_line1:
            return "Line 1: \n" + str(self.line1)
        elif self.meas_line2:
            return "Line 2: \n" + str(self.line2)
        elif self.meas_line3:
            return "Line 2: \n" + str(self.line3)
        else:
            return "No Line measurements specified."
            
    # methods
    def meas_freq(self):
        """Returns the measured frequency."""
        return convert_to_long(
                self.read_input_registers(self.REG_FREQ, self.READ_2_REG))
    
    def update_measurements(self):
        """Update all the measurements."""
        self.freq = self.meas_freq()
        if self.meas_line1:
            self.line1.update_line_measurements()
        if self.meas_line2:
            self.line2.update_line_measurements()
        if self.meas_line3:
            self.line3.update_line_measurements()
            
    def pqube_phase_log(self):
        """Returns updated measurements as a list for data logging."""
        self.update_measurements()
        values = [self.freq]
        if  self.meas_line1:
            values.extend([self.line1.v_rms,
                           self.line1.v_mag_fundamental,
                           self.line1.v_angle_funamental,
                           self.line1.i_rms,
                           self.line1.i_mag_funamental,
                           self.line1.i_angle_fundamental,
                           self.line1.apparent_power, self.line1.real_power, 
                           self.line1.reactive_power, 
                           self.line1.v_thd, self.line1.i_tdd])
        else:
            values.extend([""]*11)
            
        if self.meas_line2:
            values.extend([self.line2.v_rms,
                           self.line2.v_mag_fundamental,
                           self.line2.v_angle_funamental,
                           self.line2.i_rms, 
                           self.line2.i_mag_funamental,
                           self.line2.i_angle_fundamental,
                           self.line2.apparent_power, self.line2.real_power, 
                           self.line2.reactive_power, self.line2.v_thd, 
                           self.line2.i_tdd])
        else: values.extend([""]*11)
        
        if self.meas_line3:
            values.extend([self.line3.v_rms,
                           self.line3.v_mag_fundamental,
                           self.line3.v_angle_funamental,
                           self.line3.i_rms, 
                           self.line3.i_mag_funamental,
                           self.line3.i_angle_fundamental,
                           self.line3.apparent_power, self.line2.real_power, 
                           self.line3.reactive_power, self.line2.v_thd, 
                           self.line3.i_tdd])
        else: values.extend([""]*11)
                
        if not(self.meas_line1) and not(self.meas_line2) and not(self.meas_line3):
            values = list([""]*34)
        
        return values
    
    
    
class PQube(ModbusClient):
    """PQube class to communicate with the pQube device via TCP/IP.
    
    Attributes:
        |  hostname: Host IP address, default="10.60.36.5"
        |  port: comm. port, default=502
        |  auto_open: default True
        |  debug: default False
        |  power_config: Power configuration on PQube device, possible values:
           "split_single_phase", "3p_delta", "3p_wye", "single_phase_l1_l2"
        |  meas_line1: Valid only when power_config="split_single_phase" or
           "3p_wye" is set. Measures Line 1 attributes. Default False.
        |  meas_line2: Valid only when power_config="split_single_phase" or
           "3p_wye" is set. Measures Line 2 attributes. Default False.
        |  meas_line3: Valid only when power_config="3p_wye" is set. 
           Measures Line 3 attributes. Default False.
        |  meas_line1_line2: Valid only when power_config="3p_delta" or 
           "single_phase_l1_l2" is set. Measures L1-L2 attributes. Default False
        |  meas_line2_line3: Valid only when power_config="3p_delta" is set.
           Measures L2-L3 attributes. Default False
        |  meas_line3_line1: Valid only when power_config="3p_delta" is set.
           Measures L3-L1 attributes. Default False
        |  measurements: Object holds the specified measurements.
        
    Methods:
        |  pqube_log: updates all the collected data and returns as a list.    
    """
    
    def __init__(self, hostname="10.60.36.5", port=502, auto_open=True, 
                 debug=False, power_config="split_single_phase",
                 meas_line1=False, meas_line2=False, meas_line3=False,
                 meas_line1_line2=False, meas_line2_line3=False,
                 meas_line3_line1=False):
        ModbusClient.__init__(self, host=hostname, port=port, 
                              auto_open=auto_open, debug=debug)
        self.power_config = power_config
        "TODO: Expand power_config check for all possible PQube configurations"
        "PQube returns a list, i.e., [0]"
        if self.power_config=="split_single_phase":
            if meas_line1_line2 or meas_line2_line3 or meas_line3_line1 or meas_line3:
                raise ValueError("meas_line1_line2, meas_line2_line3, " +
                                 "meas_line3_line1 cannot be set to True " + 
                                 "for split_single_phase power configuration.")
            self.measurements = PQubeSplit1p(hostname=hostname, port=port,
                                             auto_open=auto_open, debug=debug,
                                             meas_line1=meas_line1, 
                                             meas_line2=meas_line2)
        elif self.power_config=="3p_delta":
            if meas_line1 or meas_line2 or meas_line3:
                raise ValueError("meas_line1, meas_line2, meas_line3 " + 
                                 "cannot be set to " + 
                                 "True for 3p_delta power configuration.")
            self.measurements = PQube3pDelta(hostname=hostname, port=port, 
                                             auto_open=auto_open, debug=debug,
                                             meas_line1_line2=meas_line1_line2,
                                             meas_line2_line3=meas_line2_line3,
                                             meas_line3_line1=meas_line3_line1)
            
        elif self.power_config=="3p_wye":
            if meas_line1_line2 or meas_line2_line3 or meas_line3_line1:
                raise ValueError("meas_line1_line2, meas_line2_line3, " +
                                 "meas_line3_line1 cannot be set to True " + 
                                 "for 3p_wye power configuration.")
            self.measurements = PQube3pWye(hostname=hostname, port=port,
                                             auto_open=auto_open, debug=debug,
                                             meas_line1=meas_line1, 
                                             meas_line2=meas_line2, 
                                             meas_line3=meas_line3)
            
        elif self.power_config=="single_phase_l1_l2":
            if meas_line1 or meas_line2 or meas_line3 or meas_line2_line3 or meas_line3_line1:
                raise ValueError("meas_line1, meas_line2, meas_line3, " +
                                 "meas_line2_line3, meas_line3_line1 " +
                                 "cannont be set to True for " +
                                 "single_phase_L1_L2 power configuration")
            self.measurements = PQube1pLL(hostname=hostname, port = port, 
                                          auto_open=auto_open, debug=debug, 
                                          meas_line1_line2=meas_line1_line2)
        else:
            raise ValueError("Unknown power configuration.")
            
    def __str__(self):
        return str(self.measurements)
            
    def pqube_log(self):
        return self.measurements.pqube_phase_log() 
    
    