from flask import Flask, render_template, request, session, jsonify
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "um_segredo_qualquer"  # troca depois

# ---------- MODELO DE DADOS EM MEMÓRIA ----------

BOARD = [

    # 0 - início
    {"index":0, "nome":"Início", "tipo":"especial", "grupo":"especial"},

    # RIO DE JANEIRO (baratos)
    {"index":1,  "nome":"Copacabana", "tipo":"propriedade", "preco":80,  "aluguel":20, "grupo":"rio"},
    {"index":2,  "nome":"Ipanema",    "tipo":"propriedade", "preco":120, "aluguel":30, "grupo":"rio"},
    {"index":3,  "nome":"Leblon",     "tipo":"propriedade", "preco":160, "aluguel":40, "grupo":"rio"},

    # sorte
    {"index":4, "nome":"Sorte ou Revés", "tipo":"sorte", "grupo":"especial"},

    # SÃO PAULO (preço médio)
    {"index":5, "nome":"Brás",       "tipo":"propriedade", "preco":180, "aluguel":45, "grupo":"sp"},
    {"index":6, "nome":"Mooca",      "tipo":"propriedade", "preco":220, "aluguel":55, "grupo":"sp"},
    {"index":7, "nome":"Jardins",    "tipo":"propriedade", "preco":260, "aluguel":65, "grupo":"sp"},

    # imposto
    {"index":8, "nome":"Imposto Municipal", "tipo":"imposto", "valor":120, "grupo":"especial"},

    # PARIS (média)
    {"index":9,  "nome":"Montmartre", "tipo":"propriedade", "preco":280, "aluguel":70, "grupo":"paris"},
    {"index":10, "nome":"Belleville", "tipo":"propriedade", "preco":320, "aluguel":80, "grupo":"paris"},
    {"index":11, "nome":"Le Marais",  "tipo":"propriedade", "preco":360, "aluguel":90, "grupo":"paris"},

    # prisão
    {"index":12, "nome":"Prisão", "tipo":"prisao", "grupo":"especial"},

    # TOKYO (média-alta)
    {"index":13, "nome":"Shibuya", "tipo":"propriedade", "preco":380, "aluguel":95, "grupo":"tokyo"},
    {"index":14, "nome":"Shinjuku", "tipo":"propriedade", "preco":420, "aluguel":110, "grupo":"tokyo"},
    {"index":15, "nome":"Ginza",    "tipo":"propriedade", "preco":480, "aluguel":120, "grupo":"tokyo"},

    # empresa
    {"index":16, "nome":"Call Link", "tipo":"propriedade", "preco":300, "aluguel":75, "grupo":"empresa"},

    # NEW YORK (caras)
    {"index":17, "nome":"Brooklyn",   "tipo":"propriedade", "preco":500, "aluguel":130, "grupo":"ny"},
    {"index":18, "nome":"Harlem",     "tipo":"propriedade", "preco":540, "aluguel":140, "grupo":"ny"},
    {"index":19, "nome":"Manhattan",  "tipo":"propriedade", "preco":600, "aluguel":160, "grupo":"ny"},

    # sorte
    {"index":20, "nome":"Sorte ou Revés", "tipo":"sorte", "grupo":"especial"},

    # DUBAI (muito caras)
    {"index":21, "nome":"Deira",      "tipo":"propriedade", "preco":620, "aluguel":165, "grupo":"dubai"},
    {"index":22, "nome":"Marina",     "tipo":"propriedade", "preco":700, "aluguel":180, "grupo":"dubai"},
    {"index":23, "nome":"Palm Jumeirah", "tipo":"propriedade", "preco":780, "aluguel":200, "grupo":"dubai"},

    # empresa cara
    {"index":24, "nome":"CNPEM",   "tipo":"propriedade", "preco":600, "aluguel":150, "grupo":"empresa"},
    {"index":25, "nome":"Nvidia", "tipo":"propriedade", "preco":550, "aluguel":135, "grupo":"empresa"},

    # PARADA LIVRE
    {"index":26, "nome":"Ponto de Descanso", "tipo":"especial", "grupo":"especial"},

    # EMPRESAS PREMIUM (quase finais)
    {"index":27, "nome":"Algar", "tipo":"propriedade", "preco":820, "aluguel":210, "grupo":"empresa"},
    {"index":28, "nome":"CEMIG", "tipo":"propriedade", "preco":870, "aluguel":220, "grupo":"empresa"},

    # imposto
    {"index":29, "nome":"Receita Federal", "tipo":"imposto", "valor":250, "grupo":"especial"},

    # ULTRA CARAS – FINAL (DUBAI+NEW YORK combo VIP)
    {"index":30, "nome":"Upper East Side", "tipo":"propriedade", "preco":900, "aluguel":230},
    {"index":31, "nome":"Times Square",    "tipo":"propriedade", "preco":950, "aluguel":240},
    {"index":32, "nome":"Burj Khalifa",    "tipo":"propriedade", "preco":1100, "aluguel":280},

    # empresa MAIS CARA DO JOGO
    {"index":33, "nome":"NEURORA", "tipo":"propriedade", "preco":1500, "aluguel":400, "grupo":"empresa"},

    # corredor final
    {"index":34, "nome":"Estação Central", "tipo":"especial", "grupo":"especial"},
    {"index":35, "nome":"Sorte ou Revés", "tipo":"sorte", "grupo":"especial"},

    # bairros alternativos
    {"index":36, "nome":"Little Tokyo LA", "tipo":"propriedade", "preco":500, "aluguel":120},
    {"index":37, "nome":"Brooklyn Tech Park", "tipo":"propriedade", "preco":650, "aluguel":160},

    # empresa secundária
    {"index":38, "nome":"FertMinas", "tipo":"propriedade", "preco":450, "aluguel":115, "grupo":"empresa"},

    # parte final
    {"index":39, "nome":"Avenida Paulista VIP", "tipo":"propriedade", "preco":900, "aluguel":230},
    {"index":40, "nome":"Copan SP", "tipo":"propriedade", "preco":780, "aluguel":195},
    {"index":41, "nome":"Hollywood Boulevard", "tipo":"propriedade", "preco":880, "aluguel":215},

    # quase-end
    {"index":42, "nome":"Tribunal de Justiça", "tipo":"imposto", "valor":180},

    # 43 – última casa antes de voltar
    {"index":43, "nome":"Estação Final", "tipo":"especial"}
]


