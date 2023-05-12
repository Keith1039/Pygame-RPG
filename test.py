#import os
file = open('event_text/event1.txt')
for i in range(10):
    print(file.readline())
    print(i)
