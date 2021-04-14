"""
과거 영상 분석 및 병렬 멀티 프로세싱 관련 테스트 흔적
pafy : youtube 영상 관련 패키지
multi_analy : 그냥 opencv로 영상재생한다 생각하셈

결국 threading은 한번에 한 쓰레드만 작동하기 때문에
정말 병렬처리를 python으로 하고 싶다면 multiprocessing이 답이다.
각각 비동기로 프로세스를 추가하고 싶다면 apply_async를 쓰시라
사실 이 테스트처럼 프로세스 실행할 리스트가 미리 다 정의 되어 있고
동시에 실행시킬거라면 map_async를 쓰면 된다
"""
import multi_analy
import pafy
import time
# from threading import Thread
from multiprocessing import Process, Pool
import multiprocessing as mp
import logging
import warnings

# logging.basicConfig(level=logging.WARNING, format='(%(process)-9s) %(message)s',)
# warnings.filterwarnings(action='ignore')

###############
def youtube(url):
    vPafy = pafy.new(url)
    play = vPafy.getbest(preftype="any")
    return play.url
###############

if __name__ == '__main__':

    # Stream by web for test
    url = []
    url.append('https://www.youtube.com/watch?v=vL11zZZENtg')
    url.append('https://www.youtube.com/watch?v=cIUadXWD45Y')
    url.append('https://www.youtube.com/watch?v=i_2TnX0Xc5c')
    url.append('https://www.youtube.com/watch?v=7N3o0ZJLFJg')
    url.append('https://www.youtube.com/watch?v=86EB_ZrJE5g')
    url.append('https://www.youtube.com/watch?v=iFd8R4MXfzw')
    url.append('https://www.youtube.com/watch?v=xvX_BFYXQv0')
    url.append('https://www.youtube.com/watch?v=B8AN_SFRO0w')
    url.append('https://www.youtube.com/watch?v=oJiIPDyuPyk')
    url.append('https://www.youtube.com/watch?v=ChjHlfmwcys')

    # python 3.8 이상부터는 spawn 안써도됨 하지만 tensorflow1.14 때문에 python3.6 써야되서 필요
    mp.set_start_method('spawn')
    p = Pool(processes=10)

    for u in url:
        p.apply_async(func=multi_analy.Analy_esrc, args=(youtube(u), 'Thread-1',)).ready()
