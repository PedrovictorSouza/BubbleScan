import React, { useState } from 'react';
import DevbotLog from './DevbotLog';
import ResultadoAnalise from './ResultadoAnalise';
import axios from 'axios';

export default function HomeScreen() {
  const [inputUrl, setInputUrl] = useState('');
  const [urlError, setUrlError] = useState('');
  const [mostrarResultado, setMostrarResultado] = useState(false);
  const [resultadoTitulo, setResultadoTitulo] = useState('');
  const [resultadoPalavras, setResultadoPalavras] = useState([]);
  const [resultadoTecnologias, setResultadoTecnologias] = useState([]);
  const [resultadoSentimento, setResultadoSentimento] = useState('');
  const [areaAtencao, setAreaAtencao] = useState('');
  const [caracterizacaoCultural, setCaracterizacaoCultural] = useState([]);
  const [boasPraticas, setBoasPraticas] = useState([]);
  const [exemplo, setExemplo] = useState('');
  const [logs, setLogs] = useState([]);
  const [showLog, setShowLog] = useState(false);
  const [loadingDots, setLoadingDots] = useState(0);

  const isMock = import.meta.env.VITE_USE_MOCK === 'true';
  const endpoint = isMock
    ? 'http://127.0.0.1:8000/api/analise-mock'
    : `${import.meta.env.VITE_API_URL}/api/analise`;

  React.useEffect(() => {
    let interval;
    if (showLog && logs.length > 0 && logs[logs.length - 1].includes('Análise concluída')) {
      interval = setInterval(() => {
        setLoadingDots(d => (d + 1) % 4);
      }, 400);
    } else {
      setLoadingDots(0);
    }
    return () => clearInterval(interval);
  }, [showLog, logs]);

  const analisarUrl = async () => {
    setUrlError('');
    setMostrarResultado(false);
    setShowLog(true);
    setLogs(["Preparando análise..."]);

    setTimeout(() => setLogs(logs => [...logs, "Coletando dados..."]), 500);
    setTimeout(() => setLogs(logs => [...logs, "Enviando para IA..."]), 1000);
    setTimeout(() => setLogs(logs => [...logs, "Processando resposta..."]), 1500);

    if (inputUrl.trim().toLowerCase() === 'teste') {
      setTimeout(() => {
        setResultadoPalavras(["privacy", "signal", "encryption", "cloud", "ai"]);
        setResultadoTecnologias(["Spring Boot", "Docker", "Java"]);
        setResultadoSentimento("estresse coletivo");
        setAreaAtencao("O desejo precisa ser filtrado antes de ser apresentado.\nSe você mostrar ambição demais, vão te chamar de egocêntrico.\nNa cultura hacker, crie como quem apenas quis resolver um problema,\ne deixe que os outros descubram que foi genial.");
        setCaracterizacaoCultural([
          "Comunicação direta e objetiva",
          "Valorização do conhecimento técnico",
          "Abertura para inovação"
        ]);
        setBoasPraticas([
          "Evite sarcasmo e ironia",
          "Valorize contribuições construtivas",
          "Use exemplos práticos ao argumentar"
        ]);
        setExemplo("Em uma discussão sobre segurança, membros destacaram soluções práticas e evitaram julgamentos pessoais, promovendo um ambiente de aprendizado coletivo.");
        setLogs(logs => [...logs, "Análise concluída!"]);
        setTimeout(() => {
          setShowLog(false);
          setMostrarResultado(true);
        }, 1200);
      }, 2000);
      return;
    }

    try {
      const response = await axios.post(endpoint, {
        url: inputUrl
      });
      const { titulo, palavras_chave, tecnologias, sentimento, area_atencao, caracterizacao_cultural, boas_praticas, exemplo } = response.data;
      setResultadoTitulo(titulo);
      setResultadoPalavras(palavras_chave);
      setResultadoTecnologias(tecnologias);
      setResultadoSentimento(sentimento);
      setAreaAtencao(area_atencao);
      setCaracterizacaoCultural(Array.isArray(caracterizacao_cultural) ? caracterizacao_cultural : (caracterizacao_cultural ? [caracterizacao_cultural] : []));
      setBoasPraticas(Array.isArray(boas_praticas) ? boas_praticas : (boas_praticas ? [boas_praticas] : []));
      setExemplo(exemplo);
      setLogs(logs => [...logs, "Análise concluída!"]);
      setTimeout(() => {
        setShowLog(false);
        setMostrarResultado(true);
      }, 1200);
    } catch (error) {
      const errorMessage = `[✘] Erro na requisição: ${error.message}`;
      setLogs(logs => [...logs, errorMessage]);
      setTimeout(() => setShowLog(false), 2000);
      setUrlError('Erro na análise. Tente novamente.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h1
                  className={`text-2xl font-bold mb-2 text-center text-gray-900`}
                  style={{ ...(mostrarResultado ? { fontSize: '16pt' } : {}), marginBottom: '5px' }}
                >
                  Bubble <span style={{ fontFamily: 'Lexend Giga, sans-serif' }}>Scan</span>
                </h1>
                <p className="text-sm text-gray-600 text-center mb-8 -mt-2">Feramenta de mapeamento do impulso coletivo.</p>
                {/* Input URL + Botão Analisar juntos */}
                <div className="mb-8 w-full">
                  <label htmlFor="url" className="block font-medium text-gray-700 mb-2 text-left" style={{ fontSize: '11pt' }}>Cole o link no campo abaixo</label>
                  <div className="flex flex-col md:flex-row md:items-center gap-4 w-full" style={{ justifyContent: 'space-between', display: 'flex' }}>
                    <input
                      type="text"
                      id="url"
                      value={inputUrl}
                      onChange={e => setInputUrl(e.target.value)}
                      placeholder="cole aqui a url"
                      className={`w-full px-4 py-2 border-2 rounded-md focus:ring-blue-500 focus:border-orange-400 italic placeholder-gray-400 ${urlError ? 'border-red-500' : 'border-gray-300'}`}
                      style={{ paddingLeft: '5px', minWidth: '220px', width: '90%' }}
                    />
                    <button
                      onClick={analisarUrl}
                      className={`analisar-btn px-6 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-300 ${inputUrl.trim() ? '' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
                      style={inputUrl.trim() ? { background: 'rgb(96, 121, 234)', color: 'white', minWidth: '120px', marginTop: '0', marginLeft: '10px' } : { minWidth: '120px', marginTop: '0', marginLeft: '10px' }}
                      disabled={!inputUrl.trim()}
                    >
                      Analisar
                    </button>
                    {urlError && <p className="mt-2 text-sm text-red-600 w-full">{urlError}</p>}
                  </div>
                </div>
                {/* Logs */}
                {showLog && (
                  <DevbotLog logs={
                    logs.map((log, idx) =>
                      idx === logs.length - 1 && log.includes('Análise concluída')
                        ? log + '.'.repeat(loadingDots)
                        : log
                    )
                  } />
                )}
                {/* Resultado */}
                {mostrarResultado && (
                  <>
                    <ResultadoAnalise
                      titulo={resultadoTitulo}
                      palavrasChave={resultadoPalavras}
                      tecnologias={resultadoTecnologias}
                      sentimento={resultadoSentimento}
                      areaAtencao={areaAtencao}
                      caracterizacaoCultural={caracterizacaoCultural}
                      boasPraticas={boasPraticas}
                      exemplo={exemplo}
                    />
                    <footer className="mt-6 text-center text-gray-500 text-sm py-6 border-t border-gray-200" style={{ marginTop: '25px', marginBottom: '25px' }}>
                      <div>Contato: <a href="mailto:contato@bubblescan.com" className="underline hover:text-blue-700">contato@bubblescan.com</a></div>
                      <div className="mt-2">Bubble Scan &copy; {new Date().getFullYear()}</div>
                    </footer>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 