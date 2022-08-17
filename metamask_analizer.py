import json
from os import walk

resultsArr = {}
for (dirPath, dirNames, filenames) in walk('metamaskLogs'):
    for filename in filenames:
        with open(dirPath + '/' + filename, errors='ignore') as f:
            content = f.read()
            f.close()

        addressArr = []
        cachePosition = 0
        while True:
            cachePosition = content.find("cachedBalances", cachePosition)
            if cachePosition == -1:
                break
            cachePosition += 16
            quotesPosition = content.find("}}", cachePosition)
            addressesJsonWrap = content[cachePosition:quotesPosition] + '}}'

            for addressesWrap in json.loads(addressesJsonWrap).values():
                for address in addressesWrap:
                    addressArr.append(address)
            cachePosition += 1

        addressArr = list(set(addressArr))

        hashStartPosition = content.find("KeyringController") + 29
        hashEndPosition = content.find("MetaMetricsController", hashStartPosition) - 4
        hashRaw = content[hashStartPosition:hashEndPosition]
        hashObj = json.loads(hashRaw.replace('\\', ''))
        if 'salt' not in hashObj or 'iv' not in hashObj or 'data' not in hashObj:
            print("! Invalid hashObj format ...")
            exit(1)
        metamask = '$metamask$' + hashObj['salt'] + '$' + hashObj['iv'] + '$' + hashObj['data']

        resultsArr[filename] = {
            'addresses': addressArr,
            'metamask': metamask
        }

prettyResult = json.dumps(resultsArr, indent=2)
print(prettyResult)
with open('result.txt', 'w') as f:
    f.write(prettyResult)

