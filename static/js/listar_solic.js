const solic_pesq_aprov = document.getElementById('solic_pes_aprov');
const solic_pes_naprov = document.getElementById('solic_pes_naprov');
const solic_ugai_naprov = document.getElementById('solic_ugai_naprov');

function remover_block(except) {
  solic_pesq_aprov.style.display = 'none';
  solic_pes_naprov.style.display = 'none';
  solic_ugai_naprov.style.display = 'none';

  if (except === 'pesq_aprov') {
    solic_pesq_aprov.style.display = 'block';
  }
  if (except === 'pesq_naprov') {
    solic_pes_naprov.style.display = 'block';
  }
  if (except === 'ugais_naprov') {
    solic_ugai_naprov.style.display = 'block';
  }
}

function exibir_content(value) {
  switch(value) {
    case 1:
      remover_block('pesq_aprov');
      break;
    case 2:
      remover_block('pesq_naprov');
      break
    case 3:
      remover_block('ugais_naprov');
      break

    default:
      break;
  }
}