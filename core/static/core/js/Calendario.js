document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos el elemento donde se renderizará el calendario
    const calendarEl = document.getElementById('calendar');

    // Inicializamos el calendario
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth', // Vista inicial
        locale: 'es', // Idioma del calendario
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/get-events/', // Ruta que devuelve los eventos en formato JSON
        eventClick: function (info) {
            // Muestra los detalles del evento al hacer clic en él
            alert(`Título: ${info.event.title}\nDescripción: ${info.event.extendedProps.description}`);
        },
        loading: function (isLoading) {
            // Muestra un mensaje de carga si es necesario
            if (isLoading) {
                console.log("Cargando eventos...");
            }
        }
    });

    // Renderizamos el calendario
    calendar.render();
});