import csv

def main():

    # Inicializar programa e ler dados
    print("Iniciando o processamento da base de dados...")

    content = ler_base()

    print("Processamento concluído com sucesso!")

    menu(content)

def menu(content):

    # Manusear opções e distribuir código
    prox = input("Qual sua próxima ação? (Digite 'relatorio' para gerar relatório, 'filtrar' para filtrar dados, 'buscar' para buscar dados, 'ordenar' para ordenar dados ou 'sair' para encerrar): ") 
    
    if prox == "relatorio":
        cont_lidos, cont_validos, cont_invalidos, cont_ausentes = processar_base(content)
        media_price, media_area, media_rooms, media_m2 = calcular(content, cont_validos)
        maior_price, maior_area, maior_rooms, maior_m2, menor_price, menor_area, menor_rooms, menor_m2 = maior_menor(content)
        relatorio(cont_lidos, cont_validos, cont_invalidos, cont_ausentes, media_price, media_area, media_rooms, media_m2, maior_price, maior_area, maior_rooms, maior_m2, menor_price, menor_area, menor_rooms, menor_m2)
        redirecionar(content)
    elif prox == "filtrar":
        filtro = input("Digite o critério de filtragem (Zip/Price/Area/Room/Long/Lat): ")
        filtrado = filtrar(content, filtro)
        print(f"Total de anúncios filtrados: {len(filtrado)}")
        exibir(filtrado)
        redirecionar(filtrado)
    elif prox == "buscar":
        termo = input("Digite o critério de busca (Address/Zip): ")
        buscado = buscar(content, termo)
        print(f"Total de anúncios encontrados: {len(buscado)}")
        exibir(buscado)
        redirecionar(buscado)
    elif prox == "ordenar": 
        criterio_1 = input("Digite o primeiro critério de ordenação (Price/Area/Room/m2): ")
        ordem_1 = input("Digite a ordem do primeiro critério (asc/desc): ")
        criterio_2 = input("Digite o segundo critério de ordenação (Price/Area/Room/m2): ")
        ordem_2 = input("Digite a ordem do segundo critério (asc/desc): ")
        ordenar(content, criterio_1, ordem_1, criterio_2, ordem_2)
        redirecionar(content)
    elif prox == "sair":
        print("Obrigado pelo uso!")
        print("Encerrando o programa...")
    else:
        print("Opção inválida. Encerrando o programa...")

def ler_base():

    # Abrir o arquivo CSV e ler seu conteúdo como um dicionário
    with open("HousingPrices-Amsterdam-August-2021.csv", "r", encoding="utf-8") as table:
        content = list(csv.DictReader(table))

        
        for row in content:

            #Transformar tipo de dados
            if row["Price"] and row["Price"] != "NA":
                text_value = row["Price"]
                numeric_value = float(text_value)
                row["Price"] = numeric_value
            if row["Price"] == "NA":
                row["Price"] = None
            if row["Area"] and row["Price"] != "NA":
                row["Area"] = int(row["Area"])
            if row["Area"] == "NA":
                row["Area"] = None
            if row["Room"]:
                row["Room"] = int(row["Room"])

            #Adicionar coluna m2
            if row["Price"] and row["Area"]:
                row["m2"] = row["Price"] / row["Area"]
            else:
                row["m2"] = None

        return content

def processar_base(content):

    # Inicializar contadores
    cont_lidos = 0
    cont_validos = 0
    cont_invalidos = 0
    cont_ausentes = 0

    # Iterar sobre cada linha do conteúdo do CSV
    for row in content:
        cont_lidos += 1

        if row["Address"] and row["Zip"] and row["Room"]:
            cont_validos += 1

            if not row["Price"] or not row["Area"]:
                cont_ausentes += 1
        else:
            cont_invalidos += 1

    return cont_lidos, cont_validos, cont_invalidos, cont_ausentes

def calcular(content, cont_validos):

    # Inicializar variáveis para calcular as médias
    total_price = 0
    total_area = 0
    total_rooms = 0
    total_m2 = 0

    for row in content:

        # Acumular preços válidos     
        if row["Price"]:
            total_price += row["Price"]
        if row["Area"]:
            total_area += row["Area"]
        if row["Room"]:
            total_rooms += row["Room"]
        if row["m2"]:
            total_m2 += row["m2"]

    # Calcular médias
    if cont_validos > 0:
        media_price = total_price / cont_validos
        media_area = total_area / cont_validos
        media_rooms = total_rooms / cont_validos
        media_m2 = total_m2 / cont_validos

    return media_price, media_area, media_rooms, media_m2

