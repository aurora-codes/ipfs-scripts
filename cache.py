import os; import sys; cli = sys.argv
ari = "aria2c -q -d /dev -o null --allow-overwrite=true --file-allocation=none -j 16 -x 16 --split=16 "
if len(cli) == 1: print "input ipfs data CIDv0 | python script.py cid0",; cid0 = raw_input(); cli = [cid0]
if len(cli) > 1: cli.pop(0);
def cache(cid):
    cid0 = cid; print cid0; base = os.popen('ipfs cid base32 '+str(cid0)); cid1 = base.read().replace('\n', '')
    print cid1; dweb = ari+'https://'+cid1+'.ipfs.dweb.link'
    print 'caching dweb.link'; os.system(dweb); print 'aria2c caching complete\n'
for cidz in cli:
    cid0 = cidz; cache(cid0); wrap = os.popen('ipfs ls '+str(cid0))
    ls = wrap.read().split('\n'); ls.remove(''); lsc = len(ls)
    if lsc > 0:
        print cid0+' '+str(lsc)+' objects\n'
        for obj in ls:
            pin = obj.split(' '); cache(pin[0])
    if lsc == 0: continue
print 'all downloads to /dev/null complete\n'
