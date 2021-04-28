# -*- coding: utf-8 -*-

'''
# 클래스형 데코레이터 #
사과 두 개와 배 세 개가 있다.
이들의 개수를 세어보자.
답은?
'''

# 좋아. 세어보자.
class fruit_counting:
    def __init__(self, operator):
        self.formula = operator

    def __call__(self, function):
        def wrapper(fruit1, fruit2):
            return function([fruit1, fruit2], eval(str(fruit1) + self.formula + str(fruit2)))
        return wrapper

# 과일 개수 세기를 시작하자.
@fruit_counting('+')
def fruit_basket(fruit, result):
    return '총 {0}개가 있네~'.format(result)

print fruit_basket(2,3)
