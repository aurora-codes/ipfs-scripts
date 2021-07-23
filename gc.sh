ipfs repo stat -H
echo "running ipfs cache garbage collection."
ipfs repo gc --quiet > /dev/null
ipfs repo stat -H
