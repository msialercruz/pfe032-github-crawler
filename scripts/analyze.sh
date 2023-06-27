# analyze
mkdir -p "$(dirname -- $2)"
curl --location 'http://localhost:5000/analyze/'"$1"'' -o "$2"