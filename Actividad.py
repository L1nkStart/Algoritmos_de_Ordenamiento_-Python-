# Tarea III. Algoritmos de Ordenamiento.
# Dado el archivo json proporcionados con datos referenciales: descargas.json
# (El equipo tiene permitido modificar los datos para hacer pruebas) y la funcion de
# carga de datos. Programar los siguiente:
# 1. Identificar y programar cada una de las clases necesarias para el
# funcionamiento del programa.(3 ptos)
# 2. Programar una clase Reporte con un menu de opciones que realice lo
# siguiente(2 pto):
# a. Listar las descargas completadas de forma descendente por tamaño
# utilizando el quicksort permitiendo a los usuarios identificar
# rapidamente los archivos mas grandes (3. ptos)
# b. Listar las descargas que no han sido completadas de forma
# ascendente por fecha de inicio(YYYY-MM-DD HH:MM) utilizando el
# mergesort (3.5 ptos)
# c. Listar las descargas a partir de una fecha(YYYY-MM-DD HH:MM)
# introducidas por el usuario ordenadas de forma ascendente segun su
# tamaño cuya url pertenezca a un dominio especificado por el usuario.
# Utilizar heapsort (4.5 ptos)
# d. Listar las descargar de forma descendente por la longitud de su url
# utilizando shellsort y que cumplan con un estado indicado por el
# usuario (4 ptos)

# Fecha: 06/03/2025
#-----------------------------ALGORITMOS DE ORDENAMIENTO--------------------------------
# Quicksort: Algoritmo de ordenamiento rapido que utiliza la técnica de divide y venceras.
# Mergesort: Algoritmo de ordenamiento estable que divide la lista en mitades, ordena cada mitad y las fusiona.
# Heapsort: Algoritmo de ordenamiento basado en arboles binarios que se organiza en forma de heap.
# Shellsort: Algoritmo de ordenamiento que mejora la eficiencia de insercion, comparando elementos separados por un intervalo.

#INTEGRANTES:
# Nombre: Eduardo Tovar 28138831
# Nombre: Luis León 31139586

#----------------CLASES NECESARIAS PARA EL FUNCIONAMIENTO DEL PROGRAMA------------------
# Clase Descarga: Representa una descarga individual con sus atributos.
# Clase HistorialDescargas: Gestiona el historial de descargas y carga desde un archivo JSON.
# Clase Reporte: Contiene el menu de opciones y los métodos para ordenar las descargas.


import json
from datetime import datetime

# Clase que representa una descarga individual
class Descarga:
    def __init__(self, url, tamano, fecha_inicio, estado):
        self.url = url
        self.tamano = tamano
        # Convertimos la cadena de fecha al objeto datetime
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
        self.estado = estado

    def __str__(self):
        return f"URL: {self.url} | Tamaño: {self.tamano} | Fecha inicio: {self.fecha_inicio} | Estado: {self.estado}"


# Clase para gestionar el historial de descargas
class HistorialDescargas:
    def __init__(self):
        self.historial_completadas = []
        self.cola_descargas = []  # Contendra pendientes, en_progreso, canceladas, etc.

    def cargar_descargas_desde_json(self, archivo_json):
        with open(archivo_json, 'r') as file:
            datos = json.load(file)
            for descarga_data in datos:
                descarga = Descarga(
                    url=descarga_data['url'],
                    tamano=descarga_data['tamano'],
                    fecha_inicio=descarga_data['fecha_inicio'],
                    estado=descarga_data['estado']
                )
                # Clasificar las descargas segun su estado
                if descarga.estado == 'completada':
                    self.historial_completadas.append(descarga)
                else:
                    self.cola_descargas.append(descarga)
        
        print("Descargas cargadas correctamente desde el archivo JSON.")

    def mostrar_descargas(self):
        print("\nDescargas en la cola (pendientes, en progreso, canceladas, etc.):")
        for descarga in self.cola_descargas:
            print(descarga)
        
        print("\nDescargas completadas:")
        for descarga in self.historial_completadas:
            print(descarga)


