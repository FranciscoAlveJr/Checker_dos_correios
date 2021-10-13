import random
import csv
import pandas as pd
import re
import requests as rq
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

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

siglas = ['AA - ETIQUETA LÓGICA SEDEX', 'AB - ETIQUETA LÓGICA SEDEX', 'AL - AGENTES DE LEITURA', 'AR - AVISO DE RECEBIMENTO', 'AS - ENCOMENDA PAC – AÇÃO SOCIAL', 'BE - REMESSA ECONÔMICA S/ AR DIGITAL', 'BF - REMESSA EXPRESSA S/ AR DIGITAL', 'BG - ETIQUETA LÓGICA REMESSA ECONÔMICA C/AR BG', 'BH - MENSAGEM FÍSICO-DIGITAL', 'BI - ETIQUETA LÓGICA REGISTRO URGENTE', 'BJ - ETIQUETA LÓGICA REMESSA EXPRESSA C/AR', 'CB - OBJETO INTERNACIONAL COLIS', 'CC - OBJETO INTERNACIONAL COLIS', 'CD - OBJETO INTERNACIONAL COLIS', 'CE - OBJETO INTERNACIONAL COLIS', 'CF - OBJETO INTERNACIONAL COLIS', 'CG - OBJETO INTERNACIONAL COLIS', 'CH - OBJETO INTERNACIONAL COLIS', 'CI - OBJETO INTERNACIONAL COLIS', 'CJ - OBJETO INTERNACIONAL COLIS', 'CK - OBJETO INTERNACIONAL COLIS', 'CL - OBJETO INTERNACIONAL COLIS', 'CM - OBJETO INTERNACIONAL COLIS', 'CN - OBJETO INTERNACIONAL COLIS', 'CO - OBJETO INTERNACIONAL COLIS', 'CP - OBJETO INTERNACIONAL COLIS', 'CQ - OBJETO INTERNACIONAL COLIS', 'CR - OBJETO INTERNACIONAL COLIS', 'CS - OBJETO INTERNACIONAL COLIS', 'CT - OBJETO INTERNACIONAL COLIS', 'CU - OBJETO INTERNACIONAL COLIS', 'CV - OBJETO INTERNACIONAL COLIS', 'CW - OBJETO INTERNACIONAL COLIS', 'CX - OBJETO INTERNACIONAL COLIS', 'CY - OBJETO INTERNACIONAL COLIS', 'CZ - OBJETO INTERNACIONAL COLIS', 'CA - OBJETO INTERNACIONAL COLIS', 'DA - ENCOMENDA SEDEX C/ AR DIGITAL', 'DB - REMESSA EXPRESSA C/ AR DIGITAL-BRADESCO', 'DC - REMESSA EXPRESSA (ÓRGÃO TRANSITO)', 'DD - DEVOLUÇÃO DE DOCUMENTOS', 'DE - REMESSA EXPRESSA C/ AR DIGITAL', 'DF - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'DG - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'DI - REMESSA EXPRESSA COM AR DIGITAL ITAU', 'DJ - ENCOMENDA SEDEX', 'DK - SEDEX EXTRA GRANDE', 'DL - SEDEX LÓGICO', 'DM - ENCOMENDA SEDEX', 'DN- ENCOMENDA SEDEX', 'DO - REMESSA EXPRESSA COM AR DIGITAL ITAU UNIBANCO', 'DP - SEDEX PAGAMENTO ENTREGA', 'DQ - REMESSA EXPRESSA COM AR DIGITAL BRADESCO', 'DR - REMESSA EXPRESSA COM AR DIGITAL SANTANDER', 'DS - REMESSA EXPRESSA COM AR DIGITAL SANTANDER', 'DT - REMESSA ECONÔMICA SEG. TRANSITO C/AR DIGITAL', 'DU - ENCOMENDA SEDEX', 'DV - SEDEX COM AR DIGITAL', 'DW - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'DX - SEDEX 10 LÓGICO', 'DY - ENCOMENDA SEDEX (ETIQUETA FÍSICA)', 'DZ - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'EA - OBJETO INTERNACIONAL EMS', 'EB - OBJETO INTERNACIONAL EMS', 'EC - ENCOMENDA PAC', 'ED - OBJETO INTERNACIONAL PACKET EXPRESS', 'EE - OBJETO INTERNACIONAL EMS', 'EF - OBJETO INTERNACIONAL EMS', 'EG - OBJETO INTERNACIONAL EMS', 'EH - OBJETO INTERNACIONAL EMS', 'EI - OBJETO INTERNACIONAL EMS', 'EJ - OBJETO INTERNACIONAL EMS', 'EK - OBJETO INTERNACIONAL EMS', 'EL - OBJETO INTERNACIONAL EMS', 'EM - SEDEX MUNDI', 'EN - OBJETO INTERNACIONAL EMS', 'EO - OBJETO INTERNACIONAL EMS', 'EP - OBJETO INTERNACIONAL EMS', 'EQ - ENCOMENDA SERVIÇO NÃO EXPRESSA ECT', 'ER - REGISTRADO', 'ES - OBJETO INTERNACIONAL EMS', 'ET - OBJETO INTERNACIONAL EMS', 'EU - OBJETO INTERNACIONAL EMS', 'EV - OBJETO INTERNACIONAL EMS', 'EW - OBJETO INTERNACIONAL EMS', 'EX - OBJETO INTERNACIONAL EMS', 'EY - OBJETO INTERNACIONAL EMS', 'EZ - OBJETO INTERNACIONAL EMS', 'FA - FAC REGISTRADO', 'FB - FAC REGISTRADO', 'FC - FAC REGISTRADO (5 DIAS)', 'FD - FAC REGISTRADO (10 DIAS)', 'FE - ENCOMENDA FNDE', 'FF - REGISTRADO DETRAN', 'FH - FAC REGISTRADO C/ AR DIGITAL', 'FJ - REMESSA ECONÔMICA C/ AR DIGITAL', 'FM - FAC REGISTRADO (MONITORADO)', 'FR - FAC REGISTRADO', 'IA - INTEGRADA AVULSA', 'IC - INTEGRADA A COBRAR', 'ID - INTEGRADA DEVOLUÇÃO DE DOCUMENTO', 'IE - INTEGRADA ESPECIAL', 'IF - CPF', 'II - INTEGRADA INTERNO', 'IK - INTEGRADA COM COLETA SIMULTÂNEA', 'IM - INTEGRADA MEDICAMENTOS', 'IN - OBJ DE CORRESPONDÊNCIA E EMS REC EXTERIOR', 'IP - INTEGRADA PROGRAMADA', 'IR - IMPRESSO REGISTRADO', 'IS - INTEGRADA STANDARD', 'IT - INTEGRADA TERMOLÁBIL', 'IU - INTEGRADA URGENTE', 'IX - EDEI ENCOMENDA EXPRESSA', 'JA - REMESSA ECONÔMICA C/AR DIGITAL', 'JB - REMESSA ECONÔMICA C/AR DIGITAL', 'JC - REMESSA ECONÔMICA C/AR DIGITAL', 'JD - REMESSA ECONÔMICA S/AR DIGITAL', 'JE - REMESSA ECONÔMICA C/AR DIGITAL', 'JF - REMESSA ECONÔMICA C/AR DIGITAL', 'JG - REGISTRADO PRIORITÁRIO', 'JH - REGISTRADO PRIORITÁRIO', 'JI - REMESSA ECONÔMICA S/AR DIGITAL', 'JJ - REGISTRADO JUSTIÇA', 'JK - REMESSA ECONÔMICA S/AR DIGITAL', 'JL - REGISTRADO LÓGICO', 'JM - MALA DIRETA POSTAL ESPECIAL', 'JN - MALA DIRETA POSTAL ESPECIAL', 'JO - REGISTRADO PRIORITÁRIO', 'JP - OBJETO RECEITA FEDERAL (EXCLUSIVO)', 'JQ - REMESSA ECONÔMICA C/AR DIGITAL', 'JR - REGISTRADO PRIORITÁRIO', 'JS - REGISTRADO LÓGICO', 'JT - REGISTRADO URGENTE', 'JU - ETIQUETA FÍSICA REGISTRO URGENTE', 'JV - REMESSA ECONÔMICA C/AR DIGITAL', 'JW - CARTA COMERCIAL A FATURAR (5 DIAS)', 'JX - CARTA COMERCIAL A FATURAR (10 DIAS)', 'JY - REMESSA ECONÔMICA (5 DIAS)', 'JZ - REMESSA ECONÔMICA (10 DIAS)', 'LA - LOGÍSTICA REVERSA SIMULTÂNEA SEDEX', 'LB - LOGÍSTICA REVERSA SIMULTÂNEA SEDEX', 'LC - OBJETO INTERNACIONAL PRIME', 'LD - OBJETO INTERNACIONAL PRIME', 'LE - LOGÍSTICA REVERSA ECONÔMICA', 'LF - OBJETO INTERNACIONAL PRIME', 'LG - OBJETO INTERNACIONAL PRIME', 'LH - OBJETO INTERNACIONAL PRIME', 'LI - OBJETO INTERNACIONAL PRIME', 'LJ - OBJETO INTERNACIONAL PRIME', 'LK - OBJETO INTERNACIONAL PRIME', 'LL - OBJETO INTERNACIONAL PRIME', 'LM - OBJETO INTERNACIONAL PRIME', 'LN - OBJETO INTERNACIONAL PRIME', 'LP - LOGÍSTICA REVERSA SIMULTÂNEA PAC', 'LQ - OBJETO INTERNACIONAL PRIME', 'LS - LOGÍSTICA REVERSA SEDEX', 'LV - LOGÍSTICA REVERSA EXPRESSA', 'LW - OBJETO INTERNACIONAL PRIME', 'LX - OBJETO INTERNACIONAL PACKET ECONÔMICA', 'LY - OBJETO INTERNACIONAL PRIME', 'LZ - OBJETO INTERNACIONAL PRIME', 'MA - TELEGRAMA – SERVIÇOS ADICIONAIS', 'MB - TELEGRAMA DE BALCÃO', 'MC - TELEGRAMA FONADO', 'MD - MAQUINA DE FRANQUEAR (LÓGICA)', 'ME - TELEGRAMA', 'MF - TELEGRAMA FONADO', 'MH - CARTA VIA INTERNET', 'MK - TELEGRAMA CORPORATIVO', 'MM - TELEGRAMA GRANDES CLIENTES', 'MP - TELEGRAMA PRÉ-PAGO', 'MS - ENCOMENDA SAÚDE', 'MT - TELEGRAMA VIA TELEMAIL', 'MY - TELEGRAMA INTERNACIONAL ENTRANTE', 'MZ - TELEGRAMA VIA CORREIOS ON LINE', 'NE - TELE SENA RESGATADA', 'NX - EDEI ENCOMENDA NÃO URGENTE', 'OA - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'OB - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'OC - ENCOMENDA SEDEX (ETIQUETA LÓGICA)', 'OD - ENCOMENDA SEDEX (ETIQUETA FÍSICA)', 'OF - ETIQUETA LÓGICA SEDEX', 'OG - ETIQUETA LÓGICA SEDEX', 'OH - ETIQUETA LÓGICA SEDEX', 'PA - PASSAPORTE', 'PB - ENCOMENDA PAC – NÃO URGENTE', 'PC - ENCOMENDA PAC A COBRAR', 'PD - ENCOMENDA PAC', 'PE - ENCOMENDA PAC (ETIQUETA FÍSICA)', 'PF - PASSAPORTE', 'PG - ENCOMENDA PAC (ETIQUETA FÍSICA)', 'PH - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'PI - ENCOMENDA PAC', 'PJ - ENCOMENDA PAC', 'PK - PAC EXTRA GRANDE', 'PL - ENCOMENDA PAC', 'PM - ENCOMENDA PAC (ETIQUETA FÍSICA)', 'PN - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'PO - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'PP - ETIQUETA LÓGICA PAC', 'PQ - ETIQUETA LOGICA PAC MINI', 'PR - REEMBOLSO POSTAL – CLIENTE AVULSO', 'PS - ETIQUETA LÓGICA PAC', 'PT - ENCOMENDA PAC', 'PU - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'PW - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'PX - ENCOMENDA PAC (ETIQUETA LÓGICA)', 'RA - REGISTRADO PRIORITÁRIO', 'RB - CARTA REGISTRADA', 'RC - CARTA REGISTRADA COM VALOR DECLARADO', 'RD - REMESSA ECONÔMICA DETRAN', 'RE - MALA DIRETA POSTAL ESPECIAL', 'RF - OBJETO DA RECEITA FEDERAL', 'RG - REGISTRADO DO SISTEMA SARA', 'RH - REGISTRADO COM AR DIGITAL', 'RI - REGISTRADO PRIORITÁRIO INTERNACIONAL', 'RJ - REGISTRADO AGÊNCIA', 'RK - REGISTRADO AGÊNCIA', 'RL - REGISTRADO LÓGICO', 'RM - REGISTRADO AGÊNCIA', 'RN - REGISTRADO AGÊNCIA', 'RO - REGISTRADO AGÊNCIA', 'RP - REEMBOLSO POSTAL – CLIENTE INSCRITO', 'RQ - REGISTRADO AGÊNCIA', 'RR - REGISTRADO INTERNACIONAL', 'RS - REM ECON ORG TRANSITO COM OU SEM AR', 'RT - REM ECON TALAO/CARTAO SEM AR DIGITA', 'RU - REGISTRADO SERVIÇO ECT', 'RV - REM ECON CRLV/CRV/CNH COM AR DIGITAL', 'RW - REGISTRADO INTERNACIONAL', 'RX - REGISTRADO INTERNACIONAL', 'RY - REM ECON TALAO/CARTAO COM AR DIGITAL', 'RZ - REGISTRADO', 'SA - ETIQUETA SEDEX AGÊNCIA', 'SB - SEDEX 10', 'SC - SEDEX A COBRAR', 'SD - REMESSA EXPRESSA DETRAN', 'SE - ENCOMENDA SEDEX', 'SF - SEDEX AGENCIA', 'SG - SEDEX DO SISTEMA SARA', 'SH - SEDEX COM AR DIGITAL', 'SI - SEDEX AGÊNCIA', 'SJ - SEDEX HOJE', 'SK - SEDEX AGÊNCIA', 'SL - SEDEX LÓGICO', 'SM - SEDEX 12', 'SN - SEDEX AGÊNCIA', 'SO - SEDEX AGÊNCIA', 'SP - SEDEX PRÉ-FRANQUEADO', 'SQ - SEDEX', 'SR - SEDEX', 'SS - SEDEX FÍSICO', 'ST - REMESSA EXPRESSA TALAO/CARTAO SEM AR DIGITAL', 'SU - ENCOMENDA SERVIÇO EXPRESSA ECT', 'SV - REMESSA EXPRESSA CRLV/CRV/CNH COM AR DIGITAL', 'SW - ENCOMENDA SEDEX', 'SX - SEDEX 10', 'SY - REMESSA EXPRESSA TALAO/CARTAO COM AR DIGITAL', 'SZ - SEDEX AGÊNCIA', 'TC - TESTE (OBJETO PARA TREINAMENTO)', 'TE - TESTE (OBJETO PARA TREINAMENTO)', 'TR - OBJETO TREINAMENTO – NÃO GERA PRÉ-ALERTA', 'TS - TESTE (OBJETO PARA TREINAMENTO)', 'VA - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'VC - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'VD - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'VE - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'VF - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'VV - OBJETO INTERNACIONAL COM VALOR DECLARADO', 'XA - AVISO CHEGADA OBJETO INT TRIBUTADO', 'XM - SEDEX MUNDI', 'XR - OBJETO INTERNACIONAL (PPS TRIBUTADO)', 'XX - OBJETO INTERNACIONAL (PPS TRIBUTADO)']   

