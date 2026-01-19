fetch('/api/dashboard/resp_tipo_solic/')
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    console.log('NOVO ENDPOIT AQUI!');
    const ctxBarUgais = document.getElementById('ctxBarUgais');
    new Chart(ctxBarUgais, {
      type: 'bar',
      data: {
        labels: ['FAUNA', 'FLORA', 'ECOLOGIA', 'GEOLOGIA', 'SOCIOECONOMIA',
          'ARQUEOLOGIA', 'TURISMO', 'RECURSOS HIDRICOS', 'EDUCAÇÃO AMBIENTAL',
          'CAVIDADES NATURAIS', 'OUTROS'],
        datasets: [{
          label: '# of Votes',
          data: [data["FAUNA"], data["FLORA"], data["ECOLOGIA"], data["GEOLOGIA"],
            data["SOCIOECONOMIA"], data["ARQUEOLOGIA"], data["TURISMO"], data["RECURSOS HIDRICO"],
            data["EDUCAÇÃO AMBIENTAL"], data["CAVIDADES NATURAIS"], data["OUTROS"]],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  })
  .catch(error => console.error('Erro', error));

fetch('/api/dashboard/resp_solic_ugai/')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const ctxUgais = document.getElementById('pie_ugais');
    new Chart(ctxUgais, {
      type: 'pie',
      data: {
        labels: ['UGAI LIBERDADE', 'UGAI ACURAUA', 'UGAI JURUPARI',
                'UGAI ANTIMARY','UGAI CHANDLESS'],
        datasets: [{
          label: '# of Votes',
          data: [data["UGAI LIBERDADE"], data["UGAI ACURAUA"],
            data["UGAI JURUPARI"], data["UGAI ANTIMARY"], data["UGAI CHANDLESS"]],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  })
  .catch(error => console.error('Erro:', error));
