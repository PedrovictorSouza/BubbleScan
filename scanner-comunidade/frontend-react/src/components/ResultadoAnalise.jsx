import React from 'react';
import './ResultadoAnalise.css';
import SentimentoCard from './analise/SentimentoCard';
import TecnologiasList from './analise/TecnologiasList';
import PalavrasChaveList from './analise/PalavrasChaveList';
import AnaliseSociocultural from './analise/AnaliseSociocultural';
import ExemploCard from './analise/ExemploCard';

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
      <h2 
        className="text-2xl font-bold text-center text-gray-800 tracking-tight" 
        style={{ letterSpacing: '0.01em', marginTop: '25px', marginBottom: '0px', fontSize: '11pt', color: 'white' }}
      >
        Resultado da Análise
      </h2>
      <div className="resultado-grid">
        <SentimentoCard sentimento={sentimento} />
        <TecnologiasList tecnologias={tecnologias} />
        <PalavrasChaveList palavrasChave={palavrasChave} />
      </div>

      <AnaliseSociocultural 
        areaAtencao={areaAtencao}
        caracterizacaoCultural={caracterizacaoCultural}
        boasPraticas={boasPraticas}
      />

      <ExemploCard exemplo={exemplo} />
    </div>
  );
} 