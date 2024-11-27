# Simulação de Rede de Entregas
Este projeto implementa uma simulação concorrente de uma rede de entregas, onde encomendas são transportadas por veículos entre pontos de redistribuição. Ele utiliza conceitos de sincronização com threads, semáforos e filas, simulando a logística de transporte.

## Estrutura
1. **Fluxo da simulação**
   - Usuário define o número de pontos de redistribuição, veículos, encomendas e capacidade de carga por veículo.
   - Os pontos, pacotes e veículos são inicializados e executados como threads.
   - Pontos de Redistribuição:
       - Cada ponto de redistribuição mantém uma fila de encomendas e utiliza semáforos para garantir que apenas um veículo por vez possa acessar o ponto.
   - Encomendas:
       - Cada pacote é criado com origem e destino aleatórios.
       - As threads dos pacotes adicionam as encomendas à fila do ponto de origem.
   - Veículos:
       - Cada veículo percorre os pontos de redistribuição, carregando pacotes e entregando-os nos destinos.
       - As entregas dos pacotes são registradas em um arquivo de log (entregas.txt).
   - A simulação termina quando todas as threads de veículos e pacotes são concluídas.
   - Durante a execução é exibido um monitoramento em tempo real do fluxo das encomendas pra complementar o arquivo de log gerado.

2. **Classes**
    - **Ponto**
      - **Descrição**: Representa um ponto de redistribuição, onde as encomendas aguardam para serem carregadas por veículos.
      - **Atributos**:
        * `id` (int): Identificador do ponto;
        * `fila` (list): Lista de encomendas aguardando transporte;
        * `semaforo` (`threading.Semaphore`): Controla o acesso exclusivo ao ponto para um veículo por vez.
      - **Métodos:**
        * `add_package:` Adiciona uma encomenda à fila do ponto;
        * `get_package:` Remove e retorna a encomenda mais antiga da fila, ou `None` se a fila estiver vazia.
    - **Pacote**
      - **Descrição**: Representa uma encomenda a ser transportada entre pontos.
      - **Atributos**:
        * `id` (int): Identificador único do pacote;
        * `origem` (`Ponto`): Ponto de redistribuição de origem;
        * `destino` (`Ponto`): Ponto de redistribuição de destino;
        * `horaCarregamento` (datetime): Horário em que o pacote foi carregado no veículo.
        * `horaEntrega` (datetime): Horário em que o pacote foi entregue no destino.
        * `idVeiculo` (int): Identificador do veículo que transportou o pacote.
        * `horaCriacao` (datetime): Horário de criação da encomenda.
      - **Métodos:**
        * `entregar`:
          * Marca o pacote como entregue no destino.
          * Registra o horário de entrega e o veículo responsável.
          * Gera um log e arquivo de rastro da encomenda.
    - **Veiculo**
      - **Descrição**: Representa um veículo que transporta encomendas entre os pontos de redistribuição.
      - **Atributos**:
        * `id` (int): Identificador do veículo.
        * `capacidade` (int): Capacidade máxima de carga do veículo.
        * `encomendas` (list): Lista de encomendas atualmente carregadas no veículo.
      - **Métodos**:
        * `run()`:
            * Carrega encomendas: Verifica a fila do ponto atual e carrega encomendas disponíveis, respeitando a capacidade do veículo.
            * Transporta encomendas: Simula o transporte para um ponto de destino escolhido aleatoriamente.
            * Descarrega encomendas: Marca as encomendas entregues ao chegar no devido destino.

3. **Funcionalidades**
    - Simulação de transporte de encomendas por veículos entre pontos de redistribuição.
    - Gerenciamento de filas em pontos de redistribuição.
    - Sincronização de acesso exclusivo a pontos de redistribuição usando semáforos.
    - Geração de arquivos de rastro para cada encomenda, detalhando sua movimentação.

4. **Tecnologias utilizadas**
    - Linguagem: Python.
    - Bibliotecas: `threading`, `random`, `time`, `datetime`.
  
## Execução
### Entradas
O programa solicita os seguintes parâmetros ao usuário:
- S: Número de pontos de redistribuição.
- C: Número de veículos.
- P: Número de encomendas.
- A: Capacidade máxima de carga de cada veículo.

### Exemplo de execução
Utilize `python main.py` para executar uma simulação.

### Monitoramento
Como saída para o programa, o sistema registra o deslocamento dos veículos, carregamento e entrega das encomendas no console.
Exemplo de saída:
```
Ponto X aberto.
Veiculo Y chegou ao ponto X.
Veiculo Y carregou a encomenda Z em X.
Veiculo Y esta viajando de X para V.
Veiculo Y chegou ao ponto V.
Veiculo Y entregou a encomenda Z em V.
```
Além disso, também é possível visualizar as informações de cada encomenda no arquivo de rastro gerado.
Exemplo de arquivo de rastro:
```
Encomenda Z
Origem: X -> Destino: V
Chegada ao ponto de origem: 2024-11-27 01:35:33.893311
Carregada no veiculo Y às: 2024-11-27 01:35:33.893311
Descarregada em V às: 2024-11-27 01:35:35.514473
```
