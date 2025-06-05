// Mostrar/Ocultar opciones filtro
document.getElementById('btn-filtro').addEventListener('click', () => {
  const opciones = document.getElementById('filtro-opciones');
  opciones.style.display = opciones.style.display === 'none' ? 'flex' : 'none';
});

function filtrarEstudiantes() {

  const nivel = document.getElementById('filtro-nivel').value;
  const paralelo = document.getElementById('filtro-paralelo').value;
  const id_periodo = document.getElementById('filtro-periodo') ? document.getElementById('filtro-periodo').value : null;
  const buscar = document.getElementById('buscar-estudiante').value.trim().toLowerCase();
  const contenedor = document.getElementById('contenedorCards');

  if (!contenedor) {
    console.warn('contenedorCards no encontrado');
    return;
  }

  // Construir URL con parámetros
  const url = new URL('/data_estudiantes', window.location.origin);
  if (nivel) url.searchParams.append('nivel', nivel);
  if (paralelo) url.searchParams.append('paralelo', paralelo);
  if (id_periodo) url.searchParams.append('id_periodo', id_periodo);

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const contenedor = document.getElementById('contenedorCards');
      contenedor.innerHTML = '';

      if (!data.length) {
        contenedor.innerHTML = '<p>No hay estudiantes registrados actualmente.</p>';
        return;
      }

      // Si hay búsqueda de texto, filtrar por cédula o nombre
      let resultados = data;
      if (buscar) {
        resultados = data.filter(est =>
          est.Cedula.toLowerCase().includes(buscar) ||
          (`${est.Nombre} ${est.Apellido}`.toLowerCase().includes(buscar))
        );
      }

      resultados.forEach(est => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
                    <div class="card__content">
                        <h3 class="card__title">${est.Cedula}</h3>
                        <p><b>Nombre:</b> ${est.Nombre} ${est.Apellido}</p>
                        <p><b>Nivel:</b> ${est.NivelCurso} ${est.Paralelo}</p>
                        <p><b>Periodo:</b> ${est.idPeriodo || 'N/A'}</p>
                    </div>
                    <div class="card__btn">
                        <button type="button" class="btn btn__edit" data-id="${est.idEstudiante}">
                            Editar
                        </button>
                        <button type="button" class="btn btn__delete" data-id="${est.idEstudiante}">
                            Borrar
                        </button>
                    </div>
                `;
        contenedor.appendChild(card);
      });
    })
    .catch(err => console.error('Error cargando estudiantes:', err));
}

// Listeners para disparar filtros
document.getElementById('filtro-nivel').addEventListener('change', filtrarEstudiantes);
document.getElementById('filtro-paralelo').addEventListener('change', filtrarEstudiantes);
document.getElementById('buscar-estudiante').addEventListener('input', filtrarEstudiantes);
if (document.getElementById('filtro-periodo')) {
  document.getElementById('filtro-periodo').addEventListener('change', filtrarEstudiantes);
}

// Ejecutar filtro inicial al cargar página
filtrarEstudiantes();