paises = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'EM', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'ID', 'IE', 'IE', 'IL', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IQ', 'IR', 'IR', 'IS', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OA', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WO', 'WS', 'YE', 'YU', 'ZA', 'ZM', 'ZR', 'ZW']

def codigo():
    # Preferências do usuário
    try:
        btn_gerar.config(state=DISABLED, relief='sunken')
        num_inicial = vnum.get()
        if len(num_inicial) != 3:
            raise KeyError
        total_gerar = int(vtotal.get())
        sigla = cb_siglas.get()
        pais = cb_paises.get()

        parcela = 100/total_gerar
        etapa = 0

        # Gera um código um código com os dados anteriores
        gerados = [f'{sigla[:2]}{num_inicial}{"".join([str(random.randrange(10)) for a in range(6)])}{pais}' for i in range(total_gerar)]
        cont = 0

        vstatus.config(state=NORMAL)
        vstatus.delete('1.0', END)

        # Verifica se o código é válido e, se for, grava em um arquivo csv
        for codigo in gerados:
            try:
                etapa+=parcela
                barraVar.set(etapa)
                porcento['text'] = f'{int(etapa)} %'
                janela.update()
                if checker(codigo):
                    local = checker(codigo)[1]['local']
                    data = checker(codigo)[1]['data']
                    entregue = checker(codigo)[0]['Entregue']
                    vstatus.insert(INSERT, f'{codigo} - {local}\n')
                    cont+=1
                    with open('dados/cv.csv', 'a+', newline='', encoding='UTF-8') as arq:
                        writer = csv.writer(arq)
                        writer.writerow([codigo, local, data, entregue])
            except Exception:
                continue

        vstatus.insert(INSERT, f'\n{len(gerados)} códigos gerados. {cont} válidos.')
        vstatus.config(state=DISABLED)

        df = pd.read_csv('dados/cv.csv')
        locais = set(df['Local'].tolist())
        regioes = sorted(list(locais))
        regioes.insert(0, 'TODAS AS REGIÕES')

        cb_regioes['values'] = regioes
        porcento['text'] = '100 %'
        btn_gerar.config(state=NORMAL, relief='raised')
    except ValueError:
        messagebox.showerror(title='ERRO!', message='Não foi dada a quantidade de códigos a gerar.')
        btn_gerar.config(state=NORMAL, relief='raised')
    except KeyError:
        messagebox.showerror(title='ERRO!', message='A quantidade de números iniciais não é igual a 3.')
        btn_gerar.config(state=NORMAL, relief='raised')
    janela.update()

