# Python(Decorator) #

* 주의사항
 ``` markdown
python 2.7에서 작성되었습니다.
이 글은 필자가 직접 공부하며 알게된 주관적인 내용들을 담고 있으므로 그 점을 유의하며 읽어주시면 감사하겠습니다.
```

# 목차 #
 1. Class형 Decorator의 작성법
 2. Tip
 3. 마무리
***

## Class형 Decorator의 작성법 (인수 X) ##

그러면 지난번에 이어서 이번엔 함수형이 아니라 class형의 데코레이터 작성법을 알아보자.

이번에는 재귀함수에 대한 사전 지식이 있어야 코드를 읽는데에 있어서 어려움이 있지 않을 것이라고 생각하기 때문에  
재귀함수에 대해서 모른다면 공부해오는 것을 추천한다.

 ``` python
class readingTheBook:
    def __init__(self, function):
        self.function = function
        self.total_page = 513
        self.amount_read = []
        self.add_read = 3

    def __call__(self, reading, days):
        if self.total_page > 0: # 3
            self.total_page = self.total_page - reading
            days += 1 # 하루가 지났네..
            self.amount_read.append([reading, days]) # 얼마나 읽었는지 기록해놔야지..
            reading += self.add_read  # 오늘 이렇게나 읽었다!
            self.add_read += 3  # 더욱 열심히 읽어보자.
            self.__call__(reading, days)
        else:
            return self.function(self.amount_read, days)

@readingTheBook # 2
def read_books(page, days):
    for page_read, day in page:
        print '{}일째 {} 만큼 읽었네'.format(day, page_read)
    print '걸린 날짜 : {}일'.format(days)
    return True

read_books(37, 0) # 1

# -----
결과 : 
1일째 37 만큼 읽었네
2일째 40 만큼 읽었네
3일째 46 만큼 읽었네
4일째 55 만큼 읽었네
5일째 67 만큼 읽었네
6일째 82 만큼 읽었네
7일째 100 만큼 읽었네
8일째 121 만큼 읽었네
걸린 날짜 : 8일
```

코드 설명을 하는 이쪽 글을 먼저보지 말고 한번 위의 코드가 어떻게 동작해서 아래의 결과가 나오는 것인지 한번 추론을 해보는 것을 권장한다.

먼저 #1이다. #1에서는 1편을 봤다면 알겠지만, 곧바로 #2로 호출할 함수(read_books)를 데코레이터가 되는 readingTheBook에게 넘겨준다.  
 그리고 클래스형 데코레이터에서만 보이는 특징인데 __init__메서드에 **호출할 함수**를 넘겨준다.  
이는 함수형 데코레이터에서의 첫번째 함수에 호출할 함수를 넘겨주는 현상과 같다.

그리고 클래스형에서는 __call__메서드에 인자값이 넘어간다.  
클래스형 데코레이터를 쓰고 싶으면 __call__메서드를 반드시 작성해야한다.

만약 작성하지 않으면 아래와같은 에러가 발생한다.
> AttributeError: readingTheBook instance has no __call__ method

에러 메시지를 읽어보면 readingTheBook 인스턴스가 __call__메서드를 가지고 있지 않다고 한다.

이것은 이전 편에서는 설명을 안하고 넘어갔었지만, 사실 데코레이터는 일반적으로 우리가 클래스를 작성하고 그 클래스를 객체에 할당하는 과정이 포함되어있다.

어디에 있느냐하면 #1을 지나 #2가 된 순간에 아래처럼 작동한다.

``` python
> instance = readingTheBook(read_books(37, 0))
> instance()
``` 

만약 위의 코드가 이해가 안된다면 구글에서 **클래스와 인스턴스**에 대해서 찾아보거나 이 글의 다음 글을 기다리는 것을 추천한다.

그러면 마저 이어서 코드의 해석으로 돌아가자.

