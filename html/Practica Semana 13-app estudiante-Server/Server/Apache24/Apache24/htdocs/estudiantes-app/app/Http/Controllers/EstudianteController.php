<?php

namespace App\Http\Controllers;

use App\Models\Estudiante;
use Illuminate\Http\Request;

class EstudianteController extends Controller
{
    public function create()
    {
        return view('formulario');
    }

    public function store(Request $request)
    {
        Estudiante::create([
            'nomEstudiante' => $request->nombre,
            'dirEstudiante' => $request->direccion,
            'ciuEstudiante' => $request->ciudad
        ]);
        return redirect('/')->with('mensaje', 'Estudiante registrado');
    }
}
