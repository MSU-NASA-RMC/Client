# -*- coding: utf-8 -*-

import sys
from PyQt5 import Qt, QtCore, QtWidgets

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import client
from UIdesign import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, client, parent=None):
        super(Window, self).__init__(parent)
        self.client = client

        # setup buttons
        self.connection_button = None
        self.autonomy_button = None

        self.setupUi(self)

        # connect methods
        self.connection_button.triggered.connect(self.on_connection_button)
        self.autonomy_button.triggered.connect(self.on_autonomy_button)
        self.autonomy_button.setEnabled(False)
        self.motor_speed_to_adjust = 1

        self.drive_keys_pressed = []

        self.actuator_keys_pressed = []

        self.bucket_keys_pressed = []

        self.show()

    def on_message_return(self, message):
        print (message)

    def on_connection_button(self):
        if self.connection_button.text() == "open connection":
            self.client.open_connection(self.on_message_return)
            self.autonomy_button.setEnabled(True)
            self.connection_button.setText("close connection")

        elif self.connection_button.text() == "close connection":
            quit_message = 'Are you sure you want to close the connection?'
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   quit_message,
                                                   QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.Yes)

            if reply == QtWidgets.QMessageBox.Yes:
                self.client.close_connection()
                self.connection_button.setText("open connection")
                self.autonomy_button.setEnabled(False)

    def on_autonomy_button(self):
        if self.autonomy_button.text() == "activate autonomy":
            warning_message = 'Are you sure you want to activate autonomy?'
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   warning_message,
                                                   QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.Yes)

            if reply == QtWidgets.QMessageBox.Yes:
                self.autonomy_button.setText("deactivate autonomy")
                pass
        elif self.autonomy_button.text() == "deactivate autonomy":
            warning_message = 'Are you sure you want to deactivate autonomy?'
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   warning_message,
                                                   QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.Yes)

            if reply == QtWidgets.QMessageBox.Yes:
                self.autonomy_button.setText("activate autonomy")
                pass

    def keyPressEvent(self, event):
        if self.client.connection is None or \
                        self.client.is_autonomy_acticated():
            return
        key = event.key()

        if not event.isAutoRepeat():
            # Driving logic
            if key == QtCore.Qt.Key_W:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)
                self.client.drive_forward(self.client.get_drive_speed())
            elif key == QtCore.Qt.Key_S:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)
                self.client.drive_reverse(self.client.get_drive_speed())
            elif key == QtCore.Qt.Key_A:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)
                self.client.turn_right(self.client.get_drive_speed())
            elif key == QtCore.Qt.Key_D:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)
                self.client.turn_left(self.client.get_drive_speed())

            # Motor speed adjustment mode logic
            elif key == QtCore.Qt.Key_1:
                self.motor_speed_to_adjust = client.Motor.DRIVE_MOTORS.value
                print ('Motor speed adjustment mode:', str(self.motor_speed_to_adjust))
            elif key == QtCore.Qt.Key_2:
                self.motor_speed_to_adjust = client.Motor.ACTUATOR.value
                print ('Motor speed adjustment mode:', str(self.motor_speed_to_adjust))
            elif key == QtCore.Qt.Key_3:
                self.motor_speed_to_adjust = client.Motor.BUCKET.value
                print ('Motor speed adjustment mode:', str(self.motor_speed_to_adjust))

            # Actuator logic
            elif key == QtCore.Qt.Key_U:
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)
                self.client.actuator_forward(self.client.get_actuator_speed())
            elif key == QtCore.Qt.Key_J:
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)
                self.client.actuator_reverse(self.client.get_actuator_speed())

            # Bucket logic
            elif key == QtCore.Qt.Key_I:
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)
                self.client.bucket_forward(self.client.get_bucket_speed())
            elif key == QtCore.Qt.Key_K:
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)
                self.client.actuator_reverse(self.client.get_bucket_speed())

        # Motor speed adjustment logic
        if key == QtCore.Qt.Key_Up:
            if self.client.motor_speeds[self.motor_speed_to_adjust] < client.MAX_MOTOR_SPEED:
                if self.motor_speed_to_adjust is 0:
                    self.client.set_drive_speed(self.client.get_drive_speed() + 1)
                elif self.motor_speed_to_adjust is 1:
                    self.client.set_actuator_speed(self.client.get_actuator_speed() + 1)
                elif self.motor_speed_to_adjust is 2:
                    self.client.set_bucket_speed(self.client.get_bucket_speed() + 1)
                print (self.client.motor_speeds[self.motor_speed_to_adjust])
                self.update_motor_speeds()
                if len(self.drive_keys_pressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.drive_keys_pressed[-1],
                                                    QtCore.Qt.NoModifier))
        elif key == QtCore.Qt.Key_Down:
            if self.client.motor_speeds[self.motor_speed_to_adjust] > 0:
                if self.motor_speed_to_adjust is 0:
                    self.client.set_drive_speed(self.client.get_drive_speed() - 1)
                elif self.motor_speed_to_adjust is 1:
                    self.client.set_actuator_speed(self.client.get_actuator_speed() - 1)
                elif self.motor_speed_to_adjust is 2:
                    self.client.set_bucket_speed(self.client.get_bucket_speed() - 1)
                print (self.client.motor_speeds[self.motor_speed_to_adjust])
                self.update_motor_speeds()
                if len(self.drive_keys_pressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.drive_keys_pressed[-1],
                                                    QtCore.Qt.NoModifier))

    def update_motor_speeds(self):
        self.left_motor_target_speed.setText("left motor: " + str(self.client.get_drive_speed()))
        self.right_motor_target_speed.setText("right motor: " + str(self.client.get_drive_speed()))
        self.actuator_target_speed.setText("actuator: " + str(self.client.get_actuator_speed()))
        self.bucket_target_speed.setText("bucket: " + str(self.client.get_bucket_speed()))

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() or self.client.connection is None \
                or self.client.is_autonomy_acticated():
            return

        key = event.key()

        if key in self.drive_keys_pressed:
            self.drive_keys_pressed.remove(key)

        if key in self.actuator_keys_pressed:
            self.actuator_keys_pressed.remove(key)

        if key in self.bucket_keys_pressed:
            self.bucket_keys_pressed.remove(key)

        # Driving logic
        if not len(self.drive_keys_pressed):
            if key == QtCore.Qt.Key_W:
                self.client.drive_forward(0)
            elif key == QtCore.Qt.Key_S:
                self.client.drive_reverse(0)
            elif key == QtCore.Qt.Key_A:
                self.client.turn_left(0)
            elif key == QtCore.Qt.Key_D:
                self.client.turn_right(0)

        # Actuator logic
        if not len(self.actuator_keys_pressed):
            if key == QtCore.Qt.Key_U:
                self.client.actuator_forward(0)
            elif key == QtCore.Qt.Key_J:
                self.client.actuator_reverse(0)

        # Bucket logic
        if not len(self.bucket_keys_pressed):
            if key == QtCore.Qt.Key_I:
                self.client.bucket_forward(0)
            elif key == QtCore.Qt.Key_K:
                self.client.bucket_reverse(0)



def main(client):
    app = QApplication(sys.argv)
    window = Window(client)
    sys.exit(app.exec_())

if __name__ == '__main__':
    client = client.Client()
    main(client)