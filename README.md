# Tech Challenge - Fase 4


## Turma
Grupo 16


### Integrantes

Jonathan Maximo da Silva
jonathan.desenv@gmail.com

Michael Juvenal de Oliveira
Michael.etec@gmail.com

Samuel Kazuo Watanabe
kazuo_w@hotmail.com

Samuel Rodrigues de Barros Mesquita Neto
samuelr.neto98@gmail.com


## Sobre o desafio

O Tech Challenge desta fase será a criação de uma aplicação que utilize análise de vídeo, através de técnicas de reconhecimento facial, análise de expressões emocionais em vídeos e detecção de atividades.


### Tarefas que o projeto precisa realizar:

1. Reconhecimento facial: Identifique e marque os rostos presentes no vídeo.
2. Análise de expressões emocionais: Analise as expressões emocionais dos rostos identificados.
3. Detecção de atividades: Detecte e categorize as atividades sendo realizadas no vídeo.
4. Geração de resumo: Crie um resumo automático das principais atividades e emoções detectadas no vídeo.


## Entregáveis

1. Código Fonte: todo o código fonte da aplicação deve ser entregue em um repositório Git, incluindo um arquivo README com instruções claras de como executar o projeto.
2. Relatório: o resumo obtido automaticamente com as principais atividades e emoções detectadas no vídeo. Nesse momento esperando que o relatório inclua:
  -  Total de frames analisados.
  -  Número de anomalias detectadas.
Observação: movimento anômalo não segue o padrão geral de atividades (como gestos bruscos ou comportamentos atípicos) esses são classificados como anômalos.
3. Demonstração em Vídeo: um vídeo demonstrando a aplicação em funcionamento, evidenciando cada uma das funcionalidades implementadas.


## Nosso projeto

Este projeto será estruturado da seguinte forma:

- Na estrutura de pasta **src** ficarão organizados os códigos-fonte do projeto.
- Apesar de não ser uma boa prática de clean code, é possível que implementemos documentação a fim de apoiar nas explicações e/ou motivações para as ações e configurações, para fins acadêmicos;
- Na estrutura de pastas de **assets** conterá os materiais e arquivos de apoio ao projeto. Também será onde iremos gerar as resultantes (relatórios) da execução;

### Como funciona?

#### Configurações
A idéia inicial do projeto é que a gente deixe as configurações gerais para uso do sistema em um arquivo simple, chamado 'config.json', na pasta 'assets'.

Um exemplo dele abaixo, para facilitar o entendimento:

```json
{
  "general": {
    "path_in": "assets\\videos\\in",
    "path_out": "assets\\videos\\out"
  },
  "video": {
    "extension": ".mp4",
    "filename": "Unlocking Facial Recognition_ Diverse Activities Analysis.mp4"
  }
}
```

| chave | descrição | obrigatório |
| --- | --- | --- |
| general | para agrupar configuracoes gerais do projeto | - |
| general.path_in | caminho que indica os arquivos de entrada | S |
| general.path_out | caminho que indica os arquivos de saída | S |
| video | para agrupar configuracoes do video a ser analisado | - |
| video.extension | extensão do(s) vídeo(s) que serão analisados | S |
| video.filename | nome do arquivo de vídeo que será analisado | S |

#### FaceDetector - Analistar de Atividades e Expressões Faciais
A idéia foi colcoar dentro desta classe a solução do projeto, para facilitar o uso dele.

Para utlizá-la, ao instanciar a classe será necessario passar alguns valores de parâmetros, conforme abaixo:

| parâmetro | descrição | tipo | obrigatório |
| --- | --- | --- | --- |
| in_basepath | caminho que indica os arquivos de entrada | string | S |
| out_basepath | caminho que indica os arquivos de saída | string | S |
| video_extension | extensão do(s) vídeo(s) que serão analisados | string | S |

Teremos o método público **detect**, onde deve ser informado o nome do arquivo de vídeo a ser analisado (**video_filename**). 

Obs.: O arquivo de vídeo deverá estar na pasta equivalente ao **in_basepath**, e somente deve ser passado o nome do arquivo do vídeo (com a extensão) em **video_filename**

##### Método detect

O método irá usar a biblioteca **cv2** (OpenCV Python binary extension loader), que irá simplificar para a captura/leitura dos vídeo informado.

Basicamente, estes seriam os passos:

- O arquivo será lido, onde será possível pegar algumas propriedades que serão úteis para ser utilizadas mais para frente pelas demais bibliotecas;
- Será feita a leitura do vídeo por frame, sedo que, para cada captura, será analisada as expressões (método **__analyse_expressions**), passando o frame e seu identificador
- Será analisada ações frame-a-frame, onde será identificada e analisada as expressões faciais nos vídeos.
- Para este trabalho, iremos gravar um relatório das emoções identificadas com identificadores do frame (**__add_frame_emotion_report__**) , e serão geradas por amostragem algumas imagens do frame (**__generate_image__**), visando para apoiar este trabalho.
- Após isso será gravado o frame no novo vídeo.


## Documentação de apoio de

- [OpenCV](https://docs.opencv.org/4.x/)
- [DeepFace](https://github.com/serengil/deepface)
