let me = null;
let stateInterval = null;
let lastDiceAnimation = null;


async function joinGame() {
  const nome = prompt("Digite seu nome:");
  if (!nome) return;

  const resp = await fetch("/api/join", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ nome })
  });

  const data = await resp.json();
  if (resp.ok) {
    me = data;
    startPollingState();
  } else {
    alert(data.error || "Erro ao entrar no jogo");
  }
}

function startPollingState() {
  if (stateInterval) clearInterval(stateInterval);
  fetchState();
  stateInterval = setInterval(fetchState, 2000);
}

async function fetchState() {
  const resp = await fetch("/api/state");
  const data = await resp.json();
  if (!resp.ok) {
    console.error(data);
    return;
  }

  me = data.me;
  renderState(data);
}

function renderState(data) {
    
        if (
        data.animacao_timestamp !== null &&             // existe timestamp
        data.ultimo_dado &&                             // dado existe
        Array.isArray(data.ultimo_dado) &&              // é um array com 2 números
        data.animacao_timestamp !== lastDiceAnimation && // é realmente nova
        data.animacao_timestamp > Date.now() / 1000 - 3 // não é velha
        ) {
            lastDiceAnimation = data.animacao_timestamp;
            mostrarAnimacaoDado(data.ultimo_dado);
        }
        window.currentBoard = data.board;
        window.gameState = data;

  const meInfo = document.getElementById("me-info");
  meInfo.innerHTML = `
    <strong>Você:</strong> ${me.nome} | 💰 R$ ${me.saldo} | 📍 Casa ${me.posicao}
  `;

  const turnoInfo = document.getElementById("turno-info");
  const jogadorAtual = data.jogadores.find(j => j.id === data.jogador_atual_id);
  turnoInfo.innerHTML = `
    <strong>Turno:</strong> ${jogadorAtual ? jogadorAtual.nome : "-"}
    ${jogadorAtual && jogadorAtual.id === me.id ? "(É a sua vez!)" : ""}
  `;

  // jogadores
  const playersDiv = document.getElementById("players-list");
  playersDiv.innerHTML = "";
  data.jogadores.forEach(j => {
    const div = document.createElement("div");
    div.className = "player-card";
    div.innerHTML = `
      <strong>${j.nome}</strong><br>
      💰 R$ ${j.saldo} | 📍 ${j.posicao}
    `;
    playersDiv.appendChild(div);
  });

  // select de destino da transferência
  const select = document.getElementById("destino-select");
  select.innerHTML = "";
  data.jogadores
    .filter(j => j.id !== me.id)
    .forEach(j => {
      const opt = document.createElement("option");
      opt.value = j.id;
      opt.textContent = j.nome;
      select.appendChild(opt);
    });

  // ----- RENDER TABULEIRO EM GRID -----
const grid = document.getElementById("board-grid");
grid.innerHTML = "";

const gridMapping = [
  // LINHA 0 (topo)
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,

  // LINHA 1
  43, null, null, null, null, null, null, null, null, null, null, 12,

  // LINHA 2
  42, null, null, null, null, null, null, null, null, null, null, 13,

  // LINHA 3
  41, null, null, null, null, null, null, null, null, null, null, 14,

  // LINHA 4
  40, null, null, null, null, null, null, null, null, null, null, 15,

  // LINHA 5
  39, null, null, null, null, null, null, null, null, null, null, 16,

  // LINHA 6
  38, null, null, null, null, null, null, null, null, null, null, 17,

  // LINHA 7
  37, null, null, null, null, null, null, null, null, null, null, 18,

  // LINHA 8
  36, null, null, null, null, null, null, null, null, null, null, 19,

  // LINHA 9
  35, null, null, null, null, null, null, null, null, null, null, 20,

  // LINHA 10
  34, null, null, null, null, null, null, null, null, null, null, 21,

  // LINHA 11 (base)
  33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22
];


gridMapping.forEach((boardIndex, i) => {
  const div = document.createElement("div");

  // ------------------------------
  // CASAS VAZIAS (null)
  // ------------------------------
  if (boardIndex === null) {
    div.className = "casa vazia";
    div.style.background = "transparent";
    div.style.border = "none";
    grid.appendChild(div);
    return;
  }

  // ------------------------------
  // CASAS VÁLIDAS
  // ------------------------------
  const casa = data.board[boardIndex];
  const playersHere = data.jogadores.filter(j => j.posicao === boardIndex);

  // classes corretas
  div.classList.add("casa");

  if (casa.grupo) {
    div.classList.add(`grupo-${casa.grupo}`);
  }

  if (casa.tipo === "propriedade") {
    if (casa.dono_id === me.id) div.classList.add("dono-me");
    else if (casa.dono_id) div.classList.add("dono-outro");
  }

  // conteúdo visual
  div.innerHTML = `
    <div class="casa-nome">${boardIndex} — ${casa.nome}</div>
    <div class="casa-info">
      ${
        casa.tipo === "propriedade"
          ? `💰 R$${casa.preco} / Aluguel R$${casa.aluguel}`
          : casa.tipo
      }
    </div>
    <div class="players-here">
      ${playersHere.map(p => "👤").join(" ")}
    </div>
  `;

  // CLICK EVENT
  div.onclick = () => abrirModalCasaInfo(boardIndex, casa);

  grid.appendChild(div);
});



  // log
  const logUl = document.getElementById("log-list");
  logUl.innerHTML = "";
  data.log.forEach(entry => {
    const li = document.createElement("li");
    li.textContent = entry;
    logUl.appendChild(li);
  });
}

