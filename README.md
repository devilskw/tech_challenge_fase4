# Tech Challenge - Fase 4

## Turma
Grupo 16


### Integrantes

Samuel Kazuo Watanabe
kazuo_w@hotmail.com

Jonathan Maximo da Silva
jonathan.desenv@gmail.com

Samuel Rodrigues de Barros Mesquita Neto
samuelr.neto98@gmail.com

Michael Juvenal de Oliveira
Michael.etec@gmail.com


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
	"path_in": "assets\\in",
	"path_out": "assets\\out",
	"webcam": false,
	"test": true,
	"analyzers":{
		"face_analyzer":{
			"min_detection_confidence": 0.4
		},
		"gesture_analyzer":{
			"min_detection_confidence": 0.4
		}
	}
}

```

| chave | descrição | obrigatório |
| --- | --- | --- |
| path_in | caminho que indica os arquivos de entrada | S |
| path_out | caminho que indica os arquivos de saída | S |
| webcam | para testar com webcam | S |
| test | se ligado gera dados e imagens por amostragem | S |
| analyzers.face_analyzer.[min_detection_confidence](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md) | Vai entre 0 e 1, para o modelo considerar que o quanto a detecção considera sucesso | S |
| analyzers.gesture_analyzer.[min_detection_confidence](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/pose.md) | Vai entre 0 e 1, para o modelo considerar que o quanto a detecção considera sucesso | S |

---

## MyRecognizer: Video Analyzer

Os passos e idéias principais para este projeto foram:

- Ler algumas configuarações para a aplicação de **assets/config.json**
- ler o video que estaria em **assets/in**
- todo arquivo de output gravar em **assets/out**
- fazer a detecção e análise facial de emoções
- gravar as coordenadas no vídeo
- gerando um relatório e algumas imagens de amostragem
- fazer a detecção e análise de atividades/gestos
- possibilitar criar regras (e aumentar no futuro) para possíveis gestos (braço levantado, deitado, etc)
- gravar as coordenadas das [posições](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker?hl=pt-br) no vídeo
- gerando um relatório das posições e dos gestos separados e algumas imagens de amostragem

## Como rodo o projeto?

1. Copie o arquivo de vídeo (de preferência, renomeie o arquivo para teste.mp4) na pasta **assets/in**
2. verifique se tem arquivo na pasta **assets/out**. Se tiver, pode excluir
3. Abra o arquivo config.json e verifique se quer mudar alguma configuração
4. Na pasta raiz do projeto, usando o prompt de comando ou bash, digite o comando abaixo para instalar as dependências necessárias (lembrando que precisa ter o pythonmais recente instalado)

```bash
pip install -r requirements.txt
```

5. Ainda no prompt de comando ou bash, acesse a pasta src e execute o comando do python para iniciar a aplicação

```bash
cd src
python main.py
```

Obs.: Poderá também debugar pela IDE como o VsCode, apontando a execução para o arquivo main.py

### Documentação de apoio de

- [OpenCV](https://docs.opencv.org/4.x/)
- [DeepFace](https://github.com/serengil/deepface)
- [Pose Landmarks](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker?hl=pt-br)
- [PoseLandmark.Type](https://developers.google.com/android/reference/com/google/mlkit/vision/pose/PoseLandmark.Type)
