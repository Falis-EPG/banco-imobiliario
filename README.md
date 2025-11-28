🧩 Banco Imobiliário – Bus Edition
Um jogo multiplayer estilo Banco Imobiliário, feito para rodar offline em um notebook e acessível por celulares via hotspot.
📌 Sobre o Projeto

Banco Imobiliário – Bus Edition é uma versão digital multiplayer do clássico jogo de tabuleiro Monopoly, criada especialmente para viagens longas, onde um notebook funciona como servidor local e os jogadores acessam via celulares conectados ao hotspot.

Foi desenvolvido com:

Flask (Python) → servidor e lógica do jogo

MySQL (opcional) → persistência futura

HTML, CSS, JS → interface responsiva mobile-first

Grid 12×12 que simula um tabuleiro real

Sistema de cartas, propriedades, aluguel, imposto, prisões e sorte/revés

Animação 3D de dados sincronizada para todos os jogadores

🎮 Funcionalidades Principais
🧍‍♂️ Modo Multiplayer Local

Cada jogador acessa pelo navegador do celular

Notebook atua como servidor Flask

Jogadores entram com nome e ganham uma sessão única

🎲 Sistema de Dados 3D

Dois dados 3D com animação realista

Animação aparece em todas as telas simultaneamente

Movimento do jogador só ocorre após a animação terminar

🗺️ Tabuleiro 12×12

Layout inspirado em tabuleiros reais

44 casas ativas (cidades, bairros, empresas, eventos)

Cores e grupos visuais para cada cidade / região

Clique em qualquer casa → abre modal com detalhes

🏘️ Propriedades e Cidades

Cada cidade tem 3 bairros (barato, médio e caro)
Exemplos incluídos:

Rio de Janeiro

São Paulo

Paris

Tokyo

New York

Dubai

Além de empresas especiais como:

OceanAir

HyperFood

XBank

Neurora (a mais cara do jogo)

💸 Economia do Jogo

Comprar propriedades

Pagar aluguel automaticamente

Pagamento de impostos

Transferência de dinheiro entre jogadores (visível no log)

Cartas de Sorte e Revés afetando saldo

🔐 Prisão

Jogador pode ser preso por carta ou ao cair na casa

Só sai:

Após 3 turnos

Ou tirando números iguais nos dados

📝 Log em tempo real

Todas as ações registradas

Transferências, compras, rolagens e penalidades

Visível para todos os jogadores

💼 Tela de Propriedades

Jogador pode visualizar todas as propriedades compradas

Modal dedicado ao inventário

📱 Interface Mobile First

O jogo foi projetado para uso em celulares:

Botões grandes

Tabuleiro centralizado

Texto legível mesmo com escala automática

UI acompanha o tamanho do tabuleiro (zoom global)

🧩 Estrutura de Arquivos
/project
│── app.py                # Servidor Flask + lógica do jogo
│── requirements.txt      # Dependências Python
│── README.md             # Este arquivo
│── /templates
│     └── index.html      # Interface principal
│── /static
      ├── app.js          # Lógica do cliente
      ├── styles.css      # Estilo da interface
      └── assets/         # Imagens (opcional)

🚀 Como Rodar o Servidor
1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/banco-imobiliario-bus.git
cd banco-imobiliario-bus

2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Rodar o servidor
python app.py


O servidor rodará em:

http://0.0.0.0:5000

5. Conectar os jogadores

Ative o hotspot do notebook

Conecte os celulares ao Wi-Fi

No celular, acesse:

http://IP_DO_NOTEBOOK:5000

🔧 Configuração do Tabuleiro

O tabuleiro utiliza um grid 12×12 e um mapeamento lógico de 44 casas.

Cidades, bairros e empresas são definidos no backend (BOARD), com:

preço

aluguel

tipo

grupo visual

dono

comportamento especial

🎲 Animação 3D dos Dados

A animação:

É ativada pelo backend via animacao_timestamp

Só dispara quando o servidor envia uma nova rolagem

Usa transform: rotateX/Y() para posicionar a face correta

Permite duplos (dobles) para repetir o turno

⚠️ Limitações e Planos Futuros

Persistência em MySQL opcional (não ativada por padrão)

Sem suporte para salas múltiplas ainda

Sem construção de casas/hotéis (planejado)

Sem skins visuais temáticas (planejado)

🤝 Contribuidores

Dev principal: Você

Design assistido por IA (ChatGPT)

Testes executados diretamente na viagem 🚌

📄 Licença

Este projeto pode ser distribuído livremente para uso pessoal.
Para uso comercial, consulte o autor.

⭐ Contribua!

Se gostou do projeto:

Deixe uma estrela no repositório ⭐

Envie PRs com melhorias ou correções

Sugira novos modos de jogo
