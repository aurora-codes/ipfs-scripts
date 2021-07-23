import os; print "input ipfs gateway url:",
ari = "aria2c -d /dev -o null --allow-overwrite=true --file-allocation=none -j 16 -x 16 --split=16 "
url = raw_input(); aria = ari+url; os.system(aria)
