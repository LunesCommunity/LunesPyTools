#!/usr/bin/python
import LunesPy

LunesPy.setNode(node = 'https://lunesnode.lunes.io')
myAddress = LunesPy.Address(privateKey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
myAddress.createAlias('node_do_alias')
