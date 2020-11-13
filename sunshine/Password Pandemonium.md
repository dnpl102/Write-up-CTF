##  Password Pandemonium

Để solve bài này chúng ta cần bypass các filter sau:

- Không được quá dài hoặc quá ngắn
- Có từ 2 kí tự đặc biệt trở lên
- 1 emoji trở lên
- có 1 số nguyên tố trở lên
- Tổng số kí tự in hoa phải bằng số kí tự in thường
- phải là chuỗi palindrome
- kí tự đầu tiên md5(password) phải là số
  ```sh
    md5(// 1Zz😒zZ1 //) = 67e09e9efc73abdc85e1a7d4d68712ee
  ```
- eval(password) == true (javascript)

 ```sh
Trong javascript có nhiều cách để eval() trả về true 
 
   eval(true) -> true
   eval("true") -> true
   eval('"1" == 1') -> true
   eval('123 != 231') -> true
   eval('123 !==! 231') -> true
   eval('true abc') -> error
   Thử với dấu comment // or /* trong js
   eval('true /*abc*/') -> true
   eval('true //abc') -> true
 ```

- Kết hợp những điều kiện trên, ta có password:
 ```sh
    true //1Zz😒zZ1 // eurt
    "@@ 1Zz😒"!=!"😒zZ1 @@"
 ```
 
 -> Flag: sun{Pal1ndr0m1c_EcMaScRiPt}