PRISAO_INDEX = 6

CARTAS = [
    {"texto": "Você esqueceu o lanche dentro da mochila e agora ela fede a morte. Compre outra. -R$120.", "valor": -120},
    {"texto": "Um idoso te confundiu com o neto e te deu R$50 pra ‘comprar juízo’. +R$50.", "valor": 50},
    {"texto": "Você caiu do ônibus porque o motorista arrancou rápido demais. Pague o SUS em dia. -R$40.", "valor": -40},
    {"texto": "Encontrou uma nota amassada de R$20 no banco do ônibus. Achado não é roubado. +20.", "valor": 20},
    {"texto": "Seu cartão clonou porque você conectou no Wi-Fi do ônibus. -R$300.", "valor": -300},

    {"texto": "Te ofereceram um Pix de R$500 ‘por engano’. Você aceitou. +R$500.", "valor": 500},
    {"texto": "Você pediu um dogão na rodoviária e passou mal. Compra remédio. -R$60.", "valor": -60},
    {"texto": "A cobradora achou você simpático. ‘Vai de graça hoje’. +R$15.", "valor": 15},
    {"texto": "Alguém soltou um pum silencioso mortal no ônibus e todos acharam que foi você. Vergonha custa caro. -R$30.", "valor": -30},
    {"texto": "Você se tornou o passageiro que segura a porta e atrasa todo mundo. Pague o karma. -R$90.", "valor": -90},

    {"texto": "Um influencer te filmou dormindo no ônibus e você viralizou. Recebeu doações. +R$200.", "valor": 200},
    {"texto": "Você pegou o ônibus errado e deu a volta na cidade. Pague a tarifa extra. -R$70.", "valor": -70},
    {"texto": "Tentou pular a catraca, mas ficou preso. Pague a multa (e a vergonha). -R$150.", "valor": -150},
    {"texto": "Você achou R$100 dentro do banco rasgado do ônibus. +R$100.", "valor": 100},
    {"texto": "O motorista estava inspirado e quase te jogou na parede. Pague o seguro imaginário. -R$50.", "valor": -50},

    {"texto": "Hoje é seu dia de sorte. A gasolina baixou! +R$70.", "valor": 70},
    {"texto": "Você derrubou café no seu colega. Pague outro café. -R$15.", "valor": -15},
    {"texto": "Ganhou uma rifa aleatória no trabalho. +R$120.", "valor": 120},
    {"texto": "Perdeu o VR porque o cartão encostou no leitor errado. -R$200.", "valor": -200},
    {"texto": "Alguém te passou um troco errado pra mais. Finge costume. +R$30.", "valor": 30},

    {"texto": "Você deu a sorte grande e achou um celular perdido! Mas a aura do dono era pesada… devolveu. +R$20.", "valor": 20},
    {"texto": "Você viu um ônibus chegando, correu, tropeçou e caiu na frente dele. Pague sua dignidade. -R$25.", "valor": -25},
    {"texto": "Uma igreja no centro estava distribuindo marmitas. +R$12.", "valor": 12},
    {"texto": "O fiscal entrou no ônibus e seu cartão não passou. Multa! -R$90.", "valor": -90},
    {"texto": "Você ganhou um cupom de 10% no mercado. Economizou! +R$10.", "valor": 10},

    {"texto": "O pneu do ônibus estourou e todos tiveram que descer. Perdeu tempo = perdeu dinheiro. -R$35.", "valor": -35},
    {"texto": "A moça do lado dormiu no seu ombro. Você ganhou R$5 de conforto emocional. +5.", "valor": 5},
    {"texto": "Seu crush te visualizou e não respondeu. Sofrência te fez gastar no iFood. -R$70.", "valor": -70},
    {"texto": "O cobrador te confundiu e devolveu a mais. +R$15.", "valor": 15},
    {"texto": "Você discutiu com o motorista e ele te mandou descer. -R$20.", "valor": -20},

    # CARTAS ESPECIAIS
    {"texto": "Você tentou dar uma ‘carteirada’ no motorista. Vá direto para a prisão!", "prisao": True},
    {"texto": "Um fiscal corrupto ofereceu ‘acordo’. Você aceitou. Mova 3 casas à frente.", "mover": 3},
    {"texto": "Você esqueceu de pagar as contas e o Serasa te achou. Volte 2 casas e pague R$40.", "mover": -2, "valor": -40},
    {"texto": "Um mendigo te deu conselhos de vida muito bons. Avance uma casa.", "mover": 1},
    {"texto": "Você entrou em um ônibus errado que estava indo para o bairro mais perigoso. Vá direto para a prisão!", "prisao": True},
]

