import requests
r = requests.get('https://api.github.com/user', auth=('625707127@qq.com', '5211314hzy'))
print(r.status_code)
result=r.json()
print(result["login"])
assert result["login"]=="TurnSheep"