def reg_select():
    filtr.config(state=NORMAL)
    re = cb_regioes.get()  
    if cb_entreg.get() == 'ENTREGUE':
        ent = 'Sim'
    elif cb_entreg.get() == 'NÃO ENTREGUE':
        ent = 'Não'
    elif cb_entreg.get() == 'AMBOS':
        ent = 'ambos'
        
    df = pd.read_csv('dados/cv.csv')

    if re == 'TODAS AS REGIÕES':
        codigos_regiao = df['Codigo'].tolist()
        local_regiao = df['Local'].tolist()
        data_regiao = df['Data'].tolist()
        entreg_regiao = df['Entregue'].tolist()
        filtr.delete('1.0', END)

        for i in range(len(codigos_regiao)):
            codigo = codigos_regiao[i]
            local = local_regiao[i]
            data = data_regiao[i]
            entregue = entreg_regiao[i]
            if entregue == ent:
                filtr.insert(INSERT, f'Código: {codigo}, Local: {local}, Data: {data}, Entregue: {entregue}\n')
            if ent == 'ambos':
                filtr.insert(INSERT, f'Código: {codigo}, Local: {local}, Data: {data}, Entregue: {entregue}\n')
            janela.update()
    else:
        c_regiao = df[df.Local==re]
        codigos_regiao = c_regiao['Codigo'].tolist()
        local_regiao = c_regiao['Local'].tolist()
        data_regiao = c_regiao['Data'].tolist()
        entreg_regiao = c_regiao['Entregue'].tolist()
        filtr.delete('1.0', END)

        for i in range(len(codigos_regiao)):
            codigo = codigos_regiao[i]
            local = local_regiao[i]
            data = data_regiao[i]
            entregue = entreg_regiao[i]
            if entregue == ent:
                filtr.insert(INSERT, f'Código: {codigo}, Local: {local}, Data: {data}, Entregue: {entregue}\n')
            elif ent == 'ambos':
                filtr.insert(INSERT, f'Código: {codigo}, Local: {local}, Data: {data}, Entregue: {entregue}\n')
            janela.update()

    filtr.config(state=DISABLED)

