let paginaAtual = 1;
const urlAPI = '/api/pesq_n_aprov_resp/';
const container = document.getElementById('container-resultados');
const infoPaginaSpan = document.getElementById('info-pagina');
const btnAnterior = document.getElementById('btn-anterior');
const btnProximo = document.getElementById('btn-proximo');

function carregarPagina(numeroDaPagina) {
  btnAnterior.disabled = true;
  btnProximo.disabled = true;

  // Ponto chave: fazer a requisição para o backend Django
  fetch(`${urlAPI}?page=${numeroDaPagina}`)
    .then(response => response.json())
    .then(data => {
      renderizarItens(data.items);

      paginaAtual = data.currentPage;
      infoPaginaSpan.textContent = `Página ${data.currentPage} de ${data.totalPages}`;

      //caso não tenha pagina anterior ou proxima, desabilita o botão
      btnAnterior.disabled = !data.hasPrevious;
      btnProximo.disabled = !data.hasNext;
    })
    .catch(error => {
      console.error('Erro ao carregar a página:', error);
      container.innerHTML = '<p>Ocorreu um erro ao carregar os dados.</p>';
    });
}

function renderizarItens(items) {
  container.innerHTML = ''; // Limpa o container
  items.forEach(item => {
    // Cria um div para o card
    const card = document.createElement('div');
    card.className = 'card_items'; // Adiciona classe CSS para estilização

    // Título da ação
    const titulo = document.createElement('h5');
    titulo.textContent = item.acao_realizada;
    card.appendChild(titulo);

    // Formatando data aqui
    var str_data = item.data_solicitacao;
    str_data = str_data.split('-');

    var data_format = [`${str_data[2]}/${str_data[1]}/${str_data[0]}`];

    // Data da solicitação
    const data = document.createElement('p');
    data.textContent = `Data da solicitação: ${data_format}`;
    card.appendChild(data);

    // Link opcional (exemplo: para detalhes, ajuste conforme necessário)
    const link = document.createElement('a');
    link.textContent = 'Ver Detalhes'; // Texto do link

    link.href = `${window.location.origin}/home/info_pesquisa/${item.id}/`;
    // link.classList.add('btn_card');
    // link.className = 'btn_card';
    card.appendChild(link);

    // Adiciona o card ao container
    container.appendChild(card);
  });
}

btnProximo.addEventListener('click', () => {
  carregarPagina(paginaAtual + 1);
});

btnAnterior.addEventListener('click', () => {
  carregarPagina(paginaAtual - 1);
});

carregarPagina(1);
