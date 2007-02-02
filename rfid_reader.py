from device_manager import DeviceManager
from phidget_rfid import PhidgetRFID

dm = DeviceManager()
dm.find()

print 'Possible matches:\n-----------------'
i = 1
for dev in dm.matches:
    print '%d. %s\n~~~\n%s\n~~~' % (i, dev.product, dev)
    i = i + 1

reader = PhidgetRFID(dm.matches[0])
reader.init()
