const div = document.getElementById('rutas');
let rutas = {};
if (window.location.pathname !== "/app/inicio/") {
  rutas = {
    add: div.dataset.add,
    get: div.dataset.get,
    update: div.dataset.update,
    delete: div.dataset.delete,
    asignacion: div.dataset.asignaciones
  };
}

document.addEventListener('DOMContentLoaded', () => {
  const estudianteSelect = document.getElementById('select-estudiante');
  const materiaSelect = document.getElementById('select-materia');
  const quimestreSelect = document.getElementById('quimestre-select');
  const form = document.getElementById('form-quimestre');
  const notaInputs = ['NotaAutonoma', 'NotaPractica', 'NotaLeccion', 'NotaExamen'];
  const promedioInput = form.querySelector('[name="PromedioQuimestre"]');
  const rutaGet = rutas.get;
  const rutaAdd = rutas.add;

  const extraForm = document.getElementById('quimestre-form');
  const placeholder = document.getElementById('modal-quimestre');
  placeholder.appendChild(extraForm);

  let idMatriculaAsignacion = null;

  // Inicializa el formulario deshabilitado
  toggleForm(false);
  materiaSelect.disabled = true;
  quimestreSelect.disabled = true;

  estudianteSelect.addEventListener('change', () => {
    const idEstudiante = estudianteSelect.value;
    if (!idEstudiante) return;

    materiaSelect.innerHTML = '<option disabled selected>Cargando materias...</option>';
    materiaSelect.disabled = true;
    quimestreSelect.value = '';
    quimestreSelect.disabled = true;
    toggleForm(false);
    form.reset();

    fetch(`${rutas.asignacion}/${idEstudiante}`)
      .then(res => res.json())
      .then(data => {
        materiaSelect.innerHTML = '<option value="" disabled selected>Seleccione una materia</option>';
        data.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m.idMatriculaAsignacion;
          opt.textContent = `${m.materia} - ${m.profesor} (${m.nivel}${m.paralelo})`;
          materiaSelect.appendChild(opt);
        });
        materiaSelect.disabled = false;
      })
      .catch(err => {
        console.error(' * Error al cargar materias:', err);
        materiaSelect.innerHTML = '<option disabled selected>Error al cargar</option>';
      });
  });

  materiaSelect.addEventListener('change', () => {
    idMatriculaAsignacion = materiaSelect.value;
    quimestreSelect.value = '';
    quimestreSelect.disabled = !idMatriculaAsignacion;
    toggleForm(false);
    form.reset();
  });

  quimestreSelect.addEventListener('change', () => {
    const quimestre = quimestreSelect.value;
    if (!quimestre || !idMatriculaAsignacion) {
      toggleForm(false);
      return;
    }

    toggleForm(true);
    form.reset();
    form.querySelector('[name="Quimestre"]').value = quimestre;
    form.querySelector('[name="idMatriculaAsignacion"]').value = idMatriculaAsignacion;

    fetch(`${rutaGet}/${idMatriculaAsignacion}/${quimestre}`)
      .then(res => res.json())
      .then(data => {
        if (data && data.idCalificacionQuimestre) {
          notaInputs.forEach(nombre => {
            form.querySelector(`[name="${nombre}"]`).value = data[nombre] || 0;
          });
          calcularPromedio();
        }
      });
  });

  notaInputs.forEach(nombre => {
    const input = form.querySelector(`[name="${nombre}"]`);
    input.addEventListener('input', calcularPromedio);
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const datos = {};
    new FormData(form).forEach((v, k) => datos[k] = v || 0);

    fetch(rutaAdd, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    })
      .then(res => res.json())
      .then(resp => {
        alert(resp.msg || 'Calificación guardada correctamente');
        form.reset();
        toggleForm(false);
        quimestreSelect.value = '';
      })
      .catch(err => {
        console.error(' * Error al guardar calificación:', err);
      });
  });

  function calcularPromedio() {
    let suma = 0;
    let count = 0;
    notaInputs.forEach(nombre => {
      const val = parseFloat(form.querySelector(`[name="${nombre}"]`).value) || 0;
      suma += val;
      count += 1;
    });
    promedioInput.value = (suma / count).toFixed(2);
  }

  function toggleForm(habilitar) {
    form.querySelectorAll('input, select, button').forEach(el => {
      if (['Quimestre'].includes(el.name)) return;
      el.disabled = !habilitar;
    });
  }
});
