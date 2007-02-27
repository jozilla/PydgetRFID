HAL_STR = 'org.freedesktop.Hal'
DEV_STR = 'org.freedesktop.Hal.Device'
HAL_MGR_STR = 'org.freedesktop.Hal.Manager'

HAL_MGR_NS_STR = '/org/freedesktop/Hal/Manager'

class NoDeviceFoundError(Exception):
    def __str__(self):
        return 'No suitable PhidgetRFID device was found'
