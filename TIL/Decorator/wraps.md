# Python(Decorator) #

* 주의사항
 ``` markdown
python 2.7에서 작성되었습니다.
이 글은 필자가 직접 공부하며 알게된 주관적인 내용들을 담고 있으므로 그 점을 유의하며 읽어주시면 감사하겠습니다.
```

# 목차 #
 1. Decorator 정의
 2. Decorator의 작성법

***

## Decorator 정의 ##

Decorator는 사전에는 ‘장식하는 사람' 또는 ‘장식’으로 나와있다.

이에 대해서는 다른 사람들과 이야기를 나눠본적이 없어서 잘 모르지만,
decorator라는 이름이 붙은 저의 생각은

> 화가의 그림(Main 기능)에 조명, 액자 등(추가 기능)을 통해 그 그림을 더욱 돋보이게 한다.

위와 같습니다.

***

## Decorator의 작성법 ##

python에서의 Decorator의 작성법에는 **4가지** 방법이 있습니다.

함수형 데코레이터 2가지, Class형 데코레이터 2가지인데, 각각의 2가지는 데코레이터 함수에 매개변수를 전달하느냐 하지않는냐로 나눠집니다.

먼저 함수형부터 다뤄보겠습니다.

## 1. 함수형 데코레이터(데코레이터에 인수 전달 X) ##

 ``` python
def product_buying(function): # 1
    def wrapper(arg):
        arg = arg-5000
        return function(arg) # 5
    return wrapper # 6

@product_buying # 2-1
def money_eating_machine(money): # 2
    money_you_have = money
    return '거스름 돈 : {}'.format(money_you_have)

print money_eating_machine(10000) # 3

# -----
결과 : 거스름 돈 : 5000 # 4
```

위의 코드는 'product_buying'라는 데코레이터 함수와 'payment_my_money'라는 main함수(호출할 함수) 2가지의 함수로 이루어져 있습니다.
</br>#3을 보면 python을 만져본 여러분들이 보신다면 흔히 알고 계시는 함수 호출입니다.
</br>여러분들은 지금 돈먹는기계(#2)에 10,000원을 넣었고, 값을 받은 기계는 설치되어있는 로직(#1)에 의해 값을 차감하여 돈을 거슬러 줍니다.

<p/>#2-1를 보시면 @product_buying라는 것이 있습니다. 이 부분에서 자세히 설명하고 Decorator 작성법 2번째로 넘어가겠습니다.

@는 python에서 데코레이터를 뜻하는데, '아래의 함수는 데코레이터 함수에 전달하겠다.' 라는 동작을 실행합니다.
</br>#2에 있는 함수에는 돈을 넣었지만 넣은 돈의 가격을 계산하는 식은 존재하지 않습니다.

하지만 출력된 결과(#4)을 보면 결과값은 5000으로 줄어있습니다.

이렇게 된 이유는 'money_eating_machine'라는 함수가 'product_buying'함수의 매개변수로 전달했다는 것이라는 것을 아셔야합니다.
</br> 그리고 wrapper함수에는 자동으로 여러분이 기계(호출한 함수)에 전달한 돈(매개변수)이 전달되고 그 값을 계산합니다.

<p/>#5의 return에서는 'money_eating_machine'함수를 한번 더 호출하는 것처럼 생겼는데, 데코레이터에서는 여기서 여러분이 호출하고 싶은 함수가 호출됩니다.

그렇다면 #3의 함수 호출은 무엇이냐? #3에서 호출한 것은 바로 #1로 #2의 함수가 넘어가서 #1 함수는 함수를 전달받게 된 것이고,
</br>#3에서 전달한 값이 wrapper함수에서 인자로 값을 받아서 처리합니다.

그 다음 과정으로 이제 main함수인 'money_eating_machine'함수의 호출이 이루어지는 것입니다.
</br> 하지만 돈먹는기계의 호출은 wrapper 함수의 내부에 존재하기 때문에 값 처리를 위하여 #6에서의 구문의 도움이 필요합니다.

그럼 Decorator 작성법 2로 넘어가서 더 자세한 이해를 하기 위해서 도움을 드리겠습니다.

## 2. 함수형 데코레이터(데코레이터에 인수 전달 O) ##

 ``` python
def product_buying(coffee, bread): # 3
    def machine(function): # 4
        def wrapper(money, list): # 5
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
            return function(money, buy_list) # 6
        return wrapper
    return machine

@product_buying(coffee=6000, bread=4500) # 1
def money_eating_machine(money, select): # 2
    money_you_have = money
    return '구매목록 : {}, 거스름 돈 : {}'.format(','.join(select), money_you_have)

print money_eating_machine(15000, ['커피','빵']) # 7

# -----
결과 : 구매목록 : 커피,빵, 거스름 돈 : 4500
```

위 코드는 조금 더 시간을 들여서 자세히 보도록 합시다.

가정 먼저 1번 작성법과 가장 크게 달라진 점은 #1이다.
</br>1번 작성법에서는 데코레이터 함수에 전달하는 인수가 전혀 없었다.
</br>하지만 이번에는 커피와 빵 가격이 정해져있고 주인장이 작성한 알고리즘(product_buying)으로 값을 전달하고 있다.

이것이 바로 데코레이터 함수에 인수를 전달하는 함수 작성법이다.

하나하나 뜯어보도록 하자.

먼저 #1에서 주인장이 설정한 coffee값과 bread값을 돈을 계산할 알고리즘을 가지고있는 곳으로 전달한다.
</br>#3에서 그 값을 받는 것이다.

그 다음으로 1번 작성법에서 나왔던 것과 똑같이 동작한다.
</br>#2의 함수가 #4의 함수의 매개변수로서 전달되고 #5에 #7에서 입력한 매개변수들을 전달한다.
</br>전달받은 매개변수들을 차리히고 #6에서 main 함수(#2)를 호출한다. (이 과정에서 구매목록이 무엇인지 계산되고 거스름돈의 계산이 완료된다.)

1번에서의 설명을 온전히 이해했다면 2번과의 차이점은 데코레이터 함수에 값을 전달하느냐 하지않느냐의 차이점 외에는 느끼지 못할 것 이다.

** 그렇다면 당신은 제대로 이해하고 있는 중이라는 증거이다. **

그러면.. 이제 Class형태의 데코레이터에 대한 이해를 할 것인데..
</br>[2편](https://github.com/Elgashia/TIL/blob/master/python/Decorator_with_python/Chapter02_Decorator.md) 에서 계속하도록 하겠습니다.

지금 간단하게 난이도에 대해 이야기를 하자면, 함수형의 데코래이터를 이해한 당신들은 더욱 난이도가 쉽다고 느낄것이니 걱정하지말자.
