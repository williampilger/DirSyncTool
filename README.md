# DirSyncTool
Unidirecional directory sincronization tool.

Ferramenta simples para sincronizar unidirecionalmente pares de diretórios.

Esta ferramenta foi feita para ser executada rotineiramente por um *Windows Server* e enviar pastas específicas para backup no google drive.
Funciona perfeitamente para enviar pastas locais para o Google Drive e vice-versa (incluindo na versão em unidade virtual, com todos arquivos somente online).


## Download do binary

- [Windows Server 2008](dist/syncdir.exe);


## Utilização

Juntamente com o executável (seja o binário ou o script python) é obrigatória a criação do arquivo de configuração conforme o modelo abaixo:

*sync_config.ini*
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

### Histórico de modificações
*As primeiras versões não foram salvas nem catalogadas adequadamente, portanto, esta relação, antes da versão 1.0, pode não estar exatamente correta.*
```txt
V0.0
- Sincronização de pastas. Copiando sempre todos os itens novamente.

V0.1
- Arquivos e diretórios já existentes não são copiados novamente
- Correção e tratamento de exceções

V0.2
- MUDANÇA DE COMO AS CONFIGURAÇÕES SÃO SALVAS
- Lista de arquivos ignorados

V0.3
- Correção na lista de arquivos ignorados
- Criação do LOG das operações

V1.0
- Implementação do resumo ao final da operação, com contagem de arquivos com sucesso e falha
- LOGs: Melhoria no detalhamento de operações que falharam

V1.1
- Correção do nome da variável 'self' em certos pontos
- LOG: Correção do espaço de fim de Sync, que estava acontecendo na linha errada
- Identificação da versão em código
```

*Agradecimentos especiais ao ChatGPT, que fez a versão 0.0 praticamente sozinho. kkkk*

By: **will.i.am**
