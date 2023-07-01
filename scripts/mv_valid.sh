#!/bin/sh

# ORGANIZE NOTEBOOKS BY SIZE
mkdir -p notebooks/valid/sm
mkdir -p notebooks/valid/md
mkdir -p notebooks/valid/lg
# move small notebooks (<= 10KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -10240c -exec mv "{}" notebooks/valid/sm \;
# move small notebooks (<= 100KB)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -102400c -exec mv "{}" notebooks/valid/md \;
# move small notebooks (<= 1M)
find . -type f -name *.ipynb -not -path './notebooks/*/*' -size -1048576c -exec mv "{}" notebooks/valid/lg \;
