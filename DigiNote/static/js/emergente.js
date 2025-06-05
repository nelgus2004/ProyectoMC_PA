const div = document.getElementById('rutas');
let rutas = {};
if (window.location.pathname !== "/app/inicio/") {
  rutas = {
    add: div.dataset.add,
    get: div.dataset.get,
    update: div.dataset.update,
    delete: div.dataset.delete,
  };
}

// FORMULARIO EMERGENTE
document.addEventListener('DOMContentLoaded', () => {

  // Botones de Añadir (abrir formulario vacío)
  document.querySelectorAll('.btn__add').forEach(btn => {
    if (btn.closest('#mini-form')) return;
    if (btn.closest('.edit__foreign')) return;
    btn.addEventListener('click', () => {
      const name = btn.dataset.name;
      añadirRegistro(`form-${name}`);
    });
  });

  // Click en Botón de Editar
  document.querySelectorAll('.btn__edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const formId = `form-${btn.dataset.name}`;
      editarRegistro(id, formId);
    });
  });

  // Click en Botón de Borrar
  document.querySelectorAll('.btn__delete').forEach(btn => {
    if (btn.closest('#mini-form')) return;
    if (btn.closest('.edit__foreign')) return;
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      borrarRegistro(id, btn);
    });
  });

  // Click en Botón cerrar formulario
  document.querySelectorAll('.close').forEach(btn => {
    btn.addEventListener('click', cerrarForm);
  });
});

// Mostrar formulario para añadir un registro
function añadirRegistro(formId) {
  const form = document.getElementById(formId);
  form.reset();
  form.action = rutas.add;

  const btnSubmit = form.querySelector('#btn-submit');
  if (btnSubmit) {
    btnSubmit.querySelector('span').textContent = 'Guardar';
    btnSubmit.querySelector('img').src = '/static/image/save.png';
  }

  const modal = form.closest('.emergente');
  if (modal) modal.style.display = "block";
}

// Borrar registrp
function borrarRegistro(id, btn) {
  const url = `${rutas.delete}/${id}`;
  const confirmMsg = btn.dataset.confirm || "¿Seguro que quieres eliminar este registro?";
  console.log(url)
  if (confirm(confirmMsg)) {
    window.location.href = url;
  }
}

// Reutilizar formulario para actualizar registro existente
function editarRegistro(id, formId) {

  fetch(`${rutas.get}/${id}`)
    .then(res => res.json())
    .then(data => {
      try {
        const form = document.getElementById(formId);
        form.action = `${rutas.update}/${id}`;

        // Modificar el boton de enviar a aenctualizar
        const btnSubmit = form.querySelector('#btn-submit');
        if (btnSubmit) {
          btnSubmit.querySelector('span').textContent = 'Actualizar';
          btnSubmit.querySelector('img').src = '/static/image/update.png';
        }

        Object.keys(data).forEach(campo => {
          const input = form.querySelector(`[name="${campo}"]`);
          if (input) {
            let valor = data[campo] || '';

            if (input.type === 'date' && valor) {
              const fecha = new Date(valor);
              valor = fecha.toISOString().split('T')[0]; // formato YYYY-MM-DD
            }

            if (input.multiple && Array.isArray(valor)) {
              [...input.options].forEach(option => {
                option.selected = valor.includes(option.value);
              });
            } else {
              input.value = valor;
            }
          }
        });

        const modal = form.closest('.emergente');
        if (modal) modal.style.display = "block";
      } catch (error) {
        console.error("Error al editar registro:", error.message);
      }
    });
}

// Cerrar formulario
function cerrarForm() {
  const modal = document.querySelector('.emergente[style*="block"]');
  if (modal) modal.style.display = "none";
}