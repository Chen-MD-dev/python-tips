# -*- coding: utf-8 -*-

'''
# 함수형 데코레이터 #
다음 날 시작되는 축제를 위해서 어떤 소품 하나가 필요해서 소품 매장에 가서 그 물건을 구매하였다.
그 값은 5,000원이고 내가 가진 돈은 10,000원이다.
나는 기계에 돈을 넣었고, 거스름돈이 내 손에 들어왔다.
'''

# 주인장이 작성한 소프트웨어에 의해서 값을 차감하여 돌려준다.
def product_buying(function):
    def wrapper(arg):
        arg = arg-5000
        return function(arg)
    return wrapper

# 돈 먹는 기계는 돈을 원한다.
@product_buying
def money_eating_machine(money):
    money_you_have = money
    return '거스름 돈 : {}'.format(money_you_have)

print money_eating_machine(10000)
