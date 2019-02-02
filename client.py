import argparse

from PyQt5.QtCore import QThread, pyqtSignal

import UIlogic
from connection import *
from message import *

DEFAULT_CLIENT_IP_ADDRESS = '0.0.0.0'
DEFAULT_CLIENT_PORT_NUMBER = 1123

DEFAULT_CONTROLLER_IP_ADDRESS = '192.168.1.6'
DEFAULT_CONTROLLER_PORT_NUMBER = 5813

DEFAULT_BUFFER_SIZE = 1024

MAX_MOTOR_SPEED = 100
MAX_SERVO_ANGLE = 180


class Motor(enum.Enum):
    DRIVE_MOTORS = 0
    ACTUATOR = 1
    BUCKET = 2

class ConnectionThread(QThread):
    # create the signals that will be emitted from this QThread
    message = pyqtSignal(str)

    def __init__(self, connection):
        QThread.__init__(self)
        self.connection = connection
        self.message.emit("test")

    def run(self):
        while True:
            message_received = self.connection.get_message()

            if message_received is not None:
                self.message.emit(message_received)

class Client:

    def __init__(self, client_ip_address, client_port_number,
                 controller_ip_address, controller_port_number,
                 buffer_size):
        self.client_ip_address = client_ip_address
        self.client_port_number = client_port_number

        self.controller_ip_address = controller_ip_address
        self.controller_port_number = controller_port_number

        self.buffer_size = buffer_size

        self.motor_speeds = {0: 25, 1: 100, 2: 40}
        self.connection = None
        self.connection_thread = None
        self.clientUI = UIlogic.main(self)

        self.autonomy_activated = False

    def open_connection(self, *args, **kwargs):
        self.connection = Connection(self.client_ip_address, self.client_port_number,
                                     self.controller_ip_address, self.controller_port_number,
                                     self.buffer_size)
        self.connection_thread = ConnectionThread(self.connection)
        self.connection_thread.message.connect(*args, **kwargs)
        self.connection_thread.start()

    def send_message(self, message):
        print (message)
        if self.connection.remote_status is RemoteStatus.HANDSHAKE_SUCCESSFUL:
            self.connection.send(message)

    def close_connection(self):
        self.connection_thread.terminate()
        self.connection.close_server_socket()

    def shutdown(self):
        self.connection_thread.terminate()
        self.connection.close_server_socket()

    def set_drive_speed(self, speed):
        self.motor_speeds[Motor.DRIVE_MOTORS.value] = speed

    def get_drive_speed(self):
        return self.motor_speeds[Motor.DRIVE_MOTORS.value]

    def set_actuator_speed(self, speed):
        self.motor_speeds[Motor.ACTUATOR.value] = speed

    def get_actuator_speed(self):
        return self.motor_speeds[Motor.ACTUATOR.value]

    def set_bucket_speed(self, speed):
        self.motor_speeds[Motor.BUCKET.value] = speed

    def get_bucket_speed(self):
        return self.motor_speeds[Motor.BUCKET.value]

    def drive_forward(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'l': speed,
                        'r': speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def drive_reverse(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'l': -1 * speed,
                        'r': -1 * speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def turn_left(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'l': -1 * speed,
                        'r': 1 * speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def turn_right(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'l': 1 * speed,
                        'r': -1 * speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def actuator_forward(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'a': speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def actuator_reverse(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'a': -1 * speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def bucket_forward(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'b': speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def bucket_reverse(self, speed):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        sub_messages = {'b': -1 * speed}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def set_left_drive_enabled(self, boolean=False):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        if boolean:
            sub_messages = {'l': 'd'}
        else:
            sub_messages = {'l': 'e'}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def set_right_drive_enabled(self, boolean=False):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        if boolean:
            sub_messages = {'r': 'd'}
        else:
            sub_messages = {'r': 'e'}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def set_actuator_enabled(self, boolean=False):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        if boolean:
            sub_messages = {'a': 'd'}
        else:
            sub_messages = {'a': 'e'}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def set_bucket_enabled(self, boolean=False):
        forwarding_prefix = ForwardingPrefix.MOTOR.value
        if boolean:
            sub_messages = {'b': 'd'}
        else:
            sub_messages = {'b': 'e'}
        message = Message(forwarding_prefix, sub_messages).message
        self.send_message(message)

    def activate_autonomy(self):
        pass

    def deactivate_autonomy(self):
        pass

    def is_autonomy_acticated(self):
        return False


def main(client_ip_address, client_port_number,
         controller_ip_address, controller_port_number,
         buffer_size):
        return Client(client_ip_address, client_port_number,
                      controller_ip_address, controller_port_number,
                      buffer_size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cip', '--clientIPAddress', help='client IP address',
                        required=False, default=DEFAULT_CLIENT_IP_ADDRESS)
    parser.add_argument('-cpn', '--clientPortNumber', help='client port number',
                        required=False, type=int, default=str(DEFAULT_CLIENT_PORT_NUMBER))
    parser.add_argument('-kip', '--controllerIPAddress', help='controller IP address',
                        required=False, default=DEFAULT_CONTROLLER_IP_ADDRESS)
    parser.add_argument('-kpn', '--controllerPortNumber', help='controller port number',
                        required=False, type=int, default=str(DEFAULT_CONTROLLER_PORT_NUMBER))
    parser.add_argument('-bs', '--bufferSize', help='buffer size',
                        required=False, type=int, default=str(DEFAULT_BUFFER_SIZE))
    args = parser.parse_args()

    print ('clientIpAddress:', args.clientIPAddress)
    print ('clientPortNumber:', args.clientPortNumber)
    print ('controllerIpAddress:', args.controllerIPAddress)
    print ('controllerPortNumber:', args.controllerPortNumber)
    print ('bufferSize:', args.bufferSize)

    main(args.clientIPAddress, args.clientPortNumber,
         args.controllerIPAddress, args.controllerPortNumber,
         args.bufferSize)
