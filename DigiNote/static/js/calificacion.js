document.addEventListener('DOMContentLoaded', function () {
    const selectEstudiante = document.querySelector('select[name="idMatriculaAsignacion"]:not(#select-materia)');
    const selectMateria = document.getElementById('select-materia');
    const inputsNotas = document.querySelectorAll('input[name^="Nota"]');
    const form = document.getElementById('form-calificacion');
    const btnGuardar = document.querySelector('#btn-submit');

    // Al cambiar estudiante, obtener materias (asignaciones)
    selectEstudiante.addEventListener('change', async function () {
        const idEstudiante = this.value;

        // Limpiar y deshabilitar
        selectMateria.innerHTML = `<option disabled selected>Cargando...</option>`;
        selectMateria.disabled = true;

        try {
            const res = await fetch(`/app/calificacion/asignaciones/${idEstudiante}`);
            const asignaciones = await res.json();

            selectMateria.innerHTML = `<option value="" disabled selected>Seleccione Materia</option>`;
            asignaciones.forEach(a => {
                selectMateria.innerHTML += `<option value="${a.idMatriculaAsignacion}">${a.materia} - ${a.profesor} (${a.nivel} ${a.paralelo})</option>`;
            });

            selectMateria.disabled = false;
        } catch (err) {
            console.error('Error cargando asignaciones:', err);
            alert('No se pudieron cargar las materias.');
        }
    });

    // Al seleccionar una materia, habilitar campos de notas
    selectMateria.addEventListener('change', function () {
        inputsNotas.forEach(input => input.disabled = false);
    });

    // Enviar calificación completa (Q1, Q2 y final)
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const res = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            const text = await res.text();

            if (res.ok) {
                location.reload();
            } else {
                console.error('Error en respuesta:', text);
            }
        } catch (err) {
            console.error('Error al guardar calificación:', err);
        }
    });
});
