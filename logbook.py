import csv
import datetime
import random
import json

HORAS_TRABALHADAS_POR_DIA = 8

def generate_dataset(json_data):
    dataset = []
    etapas = json_data.get('etapas', {})
    data_inicial = datetime.datetime.strptime(json_data['data_inicial'], '%d-%m-%Y')
    data_final = datetime.datetime.strptime(json_data['data_final'], '%d-%m-%Y')

    current_date = data_inicial
    while current_date <= data_final:
        atividades_dia = []
        tempo_total = 0
        verificar_proveniencia = False

        for etapa, servicos in random.sample(etapas.items(), len(etapas)):
            for servico, atividades in random.sample(servicos['servicos'].items(), len(servicos['servicos'])):
                # if servico == 'Verificar a proveniencia dos dados' and verificar_proveniencia:
                #     continue
                
                atividades_aleatorias = random.sample(atividades['atividades'], len(atividades['atividades']))
                for atividade in atividades_aleatorias:
                    if tempo_total < HORAS_TRABALHADAS_POR_DIA:
                        tempo_max = min(HORAS_TRABALHADAS_POR_DIA - tempo_total, 2)
                        tempo = random.randint(1, tempo_max)
                        tempo_total += tempo
                        dataset.append([current_date.strftime('%d-%m-%Y'), etapa, servico, atividade, tempo])
                        atividades_dia.append(atividade)

                        if servico == 'Verificar a proveniencia dos dados':
                            verificar_proveniencia = True

        current_date += datetime.timedelta(days=1)

    return dataset



def main():
    import sys

    if len(sys.argv) != 2:
        print("Por favor, forneça um arquivo json como argumento na linha de comando. Ex.: python logbook.py "
              "my_file.json")
        sys.exit(1)
    json_file = sys.argv[1]

    try:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado: %s" % json_file)
    except Exception as e:
        print("Erro ao abrir arquivo: %s" % e)

    dataset = generate_dataset(json_data)

    try:
        project_name = json_data.get('projeto')+'.csv'
        with open(project_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['data', 'etapa', 'servico', 'atividade', 'tempo'])
            writer.writerows(dataset)
        print("Dataset gerado com sucesso!")
    except Exception as e:
        print("Erro ao escrever arquivo: %s" % e)


if __name__ == '__main__':
    main()
