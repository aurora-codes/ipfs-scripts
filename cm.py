import os; import json; import sys; cli = sys.argv # CyTube Custom Content Metadata
if len(cli) != 3: print 'python custom.py video.mp4 subtitle.en.vtt'; print 'run script in directory w/ files & example.json'; exit()
if len(cli) == 3: vid = cli[1]; sub = cli[2]
tit = vid.replace('.mp4', ''); cids = []; ded = 0; hit = 0
vidcid = os.popen("ipfs add --offline -qn '"+vid+"'").read().split('\n'); vidcid.remove(''); mp4cid = vidcid[0]
subcid = os.popen("ipfs add --offline -qn '"+sub+"'").read().split('\n'); subcid.remove(''); vttcid = subcid[0]
print mp4cid+' '+vid+'\n'+vttcid+' '+sub; cids.append(mp4cid); cids.append(vttcid)
for cid in cids:
    cidls = os.popen("ipfs ls --offline "+cid).read().split('\n'); cidls.remove('')
    if len(cidls) == 0:
        cidcat = os.popen("ipfs cat --offline "+cid).read().split('\n'); cidcat.remove('')
        if len(cidcat) == 0: ded = 1
        elif len(cidcat) != 0: continue; hit = 1
        if hit == 0: ded = 1
    elif len(cidls) != 0: continue
    if ded == 1: print cid+' not found in local ipfs repo datastore: ipfs add -w filename ?'
if ded == 1: exit()
mp4cid1 = os.popen('ipfs cid base32 '+mp4cid).read().replace('\n', ''); print mp4cid1+' '+vid
vttcid1 = os.popen('ipfs cid base32 '+vttcid).read().replace('\n', ''); print vttcid1+' '+sub
mp4url = 'https://'+mp4cid1+'.ipfs.dweb.link/'; vtturl = 'https://'+vttcid1+'.ipfs.dweb.link/'
dur = os.popen('ffprobe -i "'+vid+'" -show_entries format=duration -v quiet -of csv="p=0"'); sec = float(dur.read().replace('\n', ''))
res = os.popen('ffprobe -i "'+vid+'" -v quiet -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1')
qua = res.read().split('\n'); qua.pop(2); hei = int(qua[1])
if 720 < hei <= 1080: qua = 1080
if 540 < hei <= 720: qua = 720
if 480 < hei <= 540: qua = 540
if 360 < hei <= 480: qua = 480
if 240 < hei <= 360: qua = 360
jsn = open('example.json', 'r') # github.com/calzoneman/sync/blob/3.0/docs/custom-media.md#example
cjs = json.load(jsn); jsn.close(); cjs.pop('thumbnail', None); cjs.pop('bitrate', None);
cjs['title'] = tit; cjs['duration'] = round(sec, 3)
cjs['sources'] = [{u'url': mp4url, u'quality': qua, u'contentType': u'video/mp4'}]
cjs['textTracks'] = [{u'url': vtturl, u'default': True, u'contentType': u'text/vtt', u'name': u'English'}]
print json.dumps(cjs, ensure_ascii=False, indent = 4, sort_keys=True); file = tit.lower().replace('!', '')+'.json'
custom = open(file, 'w'); json.dump(cjs, custom); custom.close(); print '\nipfs add -w "'+file+'"\n'
