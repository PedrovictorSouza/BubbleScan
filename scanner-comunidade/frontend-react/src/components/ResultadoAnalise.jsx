import React from 'react';
import './ResultadoAnalise.css';

export default function ResultadoAnalise({
  titulo = '',
  palavrasChave = [],
  tecnologias = [],
  sentimento = '',
  areaAtencao = '',
  caracterizacaoCultural = [],
  boasPraticas = [],
  exemplo = ''
}) {
  return (
    <div className="resultado-analise mt-8">
      {titulo && (
        <div className="text-center mb-4">
          <h2 className="text-3xl font-bold text-blue-900 tracking-tight mb-2">{titulo}</h2>
        </div>
      )}
      <h2 className="text-2xl font-bold text-center text-gray-800 tracking-tight" style={{ letterSpacing: '0.01em', marginTop: '25px', marginBottom: '0px', fontSize: '11pt' }}>Resultado da Análise</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Sentimento */}
        <div
          className="secao flex flex-col items-center shadow-md sentimento-card"
          style={{
            width: '25%',
            color: 'white',
          }}
        >
          <h3 className="text-xl font-semibold mb-4 uppercase tracking-wide" style={{ color: '#000000' }}>Humor coletivo</h3>
          <div className="flex flex-row gap-2 mb-4" style={{ display: 'flex', justifyContent: 'space-between', width: '150px' }}>
            {[
              { cor: '#4ade80', label: 'Entusiasmo', match: /entusiasmo/i },
              { cor: '#a3e635', label: 'Normalidade', match: /normalidade/i },
              { cor: '#facc15', label: 'Ceticismo', match: /ceticismo/i },
              { cor: '#f59e42', label: 'Estresse', match: /estresse/i },
              { cor: '#f87171', label: 'Decepção', match: /decepção|decepcao/i },
            ].map((nivel) => (
              <div
                key={nivel.label}
                title={nivel.label}
                style={{
                  width: '20px',
                  height: '5px',
                  borderRadius: '10px',
                  background: nivel.cor,
                  opacity: nivel.match.test(sentimento) ? 1.0 : 0.3,
                  transition: 'opacity 0.3s',
                }}
              ></div>
            ))}
          </div>
          <div className="sentimento text-2xl font-extrabold" style={{ marginTop: '10px', color: '#242424' }}>
            {sentimento}
          </div>
        </div>

        {/* Tecnologias */}
        <div className="secao bg-green-50 border-l-4 border-green-400 rounded-lg shadow-md p-8 flex flex-col items-center" style={{ width: '33%' }}>
          <h3 className="text-xl font-semibold mb-4 text-green-700 uppercase tracking-wide">Tecnologias</h3>
          <ul className="space-y-2 tecnologias-list">
            {tecnologias.map((tech) => (
              <li key={tech} className="text-gray-700 text-base">{tech}</li>
            ))}
          </ul>
        </div>

        {/* Palavras-chave */}
        <div className="secao bg-blue-50 border-l-4 border-blue-400 rounded-lg shadow-md p-8 flex flex-col items-center" style={{ width: '33%' }}>
          <h3 className="text-xl font-semibold mb-4 text-blue-700 uppercase tracking-wide">Palavras-chave</h3>
          <ul className="space-y-2">
            {palavrasChave.map((palavra) => (
              <li key={palavra} className="text-gray-700 text-base">{palavra}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Grid de Análise Sociocultural */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-center text-gray-800 tracking-tight" style={{ letterSpacing: '0.01em', marginBottom: 'none', marginTop: '50px', fontSize: '11pt' }}>Análise Sociocultural</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Área de Atenção */}
          <div
            className="secao flex flex-col items-center shadow-md"
            style={{
              background: '#e6f0ff',  /* 60% - Cor dominante */
              width: '29%',
              padding: '12.5px 25px 25px 25px',
              borderRadius: '20px',
              border: '1px solid #bab8b8',
            }}
          >
            <h3 className="text-xl font-semibold mb-4 text-blue-700 uppercase tracking-wide">Área de Atenção</h3>
            <p className="text-gray-800 text-center text-base font-medium whitespace-pre-line">
              {areaAtencao}
            </p>
          </div>

          {/* Caracterização Cultural */}
          <div
            className="secao flex flex-col items-center shadow-md"
            style={{
              background: '#ccffeb',  /* 30% - Cor secundária */
              width: '29%',
              padding: '12.5px 25px 25px 25px',
              borderRadius: '20px',
              border: '1px solid #bab8b8',
            }}
          >
            <h3 className="text-xl font-semibold mb-4 text-green-700 uppercase tracking-wide">Caracterização Cultural</h3>
            <ul className="space-y-2 caracterizacao-cultural-list">
              {caracterizacaoCultural.map((item, idx) => (
                <li key={idx} className="text-gray-700 text-base">{item}</li>
              ))}
            </ul>
          </div>

          {/* Boas Práticas de Expressão */}
          <div
            className="secao flex flex-col items-center shadow-md"
            style={{
              background: '#e6ccff',  /* 10% - Cor de destaque */
              width: '24%',
              padding: '12.5px 25px 25px 25px',
              borderRadius: '20px',
              border: '1px solid #bab8b8',
            }}
          >
            <h3 className="text-xl font-semibold mb-4 text-purple-700 uppercase tracking-wide">Boas Práticas de Expressão</h3>
            <ul className="space-y-2 boas-praticas-list">
              {boasPraticas.map((item, idx) => (
                <li key={idx} className="text-gray-700 text-base">{item}</li>
              ))}
            </ul>
          </div>

          {/* Exemplo */}
          <div className="secao bg-pink-50 border-l-4 border-pink-400 rounded-lg shadow-md p-8 flex flex-col items-center" style={{ minWidth: '100%' }}>
            <h2 className="text-lg font-semibold mb-4 text-pink-700 uppercase tracking-wide" style={{ fontSize: '11pt' }}>Exemplo</h2>
            <div
              className="text-center text-base font-normal italic"
              style={{ minWidth: '120px', marginTop: 0, background: '#6079ea', color: 'white', borderRadius: '10px', padding: '15px' }}
            >
              {exemplo}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 