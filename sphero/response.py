# coding: utf-8
import struct


class Response(object):
    SOP1 = 0
    SOP2 = 1
    MRSP = 2
    SEQ = 3
    DLEN = 4

    CODE_OK = 0

    def __init__(self, header, data):
        self.header = header
        self.data = data

    @property
    def fmt(self):
        return '%sB' % len(self.data)

    def empty(self):
        return self.header[self.DLEN] == 1

    @property
    def success(self):
        return self.header[self.MRSP] == self.CODE_OK

    def seq(self):
        return self.header[self.SEQ]

    @property
    def body(self):
        return struct.unpack(self.fmt, self.data)


class GetRGB(Response):
    def __init__(self, header, body):
        super(GetRGB, self).__init__(header, body)
        # TODO: these values seem incorrect
        self.r = struct.unpack("B",body[0])[0]
        self.g = struct.unpack("B",body[1])[0]
        self.b = struct.unpack("B",body[2])[0]


class GetBluetoothInfo(Response):
    def __init__(self, header, body):
        super(GetBluetoothInfo, self).__init__(header, body)
        self.name = self.data.split('\x00', 1)[0]
        self.bta = self.data[16:].split('\x00', 1)[0]

class GetAutoReconnect(Response):
    def __init__(self, header, body):
        super(GetAutoReconnect, self).__init__(header, body)
        self.enable= struct.unpack("!B",body[0])[0]
        self.time=struct.unpack("!B",body[1])[0]

class GetPowerState(Response):
    def __init__(self, header, body):
        super(GetPowerState, self).__init__(header, body)
        self.recVer=body[0]
        self.powerState=body[1]
        self.batteryVoltage=struct.unpack("!H",self.data[2:4])[0]/100.
        self.numberCharges=struct.unpack("!H",self.data[4:6])[0]
        self.timeSinceCharge=struct.unpack("!H",self.data[6:8])[0]

class GetVoltageTripPoints(Response):
    def __init__(self, header, body):
        super(GetVoltageTripPoints, self).__init__(header, body)
        self.vLow=struct.unpack("!H",self.data[0:2])[0]/100.
        self.vCrit=struct.unpack("!H",self.data[2:4])[0]/100.

class PollPacketTimes(Response):
    def __init__(self, header, body):
        super(PollPacketTimes, self).__init__(header, body)
        self.cTime=struct.unpack("!I",self.data[0:4])[0]
        self.rxTime=struct.unpack("!I",self.data[4:8])[0]
        self.txTime=struct.unpack("!I",self.data[8:12])[0]
