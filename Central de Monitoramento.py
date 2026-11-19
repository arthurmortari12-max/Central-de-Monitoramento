TEMP_MIN = 18.0  
TEMP_MAX = 30.0   


PM25_MAX = 15.0   


RUIDO_MAX_DIURNO = 55.0    
RUIDO_MAX_NOTURNO = 50.0   

LIMITE_PERCENTUAL = 30   

NOME_AMBIENTE = "Parquinho de um prédio residencial"




def calcular_estatisticas(valores):
    """Recebe uma lista de números e devolve (média, maior, menor)."""
    soma = 0
    maior = valores[0]   
    menor = valores[0]

    for valor in valores:
        soma += valor
        if valor > maior:
            maior = valor
        if valor < menor:
            menor = valor

    media = soma / len(valores)
    return media, maior, menor


def obter_limite_ruido(hora):
    """Devolve o limite de ruído conforme a hora (0 a 23) da leitura."""
    if 7 <= hora < 22:
        return RUIDO_MAX_DIURNO
    else:
        return RUIDO_MAX_NOTURNO




def ler_quantidade():
    """Pede a quantidade de leituras (inteiro maior que zero)."""
    while True:
        texto = input("Quantas leituras deseja registrar? ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Digite um número inteiro maior que zero.")


def ler_numero(mensagem):
    """Pede um número decimal; aceita vírgula ou ponto."""
    while True:
        texto = input(mensagem).replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("Valor inválido. Digite um número (ex.: 25.5).")


def ler_dia(mensagem):
    """Pede o dia da leitura (texto no formato DD/MM/AAAA)."""
    while True:
        texto = input(mensagem).strip()
        partes = texto.split("/")
        if (len(partes) == 3 and partes[0].isdigit() and partes[1].isdigit()
                and partes[2].isdigit()):
            dia = int(partes[0])
            mes = int(partes[1])
            if 1 <= dia <= 31 and 1 <= mes <= 12:
                return texto
        print("Data inválida. Use o formato DD/MM/AAAA (ex.: 05/11/2026).")


def ler_horario(mensagem):
    """Pede o horário no formato HH:MM e devolve (hora, minuto) como inteiros."""
    while True:
        texto = input(mensagem).strip()
        partes = texto.split(":")
        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            hora = int(partes[0])
            minuto = int(partes[1])
            if 0 <= hora <= 23 and 0 <= minuto <= 59:
                return hora, minuto
        print("Horário inválido. Use o formato HH:MM (ex.: 14:30).")



def salvar_relatorio(nome_arquivo, quantidade, stats_temp, stats_pm25, stats_ruido,
                     ocorrencias, leituras_criticas, percentual, classificacao,
                     registro_alertas):
    """Grava o relatório da sequência em um arquivo .txt."""
    media_temp, maior_temp, menor_temp = stats_temp
    media_pm25, maior_pm25, menor_pm25 = stats_pm25
    media_ruido, maior_ruido, menor_ruido = stats_ruido
    ocorr_temp, ocorr_pm25, ocorr_ruido = ocorrencias

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE MONITORAMENTO AMBIENTAL\n")
        arquivo.write(f"Ambiente: {NOME_AMBIENTE}\n")
        arquivo.write(f"Quantidade de leituras: {quantidade}\n\n")

        arquivo.write("LIMITES DE REFERÊNCIA ADOTADOS\n")
        arquivo.write(f"Temperatura: {TEMP_MIN} a {TEMP_MAX} °C\n")
        arquivo.write(f"PM2,5: máximo de {PM25_MAX} µg/m³ (média de 24h)\n")
        arquivo.write(f"Ruído: máximo de {RUIDO_MAX_DIURNO} dB (07h às 22h) "
                      f"e {RUIDO_MAX_NOTURNO} dB (22h às 07h)\n\n")

        arquivo.write("ESTATÍSTICAS\n")
        arquivo.write(f"Temperatura - média: {media_temp:.2f} °C | "
                      f"maior: {maior_temp} | menor: {menor_temp}\n")
        arquivo.write(f"PM2,5 - média: {media_pm25:.2f} µg/m³ | "
                      f"maior: {maior_pm25} | menor: {menor_pm25}\n")
        arquivo.write(f"Ruído - média aritmética simplificada: {media_ruido:.2f} dB | "
                      f"maior: {maior_ruido} | menor: {menor_ruido}\n\n")

        arquivo.write("OCORRÊNCIAS CRÍTICAS POR PARÂMETRO\n")
        arquivo.write(f"Temperatura: {ocorr_temp}\n")
        arquivo.write(f"PM2,5: {ocorr_pm25}\n")
        arquivo.write(f"Ruído: {ocorr_ruido}\n\n")

        arquivo.write(f"Leituras com pelo menos uma condição crítica: "
                      f"{leituras_criticas} de {quantidade}\n")
        arquivo.write(f"Percentual de leituras críticas: {percentual:.1f}%\n\n")

        arquivo.write("ALERTAS REGISTRADOS\n")
        if len(registro_alertas) == 0:
            arquivo.write("Nenhum alerta registrado.\n")
        else:
            for alerta in registro_alertas:
                arquivo.write(alerta + "\n")

        arquivo.write("\n" + classificacao + "\n\n")
        arquivo.write("Observação: este resultado se refere a uma simulação baseada "
                      "nos critérios adotados, não sendo certificação de segurança "
                      "ambiental nem substituindo avaliação técnica do espaço.\n")




