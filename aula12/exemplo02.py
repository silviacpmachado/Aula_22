# python -m venv venv
# source ./venv/Scripts/activate
# pip install pandas numpy matplotlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 


# obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # iso-8859-1  | utf-8  | latin1 | cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    # agrupando e quantificando as variáveis quantitativa
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    # ordenando em decrescente:
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)
    
    # print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro ao obter os dados: {e}')
    exit()


# Obtendo informações
try:
    print('Obtendo informações a cerca dos roubos de veículos... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)


    print('\nMedidas de tendência Central')
    print(40*'=')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância ente média e mediana: {distancia}%')


    # Obtendo os quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)

    print('\nMedidas de Posição')
    print(40*'=')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')


    # menores
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

    # maiores
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]
    
    print('\nMunicípios com Mais Roubos')
    print(40*'=')
    print(df_roubo_veiculo_maiores)

    print('\nMunicípios com Menos Roubos')
    print(40*'=')
    # ordem decrescente
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

except Exception as e:
    print(f'Erro ao calcular as informações...')


# Medidas de Dispersão - Amplitude Total
try:
    # Amplitude Total = maior_valor - menor_valor
    # Quanto mais próximo de zero, maior a homogeneidade dos dados
    # Se for igual a 0, todos os dados são iguais
    # Quanto mais próximo do maior valor, maior a dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(40*'=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medida de dispersão {e}')


