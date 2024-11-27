import threading
import random
import time
from datetime import datetime

encomendasEntregues = 0

# Função para abrir o arquivo de log "entregas.txt"
def abrirLog():
    return open("entregas.txt", "w")

# Função para escrever mensagens no arquivo 'entregas.txt'
def escreverLog(mensagem):
    global arquivoLog
    arquivoLog.write(mensagem + "\n")

# Classe de ponto de redistribuição
class Ponto(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.fila = []
        self.semaforo = threading.Semaphore()

    def add_package(self, pacote):
        """Adicionar encomenda a fila do ponto de redistribuição."""
        self.fila.append(pacote)

    def get_package(self):
        """Retirar uma encomenda da fila do ponto de redistribuição (se houver)."""
        if self.fila:
            return self.fila.pop(0)
        return None
    
    def run(self):
        print(f"Ponto {self.id} aberto.")

# Classe para representar uma encomenda
class Pacote(threading.Thread):
    def __init__(self, id, origem, destino):
        super().__init__()
        self.id = id
        self.origem = origem
        self.destino = destino
        self.horaCarregamento = None
        self.horaEntrega = None
        self.idVeiculo = None
        self.horaCriacao = datetime.now()

    def entregar(self, veiculo):
        global encomendasEntregues

        """Simula o descarregamento da encomenda no ponto de destino."""
        self.horaEntrega = datetime.now()
        self.idVeiculo = veiculo.id
        
        veiculo.capacidade += 1
        encomendasEntregues += 1
        veiculo.encomendas.remove(self)
        print(f"Veiculo {veiculo.id} entregou a encomenda {self.id} em {self.destino.id}.")

    def gerarRastro(self):
        """Gera o rastro da encomenda no arquivo 'entregas.txt'."""
        dadosRastro = f"Encomenda {self.id}\n"
        dadosRastro += f"Origem: {self.origem.id} -> Destino: {self.destino.id}\n"
        dadosRastro += f"Chegada ao ponto de origem: {self.horaCriacao}\n"
        dadosRastro += f"Carregada no veiculo {self.idVeiculo} às: {self.horaCarregamento}\n"
        dadosRastro += f"Descarregada em {self.destino.id} às: {self.horaEntrega}\n"
        dadosRastro += f"Entregue pelo veiculo {self.idVeiculo}\n"
        
        # Salvar o rastro no arquivo 'entregas.txt'
        escreverLog(dadosRastro)

    def run(self):
        self.origem.add_package(self)

# Classe para representar um Veiculo
class Veiculo(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.capacidade = A
        self.encomendas = []

    def run(self):
        """Execução do thread de um veiculo."""

        # Escolher um ponto aleatório para começar
        local_atual = random.choice(pontos)

        while True:
            # Tentar carregar encomendas neste ponto
            local_atual.semaforo.acquire()
            try:
                print(f"Veiculo {self.id} chegou ao ponto {local_atual.id}.")
                
                # Carregar encomendas (não ultrapassando a capacidade do Veiculo)
                while len(self.encomendas) <= self.capacidade:
                    pacote = local_atual.get_package()
                    if pacote:  # Se houver encomenda no ponto, carrega
                        pacote.horaCarregamento = datetime.now()
                        self.encomendas.append(pacote)
                        self.capacidade -= 1
                        print(f"Veiculo {self.id} carregou a encomenda {pacote.id} em {local_atual.id}.")
                    else:
                        break

                # Simular o tempo de viagem até o próximo ponto (aleatório)
                time.sleep(random.uniform(0.5, 2.0))

                if not self.encomendas:
                    print(f"Veiculo {self.id} finalizou as entregas.")
                    break
            finally:
                local_atual.semaforo.release()

            pontoDestino = pontos[(pontos.index(local_atual) + 1) % S]
            print(f"Veiculo {self.id} esta viajando de {local_atual.id} para {pontoDestino.id}.")
            local_atual = pontoDestino

            # Simula o descarregamento das encomendas no ponto de destino
            for pacote in self.encomendas:
                if (pacote.destino == pontoDestino):
                    pacote.entregar(self)

# Definição dos parâmetros
try:
    S = int(input("Quantidade de pontos de redistribuição: "))
    C = int(input("Quantidade de veículos: "))
    P = int(input("Quantidade de encomendas: "))
    A = int(input("Capacidade de carga de cada veículo: "))
except ValueError:
    print("Entrada inválida. Todos os argumentos devem ser números inteiros.")
    exit()

arquivoLog = abrirLog()

pontos = [Ponto(i) for i in range(S)]

for ponto in pontos:
    ponto.start()

for ponto in pontos:
    ponto.join()

pacotes = [Pacote(i, pontos[random.randint(0, S-1)], pontos[random.randint(0, S-1)]) for i in range(P)]

for pacote in pacotes:
    pacote.start()

for pacote in pacotes:
    pacote.join()

veiculos = [Veiculo(i) for i in range(C)]

for veiculo in veiculos:
    veiculo.start()

for veiculo in veiculos:
    veiculo.join()

escreverLog(f"Entregas planejadas: {P}")
escreverLog(f"Entregas realizadas: {encomendasEntregues}\n")
for pacote in pacotes:
    pacote.gerarRastro()
escreverLog("[Finalizado] Simulacao terminada.")
arquivoLog.close()