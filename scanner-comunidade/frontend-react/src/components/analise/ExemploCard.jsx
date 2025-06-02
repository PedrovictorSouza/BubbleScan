import React from 'react';

export default function ExemploCard({ exemplo }) {
  return (
    <div 
      className="secao bg-pink-50 border-l-4 border-pink-400 rounded-lg shadow-md p-8 flex flex-col items-center" 
      style={{ minWidth: '100%' }}
    >
      <h2 
        className="text-lg font-semibold mb-4 text-pink-700 uppercase tracking-wide" 
        style={{ fontSize: '11pt' }}
      >
        Exemplo
      </h2>
      <div
        className="text-center text-base font-normal italic"
        style={{ 
          minWidth: '120px', 
          marginTop: 0, 
          background: '#6079ea', 
          color: 'white', 
          borderRadius: '10px', 
          padding: '15px' 
        }}
      >
        {exemplo}
      </div>
    </div>
  );
} 