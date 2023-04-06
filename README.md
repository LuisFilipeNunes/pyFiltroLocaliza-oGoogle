# pyFiltroLocaliza-oGoogle

Este código consiste em um script escrito em Python que é responsável por ler arquivos JSON do Google Maps Location History e extrair informações relevantes sobre os locais visitados pelo usuário, como endereço, horário de entrada e saída, tempo de permanência e hash SHA-1 do arquivo original. O objetivo é criar uma tabela de dados curados que possa ser salva em um arquivo Excel para análise posterior.

As funções utilizadas no código são:

get_differential(start_time, end_time): calcula a diferença de tempo em minutos entre duas horas (no formato "HH:MM").

create_instance(place, number, dateInfo, hash_value): cria uma instância de um local visitado com as informações relevantes (endereço, data, horário de entrada e saída, tempo de permanência e hash SHA-1).

correctTime(time): converte a hora no fuso horário do Google Maps Location History (UTC-5) para o fuso horário local do usuário.

get_day_time_specs(point): extrai informações sobre o dia e horário de visita de um local a partir do arquivo JSON.

show_table(data): exibe uma tabela com os dados curados em uma interface gráfica.

save_curated_data(data): salva os dados curados em um arquivo Excel com nome escolhido pelo usuário.

initializeRead(data, hash_value): inicializa a leitura dos dados do arquivo JSON e cria instâncias de locais visitados.

process_files(directory): processa os arquivos JSON em um diretório selecionado pelo usuário.

O código utiliza também as bibliotecas os, json, numpy, datetime, pathlib, re, hashlib, pandas e tkinter para realizar as operações descritas acima




Utilize o comando $pyinstaller locationFinder.py para montar um executável.