def executar_sequencia(numero_sequencia):
    """Executa uma análise completa. Como todas as variáveis nascem aqui dentro,
    cada nova sequência começa com dados e contadores zerados."""
    leituras = []
    ocorrencias_temperatura = 0
    ocorrencias_pm25 = 0
    ocorrencias_ruido = 0
    leituras_criticas = 0
    registro_alertas = []

    print(f"\n===== SEQUÊNCIA {numero_sequencia} - {NOME_AMBIENTE} =====")

    
    quantidade = ler_quantidade()

    for i in range(1, quantidade + 1):
        print(f"\n--- Leitura {i} de {quantidade} ---")
        dia = ler_dia("Dia da leitura (DD/MM/AAAA): ")
        hora, minuto = ler_horario("Horário da leitura (HH:MM): ")
        temperatura = ler_numero(f"Leitura {i} - Temperatura (°C): ")
        pm25 = ler_numero(f"Leitura {i} - PM2,5 (µg/m³): ")
        ruido = ler_numero(f"Leitura {i} - Ruído (dB): ")

       
        leitura = {
            "dia": dia,
            "hora": hora,
            "minuto": minuto,
            "temperatura": temperatura,
            "pm25": pm25,
            "ruido": ruido,
        }
        leituras.append(leitura)   

    
    print("\n===== ANÁLISE DAS LEITURAS =====")

    for i in range(len(leituras)):
        leitura = leituras[i]
        limite_ruido = obter_limite_ruido(leitura["hora"])
        leitura_critica = False   

        print(f"\nLeitura {i + 1} - {leitura['dia']} às "
              f"{leitura['hora']:02d}:{leitura['minuto']:02d}")

        if leitura["temperatura"] < TEMP_MIN or leitura["temperatura"] > TEMP_MAX:
            print("ALERTA: Temperatura fora dos limites estabelecidos")
            registro_alertas.append(
                f"Leitura {i + 1}: Temperatura fora dos limites estabelecidos")
            ocorrencias_temperatura += 1
            leitura_critica = True

        if leitura["pm25"] > PM25_MAX:
            print("ALERTA: Concentração de PM2,5 acima do limite adotado")
            registro_alertas.append(
                f"Leitura {i + 1}: Concentração de PM2,5 acima do limite adotado")
            ocorrencias_pm25 += 1
            leitura_critica = True

        if leitura["ruido"] > limite_ruido:
            print("ALERTA: Nível de ruído elevado em relação ao limite definido")
            registro_alertas.append(
                f"Leitura {i + 1}: Nível de ruído elevado em relação ao limite definido")
            ocorrencias_ruido += 1
            leitura_critica = True

        if leitura_critica:
            leituras_criticas += 1
        else:
            print("Leitura dentro dos limites de referência estabelecidos")


    temperaturas = []
    valores_pm25 = []
    ruidos = []

    for leitura in leituras:
        temperaturas.append(leitura["temperatura"])
        valores_pm25.append(leitura["pm25"])
        ruidos.append(leitura["ruido"])

    media_temp, maior_temp, menor_temp = calcular_estatisticas(temperaturas)
    media_pm25, maior_pm25, menor_pm25 = calcular_estatisticas(valores_pm25)
    media_ruido, maior_ruido, menor_ruido = calcular_estatisticas(ruidos)


    percentual = (leituras_criticas * 100) / quantidade


    if percentual > LIMITE_PERCENTUAL:
        classificacao = ("Estado geral: condições ambientais de atenção, "
                         "com frequência de ocorrências acima do critério estabelecido")
    else:
        classificacao = ("Estado geral: frequência de ocorrências dentro do "
                         "critério estabelecido para a simulação")

  
    print("\n===== ESTATÍSTICAS =====")
    print(f"Temperatura - média: {media_temp:.2f} °C | maior: {maior_temp} | menor: {menor_temp}")
    print(f"PM2,5 - média: {media_pm25:.2f} µg/m³ | maior: {maior_pm25} | menor: {menor_pm25}")
    print(f"Ruído - média aritmética simplificada: {media_ruido:.2f} dB | "
          f"maior: {maior_ruido} | menor: {menor_ruido}")

    print("\n===== OCORRÊNCIAS CRÍTICAS =====")
    print(f"Temperatura: {ocorrencias_temperatura}")
    print(f"PM2,5: {ocorrencias_pm25}")
    print(f"Ruído: {ocorrencias_ruido}")
    print(f"Leituras com pelo menos uma condição crítica: {leituras_criticas} de {quantidade}")
    print(f"Percentual de leituras críticas: {percentual:.1f}%")

    print("\n" + classificacao)

  
    nome_arquivo = f"relatorio_sequencia_{numero_sequencia}.txt"
    salvar_relatorio(nome_arquivo, quantidade,
                     (media_temp, maior_temp, menor_temp),
                     (media_pm25, maior_pm25, menor_pm25),
                     (media_ruido, maior_ruido, menor_ruido),
                     (ocorrencias_temperatura, ocorrencias_pm25, ocorrencias_ruido),
                     leituras_criticas, percentual, classificacao, registro_alertas)
    print(f"\nRelatório salvo no arquivo: {nome_arquivo}")




def perguntar_nova_sequencia():
    """Pergunta se o usuário quer uma nova sequência; devolve True ou False."""
    while True:
        resposta = input("\nDeseja realizar uma nova sequência? (S/N): ").strip().upper()
        if resposta == "S":
            return True
        elif resposta == "N":
            return False
        print("Digite S ou N.")




numero_sequencia = 1
continuar = True

while continuar:
    executar_sequencia(numero_sequencia)
    continuar = perguntar_nova_sequencia()
    numero_sequencia += 1

print("\nPrograma encerrado. Obrigado por utilizar a central de monitoramento!")