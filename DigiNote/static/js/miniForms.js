const div = document.getElementById('rutas');
let rutas = {};
if (window.location.pathname !== "/app/inicio/") {
  rutas = {
    deleteOther: div.dataset.delete_other || null
  };
}

document.addEventListener('DOMContentLoaded', () => {
  const miniForm = document.getElementById('mini-form');
  const name = miniForm?.dataset.name;

  const placeholder = document.getElementById('mini-form-placeholder');

  placeholder.appendChild(miniForm);

  const btnAbrir = document.getElementById(`abrir-${name}`);
  const btnEliminar = document.getElementById(`eliminar-${name}`);
  const btnCerrar = document.getElementById(`cerrar-${name}`);
  const select = document.getElementById(name);
  const form = miniForm.querySelector('form');

  // Mostrar mini formulario
  btnAbrir?.addEventListener('click', () => {
    placeholder.classList.add('visible')
    miniForm.classList.add('visible');
    select.disabled = true;

    btnAbrir.disabled = true;
    btnAbrir.classList.add('disabled-btn');
    btnEliminar.disabled = true;
    btnEliminar.classList.add('disabled-btn');
  });

  // Cerrar mini formulario
  btnCerrar?.addEventListener('click', () => {
    miniForm.classList.remove('visible');
    placeholder.classList.remove('visible');
    select.disabled = false;

    btnAbrir.disabled = false;
    btnAbrir.classList.remove('disabled-btn');
    btnEliminar.disabled = false;
    btnEliminar.classList.remove('disabled-btn');
  });

  // Guardar datos
  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();

      btnAbrir.disabled = true;
      btnAbrir.classList.add('disabled-btn');
      btnEliminar.disabled = true;
      btnEliminar.classList.add('disabled-btn');

      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData
        });

        const result = await response.json();
        console.log(result);

        if (result.id) {
          const option = document.createElement('option');
          option.value = result.id;
          option.textContent = result.nombre;
          option.selected = true;
          select.appendChild(option);

          // Ocultar formulario
          miniForm.classList.remove('visible');
          placeholder.classList.remove('visible');
          select.disabled = false;
        }
      } catch (error) {
        console.error('Error al guardar:', error);
      }

      btnAbrir.disabled = false;
      btnAbrir.classList.remove('disabled-btn');
      btnEliminar.disabled = false;
      btnEliminar.classList.remove('disabled-btn');
    });
  }

  // Eliminar
  btnEliminar?.addEventListener('click', () => {
    const idCurso = select?.value;
    if (!idCurso) {
      alert("Seleccione un curso para eliminar.");
      return;
    }
    if (confirm("¿Seguro que desea eliminar el curso seleccionado?")) {
      window.location.href = `${rutas.deleteOther}/${idCurso}`;
    }
  });
});