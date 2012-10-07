import usb.core
import usb.util

class Scale:
	device = None
	endpoint = None

	MODE_GRAMS = 0x02
	MODE_OUNCES = 0x0B
	INTERFACE = 0

	def __init__(self, vendor_id, product_id):
		# find the USB device
		self.device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

		#Get rid of kernal driver
		try:
			self.device.detach_kernel_driver(self.INTERFACE)
		except usb.core.USBError:
			print "USBError when detaching kernel driver. It's probably already detached. "

		# use the first/default configuration
		self.device.set_configuration()
		# first endpoint
		self.endpoint = self.device[0][(0,0)][0]

	def readOunces(self):
		data = self.readData()
		return (self.readGrams() / 28.3495);

	def readGrams(self):
		data = self.readData()

		grams = (data[4] + (256 * data[5]))
		if(0x05 == data[1]):
			grams = -grams

		if(data[2] == self.MODE_GRAMS):
			return grams

		return ((grams*0.1) * 28.3495)

	def readData(self):
		# read a data packet
		attempts = 10
		data = None
		while data is None and attempts > 0:
			try:
				data = self.device.read(self.endpoint.bEndpointAddress,
													 self.endpoint.wMaxPacketSize)
			except usb.core.USBError as e:
				data = None
				if e.args == ('Operation timed out',):
						attempts -= 1
						continue
		return data

	def writeData(self, data):
		self.device.write(self.endpoint.bEndpointAddress, data)

#scale = Scale(VENDOR_ID, PRODUCT_ID)
#print scale.readData()
#print scale.readOunces()

# print scale.writeData([0x00, 0x00, 0x00, 0x00])
