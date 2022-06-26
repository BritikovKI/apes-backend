from datetime import datetime
from django.http.response import JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponse
import json
from pymongo import MongoClient
from web3 import Web3
from web3.middleware import geth_poa_middleware

rate = 1
token = "0xC5aE96eF99832E0Cb8409877F47FbFed97004B79"
multisig = "0xEFc3a819695932394D89b8AF6f49e0D89EDf9A40"
sender_pk = "ff5886c7e52052fc95e4bd6956b1e420d10693e62fbe506d61fa25b152093d54"
erc20 = "0xB098cfF6a909c0DAF6B732C4c7B1B1414F4aba5d"
tokenABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous": False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"newGnosisAddress","type":"address"}],"name":"GnosisWalletSet","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address[]","name":"wallets","type":"address[]"}],"name":"addToWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"changeStatePreSale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"changeStatePublicSale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"claimYungApe","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"claimYungApeMultiple","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"isClaimed","outputs":[{"internalType":"bool","name":"tokenExists","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"numberOfTokens","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"mintLimitPerAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintLimitPerTx","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"mintedByAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"preSaleState","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"publicSaleState","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"reserve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseUri","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_newAddress","type":"address"}],"name":"setGnosisSafeWallet","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"uint256","name":"startId","type":"uint256"},{"internalType":"uint256","name":"endId","type":"uint256"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"whitelistedIdsOfWallet","outputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]
erc20ABI = [
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_benefactor",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "amount",
          "type": "address"
        }
      ],
      "name": "AddMinter",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "Fee",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "amount",
          "type": "address"
        }
      ],
      "name": "NewBenefactor",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "previousOwner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        }
      ],
      "name": "OwnershipTransferred",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "amount",
          "type": "address"
        }
      ],
      "name": "RemoveMinter",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Unwhitelisted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Whitelisted",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "addMinter",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        }
      ],
      "name": "allowance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "burn",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_benefactor",
          "type": "address"
        }
      ],
      "name": "changeBenefactor",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "decimals",
      "outputs": [
        {
          "internalType": "uint8",
          "name": "",
          "type": "uint8"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "subtractedValue",
          "type": "uint256"
        }
      ],
      "name": "decreaseAllowance",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "addedValue",
          "type": "uint256"
        }
      ],
      "name": "increaseAllowance",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "mint",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "minters",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "noTaxWhitelist",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "removeFromWhitelist",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "removeMinter",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "renounceOwnership",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transfer",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        }
      ],
      "name": "transferOwnership",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "whitelist",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ];

def nfts(request):
    address = request.GET['address']
    db = MongoClient('mongodb://localhost:27017/')  # First define the database name
    dbname = db['apes']
    stakes_collection = dbname["stakes"]
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/4c9049736af84c46ad0972910df0476a"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    apes = w3.eth.contract(address=token, abi=tokenABI)
    tokens = apes.functions.tokensOfOwner(address, 697, 6969).call()
    print(tokens)
    nfts = []
    for nft in tokens:
      if nft != 0:
        stake = stakes_collection.find_one(filter={"address": address, "nft": nft})
        taxRate, rewards = 0,0
        if stake:
          rewards = rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 97,5 /100
          if (datetime.now() - stake['stake_time']).total_seconds() / 86400 > 120 :
            taxRate = 40
          else:
            taxRate = 5
        rarity = 1
        if nft > 3000:
          rarity = 3
        elif nft > 1000:
          rarity = 2
        dict = {
          "id": nft,
          "taxRate": taxRate,
          "tier": rarity,
          "rewards": rewards,
          "imgLink": "https://ipfs.io/ipfs/QmQ9yZVsQQrmhrwiw9fFZpcnNvdZNH62JECY8PVvC4s46G/" + str(nft) + ".png"
        }
        nfts.append(dict)
    return JsonResponse({"nfts": nfts})

