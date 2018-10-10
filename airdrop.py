#!/usr/bin/python
import LunesPy as lp
import argparse
import os.path

pw.setNode("https://lunesnode.lunes.io")

parser = argparse.ArgumentParser(description='Lunes Airdrop Tool')
parser.add_argument('pkey', type=str, help='private key of the sending address')
parser.add_argument('asset', type=str, help='ID of the asset to distribute')
parser.add_argument('amount', type=str, help='amount of asset to send to each recipient')
parser.add_argument('file', type=str, help='file with the list of recipients')

args = parser.parse_args()
amount = int(args.amount)
filename = args.file

if amount <= 0:
    print("Amount must be > 0")
elif not os.path.exists(filename):
    print("File not found!")
else:
    myAddress = lp.Address(privateKey = args.pkey)
    myToken = lp.Asset(args.asset)
    with open(filename) as f:
        lines = f.readlines()
    for address in lines:
        info = myAddress.sendAsset(lp.Address(address.strip()), myToken, amount)
        print info
        myAddress.sendAsset(lp.Address(address.strip()), myToken, amount)
	print myAddress.sendAsset
        print("Sent %d %s to %s" % (amount, myToken.assetId, address.strip()))
