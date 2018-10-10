import requests

REF_NODE = "https://lunesnode.lunes.io"
MY_NODE = "htts://api.lunes.in"

def getSig(node, block):
    req = requests.get(node + '/blocks/' + block).json()
    return req['signature'], req['height']

def findFork(first, last):
    print("..searching fork (%d) " % last)
    mySig0 = getSig(MY_NODE, "at/%d" % (last - 1))
    refSig0 = getSig(REF_NODE, "at/%d" % (last - 1))
    mySig1 = getSig(MY_NODE, "at/%d" % last)
    refSig1 = getSig(REF_NODE, "at/%d" % last)
    if mySig0==refSig0 and mySig1!=refSig1:
        return last
    if mySig0==refSig0 and mySig1==refSig1:
        return findFork(last, last + round(abs(last -first) / 2))
    if mySig0!=refSig0 and mySig1!=refSig1:
        return findFork(last, last - round(abs(last -first) / 2))

mySig, myHeight = getSig(MY_NODE, "last")
refSig, refHeight = getSig(REF_NODE, "last")
if mySig==refSig and myHeight==refHeight:
    print("NODE OK - SYNCED")
elif myHeight < refHeight and getSig(MY_NODE, "at/%d" % myHeight)[0] == getSig(REF_NODE, "at/%d" % myHeight)[0]:
    print("NODE NOT SYNCED")
else:
    print("NODE FORKED AT %d" % findFork(0, min(myHeight, refHeight)))
