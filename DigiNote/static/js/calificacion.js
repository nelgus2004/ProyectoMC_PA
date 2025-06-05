document.addEventListener('DOMContentLoaded', function () {
    const selectEstudiante = document.querySelector('select[name="idMatriculaAsignacion"]:not(#select-materia)');
    const selectMateria = document.getElementById('select-materia');
    const quimestreSelect = document.querySelector('select[name="Quimestre"]');
    const btnGuardar = document.getElementById('btn-guardar-quimestre');
    const inputsNotas = document.querySelectorAll('input[name^="Nota"]');
    const form = document.getElementById('form-calificacion');

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

    // Al seleccionar quimestre, habilitar campos
    quimestreSelect.addEventListener('change', function () {
        inputsNotas.forEach(input => input.disabled = false);
    });

    // Enviar calificación
    btnGuardar.addEventListener('click', async function () {
        const formData = new FormData(form);
        const promedio = (
            parseFloat(formData.get('NotaAutonoma') || 0) +
            parseFloat(formData.get('NotaPractica') || 0) +
            parseFloat(formData.get('NotaLeccion') || 0) +
            parseFloat(formData.get('NotaExamen') || 0)
        ) / 4;

        formData.set('PromedioQuimestre', promedio.toFixed(2));

        try {
            const res = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            const text = await res.text();

            if (res.ok) {
                alert('✅ Calificación guardada correctamente.');
                location.reload(); // o cerrar modal y actualizar tabla
            } else {
                console.error('Error en respuesta:', text);
                alert('❌ Error al guardar calificación.');
            }
        } catch (err) {
            console.error('Error al guardar calificación:', err);
            alert('❌ Error de red.');
        }
    });
});