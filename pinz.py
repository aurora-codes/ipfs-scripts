import os; import bitmath # pip install bitmath
rpin = os.popen('ipfs pin ls --type=recursive').read().replace(' recursive', '').split('\n'); rpin.remove('')
print '\n'+str(len(rpin))+' recursive pins found\n'; sum = 0
for cid in rpin:
    siz = os.popen('ipfs files stat --size /ipfs/'+cid).read().split('\n')
    byt = int(siz[0]); sum = int(sum+byt); print cid,
    bit = bitmath.Byte(bytes=byt).best_prefix(); unt = str(bit).split(' ')
    if 'Byte' in unt[1]: print str(bit.format("{value:.0f} {unit}")),
    else: print str(bit.format("{value:.2f} {unit}")),
    pins = os.popen('ipfs ls --size '+cid).read().split('\n'); pins.remove(''); obs = len(pins)
    if obs == 1: print str(obs)+' object'
    if obs > 1: print str(obs)+' objects'
    for pin in pins:
        oid = pin.split(' '); cid = oid[0]; oid.pop(0); oid.pop(0); obj = ' '.join(oid).lstrip()
        siz = os.popen('ipfs files stat --size /ipfs/'+cid).read().split('\n')
        byt = int(siz[0]); print cid,
        bit = bitmath.Byte(bytes=byt).best_prefix(); unt = str(bit).split(' ')
        if 'Byte' in unt[1]: print str(bit.format("{value:.0f} {unit}"))+' '+obj
        else: print str(bit.format("{value:.2f} {unit}"))+' '+obj
sbit = bitmath.Byte(bytes=sum).best_prefix().format("{value:.2f} {unit}")
rep = os.popen('ipfs repo stat -s').read().split('\n'); rsiz = int(rep[0].replace('RepoSize:','').lstrip())
pset = bitmath.Byte(bytes=rsiz-sum).best_prefix().format("{value:.2f} {unit}")
print '\n                          recursive pins total '+str(sbit)
print '                                    pinset est '+str(pset)
os.system('ipfs repo stat -s -H; echo; df -h ~; echo')
