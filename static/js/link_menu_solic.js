const pesquisa = document.getElementById('solic_pesq');
const ugai = document.getElementById('aut_ugai');

const button_pesq = document.getElementById('pesq_btn');
const button_ugai = document.getElementById('gaui_btn');

function mostrar_formulario(value) {
  pesquisa.style.display = 'none';
  ugai.style.display = 'none';

  if (value === 'solic_pesq') {
    pesquisa.style.display = 'block';
  }else if ( value === 'aut_ugai' ) {
    ugai.style.display = 'block';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  mostrar_formulario('solic_pesq');
})