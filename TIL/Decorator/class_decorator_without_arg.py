# -*- coding: utf-8 -*-

'''
# 클래스형 데코레이터 #
얼마 전에 책을 샀다.
 이 책의 총 페이지 수는 513페이지인데, 첫 날에 읽은 페이지 수는 37페이지였다.
그 다음날에는 40페이지를 읽었고 그 다음날에는 46페이지를 읽었다.
나는 이 패턴대로 책을 읽는다면 책을 전부 읽는데 걸리는 총 날짜가 궁금해서 계산해보았다.
 그리고 덤으로 매일매일 읽은 페이지수도 계산해보자.
'''

# 좋아. 이 책을 읽어볼까?
class readingTheBook:
    def __init__(self, function):
        self.function = function
        self.total_page = 513
        self.amount_read = []
        self.add_read = 3

    def __call__(self, reading, days):
        if self.total_page > 0:
            self.total_page = self.total_page - reading
            days += 1 # 하루가 지났네..
            self.amount_read.append([reading, days]) # 얼마나 읽었는지 기록해놔야지..
            reading += self.add_read  # 오늘 이렇게나 읽었다!
            self.add_read += 3  # 더욱 열심히 읽어보자.
            self.__call__(reading, days)
        else:
            return self.function(self.amount_read, days)

# 책읽기를 시작하자.
@readingTheBook
def read_books(page, days):
    for page_read, day in page:
        print '{}일째 {} 만큼 읽었네'.format(day, page_read)
    print '걸린 날짜 : {}일'.format(days)
    return True

read_books(37, 0)