def limpar():
    vnum.delete(0, END)
    vtotal.delete(0, END)

janela = Tk()
janela.title('Checker dos Correios')
janela.resizable(False, False)
janela.iconbitmap('dados/img.ico')

opts = StringVar()

barraVar = DoubleVar()
barraVar.set(0)

cb_siglas = ttk.Combobox(janela, values=siglas, width=55, state='readonly')
cb_siglas.set('Siglas dos Correios')
cb_siglas.grid(column=0, row=0, columnspan=2, padx=50, pady=15)

cb_paises = ttk.Combobox(janela, values=paises, state='readonly')
cb_paises.set('Países')
cb_paises.grid(column=2, row=0, columnspan=2, padx=40)

Label(janela, text="Número Inicial:").grid(column=0, row=2, pady=15)
vnum = Entry(janela)
vnum.place(x=160, y=68, width=50)

Label(janela, text="Total a gerar:").grid(column=1, row=2)
vtotal = Entry(janela)
vtotal.place(x=380, y=68)

btn_gerar = Button(janela, text='Gerar', command=codigo, width=20)
btn_gerar.grid(column=0, row=3, pady=15, columnspan=2)

btn_limpar = Button(janela, text='Limpar', command=limpar, width=20)
btn_limpar.grid(column=1, row=3, columnspan=2)

