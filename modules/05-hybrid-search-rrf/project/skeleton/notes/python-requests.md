# Python requests timeout

Set a timeout on every python requests call — `requests.get(url,
timeout=10)`. The library default waits forever, and a hung API client
holds a connection open for hours.
