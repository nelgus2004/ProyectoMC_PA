// Quitar formato 'active' de las opciones al ir al inicio
document.querySelector('.sidebar__logo a')?.addEventListener('click', () => {
  document.querySelectorAll('.sidebar__options--link').forEach(item => item.classList.remove('active'));
});

document.addEventListener('DOMContentLoaded', () => {
  // Botones de Editar
  document.querySelectorAll('.btn__edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const r_get = btn.dataset.get;
      const r_update = btn.dataset.update;
      const formId = btn.dataset.form;
      const modalId = btn.dataset.modal;
      const campos = JSON.parse(btn.dataset.campos);

      editarRegistro(id, r_get, formId, modalId, r_update, campos);
    });
  });

  // Botones de Borrar
  document.querySelectorAll('.btn__delete').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = btn.dataset.delete;
      const confirmMsg = btn.dataset.confirm || "¿Seguro que quieres eliminar este registro?";
      if (confirm(confirmMsg)) {
        window.location.href = url;
      }
    });
  });

});

// FORMULARIO EMERGENTE
// Mostrar formulario
function abrirForm(action, formId, modalId) {
  const form = document.getElementById(formId);
  form.reset();
  form.action = action;
  document.getElementById('btn-submit').querySelector('span').textContent = 'Guardar';
  document.getElementById('btn-submit').querySelector('img').src = '/static/image/save.png';
  document.getElementById(modalId).style.display = "block";
}
// Cerrar formulario
function cerrarForm(modalId) {
  document.getElementById(modalId).style.display = "none";
}
// Reutilizar formulario para actualizar un registro existente
function editarRegistro(id, r_get, formId, modalId, r_update, campos) {
  fetch(r_get + '/' + id)
    .then(res => res.json())
    .then(data => {
      const form = document.getElementById(formId);
      form.action = r_update + '/' + id;
      document.getElementById('btn-submit').querySelector('span').textContent = 'Actualizar';
      document.getElementById('btn-submit').querySelector('img').src = '/static/image/update.png';

      campos.forEach(campo => {
        const input = form.querySelector(`[name="${campo}"]`);
        if (input) {
          let valor = data[campo] || '';
          if (input.type === 'date' && valor) {
            const fecha = new Date(valor);
            valor = fecha.toISOString().split('T')[0]; // formato YYYY-MM-DD
          }
          input.value = valor;
        }
      });

      document.getElementById(modalId).style.display = "block";
    });
}

// Cerrar Alert
function cerrarAlert(boton) {
  const alerta = boton.closest('.alert');
  if (alerta) {
    alerta.remove();
  }
}

// Filtro segun el valor seleccionado en una lista
document.addEventListener('DOMContentLoaded', () => {
  const filtro = document.querySelector('.filtro');
  const lista = document.querySelector('.lista');

  if (!filtro || !lista) return;

  const datos = JSON.parse(filtro.dataset.items || '[]');
  const seleccionadosRaw = filtro.dataset.selected || '[]';
  const seleccionados = Array.isArray(JSON.parse(seleccionadosRaw))
    ? JSON.parse(seleccionadosRaw)
    : [JSON.parse(seleccionadosRaw)];

  const campoFiltro = filtro.dataset.filtrarPor;
  const campoValor = filtro.dataset.valor;
  const campoTexto = filtro.dataset.texto;

  function construirTexto(item) {
    return campoTexto.split('-').map(part => item[part.trim()] || '').join(' - ');
  }

  function actualizar() {
    lista.innerHTML = '';
    const valorFiltro = filtro.value;

    datos.forEach(item => {
      if (item[campoFiltro] === valorFiltro) {
        const opt = document.createElement('option');
        opt.value = item[campoValor];
        opt.textContent = construirTexto(item);
        if (seleccionados.includes(String(item[campoValor]))) {
          opt.selected = true;
        }
        lista.appendChild(opt);
      }
    });
  }

  const valorInicial = filtro.dataset.selected;
  if (valorInicial) {
    filtro.value = valorInicial;
  }

  actualizar();

  filtro.addEventListener('change', actualizar);
});