def balance(request):
    address = request.GET['address']
    db = MongoClient('mongodb://localhost:27017/')  # First define the database name
    dbname = db['apes']
    stakes_collection = dbname["stakes"]
    users_collection = dbname["users"]
    w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4c9049736af84c46ad0972910df0476a"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    token = w3.eth.contract(address=erc20, abi=erc20ABI)

    stakes = stakes_collection.find(filter={"address": address})
    user = users_collection.find_one(filter={"address": address})
    users = users_collection.count_documents(filter={})
    num_stakes = stakes_collection.count_documents(filter={"address": address})
    print(users)
    balance = 0
    transfer_filter = token.events.Transfer.createFilter(fromBlock="0x00")
    events = transfer_filter.get_all_entries()
    additional_incentive = 0
    for transfer in events:
      print(transfer)
      additional_incentive += (transfer["args"]["value"] / 100 * 5) / users
    print(additional_incentive)
    if num_stakes == 0:
      resp = JsonResponse({"balance": 0, "tax": 0})
      return resp
    for stake in stakes:
        print(datetime.now() - stake['last_withdraw'])
        stake_time = (datetime.now() - stake['stake_time']).total_seconds() / 86400
        balance += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400
    users_collection.update_one({"address": address},{ "$set":{"balance": balance, "tax": additional_incentive} } )
    print(balance, additional_incentive)
    resp = JsonResponse({"balance": balance, "tax": additional_incentive})
    # resp["Access-"]
    return resp


