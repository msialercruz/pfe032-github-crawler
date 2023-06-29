#!/bin/sh

# RENAME ALL NOTEBOOKS ENDING WITH NUMBER EXT
find . -type f -regex '.*\.[0-9]*' -regextype grep -not -path './notebooks/*/*' | while read f; do
	newname="$(echo "$f" | sed -r 's/(.*)\.ipynb\.([0-9]*)/\1.\2.ipynb/g')"
	mv "$f" "$newname"
done

# FIND NOTEBOOKS THAT ARE INVALID, HAVE NO CODE OR USE UNSUPPORTED LIBS
mkdir -p notebooks/invalid
mkdir -p notebooks/no-code
mkdir -p notebooks/lib-unsupported
find . -type f -name *.ipynb -not -path './notebooks/*/*' | while read f; do
	# invalid notebook (not json format)
	if ! jq '.' "$f" > /dev/null 2>&1; then
		echo "invalid: $f"
		mv "$f" notebooks/invalid/
		continue
	fi
	# notebook having no code
	if ! jq '.cells | map(.cell_type) | map(select(. == "code"))' "$f" > /dev/null 2>&1; then
		echo "no code: $f"
		mv "$f" notebooks/no-code/
		continue
	fi
	# notebooks using unsupported libraries
	if [ $(grep "import tensorflow" "$f" | wc -l) -gt 0 ]; then
		echo "unsupported lib: $f"
		mv "$f" notebooks/lib-unsupported/
		continue
	fi
done

# ORGANIZE NOTEBOOKS BY SIZE
mkdir -p notebooks/organized/sm
mkdir -p notebooks/organized/md
mkdir -p notebooks/organized/lg
# move small notebooks (<= 10KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -10240c -exec mv "{}" notebooks/organized/sm \;
# move small notebooks (<= 100KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -102400c -exec mv "{}" notebooks/organized/md \;
# move small notebooks (<= 1M)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -1048576c -exec mv "{}" notebooks/organized/lg \;
