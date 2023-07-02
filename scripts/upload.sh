#!/bin/sh
curl -s --location 'http://localhost:5000/upload' \
--form 'file=@"'"$1"'"'
