# TODO

- Chall cho ta 1 file python gồm hàm encode và shift
- Ý tưởng hàm encode theo mình hiểu như sau:
Nếu kí tự msg[i] là số thì nó sẽ nhân mã ASCII của số đó với 0x1234 rồi nối vào phần đầu của output.
- Ngược lại với kí tự ko phải số thì nó nhân mã ASCII của kí tự đó với 0x10 rồi nối vào phần đầu của output

```python
def encode(msg):
    output = ''

    for i in range(len(msg)):
        temp = ord(msg[i]) * 0x40    
        temp = temp >> 4         
        if 0xc0 <= temp < 0xe8:
            output = str(int(msg[i]) * 0x1234) + output
        else:
            output = chr(ord(msg[i]) * 0x10) + output

    return output

```

- Ý tưởng hàm decode của mình là tìm các số đã encode (vì khi encode số -> số, kí tự -> kí tự)
thay thế những số đó thành 0->9 (làm ngược lại)
- Duyệt từ đầu cho đến hết msg nếu kí tự ko phải là số thì chr(ord(msg[i]) // 0x10)
- Đảo ngược msg lại (vì hàm encode nối những kí tự vào đầu)

```python
def decode(msg):
    arr_int = ['0', '4660', '9320', '13980', '18640', '23300', '27960', '32620', '37280', '41940']
    for i in range(0,10):
        msg = re.sub(re.compile(arr_int[i]),str(i),msg)
    
    msg = list(msg) # convert to list

    for i in range(len(msg)):
        if  not (48 <= ord(str(msg[i])) <= 57) : #nếu ko phải số
            msg[i] = chr(ord(msg[i]) // 0x10)

    return ''.join(msg[::-1])
```

- Ý tưởng hàm shift:
duyệt từ đầu msg đến nửa msg lấy kí tự đầu nối với kí tự cuối
vd: "abc" -> "ac"
	"abcdef" -> "afbecd"

```python
def shift(msg):
    j = len(msg) - 1
    output = ''

    for i in range(len(msg)//2):
        output += msg[i] + msg[j]
        j -= 1

    return output
```

- Hàm unshift của mình chỉ đơn giản chia làm 2 mảng chứa kí tự ở vị trí chẵn và lẻ
- Đảo ngược o2 lại
- xog nối o1 với o2
- vd : msg = "abcd" -> shift(msg) = "adbc"
  o1 = "ab"
  o2 = "dc"
  
```python
def unshift(msg):
    o1 = ''
    o2 = ''

    for i in range(len(msg)):
        if i % 2 == 0:
            o1 += msg[i] 
        else:
            o2 += msg[i]

    return o1 + o2[::-1]
```


```python
	hashed = '4660۠ܰ4660ڀ٠װװސ23300۰ސݐ18640ܠݰװۀڠ18640۰ްؠѠȐՀȐа4660ѠȐѠߐА' 
    print("[+] Flag", unshift(decode(hashed)))
```

==> Flag: AFFCTF{4lw4y5_f1n1sh_your_job!!1!}