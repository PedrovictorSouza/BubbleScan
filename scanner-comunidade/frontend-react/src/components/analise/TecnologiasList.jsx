import React from 'react';

export default function TecnologiasList({ tecnologias }) {
  return (
    <div 
      className="secao bg-green-50 border-l-4 border-green-400 rounded-lg shadow-md p-8 flex flex-col items-center resultado-card" 
      
    >
      <h3 className="text-xl font-semibold mb-4 text-green-700 uppercase tracking-wide">
        Tecnologias
      </h3>
      <ul className="space-y-2 tecnologias-list">
        {tecnologias.map((tech) => (
          <li key={tech} className="text-gray-700 text-base">
            {tech}
          </li>
        ))}
      </ul>
    </div>
  );
} 