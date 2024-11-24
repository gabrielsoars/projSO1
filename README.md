# Simulação de Rede de Entregas
Este projeto implementa uma simulação concorrente de uma rede de entregas, onde encomendas são transportadas por veículos entre pontos de redistribuição. Ele utiliza conceitos de sincronização com threads, semáforos e filas, simulando a logística de transporte.

1.  **Classes**
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
        * `pontos` (list): Lista de pontos de redistribuição disponíveis.
        * `encomendas` (list): Lista de encomendas atualmente carregadas no veículo.
      - **Métodos**:
        * `run()`:
        * Carrega encomendas: Verifica a fila do ponto atual e carrega encomendas disponíveis, respeitando a capacidade do veículo.
        * Transporta encomendas: Simula o transporte para um ponto de destino escolhido aleatoriamente.
        * Descarrega encomendas: Marca as encomendas entregues ao chegar no devido destino.
2. **Funcionalidades**
    - Simulação de transporte de encomendas por veículos entre pontos de redistribuição.
    - Gerenciamento de filas em pontos de redistribuição.
    - Sincronização de acesso exclusivo a pontos de redistribuição usando semáforos.
    - Geração de arquivos de rastro para cada encomenda, detalhando sua movimentação.
3. **Tecnologias utilizadas**
    - Linguagem: Python.
    - Bibliotecas: `threading`, `random`, `time`, `datetime`.
