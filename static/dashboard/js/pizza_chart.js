fetch('/api/dashboard/resp_solic_ugai/')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);

    anychart.onDocumentReady(function () {
      // create pie chart with passed data
      var chart = anychart.pie3d([
        ['UGAI LIBERDADE', data["UGAI LIBERDADE"]],
        ['UGAI ACURAUA', data["UGAI ACURAUA"]],
        ['UGAI JURUPARI', data["UGAI JURUPARI"]],
        ['UGAI ANTIMARY', data["UGAI ANTIMARY"]],
        ['UGAI CHANDLESS', data["UGAI CHANDLESS"]]
      ]);

      // set chart title text settings
      chart
        .title('Solicitações de uso ordenado por UGAI')
        // set chart radius
        .radius('43%')
        // create empty area in pie chart
        .innerRadius('30%');

      // set container id for the chart
      chart.container('container_pizza');
      // initiate chart drawing
      chart.draw();
    });
  })
  .catch(error => console.error('Erro:', error));
