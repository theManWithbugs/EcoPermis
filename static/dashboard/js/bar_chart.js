fetch('/api/dashboard/resp_tipo_solic/')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);

    anychart.onDocumentReady(function () {

      // create column chart
      var chart = anychart.column();

      // turn on chart animation
      chart.animation(true);

      // set chart title text settings
      chart.title('Solicitações de pesquisa');

      // create area series with passed data
      var series = chart.column([
        ['FAUNA', data["FAUNA"]],
        ['FLORA', data["FLORA"]],
        ['ECOLOGIA', data["ECOLOGIA"]],
        ['GEOLOGIA', data["GEOLOGIA"]],
        ['SOCIOECONOMIA', data["SOCIOECONOMIA"]],
        ['ARQUEOLOGIA', data["ARQUEOLOGIA"]],
        ['TURISMO', data["TURISMO"]],
        ['RECURSOS HIDRICOS', data["RECURSOS HIDRICO"]],
        ['EDUCAÇÃO AMBIENTAL', data["EDUCAÇÃO AMBIENTAL"]],
        ['CAVIDADES NATURAIS', data["CAVIDADES NATURAIS"]],
        ['OUTROS', data["OUTROS"]],
      ]);

      // set series tooltip settings
      series.tooltip().titleFormat('{%X}');

      series
        .tooltip()
        .position('center-top')
        .anchor('center-bottom')
        .offsetX(0)
        .offsetY(5)
        .format('${%Value}{groupsSeparator: }');

      // set scale minimum
      chart.yScale().minimum(0);

      // set yAxis labels formatter
      chart.yAxis().labels().format('${%Value}{groupsSeparator: }');

      // tooltips position and interactivity settings
      chart.tooltip().positionMode('point');
      chart.interactivity().hoverMode('by-x');

      // axes titles
      chart.xAxis().title('Product');
      chart.yAxis().title('Revenue');

      // set container id for the chart
      chart.container('container');

      // initiate chart drawing
      chart.draw();
    });
  })
  .catch(error => console.error('Erro:', error));