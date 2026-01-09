document.addEventListener('DOMContentLoaded', () => {

  let paginaAtual = 1;

  const container = document.getElementById('container-resultados');
  const infoPaginaSpan = document.getElementById('info-pagina');
  const btnAnterior = document.getElementById('btn-anterior');
  const btnProximo = document.getElementById('btn-proximo');

  let configAtual = {
    endpoint: '/api/pesq_aprov_resp/',
    tituloCampo: 'acao_realizada',
    detalheUrl: '/home/info_pesquisa/'
  };

  /* ============================
     CARREGAR PÁGINA
  ============================ */
  function carregarPagina(numeroDaPagina) {
    btnAnterior.disabled = true;
    btnProximo.disabled = true;

    fetch(`${configAtual.endpoint}?page=${numeroDaPagina}`)
      .then(response => response.json())
      .then(data => {
        renderizarItens(data.items);

        paginaAtual = data.currentPage;
        infoPaginaSpan.textContent =
          `Página ${data.currentPage} de ${data.totalPages}`;

        btnAnterior.disabled = !data.hasPrevious;
        btnProximo.disabled = !data.hasNext;
      })
      .catch(error => {
        console.error('Erro ao carregar página:', error);
        container.innerHTML = '<p>Erro ao carregar dados.</p>';
      });
  }

  /* ============================
     RENDERIZAR ITENS
  ============================ */
  function renderizarItens(items) {
    container.innerHTML = '';
    container.style = 'margin-top: 20px;';

    items.forEach(item => {
      const card = document.createElement('div');
      card.className = 'card_items';

      const titulo = document.createElement('h5');
      titulo.textContent = item[configAtual.tituloCampo];

      const partesData = item.data_solicitacao.split('-');
      const data = document.createElement('p');
      data.textContent =
        `Data da solicitação: ${partesData[2]}/${partesData[1]}/${partesData[0]}`;

      const link = document.createElement('a');
      link.textContent = 'Ver Detalhes';
      link.href =
        `${window.location.origin}${configAtual.detalheUrl}${item.id}/`;

      card.append(titulo, data, link);
      container.appendChild(card);
    });
  }

  /* ============================
     BOTÕES DE PAGINAÇÃO
  ============================ */
  btnAnterior.addEventListener('click', () => {
    carregarPagina(paginaAtual - 1);
  });

  btnProximo.addEventListener('click', () => {
    carregarPagina(paginaAtual + 1);
  });

  /* ============================
     CONTEXTOS (EXPOSTOS GLOBALMENTE)
  ============================ */
  window.carregarPesqAprovada = function () {
    configAtual = {
      endpoint: '/api/pesq_aprov_resp/',
      tituloCampo: 'acao_realizada',
      detalheUrl: '/home/info_pesquisa/'
    };
    carregarPagina(1);
  };

  window.carregarPesqNaoAprovada = function () {
    configAtual = {
      endpoint: '/api/pesq_n_aprov_resp/',
      tituloCampo: 'acao_realizada',
      detalheUrl: '/home/info_pesquisa/'
    };
    carregarPagina(1);
  };

  window.carregarSolicUgai = function () {
    configAtual = {
      endpoint: '/api/ped_ugais_naprov/',
      tituloCampo: 'ugai',
      detalheUrl: '/home/info_solic_ugai/'
    };
    carregarPagina(1);
  };

  /* ============================
     CARGA INICIAL
  ============================ */
  carregarPagina(1);

});
