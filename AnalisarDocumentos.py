# -*- coding: utf-8 -*-

## Antes de utilizar este programa, é preciso ter instalado o ntlk no seu computador
## para instalar via comandos, basta digitar:
##        import ntlk
##        ntlk.download()
## Após isso irá abrir um instalador para a biblioteca

import os, glob, string
from nltk.corpus import stopwords
import math, json
from scipy.spatial import distance

class Distancia:
    def __init__(self, deDoc, paraDoc, distanciaDocs):
        self.de = deDoc
        self.para = paraDoc
        self.distancia = distanciaDocs

contractions_dict = { 
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how does",
    "i'd": "I had",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

def expand_contractions(palavra, lista):
    lista.append(contractions_dict[palavra].split())

def getNomeDocumento(arquivo):
    return os.path.basename(arquivo.name).split(".txt")[0]

def separarPalavras(texto):
    palavras_separadas = [palavra.strip(string.punctuation) for palavra in texto.split()]
    return palavras_separadas

def filtrar(palavras):
    stop_words = set(stopwords.words('english'))
    palavras_filtradas = []
    for palavra in palavras:
        palavra = palavra.lower()
        if '’' in palavra:
            palavra = palavra.replace("’", "\'")
        if '\'' in palavra:
            try:
                expand_contractions(palavra)
            except: 
                continue
        if '…' in palavra:
            palavra = palavra.replace("…", "")
        if '–' in palavra:
            palavra = palavra.replace("–", "")
        if '”' in palavra:
            palavra = palavra.replace("”", "")
        if '.' in palavra:
            palavra = palavra.replace(".", "")
        if not palavra in stop_words and palavra != "uh" and palavra != "hey":
            palavras_filtradas.append(palavra) 
    return palavras_filtradas

def transformarMaiusculo(palavras):
    palavras_maiusculas = [palavra.upper() for palavra in palavras if palavra]
    return palavras_maiusculas

def calcOcorrencias(palavras):
    ocorrencias = {}
    for palavra in palavras:
        if (palavra not in ocorrencias):
            ocorrencias[palavra] = 1
        else:
            ocorrencias[palavra] += 1
    return ocorrencias

def calcTf(ocorrencias):
    tf = {}
    qtd_palavras = len(ocorrencias)
    for palavra in ocorrencias:
        tf[palavra] = ocorrencias[palavra] / qtd_palavras
    return tf

def calcTfidf(tf, qtd_documentos, todos_tf):
    tfidf = {}
    for palavra in tf:
        df = 0
        for documento in todos_tf:
            if palavra in documento:
                df += 1
                
        tfidf[palavra] = tf[palavra] * math.log10((qtd_documentos / df))
             
    return tfidf

def getPalavrasTfidfDocumento(num_documento, todos_tfidf):
    documento = {}
    for palavras_doc in todos_tfidf:
        print(str(palavras_doc))
        for tupla in palavras_doc:
            for palavra in tupla:
                try:
                    documento[palavra] = todos_tfidf[num_documento][palavra]
                except:
                    documento[palavra] = 0
                break
    return documento

def jsonData(distancias, nomes_documentos):
    json = {}
    json['nodes'] = []
    i = 0
    qtd_documentos = len(nomes_documentos)
    while i < qtd_documentos:
        dados = {}
        dados['id'] = str(i)
        dados['text'] = nomes_documentos[i]
        dados['group'] = 0
        json['nodes'].append(dados)
        i += 1
    
    json['links'] = []
    for distancia in distancias:
        dados = {}
        if (distancia.distancia != 0):
            dados['source'] = str(distancia.de)
            dados['target'] = str(distancia.para)
            dados['value'] = distancia.distancia
            json['links'].append(dados)
    return json

def main():
    path = os.getcwd() + '\\Textos'
    todos_tf = []
    todos_tfidf = []
    nomes_documentos = []
    qtd_documentos = 0
    
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(filename, 'r') as arquivo:
            qtd_documentos += 1
            nomes_documentos.append(getNomeDocumento(arquivo))
            palavras_prontas = transformarMaiusculo(filtrar(separarPalavras(arquivo.read())))      
            todos_tf.append(calcTf(calcOcorrencias(palavras_prontas)))
    
    i = 0
    while i < qtd_documentos:
        todos_tfidf.append(calcTfidf(todos_tf[i], qtd_documentos, todos_tf))
        i += 1
        
    caracteristicas_documentos = []
    j = 0
    while j < qtd_documentos:
        caracteristicas_documentos.append(getPalavrasTfidfDocumento(j, todos_tfidf))
        j += 1
        
    distancias = []
    count = 0
    for documento in caracteristicas_documentos:
        k = count
        while k < qtd_documentos:
            de = []
            para = []
            for key in documento:
                de.append(documento[key])
            for key in caracteristicas_documentos[k]:
                para.append(caracteristicas_documentos[k][key])
            distancias.append(Distancia(count, k, distance.euclidean(de, para)))
            k += 1
        count += 1
    
    with open('data.json', 'w') as arquivo_saida:
        arquivo_saida.write(json.dumps(jsonData(distancias, nomes_documentos), indent = 4))

main()