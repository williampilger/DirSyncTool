# DirSyncTool
Unidirecional directory sincronization tool.

Ferramenta simples para sincronizar unidirecionalmente pares de diretórios.

Esta ferramenta foi feita para ser executada rotineiramente por um *Windows Server* e enviar pastas específicas para backup no google drive.
Funciona perfeitamente para enviar pastas locais para o Google Drive e vice-versa (incluindo na versão em unidade virtual, com todos arquivos somente online).


## Download do binary

- [Windows Server 2008](dist/syncdir.exe);


## Utilização

Juntamente com o executável (seja o binário ou o script python) é obrigatória a criação do arquivo de configuração conforme o modelo abaixo:

*sunc_config.ini*
```ini
[Pair1]
source: path\to\source\folder1
destination: path\to\destination\folder1

[Pair2]
source: path\to\source\folder2
destination: path\to\destination\folder2

# Adicione mais pares de pastas conforme necessário
```

Agora basta executar para que a sincronização aconteça. Você pode criar uma rotina para que esta execução aconteça automaticamente.

Para fazer isso no Windows Server:
- Abra o gerenciador do servidor
- No canto superior direito clique nas *reticências*
- Clique no **Agendador de Tarefas**
- Crie uma nova tarefa para ser executada a cada X tempo ou dias



## Sobre

*Agradecimentos especiais ao ChatGPT, que fez isso praticamente sozinho. kkkk*

By: **will.i.am**
