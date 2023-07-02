#!/bin/sh

# RENAME ALL NOTEBOOKS ENDING WITH NUMBER EXT
find . -type f -regex '.*\.[0-9]*' -regextype grep -not -path './notebooks/*/*' | while read f; do
	newname="$(echo "$f" | sed -r 's/(.*)\.ipynb\.([0-9]*)/\1.\2.ipynb/g')"
	if mv "$f" "$newname"; then
		python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
	fi
done

# FIND NOTEBOOKS THAT ARE INVALID, HAVE NO CODE OR USE UNSUPPORTED LIBS
mkdir -p notebooks/invalid/not-json
mkdir -p notebooks/invalid/no-code
mkdir -p notebooks/invalid/lib-unsupported
find . -type f -name *.ipynb -not -path './notebooks/*/*' | while read f; do
	# notebook with not json format
	if ! jq '.' "$f" > /dev/null 2>&1; then
		echo "invalid: $f"
		newname="notebooks/invalid/not-json/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
		continue
	fi
	# notebook having no code
	if ! jq '.cells | map(.cell_type) | map(select(. == "code"))' "$f" > /dev/null 2>&1; then
		echo "no code: $f"
		newname="notebooks/invalid/no-code/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
		continue
	fi
	# notebooks using unsupported libraries
	if [ $(grep "import tensorflow" "$f" | wc -l) -gt 0 ]; then
		echo "unsupported lib: $f"
		newname="notebooks/invalid/lib-unsupported/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
		continue
	fi
done
