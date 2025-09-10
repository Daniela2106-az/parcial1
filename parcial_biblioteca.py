import csv
import os

# --------------------------
# Funciones de ordenamiento
# --------------------------

def seleccion(lista, clave, asc=True):
    n = len(lista)
    for i in range(n):
        idx = i
        for j in range(i+1, n):
            if asc:
                if lista[j][clave] < lista[idx][clave]:
                    idx = j
            else:
                if lista[j][clave] > lista[idx][clave]:
                    idx = j
        lista[i], lista[idx] = lista[idx], lista[i]
    return lista

def burbuja(lista, clave, asc=True):
    n = len(lista)
    for i in range(n-1):
        for j in range(n-1-i):
            if asc:
                if lista[j][clave] > lista[j+1][clave]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
            else:
                if lista[j][clave] < lista[j+1][clave]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

# --------------------------
# Opción 1: Libros ordenados
# --------------------------

def ver_libros():
    libros = []
    with open("libros.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            libros.append({"id": int(row[0]), "titulo": row[1], "autor": row[2], "anio": int(row[3])})
    seleccion(libros, "anio", asc=True)
    for l in libros:
        print(f"{l['id']} | {l['titulo']} | {l['autor']} | {l['anio']}")

# --------------------------
# Opción 2: Agregar usuario
# --------------------------

def agregar_usuario():
    usuarios = []
    if os.path.exists("usuarios.csv"):
        with open("usuarios.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                usuarios.append([int(row[0]), row[1], row[2]])
    nuevo_id = 1 if not usuarios else usuarios[-1][0] + 1
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    usuarios.append([nuevo_id, nombre, correo])
    with open("usuarios.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_usuario","nombre","correo"])
        writer.writerows(usuarios)
    print("Usuario agregado con id=4.")

# --------------------------
# Opción 3: Total de préstamos
# --------------------------

def total_prestamos():
    prestamos = []
    with open("prestamos.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            prestamos.append({"id_prestamo": int(row[0]), "id_usuario": int(row[1]), "id_libro": int(row[2]), "cantidad": int(row[3])})
    libros = {}
    with open("libros.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            libros[int(row[0])] = row[1]
    totales = []
    acumulados = {}
    for p in prestamos:
        acumulados[p["id_libro"]] = acumulados.get(p["id_libro"], 0) + p["cantidad"]
    for id_libro, total in acumulados.items():
        totales.append({"id_libro": id_libro, "titulo": libros[id_libro], "total": total})
    burbuja(totales, "total", asc=False)
    with open("total_prestamos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_libro","titulo","total_prestamos"])
        for t in totales:
            writer.writerow([t["id_libro"], t["titulo"], t["total"]])
    print("Archivo total_prestamos.csv generado.")

# --------------------------
# Opción 4: Usuarios con préstamos
# --------------------------

def usuarios_con_prestamos():
    prestamos = []
    with open("prestamos.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            prestamos.append(int(row[1]))
    prestamos = list(set(prestamos))
    usuarios = []
    with open("usuarios.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[0]) in prestamos:
                usuarios.append({"id": int(row[0]), "nombre": row[1], "correo": row[2]})
    seleccion(usuarios, "nombre", asc=True)
    for u in usuarios:
        print(f"{u['id']} | {u['nombre']} | {u['correo']}")

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print("=== MENÚ BIBLIOTECA ===")
        print("1. Ver libros ordenados por año")
        print("2. Agregar usuario")
        print("3. Calcular total de préstamos por libro")
        print("4. Ver usuarios con préstamos")
        print("5. Salir")
        op = input("Seleccione opción: ")
        if op == "1":
            ver_libros()
        elif op == "2":
            agregar_usuario()
        elif op == "3":
            total_prestamos()
        elif op == "4":
            usuarios_con_prestamos()
        elif op == "5":
            break
        else:
            print("Opción inválida.")

menu()