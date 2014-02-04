import threading
import struct
import time

class Reception(threading.Thread):
    
    def __init__(self,serial):
        threading.Thread.__init__(self)
        self.sp=serial
        self._stopevent = threading.Event()
        self.responseEvent=threading.Event()

    def getResponse(self):
        self.responseEvent.wait()
        response = [self.header,self.body]
        self.responseEvent.clear()
        return response
    
    def run(self):
        while not self._stopevent.isSet():
            if self.sp.inWaiting() < 5:
                time.sleep(0.005)
                continue
            header=struct.unpack('5B', self.sp.read(5))
            if header[1]==0xff:
                #response packet
                self.header=header
                self.body = self.sp.read(self.header[-1])
                self.responseEvent.set()
                
            else:
                #asynchronous packet 
                pack=struct.pack('5B', header[0],header[1],header[2],header[3],header[4])
                header=struct.unpack("!3BH",pack)
                body=self.sp.read(header[-1])
                if header[2]== 0x01:
                    #power notification
                    print struct.unpack("2B",body)[0]
                elif header[2]== 0x02:
                    #Lvl 1 diagnostic response
                    print body[:-1]
                elif header[2]== 0x03:
                    #sensor data streaming
                    print self.data
                elif header[2]== 0x04:
                    #config block contents
                    print self.data
                elif header[2]== 0x05:
                    #pre-sleep warning (10sec)
                    self.stop()
                    print "sleep"
                elif header[2]== 0x06:
                    #Macro markers
                    print self:x.data
                elif header[2]== 0x07:
                    #Collision detected
                    print self.data
                elif header[2]== 0x08:
                    #orbBasic PRINT message
                    print self.data
                elif header[2]== 0x09:
                    #orbBasic error message, ASCII
                    print self.data
                elif header[2]== 0x0A:
                    #orbBasic error message, binary
                    print self.data
                elif header[2]== 0x0B:
                    #Self Level Result
                    print self.data
                elif header[2]== 0x0C:
                    #Gyro axis limit exceeded 
                    print self.data
                elif header[2]== 0x0D:
                    #Sphero's soul data
                    print self.data
                elif header[2]== 0x0E:
                    #Level up notification
                    print self.data
                elif header[2]== 0x0F:
                    #Shield damage notification
                    print self.data
                elif header[2]== 0x10:
                    #XP update notification
                    print self.data
                elif header[2]== 0x11:
                    #Boost update notification
                    print self.data
        

    def stop(self):
        self._stopevent.set( )
