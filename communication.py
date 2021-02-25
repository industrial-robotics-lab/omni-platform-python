import serial
import struct
from threading import Thread

# float array serial transceiver
class SerialTransceiver:

    def __init__(self) -> None:
        self._msg_to_send = [0, 0, 0]
        self._msg_to_receive = [0, 0, 0]

        self.theta = [0]
        self.x = [0]
        self.y = [0]

        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._transactions_count = 0
        self._wrong_len_msgs = 0
        self._is_stop = False
        self._repeats = 0

    def set_msg(self, msg):
        assert (len(msg) == 3)
        self._msg_to_send = msg

    def tx(self):
        byte_array = struct.pack('3f', self._msg_to_send[0], self._msg_to_send[1], self._msg_to_send[2])
        self._port.write(byte_array)
        self._port.write(b'\n')

    def rx(self):
        response = self._port.readline()
        if len(response) == 13:
            float_array = struct.unpack('3f', response[0:12])
            self.msg_to_receive = float_array
            if self.theta[-1] == float_array[0] and self.x[-1] == float_array[1] and self.y[-1] == float_array[2]:
                self._repeats += 1
            else:
                self.theta.append(float_array[0])
                self.x.append(float_array[1])
                self.y.append(float_array[2])
        else:
            self._wrong_len_msgs += 1
    
    def talk_arduino(self):
        while not self._is_stop:
            self.tx()
            self.rx()
            self._transactions_count += 1
        self._port.close()

    def stop(self):
        print(f"Transactions = {self._transactions_count}\n accepted={len(self.x)}\n repeats: {self._repeats}\n wrong length: {self._wrong_len_msgs}\n")
        self._is_stop = True
        self._transactions_count = 0
        self._repeats = 0
