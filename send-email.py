#!usr/bin/env python
# coding: utf-8

import urllib2
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def count_news(request):
    arq = open('qtd_editais.txt', 'r')
    qtd = int(arq.readline())
    arq.close()

    arq = open('qtd_editais.txt', 'w')
    cont = request.count('PRAC')
    arq.write(str(cont))
    arq.close()

    return cont - qtd


def find_linha(request, start):
    start = string.find(request, '<a', start)
    end = string.find(request, 'a>', start)

    if start == -1:
        return '', 0, -1
    elif string.find(request, 'PRAC', start, end) == -1:
        return '', end, -2
    else:
        if 'edital' in request[start:end].lower():
            status = 1
        elif 'resultado' in request[start:end].lower():
            status = 2
        elif 'comunicado' in request[start:end].lower():
            status = 3
        else:
            status = 4
    return "<li>" + request[start:end + 2] + "</li>", start, status


def delegate(start, qtd_news):
    editais = resultados = comunicados = diversos = ''

    while qtd_news:
        linha, start, status = find_linha(request, start + 1)

        if status != -2:
            qtd_news -= 1

            if status == 1:
                editais += linha
            elif status == 2:
                resultados += linha
            elif status == 3:
                comunicados += linha
            else:
                diversos += linha
    return editais, resultados, comunicados, diversos


URL = 'http://www.ufcg.edu.br/prt_ufcg/concursos/concursos.php'
request = urllib2.urlopen(URL).read().decode('utf-8', 'ignore')
qtd_news = count_news(request)

if qtd_news:
    topics = delegate(string.find(request, '<body>'), qtd_news)
    titles = ['Editais', 'Resultados', 'Comunicados', 'Diversos']

    content = "<h1>" + str(qtd_news) + " Novidades</h1>"
    for i in xrange(len(topics)):
        if topics[i] != '':
            content += "<h2>" + titles[i] + "</h2>"
            content += "<u>" + topics[i] + "</u>"

    arq = open('email.txt', 'r')
    email = arq.readline()
    senha = arq.readline()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "PRAC " + str(qtd_news) + " NOVAS ATUALIZAÇÕES"
    msg['From'] = email
    msg['To'] = email
    content = MIMEText(content, 'html')
    msg.attach(content)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(email, senha)
    smtp.sendmail(email, email, msg.as_string())
    smtp.quit()
else:
	print "Não há novas atualizações"
