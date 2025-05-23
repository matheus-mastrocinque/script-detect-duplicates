# script-detect-duplicates

Este script ajuda a organizar um acervo de imagens identificando imagens duplicadas, mesmo que:

Tenham nomes diferentes;

Estejam em pastas diferentes;

Tenham pequenas alterações (como tamanho ou compressão diferente).

✅ O que ele faz na prática:
Procura todas as imagens numa pasta e subpastas.

Compara os arquivos:

Pelo nome do arquivo.

Pelo conteúdo do arquivo (mesmo arquivo, mesmo hash).

Pela aparência (visualmente iguais ou parecidas).

Gera um relatório com as duplicatas encontradas.

Pergunta se você quer mover os duplicados para uma pasta de backup.

Se você aceitar, ele cria a pasta backup_files e move os duplicados para lá.

▶️ Como usar?
Coloque o script detect_duplicates.py na pasta do projeto.

No terminal, rode:

python detect_duplicates.py

Digite o caminho da pasta onde estão as imagens.

Espere a análise terminar.

Responda s ou n para mover ou não os duplicados.

📁 Resultado
Um arquivo chamado duplicates_log.csv com a lista de imagens duplicadas.

Uma pasta backup_files com os arquivos duplicados (se você optar por mover).
