import requests # Importa o módulo requests para fazer requisições HTTP
import json # Importa o módulo json para converter o resultado em JSON
import time # Importa o módulo time para fazer o sleep
from prometheus_client import start_http_server, Gauge # Importa o módulo Gauge do Prometheus para criar a nossa métrica e o módulo start_http_server para iniciar o servidor

url_numero_pessoas = 'http://api.open-notify.org/astros.json' # URL para pegar o número de astronautas
url_local_ISS = 'http://api.open-notify.org/iss-now.json' # URL para pegar a localização do ISS

def pega_local_ISS(): # Função para pegar a localização da ISS
    try:
        """
        Pegar o local da estação espacial internacional
        """
        response = requests.get(url_local_ISS) # Faz a requisição para a URL
        data = response.json() # Converte o resultado em JSON
        return data['iss_position'] # Retorna o resultado da requisição
    except Exception as e: # Caso ocorra algum erro
        print("Não foi possível acessar a url!") # Imprime uma mensagem de erro
        raise e # Lança a exceção

def pega_numero_astronautas(): # Função para pegar o número de astronautas
    try: # Tenta fazer a requisição HTTP
        """
        Pegar o número de astronautas no espaço 
        """
        response = requests.get(url) # Faz a requisição HTTP
        data = response.json() # Converte o resultado em JSON
        return data['number'] # Retorna o número de astronautas
    except Exception as e: # Se der algum erro
        print("Não foi possível acessar a url!") # Imprime que não foi possível acessar a url
        raise e # Lança a exceção

def atualiza_metricas(): # Função para atualizar as métricas
    try:
        """
        Atualiza as métricas com o número de astronautas e local da estação espacial internacional
        """
        numero_pessoas = Gauge('numero_de_astronautas', 'Número de astronautas no espaço') # Cria a métrica para o número de astronautas
        longitude = Gauge('longitude_ISS', 'Longitude da Estação Espacial Internacional') # Cria a métrica para a longitude da estação espacial internacional
        latitude = Gauge('latitude_ISS', 'Latitude da Estação Espacial Internacional') # Cria a métrica para a latitude da estação espacial internacional

        while True: # Enquanto True
            numero_pessoas.set(pega_numero_astronautas()) # Atualiza a métrica com o número de astronautas
            longitude.set(pega_local_ISS()['longitude']) # Atualiza a métrica com a longitude da estação espacial internacional
            latitude.set(pega_local_ISS()['latitude']) # Atualiza a métrica com a latitude da estação espacial internacional
            time.sleep(10) # Faz o sleep de 10 segundos
            print("O número atual de astronautas no espaço é: %s" % pega_numero_astronautas()) # Imprime o número atual de astronautas no espaço
            print("A longitude atual da Estação Espacial Internacional é: %s" % pega_local_ISS()['longitude']) # Imprime a longitude atual da estação espacial internacional
            print("A latitude atual da Estação Espacial Internacional é: %s" % pega_local_ISS()['latitude']) # Imprime a latitude atual da estação espacial internacional
    except Exception as e: # Se der algum erro
        print("Problemas para atualizar as métricas! \n\n====> %s \n" % e) # Imprime que ocorreu um problema para atualizar as métricas
        raise e # Lança a exceção
        
def inicia_exporter(): # Função para iniciar o exporter
    try:
        """
        Iniciar o exporter
        """
        start_http_server(8899) # Inicia o servidor do Prometheus na porta 8899
        return True # Retorna True
    except Exception as e: # Se der algum erro
        print("O Servidor não pode ser iniciado!") # Imprime que não foi possível iniciar o servidor
        raise e # Lança a exceção

def main(): # Função principal
    try:
        inicia_exporter() # Inicia o exporter
        print('Exporter Iniciado') # Imprime que o exporter foi iniciado
        atualiza_metricas() # Atualiza as métricas
    except Exception as e: # Se der algum erro
        print('\nExporter Falhou e Foi Finalizado! \n\n======> %s\n' % e) # Imprime que o exporter falhou e foi finalizado
        exit(1) # Finaliza o programa com erro


if __name__ == '__main__': # Se o programa for executado diretamente
    main() # Executa o main
    exit(0) # Finaliza o programa

