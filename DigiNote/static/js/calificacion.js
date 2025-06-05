document.addEventListener('DOMContentLoaded', () => {
  const estudianteSelect = document.querySelector('[name="idMatriculaAsignacion"]');
  const materiaSelect = document.getElementById('select-materia');
  const quimestreSelect = document.querySelector('[name="Quimestre"]');
  const btnGuardarQuimestre = document.getElementById('btn-guardar-quimestre');
  const btnSubmit = document.querySelector('#btn-submit');
  const form = document.getElementById('form-calificacion');
  const rutaAsignaciones = `/app/calificacion/asignaciones/`;
  const rutaGet = rutas.get;
  const rutaAdd = rutas.add;

  const notaInputs = ['NotaAutonoma', 'NotaPractica', 'NotaLeccion', 'NotaExamen'];
  const promedioInput = form.querySelector('[name="PromedioQuimestre"]');

  let idMatriculaAsignacion = null;
  let datosTemporales = { "1": null, "2": null };

  toggleNotas(false);
  materiaSelect.disabled = true;
  quimestreSelect.disabled = true;

  estudianteSelect.addEventListener('change', () => {
    const idEstudiante = estudianteSelect.value;
    if (!idEstudiante) return;

    materiaSelect.innerHTML = '<option disabled selected>Cargando materias...</option>';
    materiaSelect.disabled = true;
    quimestreSelect.value = '';
    quimestreSelect.disabled = true;
    form.reset();
    datosTemporales = { "1": null, "2": null };

    fetch(`${rutaAsignaciones}/${idEstudiante}`)
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
      });
  });

  materiaSelect.addEventListener('change', () => {
    idMatriculaAsignacion = materiaSelect.value;
    quimestreSelect.value = '';
    quimestreSelect.disabled = !idMatriculaAsignacion;
    toggleNotas(false);
    form.reset();
  });

  quimestreSelect.addEventListener('change', () => {
    const quimestre = quimestreSelect.value;
    if (!quimestre || !idMatriculaAsignacion) {
      toggleNotas(false);
      return;
    }

    form.reset();
    toggleNotas(true);

    // Precargar datos si ya se guardaron temporalmente
    if (datosTemporales[quimestre]) {
      cargarEnFormulario(datosTemporales[quimestre]);
    } else {
      // Cargar del backend si existe
      fetch(`${rutaGet}/${idMatriculaAsignacion}/${quimestre}`)
        .then(res => res.json())
        .then(data => {
          if (data && data.idQuimestre) {
            cargarEnFormulario(data);
            calcularPromedio();
          }
        });
    }
  });

  notaInputs.forEach(nombre => {
    form.querySelector(`[name="${nombre}"]`).addEventListener('input', calcularPromedio);
  });

  btnGuardarQuimestre.addEventListener('click', () => {
    const quimestre = quimestreSelect.value;
    if (!quimestre) return;

    const datos = {
      Quimestre: quimestre,
      idMatriculaAsignacion,
      PromedioQuimestre: promedioInput.value
    };
    notaInputs.forEach(nombre => {
      datos[nombre] = form.querySelector(`[name="${nombre}"]`).value || 0;
    });

    datosTemporales[quimestre] = datos;
    alert(`Notas del Quimestre ${quimestre} guardadas temporalmente.`);
    form.reset();
    toggleNotas(false);
    quimestreSelect.value = '';
  });

  form.addEventListener('submit', e => {
    e.preventDefault();

    const quim1 = datosTemporales["1"];
    const quim2 = datosTemporales["2"];

    if (!quim1 && !quim2) {
      return alert("Debe guardar al menos un quimestre.");
    }

    const payload = {
      idMatriculaAsignacion,
      quimestres: []
    };

    if (quim1) payload.quimestres.push(quim1);
    if (quim2) payload.quimestres.push(quim2);

    fetch(rutaAdd, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(resp => {
        alert(resp.msg || 'Calificaciones guardadas correctamente');
        form.reset();
        quimestreSelect.disabled = true;
        materiaSelect.disabled = true;
        toggleNotas(false);
        datosTemporales = { "1": null, "2": null };
      })
      .catch(err => console.error(' * Error al guardar calificaciones:', err));
  });

  function toggleNotas(habilitar) {
    notaInputs.forEach(nombre => {
      const input = form.querySelector(`[name="${nombre}"]`);
      if (input) input.disabled = !habilitar;
    });
  }

  function cargarEnFormulario(datos) {
    notaInputs.forEach(nombre => {
      form.querySelector(`[name="${nombre}"]`).value = datos[nombre] || 0;
    });
    calcularPromedio();
  }

  function calcularPromedio() {
    let suma = 0;
    notaInputs.forEach(nombre => {
      suma += parseFloat(form.querySelector(`[name="${nombre}"]`).value) || 0;
    });
    promedioInput.value = (suma / notaInputs.length).toFixed(2);
  }
});
