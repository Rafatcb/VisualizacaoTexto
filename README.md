# Visualização de Texto
Projeto realizado na disciplina de Visualização de Informação, UNICAMP - 20187.

***
### Descrição
Uma página web que mostra o nível de similaridade entre um conjunto de textos. Os textos são avaliados conforme o cálculo do **Tf-idf** de cada palavra de cada texto, posteriormente é feito o cálculo da **distância de Manhattan** entre todas as palavras de todos textos, então é feito um grafo de forças no estilo **Galaxy** para a visualização, onde as arestas não são exibidas e os nós são um retângulo com baixa opacidade sendo identificáveis pelo nome do arquivo que o retângulo representa.

O tratamento dos textos (remoção das _stop words_ e pontuações) e cálculo do **Tf-idf** é feito através do Python, e a visualização é feita em HTML, CSS e Javascript. Foi utilizada a biblioteca [D3.js](https://d3js.org/) para a visualização.

Os textos utilizados estão na pasta **Textos** e são transcrições dos episódios da primeira temporada de **Game of Thrones**.

***
### Objetivo
Desenvolver um sistema que permita a visualização do nível de similaridade entre um conjunto de textos através da técnica **Galaxy**, utilizando o cálculo **Tf-idf** e o cálculo de distância entre os vetores de característica de cada texto.

***
### Conhecimentos Aplicados
HTML, CSS, Javascript, JSON, Python.

### Observações
* É necessário a hospedagem em um servidor (mesmo que seja local) para o site funcionar corretamente.
