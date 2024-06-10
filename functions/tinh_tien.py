
def tinh_tien(thansohoc, nhantuonghoc, sinhtrachoc):

    value= {
        1:0,
        5:1,
        10:2
    }
    def count_zeros(lst):
        count = 0
        for num in lst:
            if num == 0:
                count += 1
        return count
    bought=[1,1,1]
    if thansohoc == 0:
        bought[0] = 0
    if nhantuonghoc == 0:
        bought[1] = 0
    if sinhtrachoc == 0:
        bought[2] = 0
    
    cost={
       "thansohoc": 100000,
        "nhantuonghoc": 300000,
        "sinhtrachoc": 500000, 
    }
    thansohoc_cost= 0
    nhantuonghoc_cost= 0
    sinhtrachoc_cost= 0
    if bought[0]>0:
        
        if value[thansohoc] == 1:
            discount = 0.9
        elif value[thansohoc]==2:
            discount = 0.8
        else:
            discount=1
        thansohoc_cost= thansohoc * cost['thansohoc'] * discount
    if bought[1]>0:
        
        if value[nhantuonghoc] == 1:
            discount = 0.9
        elif value[nhantuonghoc]==2:
            discount = 0.8
        else:
            discount=1
        nhantuonghoc_cost= nhantuonghoc * cost['nhantuonghoc'] * discount
    if bought[2]>0:
        
        if value[sinhtrachoc] == 1:
            discount = 0.9
        elif value[sinhtrachoc]==2:
            discount = 0.8
        else:
            discount=1
        sinhtrachoc_cost= sinhtrachoc * cost['sinhtrachoc'] * discount
    num0= count_zeros(bought)
    tong_tien=thansohoc_cost + nhantuonghoc_cost +sinhtrachoc_cost
    if num0 ==0:
        tong_tien= tong_tien * 0.9
    elif num0==1:
        tong_tien= tong_tien * 0.95
    else:
        pass
    

    return round(tong_tien)