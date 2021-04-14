# Collections
일반 자료형의(dict, list, set, tuple) 컨테이너 타입을 조금 더 발전시킨 형태
파이썬 기본 패키지에 포함되어 있음
|자료형|설명|
|------|---|
|namedtuple|다수의 필드 정보를 가지는 데이터를 저장할 때, 클래스의 객체를 생성하여 저장하는 대신 튜플의 서브클래스를 만들어 저장하는 형태.객체형태보다 메모리 소모가 적으므로 공식 메뉴얼에서 추천하는 방법|
|deque|양 쪽으로 데이터의 append, pop이 가능한 큐|
|ChainMap|여러 맵의 단일 뷰를 만들어주는 클래스. 서로 다른 데이터를 가지는 맵들을 체인처럼 묶어줌으로써 하나의 단일 딕셔너리처럼 취급할 수 있다.|
|Counter|딕셔너리(dict)의 서브클래스로, 객체의 개수를 세어주는 모듈. 객체를 해시화하여 카운트하므로, 해싱이 가능한 객체여야 한다.|
|OrderedDict|딕셔너리(dict)의 서브클래스로, 추가된 엔트리의 순서를 기억하는 딕셔너리|
|defaultdict|딕셔너리(dict)의 서브클래스로, 존재하지 않는 key을 호출해도 에러를 내지 않는 딕셔너리|
***
# namedtuple
다수의 필드 정보를 가지는 데이터를 저장할 때, 클래스의 객체를 생성하여 저장하는 대신 튜플의 서브클래스를 만들어 저장하는 형태
```python
from collections import namedtuple

Book = namedtuple('Book', ['title', 'auther', 'price'])

book1 = Book('Millenium', 'Steve larsson', 12000)


## test

print("%s, %s, %s" % (book1.title, book1.auther, book1.price))
## expected: Millenium, Steve larsson, 12000

print(book1)
## expected: Book(title='Millenium', auther='Steve larsson', price=12000)
```
네임드 튜플에 Book이라는 타입 이름을 가지는 서브클래스를 생성하였다.
Book은 title, auther, price라는 각각의 필드를 가진다.
Book이라는 클래스를 새로 생성하여 사용하는 대신, 네임드 튜플이라는 자료형에 저장하여 사용하고 있다.