pb = ttk.Progressbar(janela, variable=barraVar, maximum=100, length=500)
pb.grid(column=0, row=5, columnspan=4)

porcento = Label(janela, text='0 %')
porcento.grid(column=3, row=5, columnspan=4)

vstatus = scrolledtext.ScrolledText(janela, width=70, height=10, font=('arial', 10), )
vstatus.config(state=DISABLED, relief='groove', bd=3)
vstatus.grid(column=0, row=6, columnspan=4, pady=15)

df = pd.read_csv('dados/cv.csv')
locais = set(df['Local'].tolist())
regioes = sorted(list(locais))
regioes.insert(0, 'TODAS AS REGIÕES')

cb_regioes = ttk.Combobox(janela, values=regioes, state='readonly', width=30)
cb_regioes.set('TODAS AS REGIÕES')
cb_regioes.grid(column=0, row=7, pady=15, padx=100, columnspan=2)

cb_entreg = ttk.Combobox(janela, values=['AMBOS', 'NÃO ENTREGUE', 'ENTREGUE'], state='readonly', width=15)
cb_entreg.set('NÃO ENTREGUE')
cb_entreg.grid(column=1, row=7, columnspan=2)

btn_filtrar = Button(janela, text='Filtrar', command=reg_select, width=20)
btn_filtrar.grid(column=0, row=8, columnspan=4)

filtr = scrolledtext.ScrolledText(janela, width=90, height=10, font=('arial', 10), wrap='word')
filtr.config(state=DISABLED, relief='groove', bd=3)
filtr.grid(column=0, row=9, columnspan=4, pady=20)

janela.mainloop()

