# new backend

fastapi + redis

## environment
- python 3.11.2
- redis

```bash
pip install -r requirements.txt
python app.py
```

## api

看接口可以去swaager-ui，路径为`/docs`，测试机为[http://124.220.153.22:8000/docs](http://124.220.153.22:8000/docs)

## 认证

对于所有非幂等的请求做了Bearer认证，token获取方式请看`/auth/token`接口。如果要在swagger-ui测试接口，点击右上角Authorize提交你拿到的token即可。

注意：新后段对token做了封装，不要从老后段获取token！