readingTheBook 클래스에서 init 메서드에 호출할 함수가 저장이 되었고, call 메서드에서 인자값이 저장이 되었다.  
코드의 내용중 #3을 잘보면 self.total_page가 있다.  
[class_decorator_without_arg.py](https://github.com/Elgashia/studied_list/blob/master/python/%EB%8D%B0%EC%BD%94%EB%A0%88%EC%9D%B4%ED%84%B0/class_decorator_without_arg.py)파일을 참조해보면 
self.total_page는 책의 총 페이지 수 이다.

코드의 #3의 의미는 total_page가 0이 되면 즉, 책을 다 읽으면 그동안의 결과를 반환하는 else로 넘어가게 된다.  
 만약 다 읽지 않았다면, 오늘 읽은 페이지 수를 total_page에서 값을 빼고 하루가 지났음을 amount_read라는 리스트에 기록한다.
 
그리고 그외의 다른 과정들을 거쳐서 책을 다읽으면 위의 결과가 출력이 되는 것이다.

***

여기까지 집중하며 읽어준 독자여러분들에게 먼저 감사를 표한다.  
정말로 그럴지는 모르겠지만 아마도 코드들을 읽는 것에 있어서 다른 분들이 데코레이터에 대해서 적어놓은 글들보다 힘들었으리라고 생각한다.  
 하지만 제가 이렇게 코드들에 스토리들을 부여하고 조금 복잡한 로직들을 넣어놓은 이유는 데코레이터들을 이해만하지말고 여러 로직이 부여된 코드를 보면서 '아, 내가 이걸 이렇게 사용하면 되겠구나..'  
하고 생각하기를 바라서이다.

그러면 슬슬 다음 작성법인 클래스형 데코레이터에 인수가 있는 경우에 대해서 살펴보면서 데코레이터에 대해서 복습을 한번 더 하고  
 다른 곳에서는 설명이 별로 있지 않은 부분에 대해서 '이런 방법도 있구나'를 인식시키기 위한 과정으로 들어가도록 하겠다.  
이것은 설명이 아니라 말그대로 이런 방법도 존재한다는 것을 알았으면 좋겠다.. 하는 글쓴이의 바람일 뿐이다.  

이것이 왜 이렇게되는 것인지는 그 구조를 아직 모르고 있다..~~(만약 있다면 알려주세요.. ㅠㅠ)~~

## Class형 Decorator의 작성법 (인수 O) ##

``` python
class fruit_counting:
    def __init__(self, operator):
        self.formula = operator

    def __call__(self, function):
        def wrapper(fruit1, fruit2):
            return function([fruit1, fruit2], eval(str(fruit1) + self.formula + str(fruit2)))
        return wrapper

@fruit_counting('+')
def fruit_basket(fruit, result):
    return '총 {0}개가 있네~'.format(result)

print fruit_basket(2,3)
```

이번에는 로직이 상당히 쉬운 녀석으로 작성해보았다.  
 하지만 이번 코드는 데코레이터의 목적인 기능 추가가아니라 기능 변형이 되어버리니까 이런식으로 코드를 짜지 않도록 주의하자.

이번 코드는 2와 3을 더하는 아주 간단한 녀석이지만, fruit_counting라는 클래스형 데코레이터에 '+'라는 string을 추가하였다.

그리고 데코레이터에 인수가 없는 코드와는 다르게 init 메서드에서는 인수를 넣어주고, call 메서드에서 함수를 받는다.  
이 함수에 추가할 매개변수들을 call 메서드 내부의 wrapper함수에서 받아서 self.formula(== '+')와 두 매개변수를 더해주고 있다.

어떤가? 아주 간단하지 않은가?

그러면 곧바로 간단 Tip 하나를 알려주고 데코레이터에 대해서 마치려고 한다.

사실 여기까지 전부 이해했다면 데코레이터를 사용할 수 있다고 자부해도 된다.  
이제 남은 것은 직접 사용해보는 것 뿐이니까..

## Tip~ ##

``` python
def handler(qry_function):
    db_con = "db~~"
    db_cursor = "session"
    print db_con, db_cursor
    def wrapper(db_qry):
        print db_qry
        return True
    return wrapper

@handler
def db_qry(qry):
    return qry

for i in range(0, 10):
    db_qry('select * from table_name')
```

위의 코드는 1편에서 보았던 함수형 데코레이터이다. ~~(이것은 글쓴이가 실제로 사용하고 있는 방법이다.)~~
위의 코드는 직접 실행해보며 결과를 확인해보기를 권장한다. ~~(만약 이 내용에 대해 자세히 아는 분이 있다면 알려주세요.. ㅠㅠ)~~

보통 함수를 사용하는 이유는 여러가지가 있겠지만, 그 중에 하나가 코드 재사용인데, 데코레이터로도 충분히 재사용을 할 수가 있다.  

위의 코드대로 설명을 해보자면, python으로 db에 쿼리를 날릴필요가 있는데 그것이 여러번이라고하자.  
 그런데 python에서는 db와의 연동이 필요한데, 그것을 쿼리 날릴때마다 db와 계속 통신을 시도할 수는 없잖은가?  
그래서 글쓴이가 시도한 방법인데, 데코레이터를 통해서 wrapper의 바로 밖이고 데코레이터 안쪽에서 그 연결을 시도해놓는 것이다.

위의 코드를 직접실행해보았다면 'db_con, db_cursor' 이 두 변수가 딱 한번만 출력된다는 것을 눈치챘을것이다.

***

## 마무리 ##
설명이 굉장히 짧았지만, Tip에서는 이런식으로도 재사용을 방지할 수 있다는 것을 알아가고 이에 대한 지식이 있으신 분께 이것이 왜 이런 현상이 일어나는지 도움도 받고자 함이다.

그러면, 이것으로 python 데코레이터편을 마치도록 하겠습니다.