# Outliers
try:
#   IQR (Intervalo Interquartil)
#   É a amplitude dos 50% dos dados mais centrais
#   IQR = q3 - q1
#   Ele ignora os valores mais extremos, max e min estão fora.
#   Não sofre influência dos extremos
#   Quanto mais próximo de zero, maior a homogeneidade dos dados
#   Se for igual a 0, todos os dados são iguais
#   Quanto mais próximo do Q3, maior a dispersão
    iqr = q3 - q1  # 969.5

    # print(f'\nIQR: {iqr}')

    # limite inferior
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior
    limite_superior = q3 + (1.5 * iqr)


    # outliers
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
        
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print('\nMedidas:')
    print(40*'=')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')  # mediana
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')


    print('\nOutliers Superiores:')
    print(40*'=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores)


    print('\nOutliers Inferiores:')
    print(40*'=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores)

except Exception as e:
    print(f'Erro ao calcular Outliers {e}')


# Calculando a Assimetria
try:
    # Assimetria
    # Medida q indica como os dados estão distriuidos em torno do valor central
    # Estão distribuidos em torno do Centro?
    # Existe uma qtd maior de registros altos ou baixos?
    # Para que lado está o peso.
    # É a medida usada para descrever o grau de simetria ou assimetria

    # INTERPRETAÇÃO (Pontos de Observação):
    # Assimetria > 1: Positiva Alta
    # Valores Altos puxando a média para cima.
    # A média tende a ser maior que a mediana

    # Assimetria entre 0.5 e 1: Positiva Moderada
    # Há cauda à direita, mas é menos acentuada

    # Assimetria entre -0.5 e 0.5: Distribuição aproximadamente Simétrica
    # Tendência de dados equilibrados
    # A média, a mediana, e a moda tenha valores próximos

    # Assimetria entre -1 e -0.5: Negativa Moderada
    # Há cauda à esquerda, mas é menos acentuada

    # Assimetria < -1: Negativa Alta
    # Valores Baixo puxando a média para Baixo.
    # A média tende a ser menor que a mediana
    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()


    # Curtose de Fisher (Padrão do Pandas)
    # Descreve o formato da distribuição
    # Nos ajuda a entender como os dados estão concentrados, 
    # se próximo a média, ou mais espalhados.
    # Pode indicar outliers.

    # Interpretação:
    # Curtose = 0 (Mesocúrtica)
    # Concentração moderada no centro
    # Extremos com menos relevância


    # Curtose > 0 (leptocúrtica) 
    # Pico mais alto
    # Mais valores próximo a média
    # Comum ter outliers bem pesados


    # Curtose < 0 (platicúrtica)
    # Pico mais achatado
    # Dados mais espalhado
    # Poucos extremos, mas pode haver outliers

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()

    print('\nMedidas de Distribuição')
    print(40*'=')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao calcular medida de distribuição: {e}')

# Medidas de Dispersão "Variabilidade"
try:
    print('Calculando a Variabilidade dos dados')
    # Variância - É uma medida para observar a dispersão dos dados.
    # Observa-se em relação a média
    # É a média dos quadrados, das diferenças entre cada valor e a média.
    # OBS: O resultado da variância está elevado ao quadrado.

    # Interpretação:
    # Quanto maior a variância, maior é o afastamento dos valores em relação a média.
    # Neste caso, a variância elevada indica alta dispersão.

    variancia = np.var(array_roubo_veiculo)

    distancia_var_media = variancia / (media_roubo_veiculo ** 2)* 100

    # Desvio Padrão - É a raiz quadrada da variância. É a normalização da variância.Por isso é mais fácil a interpretação.
    # Apresenta o quanto os dados estão afastados da média, tanto para mais quanto para menos.
    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação
    # É a magnitude do Desvio Padrão em relação a média
    coef_variacao = desvio_padrao / media_roubo_veiculo



    print('\nMedidas de dispersão')
    print(40*'=')
    print(f'Variância: {variancia}')
    print(f'Distância entre Média e Variância: {distancia_var_media}%')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variacao}')
    


    

except Exception as e:
    print(f'Erro ao calcular a dispersão: {e}')


# Visualizando os dados
try:
    # mostrando cidade com maiores roubos
    # plt.figure(figsize=(16, 8))
    plt.subplots(2, 2, figsize=(16, 8))


    # 1 Maiores
    plt.subplot(2, 2, 1)
    
    df_roubo_veiculo_maiores = (
        df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False)
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=True)
    )
    plt.barh(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])


    # Rótulo de dados
    deslocamento = max(df_roubo_veiculo_maiores['roubo_veiculo']) * 0.01


    for i, valor in enumerate(df_roubo_veiculo_maiores['roubo_veiculo']):
        plt.text(
            valor + deslocamento,   #posição X
            i,       #posição y
            f'{valor:,}',
            ha='left',
            fontsize=8
        )



    plt.title('Cidades com maiores casos de roubos')


    # POSIÇÃO 2 Menores
    plt.subplot(2, 2, 2) 

    plt.hist(array_roubo_veiculo, bins=198)
    plt.axvline(media_roubo_veiculo, color='green', linewidth=1)
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=1)

    # P/ printar as faixas de intervalo do Histograma
    contagens, limites = np.histogram(array_roubo_veiculo, bins=198)

    print('\nFaixas do Histograma')
    for i in range(len(contagens)):
        if contagens[i] > 0:
            print(
                f'Faixa {i+1}: '
                f'{limites[i]:.0f} até {limites[i+1]:.0f} roubos: '
                f'=> {contagens[i]} municípios'
            )


    # POSIÇÃO 3 - BOXPLOT
    plt.subplot(2, 2, 3)
    
    # showfliers=False - retira outliers
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('Boxplot dos Roubos por Municípios')


    # POSIÇÃO 4 - MEDIDAS ESTATÍSTICAS
    plt.subplot(2, 2, 4) 
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.7, f'Distância: {distancia}', fontsize=10)
    plt.text(0.1, 0.6, f'Menor Valor: {minimo}', fontsize=10)
    plt.text(0.1, 0.5, f'Limite Inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior}', fontsize=10)
    plt.text(0.1, 0.1, f'Maior Valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=10)

    plt.text(0.5, 0.9, f'Assimetria: {assimetria}', fontsize=10)
    plt.text(0.5, 0.8, f'Curtose: {curtose}', fontsize=10)
    plt.text(0.5, 0.7, f'Variância: {variancia}', fontsize=10)
    plt.text(0.5, 0.6, f'Distância Variância: {distancia_var_media}', fontsize=10)
    plt.text(0.5, 0.5, f'Desvio Padrão: {desvio_padrao}', fontsize=10)
    plt.text(0.5, 0.4, f'Coef. de Variação: {coef_variacao} %', fontsize=10)

    plt.title('Resumo Estatístico')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao plotar gráfico: {e}')

