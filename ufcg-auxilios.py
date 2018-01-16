#!/usr/bin/env python
# coding utf-8

import urllib2
import string


def find_edital(request, start_index):
    start = string.find(request, '<a', start_index)
    end = string.find(request, 'a>', start_index)

    if start == -1:
        return '', 0, -1
    elif string.find(request, 'PRAC', start, end) == -1:
        return '', end, -2
    else:
        return request[start:end + 2], start, 1


url = 'http://www.ufcg.edu.br/prt_ufcg/concursos/concursos.php'
request = urllib2.urlopen(url).read()
start_index = string.find(request, '<body>')

cont = 0
while True:
    edital, start_index, status = find_edital(request, start_index + 1)

    if status == -1:
        break

    if status != -2:
        print edital
        cont += 1

print cont
