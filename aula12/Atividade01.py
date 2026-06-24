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


# Visualizando os dados de forma otimizada
try:
    # Aumentamos um pouco a altura para dar mais "respiro" entre os elementos
    plt.figure(figsize=(16, 10))
    
    # POSIÇÃO 1 - TOP 10 CISPs (Ajustado para não embolar texto)
    plt.subplot(2, 2, 1)
    top10 = df_recuperacao.nlargest(10, 'recuperacao_veiculos')
    top10 = top10.sort_values('recuperacao_veiculos')
    
    bars = plt.barh(
        top10['cisp'].astype(str), 
        top10['recuperacao_veiculos'], 
        color='#1f77b4', 
        edgecolor='black',
        height=0.6
    )

    # Adiciona os rótulos de texto com um espaçamento dinâmico seguro
    max_value = top10['recuperacao_veiculos'].max()
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + (max_value * 0.02),  # 2% de margem dinâmica à direita da barra
            bar.get_y() + bar.get_height()/2,
            f'{int(width):,}',
            va='center',
            ha='left',
            fontsize=10,
            weight='bold'
        )
        
    plt.title('Top 10 CISPs com Maior Recuperação de Veículos', fontsize=12, weight='bold', pad=15)
    plt.xlabel('Veículos Recuperados', fontsize=10)
    plt.ylabel('Número da CISP', fontsize=10)
    # Aumenta o limite do eixo X para o texto do último colocado não ser cortado
    plt.xlim(0, max_value * 1.15)
    plt.grid(axis='x', alpha=0.3, linestyle='--')
 
    # POSIÇÃO 2 - HISTOGRAMA (Com legenda explicativa)
    plt.subplot(2, 2, 2)
    plt.hist(array, bins=25, color='#d62728', edgecolor='black', alpha=0.7)
    plt.axvline(media, color='green', linestyle='--', linewidth=2, label=f'Média: {media:.1f}')
    plt.axvline(mediana, color='orange', linestyle='-', linewidth=2, label=f'Mediana: {mediana:.1f}')
    plt.title('Distribuição e Concentração das Recuperações', fontsize=12, weight='bold', pad=15)
    plt.xlabel('Volume de Veículos Recuperados', fontsize=10)
    plt.ylabel('Quantidade de CISPs', fontsize=10)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # POSIÇÃO 3 - BOXPLOT (Substituído o parâmetro incorreto por vert=False)
    plt.subplot(2, 2, 3)
    plt.boxplot(
        array, 
        vert=False,          # CORREÇÃO CRÍTICA: vert=False em vez de orientation
        patch_artist=True, 
        notch=False,
        boxprops=dict(facecolor='#2ca02c', color='black', alpha=0.7),
        flierprops=dict(marker='o', markerfacecolor='black', markersize=6, linestyle='none')
    )
    plt.title('Identificação Estatística de Outliers', fontsize=12, weight='bold', pad=15)
    plt.xlabel('Veículos Recuperados', fontsize=10)
    # Remove as marcações desnecessárias do eixo Y do boxplot deitado
    plt.yticks([]) 
    plt.grid(axis='x', alpha=0.3, linestyle='--')

    # POSIÇÃO 4 - CARD DE MÉTRICAS (Formatado como tabela limpa)
    plt.subplot(2, 2, 4)
    plt.title('Relatório Estatístico Consolidado', fontsize=12, weight='bold', pad=15)
    
    # Criamos um texto estilizado simulando um painel/card
    texto_metricas = (
        f"🔹 Tendência Central:\n"
        f"  • Média: {media:,.2f}\n"
        f"  • Mediana: {mediana:,.2f}\n"
        f"  • Distância Média/Mediana: {distancia:.1f}%\n\n"
        f"🔹 Posição e Dispersão:\n"
        f"  • Q1 (25%): {q1:,.2f}  |  Q3 (75%): {q3:,.2f}\n"
        f"  • Amplitude Total: {amplitude:,}\n"
        f"  • IQR (Intervalo Interquartil): {iqr:,.2f}\n\n"
        f"🔹 Formato da Curva:\n"
        f"  • Assimetria (Skew): {assimetria:.2f}\n"
        f"  • Curtose: {curtose:.2f}\n"
        f"  • Coef. de Variação: {coef_variacao:.2f} ({coef_variacao*100:.1f}%)"
    )
    
    plt.text(0.05, 0.85, texto_metricas, fontsize=11, family='monospace', va='top', ha='left', linespacing=1.5)
    plt.axis('off') # Remove as bordas do gráfico para parecer um card de texto

    # O tight_layout organiza o espaçamento entre os subplots automaticamente
    plt.tight_layout(pad=3.0)
    plt.show()

except Exception as e:
    print(f'Erro ao renderizar os gráficos atualizados: {e}')