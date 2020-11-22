# exfil

- Đầu tiên, phân tích sơ qua thì ta thấy file capture này đang mô phỏng lại quá trình attacker "data exfiltration" lên server thông qua protocol mysql
- Filter "mysql" ta sẽ thấy được hàng loạt các câu lệnh mysql injection được attacker gửi lên server
![1](1.png)

- Xét đoạn mysql sau:
![2](2.png)
```mysql
	SLEEP((SELECT ASCII(substr((SELECT group_concat(database_name) FROM mysql.innodb_table_stats), 1, 1)) >> 7 & 1) * 3)
```
- Xử lý luồng thực thi từ trong ra ngoài thì ta sẽ có:
	- SELECT group_concat(database_name) FROM mysql.innodb_table_stats
group_concat(database_name) lấy tất cả record của Field database_name từ bảng mysql.innodb_table_stats (bảng này chứa tên các bảng được khởi tạo).
	- substr(string, 1,1) : lấy kí tự đầu tiên của string
	- ASCII (char): chuyển kí tự sang mã ASCII
	- shift right 7 <==> chia cho 2 ^ 7, and với 1
	- Nếu kết quả là 0 thì sẽ không sleep, 1 thì sleep 1*3 (s)
- Vậy chỉ cần dựa vào thời gian trao đổi giữa các gói tin attacker có thể dễ dàng bruteforce được database_name.
- Ta tiếp tục xét đoạn mysql sau:
![3](3.png)
	```mysql
		SLEEP((SELECT ASCII(substr((SELECT group_concat(table_name) FROM mysql.innodb_table_stats WHERE database_name=0x64625f6d33313439), 1, 1)) >> 2 & 1) * 3)
	```
	- Sau khi đã bruteforce được database_name là 0x64625f6d33313439, attacker tiếp tục tìm những database do user khởi tạo

- Phân tích những gói tin mysql tiếp theo, ta sẽ thấy attacker đã brute thành công database có tên là db_m3149.users, table user và password

```mysql
	SELECT SLEEP((SELECT ASCII(substr((SELECT user FROM db_m3149.users), 1, 1)) >> 6 & 1) * 3)
	SELECT SLEEP((SELECT ASCII(substr((SELECT password FROM db_m3149.users), 3, 1)) >> 5 & 1) * 3)
```

- Với cách tấn công như mình đã phân tích ở trên, attacker có thể lấy toàn bộ user,password từ phía server
- Nếu là người kiên nhẫn thì bạn cũng có thể tìm ra user với password và lấy được flag
- Nhưng ... mình là người chơi hệ code nên thôi code vậy
- OK, sau khi phân tích xong, việc chúng ta cần làm là xử lý dữ liệu
- Ban đầu mình filter mysql contains "db_m3149.users" để lọc ra dữ liệu cần thiết, sau đó export sang json để xử lý
nhưng có 1 vấn đề là sau khi export thì bị duplicate key (json parse sẽ reject những key trùng nhau và chỉ lấy key ở cuối)
![4](4.png)

- Mình bị stuck đoạn này khá lâu và tìm đến tshark (mình tạm gọi là phiên bản terminal của Wireshark)

```sh
	tshark -Y "mysql contains db_m3149.users" -r capture.pcap -Tjson --no-duplicate-keys -w result.json
	segment found (oh no !!!!)
	-- TRY AGAIN --
	tshark -Y "mysql contains db_m3149.users" -r capture.pcap -Tjson --no-duplicate-keys > result.json
	(Ờ mây zing, gút chóp em)
```

- Không dài dòng nữa code thôi :v

```python
import json,re

f = open('result.json','r').read()

j = json.loads(f)

user   = []
passwd = []

for i in j:
	if(float(i['_source']['layers']['frame']['frame.time_delta']) > 2):
		temp = i['_source']['layers']['mysql'][1]['mysql.field.name']
		_regextemp = re.findall(', (.*), 1\)\) >>(.*)&',temp) # regex để lấy 2 số attacker dùng để bruteforce
		if re.search('SELECT user',temp):
			user.append(_regextemp) # sau khi append thì sẽ thành mảng 3 chiều, vì sau khi regex sẽ trả về 1 mảng
		else:
			passwd.append(_regextemp)

def bruteForce(arr):
	for k in range(41,126): # Mã ASCII những kí tự hay dùng
		check = True
		for i in arr:
			if k >> i & 1 != 1:
				check = False
				break

		if(check == True):
			return chr(k)

	return 'x' # trả về x nếu ko tồn tại, đoạn này ko cần quan tâm (type = None)

def Decode(msg):
	temp = []
	i = 1
	result = ''
	for arr in msg:
		if(int(arr[0][0]) == i):
			temp.append(int(arr[0][1]))
		else:
			result += bruteForce(temp)
			i += 1
			temp = [] # reset array
			temp.append(int(arr[0][1]))

		if(arr == msg[-1]):
			result += bruteForce(temp)

	return result

print("[+] user :", Decode(user))
print("[+] password :", Decode(passwd))
```

- result :
	```sh
		[+] user : admin
		[+] password : HTB{b1t_sh1ft1ng_3xf1l_1s_c00l}
	```