<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro de Estudiante</title>
    @vite('resources/js/app.js')
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen">

    <div class="w-full max-w-md">
        @if(session('mensaje'))
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
                {{ session('mensaje') }}
            </div>
        @endif

        <form action="/guardar" method="POST" class="bg-white p-8 rounded shadow-md">
            @csrf
            <h2 class="text-2xl font-bold mb-6 text-center">Nuevo Estudiante</h2>
            <input type="text" name="nombre" placeholder="Nombre" required class="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
            <input type="text" name="direccion" placeholder="Dirección" required class="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
            <input type="text" name="ciudad" placeholder="Ciudad" required class="w-full mb-6 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
            <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-3 rounded w-full transition-colors">Guardar</button>
        </form>
    </div>

</body>
</html>


