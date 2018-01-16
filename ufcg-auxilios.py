#!/usr/bin/env python
# coding: utf-8

import urllib2
import string
import webbrowser


def find_edital(request, start_index):
    start = string.find(request, '<a', start_index)
    end = string.find(request, 'a>', start_index)

    if start == -1:
        return '', 0, -1
    elif string.find(request, 'PRAC', start, end) == -1:
        return '', end, -2
    else:
        return request[start:end + 2], start, 1


def count_news(request):
    arq = open('qtd_editais.txt', 'r')
    qtd = int(arq.readline())
    arq.close()

    arq = open('qtd_editais.txt', 'w')
    cont = request.count('PRAC')
    arq.write(str(cont))
    arq.close()

    return cont - qtd


HEAD = """
<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>UFCG auxílios</title>
    <meta name="description" content="Source code generated using layoutit.com">
    <meta name="author" content="LayoutIt!">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
  </head>
  <body>
    <div class="container">
	<div class="row">
		<div class="col-md-12">
"""

FOOT = """
</table>
</div>
</div>
</div>
</body>
"""

URL = 'http://www.ufcg.edu.br/prt_ufcg/concursos/concursos.php'

request = urllib2.urlopen(URL).read().decode('utf-8', 'ignore')
start_index = string.find(request, '<body>')

arq = open('index.html', 'w')
arq.write(HEAD)

cont_editais = count_news(request)

TITLE = """
<div class="page-header" style="margin-bottom: 30px;">
	<h1>
		Editais de auxílio <span style="font-size:20px; color:gray;">
""" + str(cont_editais) + """ novas atualizações</span>
	</h1>
</div>
"""
arq.write(TITLE)

arq.write("<table class='table table-hover'>")
while True:
    edital, start_index, status = find_edital(request, start_index + 1)

    if status == -1:
        break

    if status != -2:
        if cont_editais != 0:
            cont_editais -= 1
            arq.write("<tr class='active'>")
        else:
            arq.write("<tr>")
        arq.write('<td>')
        arq.write(edital)
        arq.write('</td>')

arq.write(FOOT)
arq.close()

webbrowser.open('./index.html', autoraise=True)
