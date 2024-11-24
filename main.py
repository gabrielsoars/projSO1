import threading
import random
import time
from datetime import datetime

# Função para escrever mensagens no arquivo 'entregas.txt'
def escreverLog(mensagem):
    with open("entregas.txt", "a") as arquivoLog:
        arquivoLog.write(mensagem + "\n")

# Classe de ponto de redistribuição
class Ponto:
    def __init__(self, id):
        self.id = id
        self.fila = []
        self.semaforo = threading.Semaphore()

    def add_package(self, pacote):
        """Adicionar encomenda a fila do ponto de redistribuição."""
        self.fila.append(pacote)

    def get_package(self):
        """Retirar uma encomenda da fila do ponto de redistribuiaoo (se houver)."""
        if self.fila:
            return self.fila.pop(0)
        return None

# Classe para representar uma encomenda
class Pacote:
    def __init__(self, id, origem, destino):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.horaCarregamento = None
        self.horaEntrega = None
        self.idVeiculo = None
        self.horaCriacao = datetime.now()

    def entregar(self, idVeiculo):
        """Simula o descarregamento da encomenda no ponto de destino."""
        self.horaEntrega = datetime.now()
        self.idVeiculo = idVeiculo
        
        # Log para o arquivo de entregas
        escreverLog(f"Encomenda {self.id} entregue em {self.destino.id} (via veiculo {idVeiculo})")
        
        # Gerar arquivo de rastro da encomenda
        self.gerarRastro()

    def gerarRastro(self):
        """Gera o rastro da encomenda no arquivo 'entregas.txt'."""
        dadosRastro = f"Encomenda {self.id}\n"
        dadosRastro += f"Origem: {self.origem.id} -> Destino: {self.destino.id}\n"
        dadosRastro += f"Chegada ao ponto de origem: {self.horaCriacao}\n"
        dadosRastro += f"Carregada no veiculo {self.idVeiculo} às: {self.horaCarregamento}\n"
        dadosRastro += f"Descarregada em {self.destino.id} às: {self.horaEntrega}\n"
        
        # Salvar o rastro no arquivo 'entregas.txt'
        escreverLog(dadosRastro)

# Classe para representar um Veiculo
class Veiculo(threading.Thread):
    def __init__(self, id, capacidade, pontos):
        threading.Thread.__init__(self)
        self.id = id
        self.capacidade = capacidade
        self.pontos = pontos
        self.encomendas = []

    def run(self):
        """Execução do thread de um veiculo."""
        while True:
            # Escolher um ponto aleatório para começar
            local_atual = random.choice(self.pontos)

            # Tentar carregar encomendas neste ponto
            local_atual.semaforo.acquire()
            escreverLog(f"Veiculo {self.id} chegou ao ponto {local_atual.id}.")
            
            # Carregar encomendas (não ultrapassando a capacidade do Veiculo)
            while len(self.encomendas) < self.capacidade:
                pacote = local_atual.get_package()
                if pacote:  # Se houver encomenda no ponto, carrega
                    pacote.horaCarregamento = datetime.now()
                    self.encomendas.append(pacote)
                    escreverLog(f"Veiculo {self.id} carregou a encomenda {pacote.id} em {local_atual.id}.")
                else:
                    break
            local_atual.semaforo.release()

            # Simular o tempo de viagem até o próximo ponto (aleatório)
            time.sleep(random.uniform(0.5, 2.0))

            if not self.encomendas:
                escreverLog(f"Veiculo {self.id} finalizou as entregas.")
                break

            # Escolher o próximo ponto (pode ser o próximo na lista ou aleatório)
            pontoDestino = random.choice(self.pontos)
            escreverLog(f"Veiculo {self.id} esta viajando de {local_atual.id} para {pontoDestino.id}.")

            # Simula o descarregamento das encomendas no ponto de destino
            for pacote in self.encomendas:
                pacote.entregar(self.id)

            # Limpar a carga do Veiculo após descarregar as encomendas
            self.encomendas = []

def main():
    # Definição dos parâmetros
    S = 5  # Pontos de redistribuição
    C = 3  # Veiculos
    P = 10  # Encomendas
    A = 2  # Capacidade do Veiculo

# try:
#     S = int(input("Quantidade de pontos de redistribuição: "))
#     C = int(input("Quantidade de veículos: "))
#     P = int(input("Quantidade de encomendas: "))
#     A = int(input("Capacidade de carga de cada veículo: "))
# except ValueError:
#     print("Entrada inválida. Todos os argumentos devem ser números inteiros.")
#     exit()

    pontos = [Ponto(i) for i in range(S)]

    pacotes = [Pacote(i, pontos[random.randint(0, S-1)], pontos[random.randint(0, S-1)]) for i in range(P)]

    for pacote in pacotes:
        pacote.origem.add_package(pacote)

    veiculos = [Veiculo(i, A, pontos) for i in range(C)]

    for veiculo in veiculos:
        veiculo.start()

    for veiculo in veiculos:
        veiculo.join()

    escreverLog("[Finalizado] Simulacao terminada.")

if __name__ == "__main__":
    main()
