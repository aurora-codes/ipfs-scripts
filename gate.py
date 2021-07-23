import os; pnct = os.popen('ipfs pin ls --type=recursive | wc -l'); print("recursive pins: "+pnct.read())
pinz = os.popen('ipfs pin ls --type=recursive'); hash = pinz.read(); tmp = hash.replace('\n', ' ')
hazh = tmp.replace(' recursive', ''); cidz = hazh.split(' '); cidz.remove('')
namz = os.popen('ipfs ls '+str(hazh)); print(namz.read())
for x in range(len(cidz)): print str('https://ipfs.io/ipfs/'+cidz[x]+'/')
print
for x in range(len(cidz)): print str('https://gateway.ipfs.io/ipfs/'+cidz[x]+'/')
os.system('echo; ipfs repo stat -s -H; echo; df -h ~; echo')
