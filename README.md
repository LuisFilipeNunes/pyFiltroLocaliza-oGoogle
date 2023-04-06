# pyFiltroLocaliza-oGoogle

Este código consiste em um script escrito em Python que tem como objetivo ler arquivos JSON exportados do aplicativo Google Maps Timeline, que contêm informações sobre a localização de um usuário em diferentes pontos do tempo, e extrair informações específicas sobre visitas a um endereço específico.

O script possui as seguintes funções:

get_differential(start_time, end_time): calcula a diferença em minutos entre dois horários passados em formato de string.

create_instance(place, number, dateInfo, hash_value): cria uma instância de informação sobre uma visita a um endereço específico e adiciona-a a uma lista global chamada dayTimeSpecs. A informação inclui o nome do endereço, o número do endereço, o dia, a hora de entrada, a hora de saída, a duração da visita em minutos, a duração da visita em horas e o hash SHA-1 do arquivo JSON de origem.

correctTime(time): corrige a diferença de fuso horário de -5 horas em relação ao horário padrão, retornando uma string com o horário corrigido.

get_day_time_specs(point): extrai informações de data e hora de uma visita a um local a partir de um ponto específico no arquivo JSON do Google Maps Timeline.
show_table(data): exibe uma tabela com os dados curados em uma janela pop-up.

save_curated_data(data): salva os dados curados em um arquivo Excel na área de trabalho e exibe-os em uma tabela utilizando a função show_table().

initializeRead(data, hash_value): função principal que percorre uma lista de pontos em um arquivo JSON e chama a função create_instance() para criar uma instância de informação para cada visita ao endereço específico.

process_directory(directory): função principal que processa todos os arquivos JSON em um diretório e chama a função initializeRead() para cada um deles. No final, retorna a lista dayTimeSpecs.

main(): função principal que solicita ao usuário que escolha um diretório e chama a função process_directory() para processar os arquivos JSON naquele diretório. Em seguida, chama a função save_curated_data() para salvar os dados curados em um arquivo Excel e exibi-los em uma tabela.


Na pasta selecionada, é interessante adicionar todos os dados de locaização do Google (semantic location history), a não ser que queira um relatório separado por mês/ano/período,


