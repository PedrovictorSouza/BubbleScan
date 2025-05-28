import { ref } from 'vue'

export function useDevbotLog() {
  const logs = ref([])

  const iniciarLogs = (url) => {
    // Limpa logs anteriores
    logs.value = []
    
    // Sequência de logs com delay
    const sequencia = [
      `→ Análise iniciada com a URL: ${url}`,
      "→ Extraindo comentários do Hacker News...",
      "→ Identificando palavras-chave...",
      "→ Mapeando tecnologias citadas...",
      "→ Analisando sentimento coletivo...",
      "→ Análise concluída."
    ]

    // Adiciona cada log com intervalo de 1 segundo
    sequencia.forEach((mensagem, index) => {
      setTimeout(() => {
        logs.value.push(mensagem)
      }, index * 1000)
    })
  }

  return {
    logs,
    iniciarLogs
  }
} 