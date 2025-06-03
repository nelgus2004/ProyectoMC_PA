// Filtro segun el valor seleccionado en una lista
document.addEventListener('DOMContentLoaded', () => {
  const filtros = document.querySelectorAll('.filtro');
  const lista = document.querySelector('.lista');

  if (!filtros || !lista) return;

  const datos = JSON.parse(filtros[0].dataset.items || '[]');
  const seleccionadosRaw = filtros[0].dataset.selected || '[]';
  const seleccionados = Array.isArray(JSON.parse(seleccionadosRaw))
    ? JSON.parse(seleccionadosRaw)
    : [JSON.parse(seleccionadosRaw)];

  function construirTexto(item, campoTexto) {
    return campoTexto.split('-').map(part => item[part.trim()] || '').join(' - ');
  }

  function actualizar() {
    lista.innerHTML = '';

    const valoresFiltros = {};
    filtros.forEach(filtro => {
      const campo = filtro.dataset.filtrarPor;
      valoresFiltros[campo] = filtro.value;
    });

    datos.forEach(item => {
      const cumpleFiltros = Object.entries(valoresFiltros).every(([clave, valor]) => item[clave] === valor);
      if (cumpleFiltros) {
        const opt = document.createElement('option');
        const campoValor = filtros[0].dataset.valor;
        const campoTexto = filtros[0].dataset.texto;
        opt.value = item[campoValor];
        opt.textContent = construirTexto(item, campoTexto);
        if (seleccionados.includes(String(item[campoValor]))) {
          opt.selected = true;
        }
        lista.appendChild(opt);
      }
    });
  }

  filtros.forEach(filtro => filtro.addEventListener('change', actualizar));
  actualizar();
});