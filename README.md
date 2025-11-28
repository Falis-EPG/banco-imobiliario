# 🧩 Banco Imobiliário – Bus Edition  
### *Um jogo multiplayer estilo Banco Imobiliário, feito para rodar offline em um notebook e acessado pelos celulares via hotspot.*

---

## 📌 Sobre o Projeto
**Banco Imobiliário – Bus Edition** é uma versão digital multiplayer do clássico jogo de tabuleiro Monopoly, criada especialmente para viagens longas, onde um notebook funciona como **servidor local** e os jogadores acessam via **celulares conectados ao hotspot**.

Tecnologias utilizadas:

- **Flask (Python)** – Servidor e lógica do jogo  
- **MySQL (opcional)** – Persistência futura  
- **HTML, CSS, JS** – Interface responsiva mobile-first  
- **Animação 3D dos dados**, sincronizada entre todos os jogadores  
- **Tabuleiro 12×12**, simulação fiel de um tabuleiro real  

---

## 🎮 Funcionalidades Principais

### 🧍‍♂️ Modo Multiplayer Local
- Conexão local via Wi-Fi hotspot  
- Cada jogador acessa pelo navegador do celular  
- Sessão individual com identificação única  

### 🎲 Sistema de Dados 3D
- Dois dados com **animação 3D realista**  
- Animação exibida simultaneamente em todos os dispositivos  
- Peça só se move após o fim da animação  

### 🗺️ Tabuleiro em GRID 12×12
- 44 casas jogáveis  
- Disposição inspirada em tabuleiros reais  
- Cidades, bairros e empresas com grupo de cor próprio  
- Clique em qualquer casa → modal com detalhes  

### 🏘️ Propriedades, Cidades e Empresas
Cada cidade possui **3 bairros** (barato, médio e caro).  
Inclui cidades como:

- Rio de Janeiro  
- São Paulo  
- Paris  
- Tokyo  
- New York  
- Dubai  

E empresas especiais como:

- OceanAir  
- HyperFood  
- XBank  
- **Neurora (a mais cara do jogo)**  

### 💸 Economia do Jogo
- Compra de propriedades  
- Aluguel automático  
- Impostos  
- Cartas de Sorte/Revés  
- Transferência de dinheiro entre jogadores (registrada no log)  

### 🔐 Prisão
- Jogador pode ser preso por carta ou casa específica  
- Só sai após:
  - 3 turnos, ou  
  - Tirar números iguais nos dados  

### 📝 Log em Tempo Real
- Todas as movimentações e ações relevantes  
- Visível para todos os jogadores  

### 📜 Inventário de Propriedades
- Modal dedicado com todas propriedades do jogador  

---

## 📱 Interface Mobile First
Projetada especificamente para smartphones:

- Botões grandes  
- Modal nítido  
- Tabuleiro com zoom global para boa visualização  
- Layout totalmente responsivo  

---
## 🧩 Estrutura do Projeto

/project
│── app.py # Servidor Flask + lógica do jogo
│── requirements.txt # Dependências Python
│── README.md # Este arquivo
│── /templates
│ └── index.html # Interface principal
│── /static
├── app.js # Lógica do cliente (front)
├── styles.css # Estilos e responsividade
└── assets/ # (imagens caso existam)


---

## 🚀 Como Rodar o Jogo

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU-USUARIO/banco-imobiliario-bus.git
cd banco-imobiliario-bus
```
### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```
### 4. Executar o servidor
```bash
python app.py
```

A aplicação ficará disponível em:
```bash
http://0.0.0.0:5000
```

###5. Acessar pelo celular

1 - Ative o hotspot do notebook<br>

2 - Conecte os celulares <br>

3 - Acesse pelo navegador:

- http://IP_DO_NOTEBOOK:5000<br>

### 🔧 Configuração do Tabuleiro

O tabuleiro usa:

Grid 12×12

44 casas jogáveis

Cidades agrupadas por cor

Empresas com preços variados

Casas especiais: Imposto, Prisão, Sorte/Revés

Toda a configuração fica no backend em uma variável BOARD.

### 🎲 Animação 3D dos Dados

Ativada via animacao_timestamp pelo backend

Animação ocorre com transform: rotateX/Y

Somente após o fim da animação o movimento acontece

### ⚠️ Limitações e Futuras Melhorias

Persistência real usando MySQL

Múltiplas salas de jogo

Construção de casas/hotéis

Sons para ações

Temas visuais alternativos
