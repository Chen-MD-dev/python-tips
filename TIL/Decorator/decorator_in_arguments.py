# -*- coding: utf-8 -*-

'''
# 함수형 데코레이터 #
나는 지금 커피와 빵을 먹기를 원한다.
그 값은 아래와 같다.
커피 : 6,000
빵 : 4,500
당신이 가진 돈은 15,000원이다.
돈먹는기계에 돈을 넣어보고 나오는 돈과 커피와 빵이 구매가 되었는지 확인해보자.
'''

# 주인장이 작성한 소프트웨어에 의해서 값을 차감하여 돌려준다.
def product_buying(coffee, bread):
    def machine(function):
        def wrapper(money, list):
            buy_list = []
            if list:
                for lt in list:
                    if lt == '커피':
                        money = money - coffee
                        buy_list.append('커피')
                    if lt == '빵':
                        money = money - bread
                        buy_list.append('빵')
            else:
                buy_list = None
            return function(money, buy_list)
        return wrapper
    return machine

# 돈 먹는 기계는 돈을 원한다.
@product_buying(coffee=6000, bread=4500)
def money_eating_machine(money, select):
    money_you_have = money
    return '구매목록 : {}, 거스름 돈 : {}'.format(','.join(select), money_you_have)

print money_eating_machine(15000, ['커피','빵'])