def maior_menor(content):

    # Inicializar variáveis para armazenar os valores máximos e mínimos
    maior_price = 0
    maior_area = 0
    maior_rooms = 0
    maior_m2 = 0
    menor_price = None
    menor_area = None
    menor_rooms = None
    menor_m2 = None

    for row in content:

        #Verificar e atualizar valores máximos
        if row["Price"] and row["Price"] > maior_price:
            maior_price = row["Price"]
        if row["Area"] and row["Area"] > maior_area:
            maior_area = row["Area"]
        if row["Room"] and row["Room"] > maior_rooms:
            maior_rooms = row["Room"]
        if row["m2"] and row["m2"] > maior_m2:
            maior_m2 = row["m2"]

        #Verificar e atualizar valores mínimos
        if row["Price"] and (menor_price is None or row["Price"] < menor_price):
            menor_price = row["Price"]
        if row["Area"] and (menor_area is None or row["Area"] < menor_area):
            menor_area = row["Area"]
        if row["Room"] and (menor_rooms is None or row["Room"] < menor_rooms):
            menor_rooms = row["Room"]
        if row["m2"] and (menor_m2 is None or row["m2"] < menor_m2):
            menor_m2 = row["m2"]

    return maior_price, maior_area, maior_rooms, maior_m2, menor_price, menor_area, menor_rooms, menor_m2


def quantificar(content):

    # Quantidade de anúncios por número de cômodos
    qua_comodos = {}
    qua_zip = {}

    for row in content:

        if row["Room"]:
            if row["Room"] in qua_comodos:
                qua_comodos[row["Room"]] += 1
            else:
                qua_comodos[row["Room"]] = 1
        if row["Zip"]:
            if row["Zip"] in qua_zip:
                qua_zip[row["Zip"]] += 1
            else:
                qua_zip[row["Zip"]] = 1
        
    return qua_comodos, qua_zip

def filtrar(content, filtro):

    # Filtrar os dados com base no critério fornecido
    if filtro == "Zip":
        filtrado_zip = filtrar_zip(content)
        return filtrado_zip
    elif filtro == "Price":
        filtrado_price = filtrar_price(content)
        return filtrado_price
    elif filtro == "Area":
        filtrado_area = filtrar_area(content)
        return filtrado_area
    elif filtro == "Room":
        filtrado_room = filtrar_room(content)
        return filtrado_room
    elif filtro == "Long":
        filtrado_long = filtrar_long(content)
        return filtrado_long
    elif filtro == "Lat":
        filtrado_lat = filtrar_lat(content)
        return filtrado_lat

def filtrar_zip(content):

    #Filtrar os dados por zip
    while True:

        filtro = input("Digite o código postal (Zip) que deseja filtrar: ")

        if filtro:
            break
    
    filtrado_zip = []

    for row in content:
        if row["Zip"]:
            if row["Zip"] == filtro:
                filtrado_zip.append(row)

    return filtrado_zip

def filtrar_price(content):

    #Filtrar dados por price
    while True:

        max_price = int(input("Digite o preço máximo (Price) que deseja filtrar: "))
        min_price = int(input("Digite o preço mínimo (Price) que deseja filtrar: "))

        if max_price and min_price and max_price > min_price:
            break

    filtrado_price = []

    for row in content:
        if row["Price"]:
            if min_price <= row["Price"] <= max_price:
                filtrado_price.append(row)

    return filtrado_price

def filtrar_area(content):

    #Filtrar dados por area
    while True:

        max_area = int(input("Digite a área máxima (Area) que deseja filtrar: "))
        min_area = int(input("Digite a área mínima (Area) que deseja filtrar: "))

        if max_area and min_area and max_area > min_area:
            break

    filtrado_area = []

    for row in content:
        if row["Area"]:
            if min_area <= row["Area"] <= max_area:
                filtrado_area.append(row)

    return filtrado_area

def filtrar_room(content):
    
    #Filtrar dados por room
    while True:

        max_room = int(input("Digite o número máximo de cômodos (Room) que deseja filtrar: "))
        min_room = int(input("Digite o número mínimo de cômodos (Room) que deseja filtrar: "))

        if max_room and min_room and max_room > min_room:
            break

    filtrado_room = []

    for row in content:
        if row["Room"]:
            if min_room <= row["Room"] <= max_room:
                filtrado_room.append(row)

    return filtrado_room

def filtrar_long(content):

    #Filtrar dados por longitude
    while True:

        max_long = float(input("Digite a longitude máxima (Long) que deseja filtrar: "))
        min_long = float(input("Digite a longitude mínima (Long) que deseja filtrar: "))

        if max_long and min_long and max_long > min_long:
            break

    filtrado_long = []

    for row in content:
        if row["Long"]:
            if min_long <= float(row["Long"]) <= max_long:
                filtrado_long.append(row)

    return filtrado_long

