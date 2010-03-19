#!/usr/bin/env python

import usb
import sys
import time

class MailNotifier:
	
	def makeData(self, color):
		return (color, 0, 0, 0, 0)
	
	def __init__(self):
		self.dev=UsbDevice(0x1294, 0x1320)
		self.dev.open()
		self.dev.handle.reset()
		
	def setColor(self, color):
		self.dev.handle.interruptWrite(0x02, self.makeData(color), 1000)
		
class UsbDevice:
	def __init__(self, vendor_id, product_id):
		busses = usb.busses()
		self.handle = None
		count = 0
		for bus in busses:
				devices = bus.devices
				for dev in devices:
					if dev.idVendor==vendor_id and dev.idProduct==product_id:
						self.dev = dev
						self.conf = self.dev.configurations[0]
						self.intf = self.conf.interfaces[0][0]
						self.endpoints = []
						for endpoint in self.intf.endpoints:
							self.endpoints.append(endpoint)
						return
		sys.stderr.write("No mail notifier found\n")

	def open(self):
		if self.handle:
			self.handle = None
		try:
			self.handle = self.dev.open()
			self.handle.detachKernelDriver(0)
			self.handle.detachKernelDriver(1)
			self.handle.setConfiguration(self.conf)
			self.handle.claimInterface(self.intf)
			self.handle.setAltInterface(self.intf)
			return True
		except:
			return False

def main(argv):
	if len(argv) != 2:
		sys.stderr.write("Usage : %s color_number\n" % argv[0])
	else:
		m = MailNotifier()
		m.setColor(int(argv[1]))

if __name__=="__main__":
	main(sys.argv)
