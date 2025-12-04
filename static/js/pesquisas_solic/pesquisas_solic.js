
function mostrar_pesquisas(except) {
  current_title = document.getElementById('h3_title');
  current_title.textContent = "";

  em_andamento = document.getElementById('pesq_andamento');
  aguardando_aprov = document.getElementById('aguardando_aprov');

  em_andamento.style.display = 'none';
  aguardando_aprov.style.display = 'none';

  // Ativa apenas o selecionado
  if (except === 'em_andamento') {
    em_andamento.style.display = 'block';
    current_title.textContent = "(Em andamento)";
  }
  if (except === 'aguardando_aprovacao') {
    aguardando_aprov.style.display = 'block';
    current_title.textContent = "(Aguardando autorização)";
  }
}

function filtrar_pesquisas(value) {
  switch (value) {
    case 1:
      mostrar_pesquisas('em_andamento');
      break;

    case 2:
      mostrar_pesquisas('aguardando_aprovacao');
      break;

    default:
      break;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  filtrar_pesquisas(1);
});