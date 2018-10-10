import pandas as pd
import requests
import math

node = 'https://lunesnode.lunes.io'

txfields = {
			'type' 				: '',
			'id' 				: '',
			'sender'			: '',
			'senderPublicKey'	: '',
			'recipient'			: '',
			'amount'			: '',
			'assetId'			: '',
			'name'				: '',
			'description'		: '',
			'quantity'			: '',
			'decimals'			: '',
			'reissuable'		: '',
			'fee'				: '',
			'feeAsset'			: '',
			'timestamp'			: '',
			'attachment'		: '',
			'signature'			: ''}

tmp=[]
last = requests.get(node + '/blocks/height').json()['height']

df = pd.DataFrame(columns = txfields.keys())

for n in range(0, int(math.ceil(last/100.0))):
    for block in requests.get(node + '/blocks/seq/%d/%d' % (node, 1 + n * 100, min(last, (n + 1) * 100))).json():
        txs = block['transactions']
        for tx in txs:
            for key in txfields.keys():
                txfields[key] = ''
                try:
                    txfields[key] = tx[key]
                except:
                    pass
            tmp.append(txfields.values())
df = df.append(pd.DataFrame(tmp, columns = txfields.keys()), ignore_index=True)
del tmp

print
print("       %12d Dataframe size (bytes)" % (df.values.nbytes + df.index.nbytes + df.columns.nbytes))
print("       %12d Blocks" % last)
print("       %12d Total TXs" % len(df))
print("       %12d Unique addresses" % len(df.recipient.unique()))
print("       %12d Assets" % len(df[df['type']==3]))
print(" %18.8f Total fees" % (sum(df.fee) / 100000000))
print
