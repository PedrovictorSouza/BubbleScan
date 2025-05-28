import React, { useState, useEffect } from 'react';

export default function DevbotLog({ logs = [] }) {
  const [dots, setDots] = useState(0);
  useEffect(() => {
    if (logs.length > 0 && !logs[logs.length - 1].toLowerCase().includes('concluída')) {
      const interval = setInterval(() => {
        setDots(d => (d + 1) % 4);
      }, 400);
      return () => clearInterval(interval);
    } else {
      setDots(0);
    }
  }, [logs]);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      background: 'rgba(255,255,255,0.95)',
      zIndex: 9999,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div className="bg-gray-900 text-gray-200 rounded-lg p-8 font-mono text-base shadow-xl w-full max-w-xl text-center border-2 border-gray-300">
        <div className="whitespace-pre-line min-h-[60px] text-base font-normal">
          {logs.length === 0 ? (
            <span className="text-gray-600">Nenhum log ainda...</span>
          ) : (
            logs.map((log, idx) => {
              const isLast = idx === logs.length - 1;
              const isLoading = isLast && !log.toLowerCase().includes('concluída');
              return (
                <div key={idx} className="leading-relaxed mb-2 flex items-center justify-center gap-2">
                  {!isLast && (
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 22,
                        height: 22,
                        borderRadius: '50%',
                        background: '#22c55e',
                      }}
                    >
                      <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
                        <path
                          d="M5 10.5L9 14.5L15 7.5"
                          stroke="white"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </span>
                  )}
                  <span style={{ marginLeft: 5 }}>
                    {log}
                    {isLoading && (
                      <span style={{ display: 'inline-block', width: 24 }}>
                        {'.'.repeat(dots)}
                        <span style={{ opacity: 0.2 }}>{'.'.repeat(3 - dots)}</span>
                      </span>
                    )}
                  </span>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
} 