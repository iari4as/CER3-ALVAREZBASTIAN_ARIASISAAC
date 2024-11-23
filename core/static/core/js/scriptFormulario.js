document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/eventos/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            // Redireccionar o actualizar la página
            window.location.href = '/';
        } else {
            const error = await response.json();
            alert(error.message || 'Error al crear el evento.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('No se pudo conectar con la API.');
    }
});