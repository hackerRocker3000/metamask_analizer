import requests
import json
import time

def checkTransactions(address):
    if json.loads(requests.get('https://api.etherscan.io/api', params={
        'module': 'account',
        'action': 'txlist',
        'page': 1,
        'offset': 1,
        'address': address,
        'apikey': 'ZWJJJFZHUV4XT8IFT9N5CGF3A8CHXR5BKH'
    }).text)['message'] == 'No transactions found':
        return False
    return True

def checkBalance(address):
    return round(int(json.loads(requests.get('https://api.etherscan.io/api', params={
        'module': 'account',
        'action': 'balance',
        'tag': 'latest',
        'address': address,
        'apikey': 'ZWJJJFZHUV4XT8IFT9N5CGF3A8CHXR5BKH'
    }).text)['result']) * 10E-19, 8)


with open('result.txt', errors='ignore') as f:
    content = json.loads(f.read())
    f.close()
addressesWithMoney = []

for log in content:
    for address in content[log]['addresses']:
        if checkTransactions(address):
            addressesWithMoney.append({
                'address': address,
                'balance': checkBalance(address)
            })
        time.sleep(0.55)

prettyResult = json.dumps(addressesWithMoney, indent=2)
print(prettyResult)
with open('addressesWithMoney.txt', 'w') as f:
    f.write(prettyResult)
    f.close()

