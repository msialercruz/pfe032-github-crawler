#!/bin/sh

# RENAME ALL NOTEBOOKS ENDING WITH NUMBER EXT
find . -type f -regex '.*\.[0-9]*' -regextype grep -not -path './notebooks/*/*' | while read f; do
	newname="$(echo "$f" | sed -r 's/(.*)\.ipynb\.([0-9]*)/\1.\2.ipynb/g')"
	mv "$f" "$newname"
done

# FIND NOTEBOOKS THAT ARE INVALID, HAVE NO CODE OR USE UNSUPPORTED LIBS
mkdir -p notebooks/invalid/not-json
mkdir -p notebooks/invalid/no-code
mkdir -p notebooks/invalid/lib-unsupported
find . -type f -name *.ipynb -not -path './notebooks/*/*' | while read f; do
	# notebook with not json format
	if ! jq '.' "$f" > /dev/null 2>&1; then
		echo "invalid: $f"
		mv "$f" notebooks/invalid/not-json
		continue
	fi
	# notebook having no code
	if ! jq '.cells | map(.cell_type) | map(select(. == "code"))' "$f" > /dev/null 2>&1; then
		echo "no code: $f"
		mv "$f" notebooks/invalid/no-code/
		continue
	fi
	# notebooks using unsupported libraries
	if [ $(grep "import tensorflow" "$f" | wc -l) -gt 0 ]; then
		echo "unsupported lib: $f"
		mv "$f" notebooks/invalid/lib-unsupported/
		continue
	fi
done
