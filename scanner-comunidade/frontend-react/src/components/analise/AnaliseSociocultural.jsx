import React from 'react';
import './AnaliseSociocultural.css';

export default function AnaliseSociocultural({ areaAtencao, caracterizacaoCultural, boasPraticas }) {
  return (
    <div className="mt-12">
      <h2 
        className="text-2xl font-bold text-center text-gray-800 tracking-tight" 
        style={{ letterSpacing: '0.01em', marginBottom: 'none', fontSize: '11pt' }}
      >
        Análise Sociocultural
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Área de Atenção */}
        <div
          className="secao flex flex-col items-center shadow-md analise-card card-area-atencao"
          style={{
            padding: '12.5px 25px 25px 25px',
            borderRadius: '20px',
            border: '1px solid #bab8b8',
          }}
        >
          <h3 className="text-xl font-semibold mb-4 text-blue-700 uppercase tracking-wide">
            <i className="fas fa-triangle-exclamation" style={{ marginRight: '6px', color: '#eab308' }}></i>
            Área de Atenção
          </h3>
          <p className="text-gray-800 text-center text-base font-medium whitespace-pre-line">
            {areaAtencao}
          </p>
        </div>

        {/* Caracterização Cultural */}
        <div
          className="secao flex flex-col items-center shadow-md analise-card card-caracterizacao-cultural"
          style={{
            padding: '12.5px 25px 25px 25px',
            borderRadius: '20px',
            border: '1px solid #bab8b8',
          }}
        >
          <h3 className="text-xl font-semibold mb-4 text-green-700 uppercase tracking-wide">
            Caracterização Cultural
          </h3>
          <ul className="space-y-2 caracterizacao-cultural-list">
            {caracterizacaoCultural.map((item, idx) => (
              <li key={idx} className="text-gray-700 text-base">
                {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Boas Práticas de Expressão */}
        <div
          className="secao flex flex-col items-center shadow-md analise-card card-boas-praticas"
          style={{
            padding: '12.5px 25px 25px 25px',
            borderRadius: '20px',
            border: '1px solid #bab8b8',
          }}
        >
          <h3 className="text-xl font-semibold mb-4 text-purple-700 uppercase tracking-wide">
            Boas Práticas de Expressão
          </h3>
          <ul className="space-y-2 boas-praticas-list">
            {boasPraticas.map((item, idx) => (
              <li key={idx} className="text-gray-700 text-base">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 