# Clase Reporte que contiene el menu de opciones y los métodos para ordenar
class Reporte:
    def __init__(self, historial):
        self.historial = historial

    # Opcion a: Ordenar descargas completadas de forma descendente por tamaño utilizando quicksort
    def quicksort_desc(self, lista):
        # Si la lista tiene 0 o 1 elemento, ya esta ordenada
        if len(lista) <= 1:
            return lista
        else:
            pivot = lista[0]
            # Elementos mayores o iguales que el pivote
            mayores = [x for x in lista[1:] if x.tamano >= pivot.tamano]
            # Elementos menores que el pivote
            menores = [x for x in lista[1:] if x.tamano < pivot.tamano]
            return self.quicksort_desc(mayores) + [pivot] + self.quicksort_desc(menores)

    # Opcion b: Ordenar descargas NO completadas de forma ascendente por fecha de inicio utilizando mergesort
    def mergesort_asc(self, lista):
        if len(lista) <= 1:
            return lista
        medio = len(lista) // 2
        izquierda = self.mergesort_asc(lista[:medio])
        derecha = self.mergesort_asc(lista[medio:])
        return self._merge(izquierda, derecha)

    def _merge(self, izquierda, derecha):
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].fecha_inicio <= derecha[j].fecha_inicio:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

    # Opcion c: Ordenar de forma ascendente por tamaño utilizando heapsort
    def heapsort_asc(self, lista):
        # Construir el heap
        n = len(lista)
        # Funcion para 'hundir' el elemento en el heap
        def heapify(arr, n, i):
            mayor = i
            izquierda = 2 * i + 1
            derecha = 2 * i + 2
            if izquierda < n and arr[izquierda].tamano > arr[mayor].tamano:
                mayor = izquierda
            if derecha < n and arr[derecha].tamano > arr[mayor].tamano:
                mayor = derecha
            if mayor != i:
                arr[i], arr[mayor] = arr[mayor], arr[i]
                heapify(arr, n, mayor)

        # Construir el heap maximo
        for i in range(n // 2 - 1, -1, -1):
            heapify(lista, n, i)

        # Extraer elementos uno a uno
        for i in range(n-1, 0, -1):
            lista[0], lista[i] = lista[i], lista[0]
            heapify(lista, i, 0)
        return lista  # La lista estara en orden ascendente por tamaño

    # Opcion d: Ordenar descargas de forma descendente por la longitud de su URL utilizando shellsort
    def shellsort_desc(self, lista):
        n = len(lista)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = lista[i]
                j = i
                while j >= gap and len(lista[j - gap].url) < len(temp.url):
                    lista[j] = lista[j - gap]
                    j -= gap
                lista[j] = temp
            gap //= 2
        return lista

    # Método para mostrar el menu de opciones y ejecutar la seleccion del usuario
    def mostrar_menu(self):
        while True:
            print("\n--- Menu Reporte de Descargas ---")
            print("1. Listar descargas completadas (orden descendente por tamaño - Quicksort)")
            print("2. Listar descargas NO completadas (orden ascendente por fecha de inicio - Mergesort)")
            print("3. Listar descargas a partir de una fecha (orden ascendente por tamaño - Heapsort)")
            print("4. Listar descargas por estado (orden descendente por longitud de URL - Shellsort)")
            print("5. Salir")
            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                # Ordenar descargas completadas por tamaño descendente
                lista = self.historial.historial_completadas.copy()
                lista_ordenada = self.quicksort_desc(lista)
                print("\nDescargas completadas ordenadas (descendente por tamaño):")
                for descarga in lista_ordenada:
                    print(descarga)

            elif opcion == "2":
                # Filtrar descargas que no han sido completadas
                lista = self.historial.cola_descargas.copy()
                lista_ordenada = self.mergesort_asc(lista)
                print("\nDescargas NO completadas ordenadas (ascendente por fecha de inicio):")
                for descarga in lista_ordenada:
                    print(descarga)

            elif opcion == "3":
                # Solicitar fecha y dominio al usuario
                fecha_usuario = input("Ingrese la fecha (YYYY-MM-DD HH:MM): ")
                try:
                    fecha_filtrar = datetime.strptime(fecha_usuario, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Formato de fecha incorrecto. Use YYYY-MM-DD HH:MM")
                    continue
                dominio = input("Ingrese el dominio (ej: example.com): ").strip()
                # Unir ambas listas de descargas
                todas = self.historial.historial_completadas + self.historial.cola_descargas
                # Filtrar descargas a partir de la fecha y que contengan el dominio en la URL
                filtradas = [d for d in todas if d.fecha_inicio >= fecha_filtrar and dominio in d.url]
                # Ordenar las filtradas por tamaño de forma ascendente utilizando heapsort
                if not filtradas:
                    print("No se encontraron descargas que cumplan los criterios.")
                else:
                    filtradas_ordenadas = self.heapsort_asc(filtradas)
                    print("\nDescargas filtradas y ordenadas (ascendente por tamaño):")
                    for descarga in filtradas_ordenadas:
                        print(descarga)

            elif opcion == "4":
                # Solicitar estado al usuario
                estado_filtrar = input("Ingrese el estado de la descarga a filtrar: ").strip()
                # Unir ambas listas de descargas
                todas = self.historial.historial_completadas + self.historial.cola_descargas
                filtradas = [d for d in todas if d.estado == estado_filtrar]
                if not filtradas:
                    print("No se encontraron descargas con ese estado.")
                else:
                    # Ordenar filtradas por la longitud de la URL de forma descendente utilizando shellsort
                    filtradas_ordenadas = self.shellsort_desc(filtradas)
                    print("\nDescargas filtradas y ordenadas (descendente por longitud de URL):")
                    for descarga in filtradas_ordenadas:
                        print(descarga)

            elif opcion == "5":
                print("Saliendo del programa...")
                break
            else:
                print("Opcion invalida. Intente nuevamente.")


# Bloque principal para ejecutar el programa
if __name__ == "__main__":
    historial = HistorialDescargas()
    # Cargar las descargas desde el archivo JSON 
    historial.cargar_descargas_desde_json("descargas.json")
    
    # (Opcional) Mostrar descargas cargadas
    # historial.mostrar_descargas()

    reporte = Reporte(historial)
    reporte.mostrar_menu()
