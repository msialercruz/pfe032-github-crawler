#!/bin/sh

# CONVERT ALL NOTEBOOKS TO PYTHON
mkdir -p notebooks/valid/sm/py
mkdir -p notebooks/valid/sm/non-convertible
mkdir -p notebooks/valid/md/py
mkdir -p notebooks/valid/md/non-convertible
mkdir -p notebooks/valid/lg/py
mkdir -p notebooks/valid/lg/non-convertible

# convert all ./notebooks/valid/sm to ./notebooks/valid/sm/py
find . -type f -name *.ipynb -path './notebooks/valid/sm/*' | while read f; do
	out="py/$(basename -- "$f")"
	out="${out%.*}"
	if ! jupyter nbconvert --to python "$f" --output "$out"; then
		echo "ERROR CONVERTING $f"
		newname="notebooks/valid/sm/non-convertible/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
	fi
done

# convert all ./notebooks/valid/md to ./notebooks/valid/md/py
find . -type f -name *.ipynb -path './notebooks/valid/md/*' | while read f; do
	out="py/$(basename -- "$f")"
	out="${out%.*}"
	if ! jupyter nbconvert --to python "$f" --output "$out"; then
		echo "ERROR CONVERTING $f"
		newname="notebooks/valid/md/non-convertible/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
	fi
done

# convert all ./notebooks/valid/lg to ./notebooks/valid/lg/py
find . -type f -name *.ipynb -path './notebooks/valid/lg/*' | while read f; do
	out="py/$(basename -- "$f")"
	out="${out%.*}"
	if ! jupyter nbconvert --to python "$f" --output "$out"; then
		echo "ERROR CONVERTING $f"
		newname="notebooks/valid/lg/non-convertible/$(basename -- "$f")"
		if mv "$f" "$newname"; then
			python3 db.py -action "update_location" --old-location "$f" --new-location "$newname"
		fi
	fi
done
