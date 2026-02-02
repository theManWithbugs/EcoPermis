const container_buttons = document.getElementById('container_buttons')
const btnAnterior = document.getElementById('btn-anterior');
const btnProximo  = document.getElementById('btn-proximo');

const container_resul = document.getElementById('container_resultados');

container_buttons.style.marginBottom = '7px';

// Guarda o ano escolhido pelo usuário
let anoAtual = null;

// Guarda a página atual da lista
let paginaAtual = 1;

function selectYear(ano) {
  anoAtual = ano;
  paginaAtual = 1;
  buscarDados();
}

btnAnterior.addEventListener('click', () => {
  if (anoAtual === null) return;
  if (paginaAtual === 1) return;

  paginaAtual--;
  buscarDados();
});

btnProximo.addEventListener('click', () => {
  if (anoAtual === null) return;

  paginaAtual++;
  buscarDados();
});

function buscarDados() {
  fetch(`/api/get_page_by_year/?year=${anoAtual}&page=${paginaAtual}`)
    .then(resposta => resposta.json())
    .then(dados => {
      objs = dados.results;
      container_resul.innerHTML = '';
      objs.forEach(obj => {
        const card = document.createElement('div');
        card.className = 'card_items';

        const titulo = document.createElement('h5');
        titulo.textContent = `${obj["ugai"]}`;

        const link = document.createElement('a');
        link.textContent = 'Ver detalhes';
        link.href = `/home/info_solic_ugai/${obj["id"]}/`;

        const data = document.createElement('p');
        data.textContent = `${obj["ativ_desenv"]}`;

        card.append(titulo, data, link);
        container_resul.appendChild(card);
      });
    })
    .catch(erro => {
      console.error('Erro ao buscar dados:', erro);
    });
}

function get_buttons() {
  fetch(`/api/get_page_by_year/`)
    .then(resposta => resposta.json())
    .then(dados => {
      years = dados.years;
      for (const x in years) {
        console.log(`${years[x]["data_solicitacao__year"]}`);
        const button = document.createElement('button');
        button.textContent = `${years[x]["data_solicitacao__year"]}`;
        button.value = `${years[x]["data_solicitacao__year"]}`;
        button.onclick = (e) => selectYear(e.target.value);
        container_buttons.appendChild(button);
      }
    })
    .catch(erro => {
      console.error('Erro ao buscar dados:', erro);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  get_buttons();
  selectYear(2026);
});
