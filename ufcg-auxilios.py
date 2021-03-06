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
    editais = resultados = comunicados = diversos = ''
    qtd_e = qtd_r = qtd_c = qtd_d = 0

    while True:
        linha, start, status = find_linha(request, start + 1)

        if status == -1:
            break

        is_new = False
        if status != -2:
            conteudo = ''
            if qtd_news != 0:
                qtd_news -= 1
                conteudo += "<tr class='active'>"
                is_new = True
            else:
                conteudo += '<tr>'

            conteudo += '<td>' + linha + '</td></tr>'

            if status == 1:
                editais += conteudo
                if is_new:
                    qtd_e += 1
            elif status == 2:
                resultados += conteudo
                if is_new:
                    qtd_r += 1
            elif status == 3:
                comunicados += conteudo
                if is_new:
                    qtd_c += 1
            else:
                diversos += conteudo
                if is_new:
                    qtd_d += 1

    return [editais, resultados, comunicados, diversos], [qtd_e, qtd_r, qtd_c, qtd_d]


def draw_tabs(qtd_news):
    classes = ['Editais ', 'Resultados ', 'Comunicados ', 'Diversos ']
    tabs = "<div class='tabbable' id='tabs-554919'><ul class='nav nav-tabs'>"
    for i in xrange(4):
        if i == 0:
            tabs += "<li class='active'>"
        else:
            tabs += "<li>"
        if qtd_news[i] == 0:
            qtd_news[i] = ''
        tabs += "<a href='#panel-" + \
            str(i + 1) + "' data-toggle='tab'>" + \
            classes[i] + "<strong>" + str(qtd_news[i]) + "</strong></a></li>"
    tabs += '</ul>'

    return tabs


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

content = (HEAD + TITLE).decode('utf-8', 'ignore')

content_tabs, qtd_news = delegate(string.find(request, '<body>'), qtd_news)

content += draw_tabs(qtd_news)
content += divide_tabs(content_tabs)
content += FOOT

arq = open('index.html', 'w')
arq.write(content.encode('utf-8', 'ignore'))
arq.close()

webbrowser.open('./index.html', autoraise=True)