def filtrar_lat(content):

    #Filtrar dados por latitude
    while True:

        max_lat = float(input("Digite a latitude máxima (Lat) que deseja filtrar: "))
        min_lat = float(input("Digite a latitude mínima (Lat) que deseja filtrar: "))

        if max_lat and min_lat and max_lat > min_lat:
            break

    filtrado_lat = []

    for row in content:
        if row["Lat"]:
            if min_lat <= float(row["Lat"]) <= max_lat:
                filtrado_lat.append(row)

    return filtrado_lat

def buscar(content, termo):

    # Buscar dados com base na entrada fornecida
    if termo == "Address":
        buscado_address = buscar_address(content)
        return buscado_address
    elif termo == "Zip":
        buscado_zip = buscar_zip(content)
        return buscado_zip
    
def buscar_address(content):

    #Buscar dados por address
    while True:

        termo = input("Digite o endereço (Address) que deseja buscar: ")

        if termo:
            break

    buscado_address = []

    for row in content:
        if row["Address"]:
            if termo.lower() in row["Address"].lower():
                buscado_address.append(row)

    return buscado_address

def buscar_zip(content):

    #Buscar dados por zip
    while True:

        termo = input("Digite o código postal (Zip) que deseja buscar: ")

        if termo:
            break

    buscado_zip = []

    for row in content:
        if row["Zip"]:
            if termo.upper() in row["Zip"]:
                buscado_zip.append(row)

    return buscado_zip

def ordenar(content, criterio_1, ordem_1, criterio_2, ordem_2):

    # Ordenar os dados com base nos critérios fornecidos
    limpa = limpeza(content, criterio_1, criterio_2)

    # Ordenar utilizando método nativo sorted, passando função lambda para inserir os dois critérios como parâmetros da ordenação
    ordenada = []
    if ordem_1 == "asc":
        if ordem_2 == "asc":
            ordenada = sorted(limpa, key=lambda x: (x[criterio_1], x[criterio_2]))
        else:
            ordenada = sorted(limpa, key=lambda x: (x[criterio_1], -x[criterio_2]))
    else:
        if ordem_2 == "asc":
            ordenada = sorted(limpa,  key=lambda x: (-x[criterio_1], x[criterio_2]))
        else:
            ordenada = sorted(limpa, key=lambda x: (-x[criterio_1], -x[criterio_2]))

    exibir(ordenada)

def limpeza(content, criterio_1, criterio_2):

    #Limpar dados inconsistentes antes de ordenação
    limpa = []
    for row in content:
        if row[criterio_1] and row[criterio_2]:
            limpa.append(row)

    return limpa

def exibir(ordenada):

    # Exibir primeiros dados
    print("Exibindo os primeiros 10 dados:")

    for row in ordenada[:10]:
        print(f"Address: {row['Address']}, Zip: {row['Zip']}, Price: {row['Price']}, Area: {row['Area']}, Room: {row['Room']}, Long: {row['Lon']}, Lat: {row['Lat']}, m2: {row['m2']}")

def relatorio(cont_lidos, cont_validos, cont_invalidos, cont_ausentes, media_price, media_area, media_rooms, media_m2, maior_price, maior_area, maior_rooms, maior_m2, menor_price, menor_area, menor_rooms, menor_m2):

    # Gerar relatório com base nos dados fornecidos
    print("Relatório:")
    print(f"Total de anúncios lidos: {cont_lidos}")
    print(f"Total de anúncios válidos: {cont_validos}")
    print(f"Total de anúncios inválidos: {cont_invalidos}")
    print(f"Total de anúncios com valores ausentes: {cont_ausentes}")
    print(f"Média de preços: {media_price:.2f}")
    print(f"Média de áreas: {media_area:.2f}")
    print(f"Média de cômodos: {media_rooms:.2f}")
    print(f"Média de preço por metro quadrado (m2): {media_m2:.2f}")
    print(f"Maior preço: {maior_price:.2f}")
    print(f"Maior área: {maior_area:.2f}")
    print(f"Maior número de cômodos: {maior_rooms:.2f}")
    print(f"Maior preço por metro quadrado (m2): {maior_m2:.2f}")
    print(f"Menor preço: {menor_price:.2f}" if menor_price is not None else "Menor preço: N/A")
    print(f"Menor área: {menor_area:.2f}" if menor_area is not None else "Menor área: N/A")
    print(f"Menor número de cômodos: {menor_rooms:.2f}" if menor_rooms is not None else "Menor número de cômodos: N/A")
    print(f"Menor preço por metro quadrado (m2): {menor_m2:.2f}" if menor_m2 is not None else "Menor preço por metro quadrado (m2): N/A")

def redirecionar(nova_tabela):

    #Redirecionamento
    while True:

        resp = input("Deseja retornar ao menu? Digite 'sim' para retornar e 'nao' para sair: ").lower()

        if resp in ['sim', 'nao']:
            break

    if resp == 'sim':
        menu(nova_tabela)
    else:
        print("Obrigado pelo uso!")
        print("Encerrando o programa...")

if __name__ == "__main__":
    main()