#!/bin/sh
curl "https://github.com/search?q=repo%3A$1%2F$2+path%3A*.ipynb+fit&type=code" --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br' -H 'Connection: keep-alive' -H 'Cookie: _octo=GH1.1.542254102.1687281470; logged_in=yes; _gh_sess=7NDOq%2FwHDFKVR9hTgetdIjx%2Fq%2F1c115HPZNknCH0IuZ1XIacudr%2FariP1NrjtZmzLz5oHGptaybb%2F1ukQqcs%2FVIZZm17iRUVCTcBkCDVWzGmG0DHjnd1mzEjZkxcAd3CxEkplHn37VAnxCNg%2FlsC2vmHX7cx7iHt08fABe%2BfBtiPEYxIcbPedS9OlB6zidplk7YrZhZqL45OdhcLoVgSsxHywD13HEWiCNnKnKB79OZjry3d1T6ZZ3tNLqNM6wi7HGJ8n0MgW5zaTxdHlvlXsTp4QiZiIER0e6wQCJYiMNIG9pKvXvXC1TE4jhWAkZui8MpCq8TIhFRDqptZYy4YG7ULIYWkYoleRYr%2FktchxPMJjHWQWtaotI1MwinvXRxJqIEEzNZ%2BxSWswkCv8ulMI93K4azJzaJCEcriN4VtqkQRXmFNOxl60gMnmFeYq7n1tL%2BncaaLx3EvuXl4ug%3D%3D--TyINVFd7bu4trgt%2F--HpzdbK1brrWuhqYrFuvDqQ%3D%3D; preferred_color_mode=dark; tz=America%2FToronto; _device_id=3a5a45ed697e310d8f138f992a92ad0b; user_session=UaQFeQUKJ7KjbP2BtGVycwAHsNJA1QbPctV7JTeXLycZJoZW; __Host-user_session_same_site=UaQFeQUKJ7KjbP2BtGVycwAHsNJA1QbPctV7JTeXLycZJoZW; tz=America%2FToronto; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; dotcom_user=msialercruz; has_recent_activity=1' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'If-None-Match: W/"921dd4b77f09c7d102d5d64a1a2a8ea8"' -o "html/notebooks/$1-$2.html"
printf "html/notebooks/$1-$2.html\n$1\n$2\n"