def withdrawToken(request):
    address = request.GET['address']
    id = request.GET['token']
    db = MongoClient('mongodb://localhost:27017/')  # First define the database name
    w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4c9049736af84c46ad0972910df0476a"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    token = w3.eth.contract(address=erc20, abi=erc20ABI)
    dbname = db['apes']
    stakes_collection = dbname["stakes"]
    users_collection = dbname["users"]

    stake = stakes_collection.find_one(filter={"nft":id, "address": address})
    user = users_collection.find_one(filter={"address": address})
    balance = 0
    tax = 0
    print(datetime.now() - stake['last_withdraw'])
    stake_time =  (datetime.now() - stake['stake_time']).total_seconds() / 86400
    if stake_time > 40:
        balance += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 97,5 /100
        tax += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 2,5 / 100
    else:
        balance += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 70 /100
        tax += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 30 / 100

    if (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 1:
      if user["withdrawn"] + balance > 650:
        unfeed = (650 - user["withdrawn"]) if (650 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 2:
      if user["withdrawn"] + balance > 1000:
        unfeed = (1000 - user["withdrawn"]) if (1000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 3:
      if user["withdrawn"] + balance > 2000:
        unfeed = (2000 - user["withdrawn"]) if (2000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 5:
      if user["withdrawn"] + balance > 3000:
        unfeed = (3000 - user["withdrawn"]) if (3000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 7:
      if user["withdrawn"] + balance > 5000:
        unfeed = (5000 - user["withdrawn"]) if (5000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 9:
      if user["withdrawn"] + balance > 7500:
        unfeed = (7500 - user["withdrawn"]) if (7500 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 10:
      if user["withdrawn"] + balance > 10000:
        unfeed = (10000 - user["withdrawn"]) if (10000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 11:
      if user["withdrawn"] + balance > 15000:
        unfeed = (15000 - user["withdrawn"]) if (15000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    elif (datetime.now() - user["initial_stake"]).total_seconds() / 86400 / 30 < 12:
      if user["withdrawn"] + balance > 20000:
        unfeed = (20000 - user["withdrawn"]) if (20000 - user["withdrawn"]) > 0 else 0
        balance = unfeed + (balance - unfeed) * 65 / 100
    account = w3.eth.account.privateKeyToAccount(sender_pk)
    w3.eth.default_account = account.address
    print(address)
    print(w3.eth.default_account)
    tx1 = token.functions.mint(address, int(balance*1000)).\
      buildTransaction({'nonce': w3.eth.getTransactionCount(w3.eth.default_account)})
    signed_tx1 = w3.eth.account.signTransaction(tx1, sender_pk)
    tx_sent1 = w3.eth.sendRawTransaction(signed_tx1.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_sent1)
    print(tx_receipt)
    tx2 = token.functions.mint(multisig, int(tax*1000)).\
      buildTransaction({'nonce': w3.eth.getTransactionCount(w3.eth.default_account)})
    signed_tx2 = w3.eth.account.signTransaction(tx2, sender_pk)
    tx_sent2 = w3.eth.sendRawTransaction(signed_tx2.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_sent2)
    print(tx_receipt)

    stakes_collection.update_many({"address": address},{ "$set":{"last_withdraw": datetime.now()} } )
    users_collection.update_one({"address": address},{ "$set":{"balance": 0,"fee": 0} } )
    return JsonResponse({"balance": balance, "tax": tax})


def withdraw(request):
  address = request.GET['address']
  db = MongoClient('mongodb://localhost:27017/')  # First define the database name
  w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4c9049736af84c46ad0972910df0476a"))
  w3.middleware_onion.inject(geth_poa_middleware, layer=0)
  token = w3.eth.contract(address=erc20, abi=erc20ABI)
  dbname = db['apes']
  stakes_collection = dbname["stakes"]
  users_collection = dbname["users"]

  stake = stakes_collection.findOne(filter={"address": address, "id": token})
  user = users_collection.find_one(filter={"address": address})
  balance = 0
  tax = 0
  print(datetime.now() - stake['last_withdraw'])
  stake_time = (datetime.now() - stake['stake_time']).total_seconds() / 86400
  if stake_time > 40:
    balance += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 97, 5 / 100
    tax += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 2, 5 / 100
  else:
    balance += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 70 / 100
    tax += rate * (datetime.now() - stake['last_withdraw']).total_seconds() / 86400 * 30 / 100


  if (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 1:
    if user["withdrawn"] + balance > 650:
      unfeed = (650 - user["withdrawn"]) if (650 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 2:
    if user["withdrawn"] + balance > 1000:
      unfeed = (1000 - user["withdrawn"]) if (1000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 3:
    if user["withdrawn"] + balance > 2000:
      unfeed = (2000 - user["withdrawn"]) if (2000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 5:
    if user["withdrawn"] + balance > 3000:
      unfeed = (3000 - user["withdrawn"]) if (3000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 7:
    if user["withdrawn"] + balance > 5000:
      unfeed = (5000 - user["withdrawn"]) if (5000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 9:
    if user["withdrawn"] + balance > 7500:
      unfeed = (7500 - user["withdrawn"]) if (7500 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 10:
    if user["withdrawn"] + balance > 10000:
      unfeed = (10000 - user["withdrawn"]) if (10000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 11:
    if user["withdrawn"] + balance > 15000:
      unfeed = (15000 - user["withdrawn"]) if (15000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100
  elif (datetime.now() - user["initial_stake"]).total_seconds()/86400/30 < 12:
    if user["withdrawn"] + balance > 20000:
      unfeed = (20000 - user["withdrawn"]) if (20000 - user["withdrawn"]) > 0 else 0
      balance = unfeed + (balance - unfeed)*65/100

  account = w3.eth.account.privateKeyToAccount(sender_pk)
  w3.eth.default_account = account.address
  print(address)
  print(w3.eth.default_account)
  tx1 = token.functions.mint(address, int(balance * 1000)). \
    buildTransaction({'nonce': w3.eth.getTransactionCount(w3.eth.default_account)})
  signed_tx1 = w3.eth.account.signTransaction(tx1, sender_pk)
  tx_sent1 = w3.eth.sendRawTransaction(signed_tx1.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_sent1)
  print(tx_receipt)
  tx2 = token.functions.mint(multisig, int(tax * 1000)). \
    buildTransaction({'nonce': w3.eth.getTransactionCount(w3.eth.default_account)})
  signed_tx2 = w3.eth.account.signTransaction(tx2, sender_pk)
  tx_sent2 = w3.eth.sendRawTransaction(signed_tx2.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_sent2)
  print(tx_receipt)



  stakes_collection.update_many({"address": address}, {"$set": {"last_withdraw": datetime.now()}})
  users_collection.update_one({"address": address}, {"$set": {"balance": 0, "fee": 0}})
  return JsonResponse({"balance": balance, "tax": tax})


@csrf_exempt
def stake(request):
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/4c9049736af84c46ad0972910df0476a"))
    apes = w3.eth.contract(address=token, abi=tokenABI)
    db = MongoClient('mongodb://localhost:27017/')# First define the database name
    dbname = db['apes']
    stakes_collection = dbname["stakes"]
    users_collection = dbname["users"]

    if request.method == "POST":
        message = json.loads(request.body)
        if not message["nft"]:
            return HttpResponseNotAllowed("Incorrect json request!")
        tokenIds = message["nft"]
        for nft in tokenIds:
            owner = apes.functions.ownerOf(nft).call()
            print(owner)
            stake = stakes_collection.find_one(filter={"nft": nft})
            user = users_collection.find_one(filter={"address": owner})
            if not user:
                user = {"address": owner,
                        "balance": 0,
                        "tax": 0,
                        "withdrawn": 0,
                        "latest_block": w3.eth.block_number,
                        "initial_stake": datetime.now()}
                users_collection.insert_one(user)
            if not stake:
                stake = { "nft": nft,
                          "last_withdraw": datetime.now(),
                          "address": owner,
                          "stake_time": datetime.now()}
                stakes_collection.insert_one(stake)
        return HttpResponse("Success!")
    return HttpResponseNotFound("Only POST request is supported!")