# python -m venv venv
# source ./venv/Scripts/activate
# pip install pandas numpy matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# OBTENDO OS DADOS


try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS,sep=';',encoding='iso-8859-1')

    # RECUPERAÇÃO DE VEÍCULOS POR CISP
  
    df_recuperacao = df_ocorrencias[['cisp', 'recuperacao_veiculos']]
    df_recuperacao = (df_recuperacao.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum())
    df_recuperacao = df_recuperacao.sort_values(by='recuperacao_veiculos',ascending=False)

except Exception as e:
    print(f'Erro ao obter os dados: {e}')
    exit()


# ANÁLISE ESTATÍSTICA

try:
    print('\nObtendo informações sobre recuperação de veículos...')

    array = np.array(df_recuperacao['recuperacao_veiculos'])
    media = np.mean(array)
    mediana = np.median(array)
    distancia = abs((media - mediana) / mediana * 100)

    print('\nMedidas de Tendência Central')
    print(40 * '=')
    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Distância Média vs Mediana: {distancia}%')

    # Obtendo os quartis
    q1 = np.quantile(array, 0.25)
    q2 = np.quantile(array, 0.50)
    q3 = np.quantile(array, 0.75)

    print('\nMedidas de Posição')
    print(40 * '=')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # menores
    df_menores = df_recuperacao[df_recuperacao['recuperacao_veiculos'] < q1]

    # maiores
    df_maiores = df_recuperacao[df_recuperacao['recuperacao_veiculos'] > q3]

    print('\nCISPs com Maiores Recuperações')
    print(40 * '=')
    print(df_maiores)

    print('\nCISPs com Menores Recuperações')
    print(40 * '=')
    print(df_menores.sort_values(by='recuperacao_veiculos', ascending=True))

except Exception as e:
    print(f'Erro ao calcular estatísticas: {e}')


# MEDIDAS DE DISPERSÃO
# Amplitude Total = maior_valor - menor_valor
# Quanto mais próximo de zero, maior a homogeneidade dos dados
# Se for igual a 0, todos os dados são iguais
# Quanto mais próximo do maior valor, maior a dispersão

try:
    maximo = np.max(array)
    minimo = np.min(array)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(40 * '=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro na dispersão: {e}')


# OUTLIERS
#   IQR (Intervalo Interquartil)
#   É a amplitude dos 50% dos dados mais centrais
#   IQR = q3 - q1
#   Ele ignora os valores mais extremos, max e min estão fora.
#   Não sofre influência dos extremos
#   Quanto mais próximo de zero, maior a homogeneidade dos dados
#   Se for igual a 0, todos os dados são iguais
#   Quanto mais próximo do Q3, maior a dispersão

try:
    iqr = q3 - q1

 # limite inferior
    limite_inferior = q1 - (1.5 * iqr)

# limite superior
    limite_superior = q3 + (1.5 * iqr)

# outliers

    df_recuperacao_outliers_superiores = df_recuperacao[df_recuperacao['recuperacao_veiculos'] > limite_superior]
    df_recuperacao_outliers_inferiores = df_recuperacao[df_recuperacao['recuperacao_veiculos'] < limite_inferior]

    print('\nOutliers Superiores')
    print(40 * '=')
    print(df_recuperacao_outliers_superiores)

    print('\nOutliers Inferiores')
    print(40 * '=')
    print(df_recuperacao_outliers_inferiores if len(df_recuperacao_outliers_inferiores) > 0 else 'Não existem outliers inferiores')

except Exception as e:
    print(f'Erro nos outliers: {e}')


# CALCULANDO ASSIMETRIA E CURTOSE


try:
    assimetria = df_recuperacao['recuperacao_veiculos'].skew()
    curtose = df_recuperacao['recuperacao_veiculos'].kurtosis()

    print('\nDistribuição dos Dados')
    print(40 * '=')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro na distribuição: {e}')


# Medidas de Dispersão "Variabilidade"


try:
    variancia = np.var(array)
    desvio_padrao = np.std(array)
    coef_variacao = desvio_padrao / media

    print('\nVariabilidade')
    print(40 * '=')
    print(f'Variância: {variancia}')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variacao}')

except Exception as e:
    print(f'Erro na variabilidade: {e}')


# Visualizando os dados


try:
    plt.figure(figsize=(16, 8))

    # 1 Maiores
    plt.subplot(2, 2, 1)
    top10 = df_recuperacao.head(10).sort_values(by='recuperacao_veiculos')
    plt.barh(top10['cisp'], top10['recuperacao_veiculos'])
    plt.title('Top 10 CISPs - Recuperação')

    # P/ printar as faixas de intervalo do Histograma
    plt.subplot(2, 2, 2)
    plt.hist(array, bins=30)
    plt.axvline(media, color='green')
    plt.axvline(mediana, color='orange')
    plt.title('Distribuição das Recuperações')

     # POSIÇÃO 3 - BOXPLOT
    plt.subplot(2, 2, 3)
    plt.boxplot(array, vert=False)
    plt.title('Boxplot')

    # POSIÇÃO 4 - MEDIDAS ESTATÍSTICAS
    plt.subplot(2, 2, 4)
    plt.text(0.1, 0.9, f'Média: {media:.2f}')
    plt.text(0.1, 0.8, f'Mediana: {mediana:.2f}')
    plt.text(0.1, 0.7, f'Amplitude: {amplitude}')
    plt.text(0.1, 0.6, f'Q1: {q1}')
    plt.text(0.1, 0.5, f'Q3: {q3}')
    plt.text(0.1, 0.4, f'IQR: {iqr}')
    plt.text(0.1, 0.3, f'Assimetria: {assimetria}')
    plt.text(0.1, 0.2, f'Curtose: {curtose}')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro nos gráficos: {e}')