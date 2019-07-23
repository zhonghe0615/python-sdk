'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/FISCO-BCOS)
  bcosliteclientpy is free software: you can redistribute it and/or modify it under the terms of the MIT License as published by the Free Software Foundation
  This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
  Thanks for authors and contributors of eth-abi，eth-account，eth-hash，eth-keys，eth-typing，eth-utils，rlp, eth-rlp , hexbytes ...and relative projects
  @author: kentzhang
  @date: 2019-06
'''
from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser
from subprocess import *
from pathlib import Path

client = BcosClient()
#info = client.init()
print(client.getinfo())

#使用java tool生成 .abi / .bin 文件
web3j_command = 'java -jar sol_tools/fboost.jar'
os.system(web3j_command)

contract_dir = "../contracts"
abi_file  = contract_dir + "/abi/HelloFBoost.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

#部署合约
print("\n>>Deploy:---------------------------------------------------------------------")
with open(contract_dir + "/bin/HelloFBoost.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()
result = client.deploy(contract_bin)
print("deploy",result)
print("new address : ",result["contractAddress"])
contract_name =  os.path.splitext(os.path.basename(abi_file))[0]
memo = "tx:"+result["transactionHash"]
#把部署结果存入文件备查
from client.contractnote import ContractNote
ContractNote.save_address(contract_name, result["contractAddress"], int(result["blockNumber"], 16), memo)
print("\n>>Deployment complete :---------------------------------------------------------------------")

# #发送交易，调用一个改写数据的接口
to_address = result['contractAddress'] #use new deploy address

#调用一下call，获取数据
print("\n>>Call:------------------------------------------------------------------------")
res = client.call(to_address,contract_abi,"get")
print("call get result:",res)




