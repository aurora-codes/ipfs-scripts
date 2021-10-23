import os; import json; import sys; cli = sys.argv # CyTube Custom Content Metadata
if len(cli) != 3: print 'python custom.py <vidCID> <subCID>'; print 'run script in directory w/ example.json'; exit()
if len(cli) == 3: vid = cli[1]; sub = cli[2]
cids = []; ded = 0; hit = 0; tit = raw_input('input title: '); mp4cid = vid; vttcid = sub; cids.append(mp4cid); cids.append(vttcid)
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
mp4cid1 = os.popen('ipfs cid base32 '+mp4cid).read().replace('\n', '');
vttcid1 = os.popen('ipfs cid base32 '+vttcid).read().replace('\n', '');
mp4url = 'https://'+mp4cid1+'.ipfs.dweb.link/'; vtturl = 'https://'+vttcid1+'.ipfs.dweb.link/'; gat = 'http://127.0.0.1:8080/ipfs/';
dur = os.popen('ffprobe -i '+gat+vid+' -v quiet -show_entries format=duration -of csv="p=0"'); sec = float(dur.read().replace('\n', ''))
res = os.popen('ffprobe -i '+gat+vid+' -v quiet -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1')
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
ari = "aria2c -d /dev -o null --allow-overwrite=true --file-allocation=none -j 16 -x 16 --split=16 "
ans = raw_input("cache urls: y / n ? ")
if ans == 'y':
    url = vtturl; aria = ari+url; os.system(aria); url = mp4url; aria = ari+url; os.system(aria)
elif ans == 'n': exit()
else: exit()
