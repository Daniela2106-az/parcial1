# ==============================
#   FUNCIONES DE ORDENAMIENTO
# ==============================

def ordenar_por_campo(lista, campo, asc=True):
    n = len(lista)
    for i in range(n - 1):
        idx_ext = i
        for j in range(i + 1, n):
            if asc:
                if int(lista[j][campo]) < int(lista[idx_ext][campo]):
                    idx_ext = j
            else:
                if int(lista[j][campo]) > int(lista[idx_ext][campo]):
                    idx_ext = j
        if idx_ext != i:
            lista[i], lista[idx_ext] = lista[idx_ext], lista[i]
    return lista


def ordenar_por_nombre(lista):
    n = len(lista)
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if lista[j][1].lower() < lista[idx_min][1].lower():
                idx_min = j
        if idx_min != i:
            lista[i], lista[idx_min] = lista[idx_min], lista[i]
    return lista

# ==============================
#   OPCIÓN 1 - VER LIBROS
# ==============================

def ver_libros():
    with open("libros.csv", "r", encoding="utf-8") as f:
        lineas = f.readlines()
    libros = []
    for l in lineas[1:]:
        partes = l.strip().split(",")
        libros.append(partes)

    libros = ordenar_por_campo(libros, 4, asc=True)

    print("--- Libros ordenados por año asc ---")
    for libro in libros:
        print(f"{libro[1]}, {libro[2]}, {libro[4]}")

# ==============================
#   OPCIÓN 2 - AGREGAR USUARIO
# ==============================

def agregar_usuario():
    with open("usuarios.csv", "r", encoding="utf-8") as f:
        lineas = f.readlines()
    usuarios = []
    for l in lineas[1:]:
        partes = l.strip().split(",")
        usuarios.append(partes)

    nuevo_id = 1 if not usuarios else int(usuarios[-1][0]) + 1
    nombre = input("Nombre del usuario: ")
    email = input("Email del usuario: ")

    with open("usuarios.csv", "a", encoding="utf-8") as f:
        f.write(f"{nuevo_id},{nombre},{email}\n")

    print(f"Usuario agregado con id={nuevo_id}.")

# ==============================
#   OPCIÓN 3 - TOTAL PRÉSTAMOS
# ==============================

def calcular_totales():
    with open("libros.csv", "r", encoding="utf-8") as f:
        lineas_libros = f.readlines()
    libros = {}
    for l in lineas_libros[1:]:
        partes = l.strip().split(",")
        libros[int(partes[0])] = partes[1]

    with open("prestamos.csv", "r", encoding="utf-8") as f:
        lineas_prestamos = f.readlines()
    prestamos = []
    for l in lineas_prestamos[1:]:
        partes = l.strip().split(",")
        prestamos.append([int(partes[2]), int(partes[3])])

    totales = {}
    for p in prestamos:
        libro_id, cantidad = p
        if libro_id not in totales:
            totales[libro_id] = 0
        totales[libro_id] += cantidad

    lista_totales = []
    for libro_id, total in totales.items():
        lista_totales.append([libro_id, libros[libro_id], total])

    lista_totales = ordenar_por_campo(lista_totales, 2, asc=False)

    print("--- Total de préstamos por libro (mayor a menor) ---")
    for t in lista_totales:
        print(f"{t[1]} , total_prestamos: {t[2]}")

    with open("total_prestamos.csv", "w", encoding="utf-8") as f:
        f.write("libro_id,titulo,total_prestamos\n")
        for t in lista_totales:
            f.write(f"{t[0]},{t[1]},{t[2]}\n")

# ==============================
#   OPCIÓN 4 - USUARIOS PRÉSTAMOS
# ==============================

def usuarios_prestamos():
    with open("usuarios.csv", "r", encoding="utf-8") as f:
        lineas_usuarios = f.readlines()
    usuarios = []
    for l in lineas_usuarios[1:]:
        partes = l.strip().split(",")
        usuarios.append([int(partes[0]), partes[1], partes[2]])

    with open("prestamos.csv", "r", encoding="utf-8") as f:
        lineas_prestamos = f.readlines()
    prestamos = []
    for l in lineas_prestamos[1:]:
        partes = l.strip().split(",")
        prestamos.append(int(partes[1]))

    usuarios_con_prestamos = []
    ids_vistos = []
    for u in usuarios:
        if u[0] in prestamos and u[0] not in ids_vistos:
            usuarios_con_prestamos.append(u)
            ids_vistos.append(u[0])

    usuarios_con_prestamos = ordenar_por_nombre(usuarios_con_prestamos)

    print("--- Usuarios con préstamos Asc ---")
    for u in usuarios_con_prestamos:
        print(f"{u[0]} , {u[1]} , {u[2]}")
 
# ==============================
#   MENÚ GENERAL
# ==============================

def menu():
    while True:
        print("=== MENÚ BIBLIOTECA ===")
        print("1. Ver libros ordenados por año")
        print("2. Agregar un nuevo usuario")
        print("3. Calcular total de préstamos por libro")
        print("4. Ver usuarios que han realizado préstamos")
        print("5. Salir")
        op = input("Seleccione opción: ")

        if op == "1":
            ver_libros()
        elif op == "2":
            agregar_usuario()
        elif op == "3":
            calcular_totales()
        elif op == "4":
            usuarios_prestamos()
        elif op == "5":
            break
        else:
            print("Opción inválida")

menu()
