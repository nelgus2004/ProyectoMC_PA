const get = document.getElementById('rutas').dataset.get;
const update = document.getElementById('rutas').dataset.update;

async function verCalificaciones(idEstudiante) {
    try {
        const response = await fetch(`${get}/${idEstudiante}`);
        const data = await response.json();


        if (!data.materias || data.materias.length === 0) {
            return;
        }

        const tabla = document.getElementById("tabla-calificaciones").querySelector("#cuerpo-tabla");
        tabla.innerHTML = "";
        data.materias.forEach((materia) => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td id="idEstudiante" style="display:none;">${data.idEstudiante}</td>
                <td>${data.cedula}</td>
                <td>${data.estudiante}</td>
                <td>${materia.profesor}</td>
                <td>${materia.materia}</td>

                <td>${materia.notas.primer_quimestre.autonoma}</td>
                <td>${materia.notas.primer_quimestre.practica}</td>
                <td>${materia.notas.primer_quimestre.leccion}</td>
                <td>${materia.notas.primer_quimestre.examen}</td>
                <td>${materia.notas.primer_quimestre.promedio}</td>

                <td>${materia.notas.segundo_quimestre.autonoma}</td>
                <td>${materia.notas.segundo_quimestre.practica}</td>
                <td>${materia.notas.segundo_quimestre.leccion}</td>
                <td>${materia.notas.segundo_quimestre.examen}</td>
                <td>${materia.notas.segundo_quimestre.promedio}</td>

                <td>${materia.notas.final}</td>
                <td class="table__btn table__actions">
                    <button type="button" class="btn btn__edit" data-id="${materia.idMatriculaAsignacion}" data-estudiante="${data.idEstudiante}" data-name="calificacion">
                        <img src="/static/image/edit.png" alt="editar">
                    </button>
                    <button type="button" class="btn btn__reset" data-id="${materia.idMatriculaAsignacion}">
                        <img src="/static/image/reset.png" alt="borrar">
                    </button>
                </td>
            `;

            tabla.appendChild(fila);
        });

    } catch (error) {
        console.error(" * Error al obtener calificaciones:", error);
    }
}

// Delegación de eventos para botones dinámicos
document.addEventListener('click', function (e) {
    const btnEdit = e.target.closest('.btn__edit');
    const btnReset = e.target.closest('.btn__reset');

    // Botón editar (abre formulario emergente con datos)
    if (btnEdit) {
        const idEstudiante = btnEdit.dataset.estudiante;
        const idMatriculaAsignacion = btnEdit.dataset.id;
        verFormularioCalificaciones(idEstudiante, idMatriculaAsignacion);
    }

    // Botón reset (enviar formulario vacío para reiniciar calificaciones)
    if (btnReset) {
        const id = btnReset.dataset.id;
        const url = `${update}/${id}`;
        if (confirm("¿Seguro que deseas resetar las calificaciones?")) {
            const formData = new FormData();
            formData.append('reset', 'true');
            fetch(url, {
                method: 'POST',
                body: formData,
            })
                .then(res => {
                    if (!res.ok) throw new Error(`Error HTTP ${res.status}`);

                    const estudianteId = document.getElementById('idEstudiante').innerHTML;
                    if (estudianteId) verCalificaciones(estudianteId);
                })
                .catch(err => {
                    console.error(" * Error al reiniciar calificación:", err);
                });

        }
    }
});

document.getElementById("btn-reload").addEventListener("click", () => {
    const tabla = document.getElementById("cuerpo-tabla");
    tabla.innerHTML = `
        <tr>
            <td colspan="16" class="table__empty">Elija un estudiante</td>
        </tr>
    `;
});



async function verFormularioCalificaciones(idEstudiante, idMatriculaAsignacion) {
    try {
        const response = await fetch(`${get}/${idEstudiante}`);
        const data = await response.json();

        console.log(data)

        if (!data.materias || data.materias.length === 0) {
            throw new Error('No se encontraron datos de calificación');
        }

        const materia = data.materias.find(m => m.idMatriculaAsignacion == idMatriculaAsignacion);
        if (!materia) throw new Error('No se encontró la materia con el ID especificado');


        const form = document.getElementById('form-calificacion');
        form.action = `${update}/${idMatriculaAsignacion}`;

        // Llenar campos estáticos
        document.getElementById("campo-estudiante").value = data.estudiante;
        document.getElementById("campo-materia").value = materia.materia;
        document.getElementById("input-idMatriculaAsignacion").value = materia.idMatriculaAsignacion;

        // Llenar campos de notas dinámicamente
        const notas = materia.notas;

        const fieldMap = {
            'NotaAutonoma1': notas.primer_quimestre.autonoma,
            'NotaPractica1': notas.primer_quimestre.practica,
            'NotaLeccion1': notas.primer_quimestre.leccion,
            'NotaExamen1': notas.primer_quimestre.examen,
            'NotaAutonoma2': notas.segundo_quimestre.autonoma,
            'NotaPractica2': notas.segundo_quimestre.practica,
            'NotaLeccion2': notas.segundo_quimestre.leccion,
            'NotaExamen2': notas.segundo_quimestre.examen
        };

        Object.entries(fieldMap).forEach(([fieldName, value]) => {
            const input = form.querySelector(`[name="${fieldName}"]`);
            if (input) {
                input.value = value || '0';
            }
        });

        document.getElementById("modal-calificacion").style.display = "block";

    } catch (error) {
        console.error("Error al cargar datos para edición:", error);
    }
}


