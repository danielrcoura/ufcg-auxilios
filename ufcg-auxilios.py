#!/usr/bin/env python
# coding: utf-8

import urllib2
import string
import webbrowser


def find_linha(request, start):
    start = string.find(request, '<a', start)
    end = string.find(request, 'a>', start)

    if start == -1:
        return '', 0, -1
    elif string.find(request, 'PRAC', start, end) == -1:
        return '', end, -2
    else:
        if 'edital' in request[start:end].lower():
            return request[start:end + 2], start, 1
        elif 'resultado' in request[start:end].lower():
            return request[start:end + 2], start, 2
        elif 'comunicado' in request[start:end].lower():
            return request[start:end + 2], start, 3
        else:
            return request[start:end + 2], start, 4


def count_news(request):
    arq = open('qtd_editais.txt', 'r')
    qtd = int(arq.readline())
    arq.close()

    arq = open('qtd_editais.txt', 'w')
    cont = request.count('PRAC')
    arq.write(str(cont))
    arq.close()

    return cont - qtd


def delegate(start, qtd_news):
    editais = ''
    resultados = ''
    comunicados = ''
    diversos = ''

    while True:
        linha, start, status = find_linha(request, start + 1)

        if status == -1:
            break

        if status != -2:
            conteudo = ''
            if qtd_news != 0:
                qtd_news -= 1
                conteudo += "<tr class='active'>"
            else:
                conteudo += '<tr>'

            conteudo += '<td>' + linha + '</td></tr>'

            if status == 1:
                editais += conteudo
            elif status == 2:
                resultados += conteudo
            elif status == 3:
                comunicados += conteudo
            elif status == 4:
                diversos += conteudo

    return editais, resultados, comunicados, diversos


def divide_tabs(tabs):
    divs = "<div class='tab-content'>"
    for i in xrange(4):
        if i == 0:
            divs += "<div class='tab-pane active' id='panel-" + \
                str(i + 1) + "'>"
        else:
            divs += "<div class='tab-pane' id='panel-" + str(i + 1) + "'>"

        divs += "<table class='table table-hover'>"
        divs += tabs[i]
        divs += "</table></div>"
    divs += "</div>"

    return divs


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

TABS = """
<div class="tabbable" id="tabs-554919">
<ul class="nav nav-tabs">
<li class="active">
<a href="#panel-1" data-toggle="tab">Editais</a>
</li>
<li>
<a href="#panel-2" data-toggle="tab">Resultados</a>
</li>
<li>
<a href="#panel-3" data-toggle="tab">Comunicados</a>
</li>
<li>
<a href="#panel-4" data-toggle="tab">Diversos</a>
</li>
</ul>
"""

FOOT = """
</div>
</div>
</div>
</div>
<script src="js/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/scripts.js"></script>
</body>
"""

URL = 'http://www.ufcg.edu.br/prt_ufcg/concursos/concursos.php'

request = urllib2.urlopen(URL).read().decode('utf-8', 'ignore')
qtd_news = count_news(request)

TITLE = """
<div class="page-header" style="margin-bottom: 30px;">
<h1>
Editais de auxílio <span style="font-size:20px; color:gray;">
""" + str(qtd_news) + """ novas atualizações</span>
</h1>
</div>
"""

content = (HEAD + TITLE + TABS).decode('utf-8', 'ignore')

tabs = delegate(string.find(request, '<body>'), qtd_news)
divs = divide_tabs(tabs)

content += divs
content += FOOT

arq = open('index.html', 'w')
arq.write(content.encode('utf-8', 'ignore'))
arq.close()

webbrowser.open('./index.html', autoraise=True)
