import socket
import time
import smbus
import time
import threading
from threading import Lock

'''
Code here is taken from the mDEV.py script found in the freenove github https://github.com/Freenove/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi
'''
def numMap(value,fromLow,fromHigh,toLow,toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

class mDEV:
    CMD_SERVO1      =   0
    CMD_SERVO2      =   1
    CMD_SERVO3      =   2
    CMD_SERVO4      =   3
    CMD_PWM1        =   4
    CMD_PWM2        =   5
    CMD_DIR1        =   6
    CMD_DIR2        =   7
    CMD_BUZZER      =   8
    CMD_IO1         =   9
    CMD_IO2         =   10
    CMD_IO3         =   11
    CMD_SONIC       =   12
    SERVO_MAX_PULSE_WIDTH = 2500
    SERVO_MIN_PULSE_WIDTH = 500
    SONIC_MAX_HIGH_BYTE = 50
    Is_IO1_State_True = False
    Is_IO2_State_True = False
    Is_IO3_State_True = False
    Is_Buzzer_State_True = False
    handle = True
    mutex = Lock()
    def __init__(self,addr=0x18):
        self.address = addr #default address of mDEV
        self.bus=smbus.SMBus(1)
        self.bus.open(1)
    def i2cRead(self,reg):
        self.bus.read_byte_data(self.address,reg)
        
    def i2cWrite1(self,cmd,value):
        self.bus.write_byte_data(self.address,cmd,value)
        
    def i2cWrite2(self,value):
        self.bus.write_byte(self.address,value)
    
    def writeReg(self,cmd,value):
        try:
            value = int(value)
            #print(value,type(value))
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address,cmd,[value>>8,value&0xff])
            time.sleep(0.001)
        except Exception as e:
            print(Exception,"I2C Error :",e)
        
    def readReg(self,cmd):      
        ##################################################################################################
        #Due to the update of SMBus, the communication between Pi and the shield board is not normal. 
        #through the following code to improve the success rate of communication.
        #But if there are conditions, the best solution is to update the firmware of the shield board.
        ##################################################################################################
        for i in range(0,10,1):
            self.bus.write_i2c_block_data(self.address,cmd,[0])
            a = self.bus.read_i2c_block_data(self.address,cmd,1)
            
            self.bus.write_byte(self.address,cmd+1)
            b = self.bus.read_i2c_block_data(self.address,cmd+1,1)
            
            self.bus.write_byte(self.address,cmd)
            c = self.bus.read_byte_data(self.address,cmd)
            
            self.bus.write_byte(self.address,cmd+1)
            d = self.bus.read_byte_data(self.address,cmd+1)
            #print i,a,b,c,d
            #'''
            if(a[0] == c and c < self.SONIC_MAX_HIGH_BYTE ): #and b[0] == d
                return c<<8 | d
            else:
                continue
            #'''
            '''
            if (a[0] == c and c < self.SONIC_MAX_HIGH_BYTE) :
                return c<<8 | d
            elif (a[0] > c and c < self.SONIC_MAX_HIGH_BYTE) :
                return c<<8 | d
            elif (a[0] < c and a[0] < self.SONIC_MAX_HIGH_BYTE) :
                return a[0]<<8 | b[0]
            else :
                continue
            '''
        return 0
        #################################################################################################
        #################################Old codes#######################################################
        #[a,b]=self.bus.read_i2c_block_data(self.address,cmd,2)
        #print "a,b",[a,b]
        #return a<<8 | b
        #################################################################################################
    def move(self,left_pwm,right_pwm,steering_angle=90):
        self.setServo('1',steering_angle)
        if left_pwm>0:
            mdev.writeReg(mdev.CMD_DIR2,1)
            mdev.writeReg(mdev.CMD_PWM2,left_pwm)
        else:
            mdev.writeReg(mdev.CMD_DIR2,0)
            mdev.writeReg(mdev.CMD_PWM2,abs(left_pwm))
        if right_pwm>0:
            mdev.writeReg(mdev.CMD_DIR1,1)
            mdev.writeReg(mdev.CMD_PWM1,right_pwm)
        else:
            mdev.writeReg(mdev.CMD_DIR1,0)
            mdev.writeReg(mdev.CMD_PWM1,abs(right_pwm))
        
    def setServo(self,index,angle):
        angle=numMap(angle,0,180,500,2500)
        if index=="1":
            self.writeReg(mdev.CMD_SERVO1,angle)
        elif index=="2":
            self.writeReg(mdev.CMD_SERVO2,angle)
        elif index=="3":
            self.writeReg(mdev.CMD_SERVO3,angle)
        elif index=="4":
            self.writeReg(mdev.CMD_SERVO4,angle)
            
    def setLed(self,R,G,B):
        if R==1:
            mdev.writeReg(mdev.CMD_IO1,0)
        else:
            mdev.writeReg(mdev.CMD_IO1,1)
        if G==1:
            mdev.writeReg(mdev.CMD_IO2,0)
        else:
            mdev.writeReg(mdev.CMD_IO2,1)
        if B==1:
            mdev.writeReg(mdev.CMD_IO3,0)
        else:
            mdev.writeReg(mdev.CMD_IO3,1)
    def setBuzzer(self,PWM):
        mdev.writeReg(mdev.CMD_BUZZER,PWM)
    def getSonicEchoTime():
        SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
        return SonicEchoTime
        
    def getSonic(self):
        SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
        distance = SonicEchoTime * 17.0 / 1000.0
        return distance
    def setShieldI2cAddress(self,addr): #addr: 7bit I2C Device Address 
        if (addr<0x03) or (addr > 0x77) :
            return 
        else :
            mdev.writeReg(0xaa,(0xbb<<8)|(addr<<1))

'''
Here starts the code I wrote
'''

class RPIServer:
	
	IP = '169.254.243.173'
	#IP = '127.0.0.1'	
	PORT = 2222
	BUFFERSIZE = 1024
	PROTOCOL = 'utf-8'

	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._socket.bind((self.IP, self.PORT))
		self._clientaddr = None
		
	def _recvmsg(self):
		msg, addr = self._socket.recvfrom(self.BUFFERSIZE)
		self._clientaddr = addr
		return msg.decode(self.PROTOCOL)
		
	def _sendmsg(self, msg):
		self._socket.sendto(msg.encode(self.PROTOCOL), self._clientaddr)
		
	def _spinmotor(self, pwmval, direc):
		mdev.writeReg(mdev.CMD_DIR1, direc)
		#mdev.writeReg(mdev.CMD_DIR2, direc)
		mdev.writeReg(mdev.CMD_PWM1, pwmval)
		#mdev.writeReg(mdev.CMD_PWM2, pwmval)
		
	def run(self):
		while True:
			print("Listening")
			command = self._recvmsg()
			print(f"Command Recieved {command}")
			#print(command, command[:2], command[2], command[2:])
			if command[:2] == 's-':
				try:
					if command[2] == '-':
						self._spinmotor(int(command[3:]), 0)
					else:
						self._spinmotor(int(command[2:]), 1)
					#print(int(command[2:]))
					self._sendmsg(f"Sping set to {command[2:]}")
					print(f"Sping set to {command[2:]}")
				except:
					self._sendmsg(f"Error Occouured")
					print("Error :(")
			elif command[:2] == 'sa':
				self._sendmsg("Stopping")
				print("Stopping Server")
				break
			else:
				print('Unrecognised Command')
				self._sendmsg('Unrecognised Command')

if __name__ == '__main__':
	
	mdev = mDEV()
	a = RPIServer()
	a.run()
