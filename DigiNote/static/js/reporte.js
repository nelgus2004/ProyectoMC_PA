
document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('[data-modalId="#reporteModal"]').addEventListener('click', () => {
    const modal = document.getElementById('reporteModal');
    if (modal) modal.style.display = 'block';
  });

  document.querySelector('#reporteModal .close').addEventListener('click', () => {
    document.getElementById('reporteModal').style.display = 'none';
  });

  const tipoSelect = document.getElementById('tipo_reporte');
  const nivelSelect = document.getElementById('nivel');
  const paraleloSelect = document.getElementById('paralelo');

  function actualizarFiltros() {
    const tipo = tipoSelect.value;
    const nivel = nivelSelect.value;

    // Si el tipo es 'all', deshabilita nivel y paralelo
    if (tipo === 'all') {
      nivelSelect.value = 'all';
      paraleloSelect.value = 'all';
      nivelSelect.disabled = true;
      paraleloSelect.disabled = true;
    } else {
      nivelSelect.disabled = false;

      // Si nivel es 'all', deshabilita paralelo
      if (nivel === 'all') {
        paraleloSelect.value = 'all';
        paraleloSelect.disabled = true;
      } else {
        paraleloSelect.disabled = false;
      }
    }
  }

  tipoSelect.addEventListener('change', actualizarFiltros);
  nivelSelect.addEventListener('change', actualizarFiltros);

  actualizarFiltros();
});

document.getElementById('form-Reporte').addEventListener('submit', (event) => {
  document.querySelector('#reporteModal .close').click();

});
