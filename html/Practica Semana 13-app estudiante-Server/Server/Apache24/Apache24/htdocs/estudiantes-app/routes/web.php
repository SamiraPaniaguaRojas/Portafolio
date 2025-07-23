<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\EstudianteController;

Route::get('/', [EstudianteController::class, 'create']);
Route::post('/guardar', [EstudianteController::class, 'store']);