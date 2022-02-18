import os; import requests # pip install requests # cid = 'QmW2WQi7j6c7UgJTarActp7tDNikE4B2qXtFCfLPdsgaTQ/cat.jpg'
print("input ipfs CIDv0 for gateway censor status ( cid | cid/file.name )"); cid = input()
if "/" in cid: path = cid.split("/"); fsl = "/"; cid = path[0]; path.pop(0); path = fsl.join(path)
else: path = ''
# cid = 'QmcvyefkqQX3PpjpY5L8B2yMd47XrVwAipr6cxUt2zvYU8/The.Big.Lebowski.mp4' # 410 Gone Error
# https://github.com/ipfs/infra/blob/master/ipfs/gateway/denylist.conf
url = 'http://localhost:8080/ipfs/'+cid+'/'+path; base = os.popen('ipfs cid base32 '+str(cid)); cid1 = base.read().replace('\n', '')
print('    checking localhost node'); lurl = 'http://'+cid1+'.ipfs.localhost:8080/'+path # default port 8080
print(url); print(lurl); ipfs = requests.get(lurl); lsc = ipfs.status_code; err = 0
if lsc == 200: print('    localhost CID OK ['+str(lsc)+']')
elif lsc != 200: print('    localhost CID ERROR ['+str(lsc)+']')
print('    checking for active public gateways'); ipfg = os.popen('./ipfg all'); # github.com/gingerhot/ipfg
sub = ['dweb.link', 'cf-ipfs.com', 'jacl.tech', 'infura-ipfs.io'] # subdomain gateways
ded = ['ipns.co', 'ipfs.ink', 'hardbin.com', 'ipfs.jbb.one', 'robotizing.net', 'ipfs.eternum.io', 'ipfs.azurewebsites.net', 'ipfs.k1ic.com']
gate = ipfg.read().replace('\n', '').split(': https://'); gate.pop(0); cnt = len(gate); print('    '+str(cnt)+' public gateways online')
print('    cf-ipfs.com [video streaming is not allowed]'); print('    cloudflare-ipfs.com [video streaming is not allowed]')
for x in range(len(gate)):
    tmp = gate[x].split(':hash'); node = tmp[0].replace('/ipfs/', ''); url = 'https://'+node+'/ipfs/'+cid+'/'+path
    for n in range(len(ded)):
        if node.count(ded[n]) > 0: err = 1; break
    if err == 0: dom = requests.get('https://'+node+'/ipfs/'); dsc = dom.status_code # print('+node+'['+str(dsc)+']'
    if err == 1: err = 0; cnt = cnt-1; continue
    if dsc >= 400:
        for n in range(len(sub)):
            if node.count(sub[n]) > 0: print(url); url = 'https://'+cid1+'.ipfs.'+node+'/'+path; break
        get = requests.get(url); sc = get.status_code
        if sc == 200: print(url),; print(' '+node+' CID OK ['+str(sc)+']')
        if sc == 410: print('    '+node+' CID CENSORED ['+str(sc)+']'); cnt = cnt-1
        if sc == 451: print('    '+node+' CID CENSORED ['+str(sc)+']'); cnt = cnt-1
        if sc == 404: print('    '+node+' CID NOT FOUND ['+str(sc)+']'); cnt = cnt-1
        if sc == 504: print('    '+node+' CID TIMEOUT ['+str(sc)+']'); cnt = cnt-1
print('    '+str(cnt)+' public gateways passed HTTP error check')
