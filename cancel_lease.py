#!/bin/python
from LunesPy import address as lp

myAddress = lp.Address(privateKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxx')
nodeAddress = lp.Address('37mCm11kpfQWiYaJuPJJG65PhgyhCQtqLxL')


lieaseId = myAddress.lease(nodeAddress, 4000000000000)
#myAddress.leaseCancel('GbSEKeXUTa85xHQRm9ZzHuHq493pCwtY9zrbHWf4b27D')
