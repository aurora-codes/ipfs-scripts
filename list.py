import os; pnct = os.popen('ipfs pin ls --type=recursive | wc -l'); print('\nrecursive pins: '+pnct.read())
pinz = os.popen('ipfs pin ls --type=recursive'); hash = pinz.read(); tmp = hash.replace('\n', ' ')
hazh = tmp.replace(' recursive', ''); namz = os.popen('ipfs ls '+str(hazh)); print(namz.read())
os.system('ipfs repo stat -s -H; echo; df -h ~; echo')
