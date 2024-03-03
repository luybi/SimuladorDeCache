# SimuladorDeCache
Um simulador de cache implementado em Python para a disciplina de AOC2.
Este projeto oferece uma ferramenta eficiente para entender e simular o comportamento de caches em sistemas computacionais.

O simulador pode simular mapeamento direto, totalmente associativo ou conjunto-associativo
Alem disso 3 politicas de substituicao sendo elas:

LRU (Least Recently Used):
Substitui o bloco que foi acessado menos recentemente.
Baseia-se na premissa de que os blocos menos recentemente usados são os menos prováveis de serem acessados novamente em breve.
Mantém um registro do histórico de acessos e substitui o bloco que foi o menos recentemente acessado quando a cache está cheia.

FIFO (First In, First Out):
Substitui o bloco que foi armazenado na cache há mais tempo.
Opera como uma fila, onde o primeiro bloco que entrou na cache é o primeiro a ser substituído quando a cache está cheia.
Não considera a frequência ou a ordem de acesso dos blocos, apenas o tempo em que foram armazenados.

Random (Aleatório):
Substitui aleatoriamente um bloco da cache quando é necessário fazer uma substituição.
Não considera o histórico de acesso ou a ordem dos blocos.
Cada bloco tem uma probabilidade igual de ser substituído, independentemente de quando foi acessado pela última vez.



Para utilizacao deste simulador use o seguinte comando:
python cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
*Certifique-se de que os arquivos de entrada se encontram no mesmo diretorio do programa python


Onde cada um destes campos possui o seguinte significado:
• cache_simulator - nome do arquivo de execução principal do simulador (todos devem usar este
nome, independente da linguagem escolhida;
• nsets - número de conjuntos na cache (número total de “linhas” ou “entradas” da cache);
• bsize - tamanho do bloco em bytes;
• assoc - grau de associatividade (número de vias ou blocos que cada conjunto possui);
• substituição - política de substituição, que pode ser Random (R), FIFO (F) ou L (LRU);
• flag_saida - flag que ativa o modo padrão de saída de dados;
• arquivo_de_entrada - arquivo com os endereços para acesso à cache.
