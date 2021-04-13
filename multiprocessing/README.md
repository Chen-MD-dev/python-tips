# GIL
자바나 C 계열의 언어를 사용하다가 파이썬을 하다보면 이해가 안되는 것이 GIL 이다.
Global Interpreter Lock 의 약자로 여러개의 쓰레드가 있을때 쓰레드간의 동기화를 위해 사용되는 기술중 하나이다.
GIL은 전역에 lock 을 걸어 두고 이 lock 을 점유해야만 코드를 실행할 수 있도록 제한한다.
따라서 동시에 하나 이상의 쓰레드가 실행되지 않는다. 
예를들어 아래 그림과 같이 3개의 쓰레드가 분산해서 일을 처리하게 될 때도 실제로 cpu 점유할 수 있는 thread 는  하나 뿐이다.
따라서 실제로 사용하는 코어는 하나뿐인 것이다.
![image](https://user-images.githubusercontent.com/78338584/114531821-33e38980-9c87-11eb-9343-f483a08130b1.png)
***
# thread context switching
os 는 스레드 하나의 작업을 진행하기 위해 해당 스레드의 context 를 읽어오고,
_다시 다른 스레드로 작업을 변경할 때 이전 스레드의 context를 저장하고  작업을 진행할 스레드의 context 를 읽어오는 작업을 말한다._
즉 한마디로 말해서 한 스레드에서 다른 스레드로 작업을 주고 받는 과정이라고 할수 있다.
context 는 정보를 나타내는데 레지스터, 커널 스택, 사용자 스택 등의 여러정보가 해당될수 있다.
![image](https://user-images.githubusercontent.com/78338584/114532355-bb30fd00-9c87-11eb-8706-cb5ea15febba.png)
***
# GIL effeciency
직관적으로 멀티코어에서도 코어를 하나밖에 사용 못한다면 GIL 을 사용해서 multithreads 를 지원하는 것은 성능
에 큰 문제가 있을거라고 생각된다. (컨텍스트 스위치 비용 발생)
하지만 대부분의 경우에 문제가 되지 않는다. 
정확히 말해서는 프로그램의 대부분 I/O bound 이기 때문이다.
I/O bound 의 경우 대부분의 시간을 I/O event 를 기다리는 데 사용하기 때문에
event 를 기다리는 동안 다른 thread 가 CPU 를 사용하면 된다.
_반대로 말해서 프로그램이 CPU bound 인 경우에는 multi threaded program 을 작성해도 성능이 향상되지 않는다._
오히려 lock 을 accquire 하고 release 하는 시간 때문에 성능이 떨어진다.
***
# GIL Advantages
멀티 쓰레드 프로그램에서 성능이 떨어질 수 있지만, CPython, PyPy, Ruby, MRI Rubinius, Lua interpreter 등 많은 
인터프리터 구현체들이 GIL을 사용하고 있다.
그 이유는 우선 GIL 을 이용한 multi threads 를 구현하는 것이 parallel 한
multi thread 를 구현하는 것보다 훨씬 쉽다는 것이다.
_게다가 이런 parallel 한 multi-threads 구현체들의 문제는 싱글 스레드에서 오히려 더 느려진다는 것이다._
그래서 CPython 이나 Ruby MRI 에서는 GIL 을 없애려는 많은 시도가 있었지만 결국 싱글 쓰레드에서의
성능저하를 극복하지 못하고 GIL 로 돌아왔다.
결국 파이썬의 창시자인 귀도 반 로섬은 CPython 에서 GIL 을 없애는 대신 싱글 쓰레드에서 
성능을 떨어뜨릴 구현은 받아들이지 않겠다고 선언하기도 했다.
***
# GIL 작업
ThreadPoolExecutor, ProcessPoolExecutor 등 비동기적 프로그래밍을 바탕으로 
GIL 이 파이썬 시스템에 미치는 영향을 최소화하였다.
하지만 멀티프로세싱을 이용하면 이러한 한계를 모두 극복할 수 있다.
여러 프로세스를 활용함으로써 여러 GIL 인스턴스를 활용해 프로그램에서 한 스레드의
바이트코드를 실행하는 데 있어 한번에 정제화할 필요가 없다.
_파이썬에서의 멀티프로세싱은 CPU 의 처리 능력을 최대로 활용할 수 있게 해준다._
***
# 하위 프로세스 활용
```python
import math
import timeit
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def count_prime(n):
    def is_prime(x):
        return bool([i for i in range(2, int(math.sqrt(x))+1) if not n % i])
    return len([i for i in range(2, n+1) if is_prime(i)])


def main():
    proc = multiprocessing.Process(target=count_prime, args=(10,))
    proc.start()
    proc.join()
    print(f"child process terminated")


if __name__ == '__main__':
    main()
```
***
# fork
포킹이란 부모 프로세스에서 자식 프로세스를 생성하기 위해 유닉스 시스템에서 사용되는 매커니즘이다.
이러한 자식 프로세스는 실제 현실처럼 부모 프로세스와 동일하게 부모의 모든 자원을 상속 받는다.
fork 명령어는 유닉스 운영환경에서의 기본 시스템 명령어다.
***
# process spawn
개별적인 프로세스를 스폰 함으로써 그 밖의 파이썬 인터프리터 프로세스를 실행할 수 있다.
여기에는 자체 전역 인터프리터 락이 포함되어 , 각 프로세스는 병렬적으로 실행할 수 있어 
_더 이상 전역 인터프리터 락의 한계에 대해 걱정할 필요가 없다._
새로 스폰된 프로세스는 해당 실행 메소드에 어떤 인자든 실행하기 위해 필요한 자원만 상속받는다.
이는 윈도우 시스템에서 새로운 프로세스를 실행할 때 일반적으로 사용되는 방법이지만, 
유닉스 시스템에서도 마찬가지로 사용된다.
***
# forkserver
forkserver 는 개별적인 프로세스를 생성하는 다소 이상한 매커니즘이지만, 유닉스 파이프를 넘어 
파일 기술어를 전달하도록 지원하고 유닉스 플랫폼에서만 사용 가능한 매커니즘이다.
프로그램이 프로세스를 시작할 때 이 매커니즘을 선택한다면 일반적으로 서버가 인스턴스화 된다.
그 후 프로세스를 생성하는 모든 요청을 다루며 파이썬에서 새로운 프로세스를 생성하려면 
새로 인스턴스화된 서버에 요청을 전달한다.
그러면 해당 서버는 프로세스를 생성하고 프로그램에서 자유롭게 사용할 수 있다.
***
# deamon process
데몬 프로세스는 데몬 스레드와 동일한 형태를 따른다.
부모 프로세스가 종료되면 데몬 프로세스도 종료된다.
데몬 플래그를 참으로 설정해 실행중인 프로세스를 데몬화 할 수 있다.
이러한 데몬 프로세스는 메인 스레드가 실행되는 동안 계속되며, 실행이 끝나거나 
메인 프로그램을 종료할경우에만 종료된다.
```python
import multiprocessing


def daemon_process():
    print(f"starting my daemon process")
    time.sleep(2)
    print(f"daemon process terminating")
    print(f"main process: {multiprocessing.current_process()}")


def main():
    proc = multiprocessing.Process(target=daemon_process)
    proc.daemon = True
    proc.start()
    print("we can carry on as per usual and out daemon will continue to execute")


if __name__ == '__main__':
    main()
```
데몬 플래그를 참으로 하면 데몬 프로세스가 종료되므로 
2초 동안 유휴 상태에 있다가 출력하는 부문의 코드는 실행되지 못한다.
하지만 데몬 플래그를 False 로 변경하고 하면 
메인 프로세스가 종료되더라도 2초후에 나머지 부분을 실행하게 된다.
***
# pid
운영체제에 있는 모든 프로세스는 프로세스 확인자를 구성하는데, 일반적으로 PID 라고 불린다.
파이썬 프로그램 내에서의 멀티프로세스 동작 시, 프로그램에서 오직 1개의 프로세스 확인자가 있을 것이라고
생각하지만 사실은 그렇지 않다.
파이썬 프로그램상에서 스폰하는 각 하위 프로세스가 운영체제 내에서 개별적으로 확인 하고자
자체 pid 수를 받는다.
자체 할당된 pid가 있는 개별적인 프로세스는 로깅 및 디버깅 같은 작업을 수행할 경우 유용하다.
```python
import time
import timeit
import multiprocessing


def child_process():
    print(f"child process with pid: {multiprocessing.current_process().pid}")
    time.sleep(2)
    print(f"child process terminating")


def main():
    print(f"main process with pid: {multiprocessing.current_process().pid}")
    process = multiprocessing.Process(target=child_process)
    process.start()


if __name__ == '__main__':
    main()
```
이는 현제 프로세스의 확인자를 가저올 수 있다.
하지만 현재 프로세스로 부터 PID 이외의 것을 얻을 수도 있다.
threading.Thread 클래스에서와 같이 개별적인 프로세스에 이름을 붙이는 작업을 할 수 있다.
어떤 형태의 작업을 수행하는 2개의 프로세스가 있고 그외 형태의 작업을 수행하는 2개의 프로세서가 있다고 하자.
이러한 작업의 출력을 기록하려면 
'프로세스 1 x 수행'
'프로세스 2 y 수행'
과 같은 네이밍은 보고 싶지 않을 것이다.
대신 자식 프로세스에 좀 더 의미 있는 네이밍을 해야 하는데 디버깅 적업 및 잘못된 부분을 찾는데 있어
많은 도움이 될것이다.
프로세스가 생성된 후 이름을 붙이고자 다음과 같이 해보자
```python
import time
import timeit
import multiprocessing


def foo():
    print(f"{multiprocessing.current_process()} just performed X")
    time.sleep(2)


def main():
    process = multiprocessing.Process(target=foo, name='child-process')
    process.start()


if __name__ == '__main__':
    main()
```
***
# terminate
실행중인 자식 프로세스를 종료하는 것에 대해 살펴보자.
로컬에서 실행하는 파이썬 코드에서는 그다지 중요하지 않지만,
방대한 서버를 다루는 기업용 파이썬 프로그램에서는 매우 중요하다.
오랜기간 실행되는 시스템에서 수천, 수만의 프로세스를 실행할 수는 없으며 일반적으로 시스템 자원에
그대로 남겨둘 수도 없다.
따라서 프로세스를 종료하는 일은 꽤 중요해 보인다.
파이썬에서 프로세스를 종료하려면 다음과 같이 Process 객체의 .terminate() 함수를 사용한다.
```python
import multiprocessing
import time


def foo():
    current_process = multiprocessing.current_process()
    print(f"child process pid: {current_process.pid}")
    for _ in range(10):
        print("child working ... ")
        time.sleep(1)
    current_process = multiprocessing.current_process()
    print(f"main process pid: {current_process.pid}")


if __name__ == '__main__':
    process = multiprocessing.Process(target=foo)
    process.start()
    print("terminating child process")
    process.terminate()
    print("child process successfully terminated")
```
자식 프로세스에서 pid 를 체크한다.
그리고 10초 동안 블로킹 한다.
하지만 부모 프로세스에서 시작과 거의 동시에 terminate() 함수를 통해서  종료한다.
***
# class
멀티프로세스 클래스를 상속받아서 필요한 기능을 추가하여 하위 클래스를 만들어 보자.
스레드나 프로세스 같은 빌트인 클래스에 기능을 추가하면 좀더 상황에 적합한 기능을 구현하는데 도움이 된다.
multiprocessing.Process 클래스를 하위 클래스화하는 자체 클래스를 구현하는 방법을 살펴보자.
새로운 클래스를 정의해 생성자와 실행함수를 구현한다.
```python
import time
import multiprocessing


class CustomProcess(multiprocessing.Process):
    def run(self):
        print(f"child process pid: {multiprocessing.current_process().pid}")
        time.sleep(1)


if __name__ == '__main__':
    print(f"main process pid: {multiprocessing.current_process().pid}")
    child = CustomProcess()
    child.start()
    child.join()
    child.run()
```
자식 프로세스 인스턴스가 생성된다.
그리고 start 함수를 통해 run 함수가 실행된다.
join 함수를 통해서 메인 프로세스가 자식 프로세스의 종료시점을 기다린다.
그리고 다시 run 함수를 통해서 자식 프로세스를 재시작한다.
재시작 할 때는 start 로 할 수는 없다.
***
# multiprocessing pool VS concurrent.futures
파이썬 애플리케이션에서 멀티프로세스로 동작할 경우, 멀티프로세싱 모듈내에서 다양한 기능을 가진 Pool 클래스를 활용할 수 있다.
Pool 크래스는 프로그램 내의 여러 자식 프로세스를 쉽게 실행하고 풀에서 작업자를 선택할 수 있다.
프로세스 풀의 multiprocessing.Pool 구현은 병렬 처리 능력을 지원하고자 거의 동일한 구현 형태를 지닌다.
하지만 concurrent.futures 모듈은 프로세스 풀 생성을 쉽게 해주는 인터페이스만 지원한다.
이러한 간단한 인터페이스는 프로그래머들로 하여금 스레드와 프로세스 풀 모두 즉각적으로 시작할 수 있게 해준다.
그러나 이러한 작업이 복잡해 특정 상황에서 세밀한 조정이 필요할 때는 오히려 불필요 하다.
ThreadPoolExecutor 와 ProcessPoolExecutor 모두 동일한 추상 클래스의 하위 클래스이므로,
상속 메소드를 이해하고 작업하기가 좀 더 쉽다.
파이썬2 와 파이썬 3 모두의 관점에서 바라보면 concurrent.futures 가 2.6버전에서도 소개됐으므로 백포트 버전 대신 멀티프로세싱 모듈에서는 이를 사용하면 되겠다.
일반적으로 multiprocess.Pool 모듈보다는 concurrent.futures 모듈이 필요조건에 적합하므로 추천한다.
하지만 concurrent.futures 모듈이 더 많은 조작을 필요로 하는 한계에 부딪혔을때를 대비해 그밖에도 대안도 알아놓자.
***
# context manager
ThreadPoolExecutor 를 활용했듯이 컨텍스트 관리자를 사용하여 멀티프로세싱 풀을 다룰 수 있다.
마찬가지로 with 키워드 형태를 활용해보자.
```python
from multiprocessing import Pool


if __name__ == '__main__':
    with Pool(4) as pool:
```
위와 같은 스타일은 코드를 간단히 하며, 풀에서 필요한 자원을 릴리즈하는 작업을 따로 다룰 필요가 없다.
__exit__ 가 자동으로 호출되기 때문이다.
다음으로 비교적 간단하게 풀의 자식 프로세스 실행을 반복하는 맵과 같은 작업을 진행할 수 있다.
```python
from multiprocessing import Pool


def task(n):
    return n*n


if __name__ == '__main__':
    with Pool(4) as p:
        print(p.map(task, [i for i in range(10)]))
```
컨텍스트 관리자 형태로 Pool 을 활용해 예제를 살펴보자. 간단한 작업을 수행하는 함수를 정의하고
메인 함수에 컨텍스트 관리자를 추가하자.
다음으로 작업 함수에 리스트를 매핑해 결과를 출력한다.
***
# apply
apply 는 ThreadPoolExecutor 의 .submit() 과 같다. 다시 말해 개별적인 작업을 풀 객체에 전달 하고자 할때 사용된다.
인자 1개를 취하는 간단한 함수를 정의해 보자. 컨텍스트 관리자로 Pool을 실행하고 각 작업의 결과를 출력한다.
```python
from multiprocessing import Pool


def task(n):
    return n*n


if __name__ == '__main__':
    with Pool(4) as p:
        print(p.apply(task, (4,)))
        print(p.apply(task, (3,)))
        print(p.apply(task, (2,)))
        print(p.apply(task, (1,)))
```
.apply() 함수는 결과가 준비될 때까지 정지되므로 병렬 수행작업에는 적합하지 않다.
병렬적으로 수행하고자 한다면 .apply() 와 비슷한 apply_async 를 사용하자
***
# apply_async
병렬적 실행 작업이 필요할 때는 apply_async 함수를 바탕으로 풀에 작업을 전달할 수 있다.
이 예제에서는 4개의 작업을 프로세싱 풀에 전달하고자 함수 내에 for 문을 사용한다.
```python
import time
from multiprocessing import Pool
import os


def foo(n):
    for i in range(5):
        print(f"i={i} pid={os.getpid()}")
        time.sleep(1)
    return n


if __name__ == '__main__':
    with Pool(4) as p:
        tasks = [p.apply_async(func=foo, args=(i,)) for i in range(4)]

        for task in tasks:
            task.wait()
            print(f"result={task.get()}")
```
실행 후에 n개의 작업이 프로세스 풀에서 선택되어 각 프로세서에서 실행됨을 볼 수 있다.
taks 배열에 전달한 순서 그대로 task.wait() 호출 했으므로 결과 또한 순서대로 콘솔에 출력된다.
여기서 apply_async 를 apply 로 변경하면 프로세스가 비동기 병렬로 되는게 아니라 하나씩 
순차적으로 실행된다.
***
# map
ThreadPoolExecutor 와 마찬가지로 multiprocessing.Pool 의 map 함수는 프로세스 풀에서
작업자에 의해 선택된 원소를 하나씩 매핑한다.
```python
import time
from multiprocessing import Pool


def foo(n):
    time.sleep(1)
    return n*n


if __name__ == '__main__':
    with Pool(4) as p:
        results = p.map(foo, [i for i in range(1, 4)])
        print(results)

```
하지만 apply 와 마찬가지로 각 작업은 결과가 준비될 때까지 정지되며, 병렬적인 비동기 성능이 필요할 경우
map_async가 필요하다.
***
# map_async
map_async 함수는 매핑이 필요한 부분에 비동기 실행이 필요한 경우 사용한다.
주어진 함수에 전달되는 작업이 비동기적으로 실행되는 부분을 제외하고는 일반적인 map 함수와 동일하다.
```pyhton
import time
from multiprocessing import Pool


def foo(n):
    time.sleep(1)
    return n*n


if __name__ == '__main__':
    with Pool(4) as p:
        results = p.map_async(foo, [i for i in range(1, 4)]).get()
        print(results)
```
***
# imap
imap 함수는 이터레이터를 반환하는 부분을 제외하고는 일반적인 map 함수와 비슷한 형태이다.
이러한 이터레이터의 사용은 굉장히 유용하고 파이썬에서는 이것을 다루는게 굉장히 좋다.
list 가 전달된 iterable = p.imap() 을 호출한다.
다음으로 next() 메소드를 사용해 이터레이터내의 모든 결과를 콘솔에 출력해 본다.
```python
import time
from multiprocessing import Pool


def foo(n):
    time.sleep(1)
    return n*n


if __name__ == '__main__':
    with Pool(4) as p:
        for item in p.imap(foo, [i for i in range(1, 4)]):
            print(item)
```
프로그램이 실행을 마치면 전달된 리스트의 모든 원소에 함수의 결과값을 그대로 출력한다.
***
# pipe
파이프는 한 프로세스에서 그 외 프로세스로 정보를 전달하는 방법을 나타낸다.
여기에는 익명 파이프와 이름이 있는 파이프, 두 종류가 있다.
파이프는 운영체제에서 자체 프로세스 간에 정보를 전달하기 위한 가장 일반적인 메커니즘이기에, 
멀티프로세스 프로그램의 작업에 동일하게 적용할 수 있다.
***
# anonymous pipe
익명 파이프는 내부 프로세스 통신을 운영체제에서 사용하는 FIFO 통신 형태다.
쉽게 말하면, 한번에 한 방향으로만 전달한다.
2개의 무전기가 있다고 하자.
한번에 한명만 의사를 전달하고자 버튼을 누르고 말할 수 있다.
나머지 사람은 그 사람이 '오버'라는 신호후 버튼을 놓으면 이제야 말을 전달할 수 있다.
다시 말해, 이중 통신을 위해서는 2개의 익명 파이프로 프로세스 간 통신을 한다.
이러한 익명 파이프는 운영체제에 의해 관리되며, 고성능 프로세스 통신에 이용된다.
***
# named pipe
이름이 있는 파이프는 운영체제가 끝날 때까지 지속된다는 점을 제외하고는 익명 파이프와 동일하다.
익명 파이프는 프로세스가 계속될 때까지 이어진다.
***
# work in pipe
지금까지 파이프가 무엇이며 운영체제에서 어떻게 작동하는지를 살펴봤으니, 이제 파이썬 프로그램에서
어떻게 활용하는지 살펴볼 차례다.
파이썬 프로그램에서 파이프를 생성하고자 os 모듈을 불러오고 os.pipe() 호출한다.
os.pipe() 메소드는 운영체제 내에 파이프를 생성하고 읽기 및 쓰기에 사용되는 튜플을 반환한다.
