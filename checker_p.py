import re
import requests as rq
from bs4 import BeautifulSoup as bs

def checker(tracking_code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Referer':'https://www2.correios.com.br/sistemas/rastreamento/default.cfm'       
    }
    url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'
    data = {'objetos': tracking_code, 'btnPesq': 'Buscar', 'acao': 'track'}

    res = rq.post(url=url, headers=headers, data=data)
    source = bs(res.text, 'html.parser')

    entregue = source.find('div', {'id':'DataEntrega'})


    dt_events = source.find_all('td', {'class': 'sroDtEvent'})
    lb_events = source.find_all('td', {'class': 'sroLbEvent'})
    
    regex = re.compile(r'\n\r\t')

    eventos = []

    for dt, lb, in zip(dt_events, lb_events):
        event = {}
        dt_info = regex.sub(' ', dt.text).split()
        event['data'], event['hora'] = dt_info[:2]
        event['local'] = ' '.join(dt_info[2:])
        event['mensagem'] = ' '.join(regex.sub(' ', lb.text).split())
        eventos.append(event)
    
    entreg = {}
    try:
        if entregue.text.strip():
            entreg['Entregue'] = 'Sim'
        else:
            entreg['Entregue'] = 'Não'
        eventos.insert(0, entreg)
    except Exception as e:
        pass

    return eventos
