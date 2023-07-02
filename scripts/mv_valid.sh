#!/bin/sh

# ORGANIZE NOTEBOOKS BY SIZE
mkdir -p notebooks/valid/sm
mkdir -p notebooks/valid/md
mkdir -p notebooks/valid/lg
# move small notebooks (<= 10KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -10240c | while read f; do
	newname="notebooks/valid/sm/$(basename -- "$f")"
	if mv "$f" "$newname"; then
		python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
	fi
done
# move small notebooks (<= 100KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -102400c | while read f; do
	newname="notebooks/valid/md/$(basename -- "$f")"
	if mv "$f" "$newname"; then
		python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
	fi
done
# move small notebooks (<= 1M)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -1048576c | while read f; do
	newname="notebooks/valid/lg/$(basename -- "$f")"
	if mv "$f" "$newname"; then
		python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
	fi
done
