import os; print "input download url:",
ari = "aria2c -j 16 -x 16 --split=16 "
url = raw_input(); aria = ari+url; os.system(aria)