async function rollDice() {
  const resp = await fetch("/api/roll_dice", { method: "POST" });
  const data = await resp.json();
  if (!resp.ok) {
    alert(data.error || "Erro ao rolar dado");
    return;
  }
  // estado será atualizado no próximo polling
}

async function buyProperty() {
  const resp = await fetch("/api/comprar", { method: "POST" });
  const data = await resp.json();
  if (!resp.ok) {
    alert(data.error || "Não foi possível comprar.");
    return;
  }
}

async function endTurn() {
  const resp = await fetch("/api/end_turn", { method: "POST" });
  const data = await resp.json();
  if (!resp.ok) {
    alert(data.error || "Erro ao encerrar turno.");
    return;
  }
}

async function transferMoney() {
  const destinoId = document.getElementById("destino-select").value;
  const valor = document.getElementById("valor-transfer").value;

  if (!destinoId || !valor) {
    alert("Selecione o destino e o valor.");
    return;
  }

  const resp = await fetch("/api/transferir", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ destino_id: parseInt(destinoId), valor: parseInt(valor) })
  });

  const data = await resp.json();
  if (!resp.ok) {
    alert(data.error || "Erro ao transferir.");
    return;
  }
}

function mostrarAnimacaoDado(valores) {
  if (!Array.isArray(valores) || valores.length !== 2) return;

  const modal = document.getElementById("dice-modal");
  const d1 = document.getElementById("dice1");
  const d2 = document.getElementById("dice2");

  modal.classList.remove("hidden");

  // Reset transform
  d1.style.transform = "rotateX(0) rotateY(0)";
  d2.style.transform = "rotateX(0) rotateY(0)";

  // Start spin
  d1.classList.add("spin");
  d2.classList.add("spin");

  // Stop spinning after 1.4s
  setTimeout(() => {
    d1.classList.remove("spin");
    d2.classList.remove("spin");

    const orientacoes = {
      1: "rotateX(0deg) rotateY(0deg)",
      2: "rotateX(-90deg)",
      3: "rotateY(90deg)",
      4: "rotateY(-90deg)",
      5: "rotateX(90deg)",
      6: "rotateY(180deg)"
    };

    // orientações finais
    d1.style.transform = orientacoes[valores[0]];
    d2.style.transform = orientacoes[valores[1]];

    // fechar modal e mover peça
    setTimeout(async () => {
      modal.classList.add("hidden");

      const resp = await fetch("/api/mover", { method: "POST" });
      const data = await resp.json();

      if (resp.ok) {
        abrirModalCasa(data.casa, data.dobles);
      }

    }, 1200);

  }, 1400);
}

