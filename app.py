<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Sistema de Producción</title>

<style>
body{
  margin:0;
  font-family: 'Segoe UI', sans-serif;
  background:#f4f6f9;
}

header{
  background: linear-gradient(90deg,#1e3c72,#2a5298);
  color:white;
  padding:20px;
  text-align:center;
  font-size:22px;
  font-weight:bold;
  letter-spacing:1px;
}

.container{
  max-width:900px;
  margin:30px auto;
  padding:20px;
}

.card{
  background:white;
  padding:25px;
  border-radius:12px;
  box-shadow:0 5px 15px rgba(0,0,0,0.08);
  margin-bottom:30px;
}

.card h2{
  margin-top:0;
  color:#2a5298;
}

label{
  font-weight:600;
  font-size:14px;
}

input, select{
  width:100%;
  padding:10px;
  margin:8px 0 15px 0;
  border-radius:8px;
  border:1px solid #ddd;
  font-size:14px;
  box-sizing:border-box;
}

select{
  appearance:none;
  background:white url("data:image/svg+xml;utf8,<svg fill='%232a5298' height='20' viewBox='0 0 24 24' width='20' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>") no-repeat right 10px center;
  background-size:15px;
}

button{
  background:#2a5298;
  color:white;
  border:none;
  padding:12px;
  width:100%;
  border-radius:8px;
  font-size:16px;
  cursor:pointer;
  transition:0.3s;
}

button:hover{
  background:#1e3c72;
}

.footer{
  text-align:center;
  font-size:12px;
  color:#888;
  margin-top:20px;
}
</style>
</head>

<body>

<header>
Sistema de Registro de Producción
</header>

<div class="container">

<div class="card">
<h2>Nuevo Registro</h2>

<form id="form">

<label>Nombre del Operador</label>
<input type="text" id="operador" placeholder="Ingrese nombre del operador" required>

<label>Exportadora</label>
<select id="exportadora" required>
  <option value="">Seleccione exportadora</option>
  <option value="Fruclem">Fruclem</option>
  <option value="JHB">JHB</option>
  <option value="Talamaya">Talamaya</option>
</select>

<label>Categoría</label>
<select id="categoria" required>
  <option value="">Seleccione categoría</option>
  <option value="Premium">Premium</option>
  <option value="Extra">Extra</option>
  <option value="Fancy Choice">Fancy Choice</option>
  <option value="Granel">Granel</option>
</select>

<label>Salida</label>
<select id="salida" required>
  <option value="">Seleccione salida</option>
  <!-- Generado dinámicamente -->
</select>

<label>Calibre</label>
<input type="text" id="calibre" placeholder="Ej: 2J, 3J, XL..." required>

<label>Peso (kg)</label>
<input type="number" id="peso" step="0.01" placeholder="Ej: 12.5" required>

<button type="submit">Guardar Registro</button>

</form>
</div>

<div class="footer">
Sistema desarrollado para control interno de producción
</div>

</div>

<script>
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyeI6iwqoQ5JOacFq7CfHzswQRz8YpVxXKprN9XVCCbPkvsDh9GdvYUhusYGkh4kAOb/exec";

const form = document.getElementById("form");
const salidaSelect = document.getElementById("salida");

/* Generar salidas del 1 al 41 automáticamente */
for(let i = 1; i <= 41; i++){
  let option = document.createElement("option");
  option.value = i;
  option.text = "Salida " + i;
  salidaSelect.appendChild(option);
}

form.addEventListener("submit", function(e){
  e.preventDefault();

  const data = {
    operador: document.getElementById("operador").value,
    exportadora: document.getElementById("exportadora").value,
    categoria: document.getElementById("categoria").value,
    salida: document.getElementById("salida").value,
    calibre: document.getElementById("calibre").value,
    peso: document.getElementById("peso").value
  };

  fetch(SCRIPT_URL,{
    method:"POST",
    body:JSON.stringify(data)
  })
  .then(res=>res.json())
  .then(response=>{
    if(response.status==="success"){
      alert("Registro guardado correctamente");
      form.reset();
    }else{
      alert("Error: "+response.messag
