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
  const endpoint = isMock ? '/api/analise-mock' : '/api/analise_auto';

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

      const { sentimento, titulo, palavras_chave, tecnologias, area_atencao, caracterizacao_cultural, boas_praticas, exemplo } = response.data;

      setResultadoSentimento(sentimento);
      setResultadoTitulo(titulo);
      setResultadoPalavras(palavras_chave || []);
      setResultadoTecnologias(tecnologias || []);
      setAreaAtencao(area_atencao || "");
      setCaracterizacaoCultural(Array.isArray(caracterizacao_cultural) ? caracterizacao_cultural : (caracterizacao_cultural ? [caracterizacao_cultural] : []));
      setBoasPraticas(Array.isArray(boas_praticas) ? boas_praticas : (boas_praticas ? [boas_praticas] : []));
      setExemplo(exemplo || "");

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
                <div className="cabecalho-bubblescan">
                  <div className="cabecalho-bubblescan-titulo" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                    <img src="/imgs/logo.png" alt="Logo BubbleScan" style={{ height: '38px', width: '38px', objectFit: 'contain' }} />
                    <h1
                      className={`text-2xl font-bold mb-2 text-center text-gray-900`}
                      style={{ ...(mostrarResultado ? { fontSize: '16pt' } : {}), marginBottom: '5px' }}
                    >
                      Bubble <span style={{ fontFamily: 'Lexend Giga, sans-serif' }}>Scan</span>
                    </h1>
                  </div>
                  {!mostrarResultado && (
                    <p className="text-sm text-gray-600 text-center mb-8 -mt-2">Ferramenta de mapeamento do impulso coletivo.</p>
                  )}
                  {/* Input URL + Botão Analisar juntos */}
                  <div className="mb-8 w-full">
                    <label
                      htmlFor="url"
                      className="block font-medium text-gray-700 mb-2 text-left"
                      style={{ fontSize: '11pt' }}
                    >
                      Cole o link no campo abaixo
                    </label>
                    <div className="flex flex-col md:flex-row md:items-center gap-4 w-full" style={{ justifyContent: 'space-between', display: 'flex' }}>
                      <div className="input-icone-wrapper" style={{ position: 'relative', width: '100%' }}>
                        <input
                          id="url"
                          placeholder="cole aqui a url"
                          className="input-com-icone w-full px-4 py-2 border-2 rounded-md focus:ring-blue-500 focus:border-orange-400 italic placeholder-gray-400 border-gray-300"
                          type="text"
                          value={inputUrl}
                          onChange={e => setInputUrl(e.target.value)}
                          style={{ paddingLeft: '38px', minWidth: '220px', width: '100%' }}
                        />
                        <img
                          src="/imgs/search-ico.png"
                          alt="ícone de busca"
                          style={{
                            position: 'absolute',
                            left: 12,
                            top: '50%',
                            transform: 'translateY(-50%)',
                            width: 18,
                            height: 18,
                            pointerEvents: 'none'
                          }}
                        />
                      </div>
                      <button
                        className="analisar-btn px-6 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-300 "
                        style={{
                          minWidth: '120px',
                          marginTop: '0px',
                          marginLeft: '10px',
                          background: 'rgb(96, 121, 234)',
                          color: 'white',
                        }}
                        onClick={analisarUrl}
                      >
                        Analisar
                      </button>
                    </div>
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
                      <div className="mt-2">BubbleScan &copy; {new Date().getFullYear()}</div>
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