async function fazerAcao(acao) {
    const resp = await fetch("/api/acao_casa", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ acao })
    });

    const data = await resp.json();

    if (!resp.ok) {
        alert(data.error || "Erro ao executar ação da casa.");
        return;
    }

    // Fecha o modal após executar a ação
    fecharModalCasa();

    // Atualiza estado no próximo polling
}



function criarBotoesModal(lista) {
  const div = document.getElementById("modal-botoes");
  div.innerHTML = "";
  lista.forEach(btn => {
    const b = document.createElement("button");
    b.innerText = btn.texto;
    b.onclick = btn.acao;
    div.appendChild(b);
  });
}
function fecharModalCasa() {
  document.getElementById("modal-casa").classList.add("hidden");
}


function abrirModalCasa(casa, dobles) {
  const modal = document.getElementById("modal-casa");
  document.getElementById("modal-titulo").innerText = casa.nome;

  let descricao = "";

  if (casa.tipo === "propriedade" && casa.dono_id === null) {
      descricao = `Preço: R$${casa.preco} / Aluguel R$${casa.aluguel}`;
      criarBotoesModal([
        {texto: "Comprar", acao: () => fazerAcao("comprar")},
        {texto: "Cancelar", acao: fecharModalCasa}
      ]);
  }
  else if (casa.tipo === "propriedade" && casa.dono_id !== null) {
      descricao = `Esta propriedade tem dono. Você pagará aluguel automaticamente.`;
      criarBotoesModal([{texto: "OK", acao: fecharModalCasa}]);
  }
  else if (casa.tipo === "imposto") {
      descricao = "Casa de imposto! Você deve pagar.";
      criarBotoesModal([{texto: "Pagar", acao: () => fazerAcao("imposto")}]);
  }
  else if (casa.tipo === "sorte") {
      descricao = "Puxe uma carta de SORTE/REVÉS!";
      criarBotoesModal([{texto: "Puxar Carta", acao: () => fazerAcao("carta")}]);
  }
  else if (casa.tipo === "prisao") {
      descricao = "Você está preso!";
      criarBotoesModal([{texto: "OK", acao: fecharModalCasa}]);
  }

  document.getElementById("modal-descricao").innerText = descricao;
  modal.classList.remove("hidden");
}

function abrirModalPropriedades() {
  const modal = document.getElementById("modal-propriedades");
  const lista = document.getElementById("lista-propriedades");

  lista.innerHTML = "";

  me.propriedades.forEach(index => {
    const casa = window.currentBoard[index];

    const div = document.createElement("div");
    div.className = "propriedade-item";
    div.innerHTML = `
      <strong>${casa.nome}</strong><br>
      Preço: R$ ${casa.preco || "-"}<br>
      Aluguel: R$ ${casa.aluguel || "-"}<br>
      Tipo: ${casa.tipo}
    `;
    lista.appendChild(div);
  });

  modal.classList.remove("hidden");
}

function fecharModalPropriedades() {
  document.getElementById("modal-propriedades").classList.add("hidden");
}

document.getElementById("btn-propriedades")
  .addEventListener("click", abrirModalPropriedades);




  function abrirModalCasaInfo(index, casa) {
  const modal = document.getElementById("modal-info-casa");

  document.getElementById("info-casa-nome").innerText = casa.nome;

  let desc = `Tipo: ${casa.tipo}<br>`;

  if (casa.tipo === "propriedade") {
    desc += `
      Preço: R$ ${casa.preco}<br>
      Aluguel: R$ ${casa.aluguel}<br>
    `;
  }

  if (casa.dono_id) {
    const dono = window.gameState.jogadores.find(j => j.id === casa.dono_id);
    desc += `<strong>Proprietário:</strong> ${dono.nome}`;
  } else {
    desc += `<strong>Proprietário:</strong> Nenhum`;
  }

  document.getElementById("info-casa-desc").innerHTML = desc;

  modal.classList.remove("hidden");
}

function fecharModalInfoCasa() {
  document.getElementById("modal-info-casa").classList.add("hidden");
}


document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btn-roll").addEventListener("click", rollDice);
  document.getElementById("btn-buy").addEventListener("click", buyProperty);
  document.getElementById("btn-end-turn").addEventListener("click", endTurn);
  document.getElementById("btn-transfer").addEventListener("click", transferMoney);

  joinGame();
});
