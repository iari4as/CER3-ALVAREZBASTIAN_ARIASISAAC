document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/get-events/', // URL que devuelve eventos y feriados
        eventClick: function (info) {
            // Mostrar detalles del evento/feriado
            alert(`Título: ${info.event.title}\nDescripción: ${info.event.extendedProps.description}`)
        }
    });

    calendar.render();
});