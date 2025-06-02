import React from 'react';

export default function SentimentoCard({ sentimento }) {
  return (
    <div
      className="secao flex flex-col items-center shadow-md sentimento-card resultado-card"
      
    >
      <h3 className="text-xl font-semibold mb-4 uppercase tracking-wide" style={{ color: '#000000' }}>
        Humor coletivo
      </h3>
      <div 
        className="sentimento text-2xl font-extrabold" 
        
      >
        {sentimento}
      </div>
    </div>
  );
} 