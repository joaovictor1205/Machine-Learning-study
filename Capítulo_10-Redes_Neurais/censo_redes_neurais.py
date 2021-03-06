#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:52:32 2020

@author: joao
"""

import pandas as pd

#importar a base de dados
base = pd.read_csv('census.csv')

#separar a base em dados categóricos
previsores = base.iloc[:, 0:14].values
classe = base.iloc[:,14].values

#importar libs
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

#transformar as informações categóricas para o formato discreto
labelEncoder_previsores = LabelEncoder()
previsores[:, 1] = labelEncoder_previsores.fit_transform(previsores[:, 1])
previsores[:, 3] = labelEncoder_previsores.fit_transform(previsores[:, 3])
previsores[:, 5] = labelEncoder_previsores.fit_transform(previsores[:, 5])
previsores[:, 6] = labelEncoder_previsores.fit_transform(previsores[:, 6])
previsores[:, 7] = labelEncoder_previsores.fit_transform(previsores[:, 7])
previsores[:, 8] = labelEncoder_previsores.fit_transform(previsores[:, 8])
previsores[:, 9] = labelEncoder_previsores.fit_transform(previsores[:, 9])
previsores[:, 13] = labelEncoder_previsores.fit_transform(previsores[:, 13])

#transformar valor para Dummy Variable
one_hot_encoder = ColumnTransformer(
    [('one_hot_encoder', OneHotEncoder(categories='auto'), [1,3,5,6,7,8,9,13])], remainder='passthrough'
)
previsores = one_hot_encoder.fit_transform(previsores).toarray()

#transformar a classe para o formato discreto
label_classe = LabelEncoder()
classe = label_classe.fit_transform(classe)

#escalonar os atributos
scaler = StandardScaler()
previsores = scaler.fit_transform(previsores)

#dividir a base entre treino e teste
from sklearn.model_selection import train_test_split
previsores_treino, previsores_teste, classe_treino, classe_teste = train_test_split(previsores, classe, test_size=0.15, random_state=0)

#SVM
from sklearn.neural_network import MLPClassifier
classificador = MLPClassifier(verbose = True,
                              max_iter = 1000,
                              tol = 0.00001)
classificador.fit(previsores_treino, classe_treino)

#resultado com os datasets de teste
resultado = classificador.predict(previsores_teste)

#analisar erros da classificação
from sklearn.metrics import confusion_matrix, accuracy_score
precisao = accuracy_score(classe_teste, resultado)
matriz = confusion_matrix(classe_teste, resultado)
