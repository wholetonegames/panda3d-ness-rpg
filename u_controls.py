from panda3d.core import InputDevice


class ConfigControls:
    def __init__(self):
        self.gamepad = None
        self.axis_threshold = 0.5
        self.axis_threshold_negative = 0 - self.axis_threshold
        self.controlList = [
            ["arrow_left", self.setDirection,  ["left", True]],
            ["arrow_right", self.setDirection, ["right", True]],
            ["arrow_up", self.setDirection,    ["up", True]],
            ["arrow_down", self.setDirection,  ["down", True]],
            ["arrow_left-up", self.setDirection,  ["left", False]],
            ["arrow_right-up", self.setDirection, ["right", False]],
            ["arrow_up-up", self.setDirection,    ["up", False]],
            ["arrow_down-up", self.setDirection,  ["down", False]],
            ["space", self.setCommand,  ["confirm", True]],
            ["space-up", self.setCommand,  ["confirm", False]],
            ["enter", self.setCommand,  ["confirm", True]],
            ["enter-up", self.setCommand,  ["confirm", False]],
            ["z", self.setCommand,  ["cancel", True]],
            ["z-up", self.setCommand,  ["cancel", False]],
            ["x", self.setCommand,  ["confirm", True]],
            ["x-up", self.setCommand,  ["confirm", False]],
            ["escape", self.setCommand,  ["cancel", True]],
            ["escape-up", self.setCommand,  ["cancel", False]],
            ["backspace", self.setCommand,  ["cancel", True]],
            ["backspace-up", self.setCommand,  ["cancel", False]],

            ["gamepad-dpad_right", self.setDirection, ["right", True]],
            ["gamepad-dpad_right-up", self.setDirection, ["right", False]],
            ["gamepad-dpad_left", self.setDirection, ["left", True]],
            ["gamepad-dpad_left-up", self.setDirection, ["left", False]],
            ["gamepad-dpad_up", self.setDirection, ["up", True]],
            ["gamepad-dpad_up-up", self.setDirection, ["up", False]],
            ["gamepad-dpad_down", self.setDirection, ["down", True]],
            ["gamepad-dpad_down-up", self.setDirection, ["down", False]],
            ["gamepad-face_a", self.setCommand,  ["confirm", True]],
            ["gamepad-face_a-up", self.setCommand,  ["confirm", False]],
            ["gamepad-face_b", self.setCommand,  ["cancel", True]],
            ["gamepad-face_b-up", self.setCommand,  ["cancel", False]],
        ]
        # self.initController()

    def initController(self):
        self.disableController()

        for control in self.controlList:
            base.accept(control[0], control[1], control[2])

        # Accept device dis-/connection events
        base.accept("connect-device", self.connect)
        base.accept("disconnect-device", self.disconnect)

    def connect(self, device):
        # gamepads = base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            self.gamepad = device
            base.attachInputDevice(device, prefix="gamepad")

    def disconnect(self, device):
        if self.gamepad != device:
            return

        base.detachInputDevice(device)
        self.gamepad = None

    def resetButtons(self):
        self.directionMap = {"left": False,
                             "right": False, "down": False, "up": False}
        self.commandMap = {"confirm": False, "cancel": False}

    def setDirection(self, key, value):
        self.directionMap[key] = value

    def setCommand(self, key, value):
        self.commandMap[key] = value

    def disableController(self):
        self.resetButtons()

        base.ignore("connect-device")
        base.ignore("disconnect-device")

        for control in self.controlList:
            base.ignore(control[0])

    def read_axis_left(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}

        left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
        left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
        return {'x': left_x.value, 'y': left_y.value}

    def read_axis_right(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}
        right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
        right_y = self.gamepad.findAxis(InputDevice.Axis.right_y)
        return {'x': right_x.value, 'y': right_y.value}

    def move_from_axis(self, is_left_axis):
        axis_obj = self.read_axis_left() if is_left_axis else self.read_axis_right()
        print(axis_obj)
        if axis_obj['x'] <= self.axis_threshold_negative:
            self.setDirection('left', True)
        else:
            self.setDirection('left', False)
        if axis_obj['x'] >= self.axis_threshold:
            self.setDirection('right', True)
        else:
            self.setDirection('right', False)

        if axis_obj['y'] <= self.axis_threshold_negative:
            self.setDirection('down', True)
        else:
            self.setDirection('down', False)
        if axis_obj['y'] >= self.axis_threshold:
            self.setDirection('up', True)
        else:
            self.setDirection('up', False)
