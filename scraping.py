import time
import pandas as pd
import bs4
import requests
import datetime

def get_soup(url: str):
    """ ### get_soup
    Faz uma requisição GET para a URL passada como parâmetro e
    retorna um objeto do tipo BeautifulSoup
    """

    html_content = requests.get(url).text
    soup = bs4.BeautifulSoup(html_content, 'lxml')
    return soup

def load_soap_data(soap_data, proposicao:int, ano:int):
    """ ### load_soap_data
    Interpreta os dados oriundos de uma página HTML
    parâmetros:
    * soap_data: objeto do tipo BeautifulSoup com os dados do HTML
    * proposicao: número da proposição
    * ano: ano da proposição (data inicial: 1997)
    """

    # obtém a lista de chave e valores oriundos do body da pagina
    keys = soap_data.find_all('dt')
    values = soap_data.find_all('dd')
    values = soap_data.find_all('dd')

    # cria um dict baseando-se na zipagem das listas
    dados = {
      key.get_text().lower(): value.get_text()
      for key, value in zip(keys, values)
    }

    # obtem o texto do paragrafo
    texto = soap_data.find('p').get_text()

    # cria um novos keys para armazenar os dados extras
    dados['texto'] = texto
    dados['proposicao'] = proposicao
    dados['ano'] = ano

    return dados

def get_data():
    """### get_data
    Obtém dados a partir do web scraping da pagina *legislador*
    """

    # define mecanismos de manipulação da URL
    url_base = "https://www.legislador.com.br//LegisladorWEB.ASP?WCI=ProposicaoTexto&ID=3&TPProposicao=1&nr"
    url_dynamic =  lambda prop, ano: f'{url_base}Proposicao={prop}&aaProposicao={ano}'

    # define dadas de inicio e fim da execução
    end_year = datetime.datetime.now().year + 1
    start_year = 2022

    result = []

    for ano in range(start_year, end_year):
        proposicao = 1
        raw_data = get_soup( url_dynamic(proposicao, ano) )
        has_data = len(raw_data.findAll('dt')) > 0

        while has_data:

            # para o processo apenas para agilizar os testes
            if proposicao >= 11: break

            result.append(load_soap_data(raw_data, proposicao, ano))

            proposicao += 1
            raw_data = get_soup( url_dynamic(proposicao, ano) )
            has_data = len(raw_data.findAll('dt')) > 0

            print('proposicao:', f'{ano}-{proposicao}', end='\r')

        print(f'Total de Preposições em {ano}:', proposicao)


    return result