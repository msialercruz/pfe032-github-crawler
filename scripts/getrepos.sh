#!/bin/sh
curl "https://github.com/search?q=created%3A%3E2022-01-01+stars%3A%3E5+language%3A%22Jupyter+Notebook%22+license%3Amit+machine+learning+&type=repositories&ref=advsearch&p=[1-$1]" --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br' -H 'Connection: keep-alive' -H 'Cookie: _octo=GH1.1.542254102.1687281470; logged_in=yes; _gh_sess=L2MIvlO1LwczcVvwNtiFyP0pfyVL%2BhlJsp1kmSxnlzfdCfrUIb3B%2BleersC1fnwsyrm6e3opv7LVb%2FEn9Z83tU6t67PYs8KOEJ1ZfTrtt2f%2Fa0Vv4Rmwy7%2B65FbUE24Uo8K4VtlmC9zKeHX7YIna8S8KA3OuC7%2FjxMSY9M0erm1tWCw9uZXQ1rcJSP0G%2FLvu8L6l4b%2B0O%2BwxQ%2BBm9YkjqaWKaD57Su7rm4Qol%2F8ktU7lzMM8OG3H%2B%2FquVP5fmPX%2BRvBuqpbAdTWWT5u8kPCM0bJfcfyin49JD5nitKR%2Bjne%2F2%2FLSqfLc98adMBVGMF67Hsqy4qCtXdXRxbcdA%2BxPZUMMejuO8laUYR%2BHPb971IV9%2BpN3KlTLJPzwXDJ21J%2BG3uNLwL4vgshrF91yOa5mwUN48nxuJa64IszMWY1cJtcodZGwXY9DLVFS%2B8BPKtUrBQYHa9ojfYxPiHHX0uekNid0V4ukR1GJHOVnq3gMnEi1i%2Fu86JdSO79Pk1vfr%2FW4CiPzyu0nDjoUxseJa81KXlIsLQV4io6GUXL5iFJGbGLZnF6tqf1%2Be%2FwgpjhgG3FAupdX3zZKT4Z1efiH7xmcTUiDcpU6QOdcb5O8DEeD6gS0QbND8Uc7OIvJT%2FlXjmE6eJO9x9Rygav6PJOBQauW4Ll2N%2BlD9qR4KGSvWtJODCmHLwLEWdwCPkCInH9BKWJ8QgFTLKDTLGFB3Q8t9pfXP3jjicJwgxOhL57jRJdO%2B8qwaS7zFhqFqtRrv76YPcaKJVIf96VzPwTepssBAz1n82t9hnzNaUC9JPsOBQev6xEgstbn6%2FkjD1qShyHU%2FAPT0m3FAegeuN4YNJu91gHXdc%2F%2F2GS7SGPaAZ%2FKZAv%2FykVbBJd9Hr%2BUjv7nY8hGU6jYhYBPgWCZcoDtIswZyjPB3JqC5Exwhc5wyAOw60HISH6Us%2BmCHDCfooR%2BhiklD4QWsa0U%2FuLG0Kcx5aV946qTbfowDRWYLNyDc2n5PqTiQ3c1OsfuYCCtgmrj3FthyHYsWEMRIKqqAIagP2gw6NR7FgUex129YwyJGZ77aCUUjhg12zACxzim2WIdZsBf%2BNmDtpYManxtKkQ1B3t08P05Mk0fMSdMVhk2uVnuOU04k1NfFUw5XgMJAq9VPIfDiHLlI7aGRJgF%2BoUsZstkQKJohngCXJ%2FsAYlUzbQISz8z2HkFTbMIMMIJcxk0I4Zs8VNofMjtn21FlTcFS9jSLA%2BMybZR9DFzeGEu%2Bvp7mArrh4wNvYdierEmwa5ti35Lgya2jEcNNukU0hdTF7lH5uQWcCE%3D--5yUWclmM4cXWRTus--rTRGZDhJ44LSQzcBR9qI1Q%3D%3D; preferred_color_mode=dark; tz=America%2FToronto; _device_id=3a5a45ed697e310d8f138f992a92ad0b; user_session=UaQFeQUKJ7KjbP2BtGVycwAHsNJA1QbPctV7JTeXLycZJoZW; __Host-user_session_same_site=UaQFeQUKJ7KjbP2BtGVycwAHsNJA1QbPctV7JTeXLycZJoZW; tz=America%2FToronto; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; dotcom_user=msialercruz; has_recent_activity=1' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: none' -H 'Sec-Fetch-User: ?1' -H 'If-None-Match: W/"af06063277c382183cd61571272f2337"' -o "html/repos/page_#1.html"