예) csv & sqlite3 import
```python
EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print(emp.name, emp.title)

import sqlite3
conn = sqlite3.connect('/companydata')
cursor = conn.cursor()
cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
for emp in map(EmployeeRecord._make, cursor.fetchall()):
    print(emp.name, emp.title)
```
csv 파일에서 불러온 각각의 엔티티는 EmployeeRecord라는 오브젝트로 맵핑하여 저장한다. 각각의 칼럼은 name, age, title, department, paygrade 라는 필드 타입으로 치환되었다.
sqlite3 쪽도 마찬가지이다. 쿼리를 실행하여 얻은 각각의 엔티티가 EmployeeRecord라는 객체로 맵핑되었고, 각 칼럼은 필드로 맵핑하여 저장하였다.
***
# deque
```python
from collections import deque

q = deque('abc')

for elm in q:
    print(elm)
    
# expected : a b c

q.append('d')
q.appendleft('e')

q

# expected : deque(['e', 'a', 'b', 'c', 'd'])

q.pop()

# expected : 'd'

q.popleft()

# expected : 'e'

q = deque('abc')

q.extend('xyz')

q

# expected : deque(['a', 'b', 'c', 'x', 'y', 'z'])

q.extendleft('xyz')

q

# expected : deque(['z', 'y', 'x', 'a', 'b', 'c', 'x', 'y', 'z'])

q.clear()

q

# expected : deque([])
```
|메소드|설명|
|----|----|
|append()|덱의 오른쪽으로 단일 데이터를 삽입한다.|
|appendleft()|덱의 왼쪽으로 단일 데이터를 삽입한다.|
|pop()|덱의 오른쪽에서 단일 데이터를 삭제한다.|
|popleft()|덱의 왼쪽에서 단일 데이터를 삭제한다.|
|extend()|덱의 오른쪽으로 다수 데이터를 삽입한다.|
|extendleft()|덱의 왼쪽으로 다수 데이터를 삽입한다.|
|clear()|덱의 데이터를 모두 삭제한다.|
***
# Counter
예) 문자열에 알파펫 갯수를 dictionary로 표현
```python
def countletters(word):
    counter = {}
    for letter in word:
        if letter not in counter:
            counter[letter] = 0
        counter[letter] += 1
    return counter

countletters("hello world")
# {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
```
동일한 기능을 collections로 표현
```python
from collections import Counter

Counter("hello world")
# {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
```
예) 가장 많이 등자하는 알파벳과 그 갯수
```python
from collections import Counter

Counter("hello world").most_common()
# [('l', 3), ('o', 2), ('h', 1), ...]

Counter("hello world").most_common(1)
# [('l', 3)]
```
***
# ChainMap
예) 두 딕셔너리의 chain
```python
from collections import ChainMap

a = {'a': 'A', 'c': 'C1'}
b = {'b': 'B', 'c': 'C2'}

m = ChainMap(a, b)

m
# ChainMap({'a': 'A', 'c': 'C1'}, {'b': 'B', 'c': 'C2'})

list(m.keys())
# ['b', 'c', 'a']

list(m.values())
# ['B', 'C1', 'A']
```
|메소드|설명|
|----|---|
|maps|등록된 매핑 객체 리스트|
|new_child|현재 인스턴스의 모든 맵을 포함된 새 객체를 반환|
|parents|현재 인스턴스의 첫 번째 맵을 제외한 새 맵을 반환|
```python
from collections import ChainMap

baseline = {'music':'bach', 'art':'rembrandt'}
adjustments = {'art':'van gogh', 'opera':'carmen'}

c = ChainMap(adjustments, baseline)

d = c.new_child()
e = c.new_child()
e.maps[0]
# {}

e.maps[-1]
# {'music': 'bach', 'art': 'rembrandt'}

e.parents
# ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

d['x'] = 1
d['x']
# 1

del d['x']
list(d)
# ['music', 'art', 'opera']

len(d)
# 3

d.items()
# ItemsView(ChainMap({}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'}))

dict(d)
# {'music': 'bach', 'art': 'van gogh', 'opera': 'carmen'}
```
***
# OrderDict
### ~python3.6
예) 기존의 dict와 OrderedDict에 'a', 'b', 'c', 'd'를 순서대로 삽입하였을 때
dict는 삽입 순서를 기억하지 못하고 'a', 'c', 'b',  'd'로 출력하는 반면
OrderedDict는 삽입한 순서에 따라 자료를 정렬하여 출력한다.
```python
from collections import OrderedDict 
  
d = {}
d['a'] = 1
d['b'] = 2
d['c'] = 3
d['d'] = 4

d
# {'a': 1, 'c': 3, 'b': 2, 'd': 4}

od = OrderedDict() 
od['a'] = 1
od['b'] = 2
od['c'] = 3
od['d'] = 4

od
# OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
```
### python3.7~
파이썬 3.7부터는 dict 라이브러리도 삽입순서를 유지한다.
파이썬 3.7부터 OrderedDict와 dict의 차이점은 == 연산자의 민감성, move_to_end 메소드, reversed 이터레이터의 사용 여부뿐이다.
- move_to_end(key, last=True) : key를 정렬된 dict의 끝으로 이동하는데, True이면 오른쪽으로 이동하고, False이면 처음으로 이동한다. key가 없으면 KeyError가 발생한다.
- reversed : 순서를 뒤집음
***
# defaultdict
1) 초기화 시에 Value 형의 타입을 정의할 수 있다.
2) **딕셔너리(dict)의 서브클래스로, 존재하지 않는 key을 호출해도 에러를 내지 않는 딕셔너리이다.**

예) 가령 [(한식, 떡볶이), (한식, 잡채), (한식, 불고기), (양식, 햄버거)]라는 자료형들을 가지고 있을 때,
음식 분류형을 키값으로 하고 그에 대응되는 음식 이름들을리스트로 가지는 딕셔너리가 만들고 싶다고 하자.
이 때, defaultdict(list)로 초기화하여 사용한다.
그러면, 위의 자료형들은 변환 시 [(한식, [떡볶이, 잡채, 불고기], (양식, [햄버거])] 의 리스트 딕셔너리로 대응될 것이다.
```python
from collections import defaultdict

s = [('한식', '떡볶이'), ('한식', '불고기'), ('한식', '닭갈비'), ('양식', '햄버거'), ('양식', '파스타')]
d = defaultdict(list)
for k, v in s:
     d[k].append(v)

sorted(d.items())
# [('양식', ['햄버거', '파스타']), ('한식', ['떡볶이', '불고기', '닭갈비'])]

d['일식']
# []
```
딕셔너리에 존재하지 않는 key값인 '일식'을 호출하면, keyError를 내는 대신 list 타입의 default null 값인 []를 리턴한다.
```python
from collections import defaultdict

d = defaultdict(int)
d['a'] = 1
d['b'] = 2

d['z']
# 0
```
그러면 defaultdict(int)로 초기화한 딕셔너리에서 존재하지 않는 key값을 호출한다면? int 타입의 default null 값인 0을 리턴한다.