game_state = {
    "jogadores": {},
    "ordem_turnos": [],
    "jogador_atual_id": None,
    "proximo_id": 1,
    "log": [],
    "ultimo_dado": None,        # <-- novo
    "animacao_timestamp": None,  # <-- novo
    "movimento_pendente": None
}

SALDO_INICIAL = 1500


def add_log(msg):
    game_state["log"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    # limita tamanho do log
    game_state["log"] = game_state["log"][:30]


def get_current_player():
    pid = game_state["jogador_atual_id"]
    if pid is None:
        return None
    return game_state["jogadores"].get(pid)


def get_player_by_session():
    pid = session.get("player_id")
    if pid is None:
        return None
    return game_state["jogadores"].get(pid)

def aplicar_carta(jogador, carta):
    if "valor" in carta:
        val = carta["valor"]
        jogador["saldo"] = max(0, jogador["saldo"] + val)


# ---------- ROTAS ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/join", methods=["POST"])
def join():
    nome = request.json.get("nome")
    if not nome:
        return jsonify({"error": "Nome obrigatório"}), 400

    # se já tiver player na sessão, só devolve
    player = get_player_by_session()
    if player:
        return jsonify({"player_id": player["id"], "nome": player["nome"]})

    # cria novo jogador
    pid = game_state["proximo_id"]
    game_state["proximo_id"] += 1

    novo = {
        "id": pid,
        "nome": nome,
        "posicao": 0,
        "saldo": SALDO_INICIAL,
        "propriedades": [],
        "preso_turnos": 0
    }
    game_state["jogadores"][pid] = novo
    game_state["ordem_turnos"].append(pid)
    session["player_id"] = pid

    if game_state["jogador_atual_id"] is None:
        game_state["jogador_atual_id"] = pid
        add_log(f"{nome} entrou no jogo e começa jogando!")

    else:
        add_log(f"{nome} entrou no jogo.")

    return jsonify({"player_id": pid, "nome": nome})


@app.route("/api/state")
def state():
    player = get_player_by_session()
    if not player:
        return jsonify({"error": "Jogador não identificado"}), 401

    # monta visão do estado
    return jsonify({
        "me": player,
        "jogador_atual_id": game_state["jogador_atual_id"],
        "jogadores": list(game_state["jogadores"].values()),
        "board": BOARD,
        "log": game_state["log"],
        "ultimo_dado": game_state["ultimo_dado"],
        "animacao_timestamp": game_state["animacao_timestamp"]
    })


@app.route("/api/roll_dice", methods=["POST"])
def roll_dice():
    player = get_player_by_session()
    if not player:
        return jsonify({"error": "Jogador não identificado"}), 401

    if player["id"] != game_state["jogador_atual_id"]:
        return jsonify({"error": "Não é seu turno"}), 400

    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    dice = [d1, d2]

    # registra apenas o resultado
    game_state["ultimo_dado"] = dice
    game_state["animacao_timestamp"] = datetime.now().timestamp()

    if player["preso_turnos"] > 0:
        # checar se tirou dobles
        if d1 == d2:
            player["preso_turnos"] = 0
            add_log(f"{player['nome']} tirou números iguais e saiu da prisão!")
        else:
            add_log(f"{player['nome']} não conseguiu sair da prisão.")
            return jsonify({"preso": True})


    # registra movimento pendente
    dobles = (d1 == d2)
    game_state["movimento_pendente"] = {
        "player_id": player["id"],
        "steps": d1 + d2,
        "dobles": dobles
    }

    add_log(f"{player['nome']} rolou o dado...")

    return jsonify({
        "dice": dice,
        "animacao_timestamp": game_state["animacao_timestamp"]
    })


@app.route("/api/mover", methods=["POST"])
def mover():
    pend = game_state.get("movimento_pendente")
    if not pend:
        return jsonify({"error": "Nenhum movimento pendente."}), 400

    player = game_state["jogadores"][pend["player_id"]]
    steps = pend["steps"]
    dobles = pend["dobles"]

    old_pos = player["posicao"]
    new_pos = (old_pos + steps) % len(BOARD)
    player["posicao"] = new_pos

    casa = BOARD[new_pos]

    # limpa mov pendente
    game_state["movimento_pendente"] = None

    # marca casa pendente
    game_state["casa_pendente"] = {
        "player_id": player["id"],
        "casa_index": new_pos,
        "dobles": dobles
    }

    return jsonify({
        "ok": True,
        "casa": casa,
        "dobles": dobles
    })

def handle_landing(player, casa):
    # propriedade livre
    if casa["tipo"] == "propriedade" and casa.get("dono_id") is None:
        add_log(f"{player['nome']} caiu em {casa['nome']} (R${casa['preco']}). Pode comprar se quiser.")
        # decisão de comprar será feita em outro endpoint
    elif casa["tipo"] == "propriedade" and casa.get("dono_id") is not None and casa["dono_id"] != player["id"]:
        # paga aluguel automaticamente
        dono = game_state["jogadores"][casa["dono_id"]]
        valor = casa["aluguel"]
        if player["saldo"] < valor:
            valor = player["saldo"]  # paga o que tem (simplificado)

        player["saldo"] -= valor
        dono["saldo"] += valor
        add_log(f"{player['nome']} pagou R${valor} de aluguel para {dono['nome']} em {casa['nome']}.")
    elif casa["tipo"] == "imposto":
        valor = casa["valor"]
        if player["saldo"] < valor:
            valor = player["saldo"]
        player["saldo"] -= valor
        add_log(f"{player['nome']} pagou R${valor} de imposto em {casa['nome']}.")
    elif casa["tipo"] == "sorte":
        # sorte simples (você pode sofisticar depois)
        valor = random.choice([-100, -50, 50, 100, 150])
        if valor >= 0:
            player["saldo"] += valor
            add_log(f"SORTE! {player['nome']} ganhou R${valor}.")
        else:
            perda = min(player["saldo"], abs(valor))
            player["saldo"] -= perda
            add_log(f"REVÉS! {player['nome']} perdeu R${perda}.")
    else:
        # neutro
        pass


@app.route("/api/comprar", methods=["POST"])
def comprar():
    player = get_player_by_session()
    if not player:
        return jsonify({"error": "Jogador não identificado"}), 401

    pos = player["posicao"]
    casa = BOARD[pos]

    if casa["tipo"] != "propriedade":
        return jsonify({"error": "Esta casa não é uma propriedade."}), 400

    if casa.get("dono_id") is not None:
        return jsonify({"error": "Propriedade já tem dono."}), 400

    preco = casa["preco"]
    if player["saldo"] < preco:
        return jsonify({"error": "Saldo insuficiente."}), 400

    player["saldo"] -= preco
    casa["dono_id"] = player["id"]
    player["propriedades"].append(casa["index"])
    add_log(f"{player['nome']} comprou {casa['nome']} por R${preco}.")

    return jsonify({"me": player, "casa": casa})


@app.route("/api/transferir", methods=["POST"])
def transferir():
    player = get_player_by_session()
    if not player:
        return jsonify({"error": "Jogador não identificado"}), 401

    data = request.json
    destino_id = data.get("destino_id")
    valor = data.get("valor")

    if not destino_id or not valor:
        return jsonify({"error": "destino_id e valor são obrigatórios"}), 400

    try:
        valor = int(valor)
    except ValueError:
        return jsonify({"error": "Valor inválido."}), 400

    if valor <= 0:
        return jsonify({"error": "Valor deve ser positivo."}), 400

    if player["saldo"] < valor:
        return jsonify({"error": "Saldo insuficiente."}), 400

    if destino_id not in game_state["jogadores"]:
        return jsonify({"error": "Jogador de destino não encontrado."}), 400

    destino = game_state["jogadores"][destino_id]

    player["saldo"] -= valor
    destino["saldo"] += valor

    add_log(f"TRANSFERÊNCIA: {player['nome']} transferiu R${valor} para {destino['nome']}.")

    return jsonify({"me": player})

@app.route("/api/acao_casa", methods=["POST"])
def acao_casa():
    data = request.json
    acao = data.get("acao")

    info = game_state.get("casa_pendente")
    if not info:
        return jsonify({"error": "Nenhuma casa pendente"}), 400

    jogador = game_state["jogadores"][info["player_id"]]
    casa = BOARD[info["casa_index"]]

    # --- COMPRA ---
    if acao == "comprar" and casa["tipo"] == "propriedade" and casa["dono_id"] is None:
        preco = casa["preco"]
        if jogador["saldo"] >= preco:
            jogador["saldo"] -= preco
            casa["dono_id"] = jogador["id"]
            jogador["propriedades"].append(casa["index"])
            add_log(f"{jogador['nome']} comprou {casa['nome']} por R${preco}.")
        else:
            return jsonify({"error": "Saldo insuficiente"}), 400

    # --- IMPOSTO ---
    elif acao == "imposto" and casa["tipo"] == "imposto":
        valor = casa["valor"]
        jogador["saldo"] = max(0, jogador["saldo"] - valor)
        add_log(f"{jogador['nome']} pagou R${valor} em impostos!")

    # --- CARTA DE SORTE/REVÉS ---
    elif acao == "carta" and casa["tipo"] == "sorte":
        carta = random.choice(CARTAS)
        aplicar_carta(jogador, carta)
        add_log(f"CARTA: {jogador['nome']} pegou '{carta['texto']}'")

        # se carta envia para prisão
        if carta.get("prisao"):
            jogador["posicao"] = PRISAO_INDEX
            jogador["preso_turnos"] = 3

    else:
        return jsonify({"error": "Ação inválida para esta casa"}), 400

    # limpar pendencia
    game_state["casa_pendente"] = None

    return jsonify({"ok": True})


@app.route("/api/end_turn", methods=["POST"])
def end_turn():
    player = get_player_by_session()
    if not player:
        return jsonify({"error": "Jogador não identificado"}), 401

    if player["id"] != game_state["jogador_atual_id"]:
        return jsonify({"error": "Não é seu turno."}), 400

    ordem = game_state["ordem_turnos"]
    idx = ordem.index(player["id"])
    proximo_idx = (idx + 1) % len(ordem)
    proximo_id = ordem[proximo_idx]
    game_state["jogador_atual_id"] = proximo_id
    proximo = game_state["jogadores"][proximo_id]

    if proximo["preso_turnos"] > 0:
        proximo["preso_turnos"] -= 1
        add_log(f"{proximo['nome']} está preso por mais {proximo['preso_turnos']} turno(s).")

    add_log(f"Turno de {player['nome']} terminou. Agora é a vez de {proximo['nome']}.")

    return jsonify({"jogador_atual_id": proximo_id})


if __name__ == "__main__":
    # ao rodar no notebook, coloque host='0.0.0.0' pra aceitar conexões da rede
    app.run(host="0.0.0.0", port=5000, debug=True)
