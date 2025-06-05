document.addEventListener('DOMContentLoaded', () => {
  const rolSelect = document.getElementById('rol-select');
  const vinculoSelect = document.getElementById('vinculo-select');
  const campoVinculo = document.getElementById('campo-vinculo');
  const rutaVinculo = document.getElementById('rutas').dataset.vinculo;

  rolSelect.addEventListener('change', () => {
    const rol = rolSelect.value;
    const nombreCampo = {
      Estudiante: 'idEstudiante',
      Profesor: 'idProfesor',
      Admin: 'idAdministrador'
    }[rol];

    if (nombreCampo) {
      vinculoSelect.disabled = false;
      campoVinculo.name = nombreCampo;

      fetch(`${rutaVinculo}/${rol}`)
        .then(res => res.json())
        .then(data => {
          vinculoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
          data.forEach(item => {
            vinculoSelect.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
          });
        });
    } else {
      vinculoSelect.disabled = true;
      vinculoSelect.innerHTML = '';
      campoVinculo.name = '';
      campoVinculo.value = '';
    }
  });

  // Cuando el usuario selecciona una opción del vínculo, actualizamos el input hidden
  vinculoSelect.addEventListener('change', () => {
    campoVinculo.value = vinculoSelect.value;
  });
});
