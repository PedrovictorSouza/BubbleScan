import React from 'react';

export default function PalavrasChaveList({ palavrasChave }) {
  return (
    <div 
      className="secao bg-purple-50 border-l-4 border-purple-400 rounded-lg shadow-md p-8 flex flex-col items-center resultado-card" 
      style={{ width: '100%' }}
    >
      <h3 className="text-xl font-semibold mb-4 text-purple-700 uppercase tracking-wide">
        Palavras-chave
      </h3>
      <ul className="space-y-2 palavras-chave-list">
        {palavrasChave.map((palavra) => (
          <li key={palavra} className="text-gray-700 text-base">
            {palavra}
          </li>
        ))}
      </ul>
    </div>
  );
} 