#!/usr/bin/python2

import requests
import math
import json
import sys

node = 'http://lunesnode.lunes.io'
nblocks = 1500 # roughly one week
total_balance = 0
total_fees = 0
generators = []
unique_generators = []
last = requests.get(node + '/blocks/height').json()['height']

blacklist = []
data = {'node': []}
trusted_json_path = './trust.json'
if len(sys.argv) > 1:
    trusted_json_path = sys.argv[1]

def get_txt(domain):
    try:
        txt_data = json.loads(json.dumps(requests.get(
            'https://dns-api.org/TXT/' + domain).json()))
        txt_value = txt_data[0]['value']
        if txt_value.find('NODE_ADDRESS') != -1:
            txt_address = txt_value.split('=')[1]
            return txt_address
    except:
        return ''


def get_address(url):
    try:
        response = requests.get(url)
        if not response.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(response)

        return response.text
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        return "Error: {}".format(e)


for n in range(0, int(math.ceil(nblocks / 100.0))):
    for block in requests.get('%s/blocks/seq/%d/%d' % (node, last - nblocks + n * 100, min(last, last - nblocks + (n + 1) * 100 - 1))).json():
        generators.append(
            (str(block['generator']), float(block['fee']) / 100000000))

for generator in set([x[0] for x in generators]):
    fees = sum(g[1] for g in filter(lambda x: x[0] == generator, generators))
    count = sum(1 for g in filter(lambda x: x[0] == generator, generators))
    total_fees += fees
    generator_balance = float(requests.get(
        node + '/consensus/generatingbalance/' + generator).json()['balance']) / 100000000
    unique_generators.append((generator, generator_balance, count, fees))
    total_balance += generator_balance

for i, generator in enumerate(sorted(unique_generators, key=lambda x: -x[1])):
    aliases = requests.get(
        node + '/addresses/alias/by-address/' + generator[0]).json()
    for alias in aliases:
        domain = alias.split(':')[2]
        if domain not in blacklist:
            address_txt_url = 'https://' + domain + '/address.txt'
            node_address = get_address(address_txt_url)
            dns_address = get_txt(domain)
            if str(generator[0]) in (node_address, dns_address):
                data['node'].append({'domain': domain, 'address': str(generator[0]), 'balance': str(generator[1]), 'share': str(
                    generator[1] / total_balance * 100), 'blocks': str(generator[2]), 'fees': str(generator[3])})


with open(trusted_json_path, 'w') as outfile:
    json.dump(data, outfile)
