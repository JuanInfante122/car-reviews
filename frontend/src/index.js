import React from 'react';
import ReactDOM from 'react-dom/client'; // Importa desde 'react-dom/client'
import App from './App';

// Selecciona el elemento del DOM donde se montará la aplicación
const rootElement = document.getElementById('root');

// Crea una raíz con el elemento del DOM
const root = ReactDOM.createRoot(rootElement);

// Renderiza la aplicación en la raíz
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
