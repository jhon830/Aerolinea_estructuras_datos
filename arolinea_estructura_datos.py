class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self._head = None

    def agregar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self._head:
            self._head = nuevo_nodo
        else:
            actual = self._head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def insertar_en_posicion(self, dato, pos):
        if pos < 0:
            raise IndexError("La posición no puede ser negativa")
        nuevo_nodo = Nodo(dato)
        if pos == 0:
            nuevo_nodo.siguiente = self._head
            self._head = nuevo_nodo
            return
        actual = self._head
        anterior = None
        i = 0
        while actual and i < pos:
            anterior = actual
            actual = actual.siguiente
            i += 1
        if i == pos:
            anterior.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = actual
        else:
            raise IndexError("Posición fuera de rango")

    def eliminar_tercer_elemento(self):
        if not self._head or not self._head.siguiente or not self._head.siguiente.siguiente:
            return False  # no hay tercer elemento
        segundo = self._head.siguiente
        tercero = segundo.siguiente
        segundo.siguiente = tercero.siguiente
        return True

    def intercambiar(self, pos1, pos2):
        if pos1 == pos2:
            return
        nodo1_prev = None
        nodo1 = self._head
        i = 0
        while nodo1 and i < pos1:
            nodo1_prev = nodo1
            nodo1 = nodo1.siguiente
            i += 1
        nodo2_prev = None
        nodo2 = self._head
        i = 0
        while nodo2 and i < pos2:
            nodo2_prev = nodo2
            nodo2 = nodo2.siguiente
            i += 1
        if not nodo1 or not nodo2:
            raise IndexError("Posición fuera de rango")
        if nodo1_prev:
            nodo1_prev.siguiente = nodo2
        else:
            self._head = nodo2
        if nodo2_prev:
            nodo2_prev.siguiente = nodo1
        else:
            self._head = nodo1
        nodo1.siguiente, nodo2.siguiente = nodo2.siguiente, nodo1.siguiente

    def buscar_por_condicion(self, condicion):
        actual = self._head
        while actual:
            if condicion(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar_por_condicion(self, condicion):
        if not self._head:
            return False
        if condicion(self._head.dato):
            self._head = self._head.siguiente
            return True
        actual = self._head
        while actual.siguiente:
            if condicion(actual.siguiente.dato):
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        actual = self._head
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def tamanio(self):
        cont = 0
        actual = self._head
        while actual:
            cont += 1
            actual = actual.siguiente
        return cont






class CargaEspecial:
    def costo(self):
        raise NotImplementedError("Método costo debe implementarse en la clase hija")


class Bicicleta(CargaEspecial):
    def __init__(self, peso, costo_por_kilo):
        if peso < 0 or costo_por_kilo < 0:
            raise ValueError("Peso y costo por kilo deben ser positivos")
        self._peso = peso
        self._costo_por_kilo = costo_por_kilo

    def costo(self):
        return self._peso * self._costo_por_kilo


class Mascota(CargaEspecial):
    def __init__(self, tipo, valor_tiquete):
        self._tipo = tipo.lower()
        self._valor_tiquete = valor_tiquete

    def costo(self):
        if self._tipo == 'perro':
            return 0.05 * self._valor_tiquete
        elif self._tipo == 'gato':
            return 0.02 * self._valor_tiquete
        return 0




class Pasajero:
    def __init__(self, nombre, genero, edad, clase, valor_tiquete):
        self._nombre = nombre
        self._genero = genero.lower()
        self._edad = edad
        self._clase = clase.lower()
        self._valor_tiquete = valor_tiquete
        self._peso_equipaje = 0
        self._cargas_especiales = ListaEnlazada()
        self._costo_equipaje_adicional = 0

    @property
    def nombre(self):
        return self._nombre

    @property
    def genero(self):
        return self._genero

    @property
    def edad(self):
        return self._edad

    @property
    def clase(self):
        return self._clase

    def set_peso_equipaje(self, peso):
        if peso < 0:
            raise ValueError("Peso equipaje no puede ser negativo")
        self._peso_equipaje = peso

    def agregar_carga_especial(self, carga):
        if not isinstance(carga, CargaEspecial):
            raise ValueError("Debe ser una carga especial")
        self._cargas_especiales.agregar_final(carga)

    def calcular_costo_equipaje_adicional(self):
        permitido = {'economica': 10, 'ejecutiva': 20, 'premium': 30}
        kg_permitidos = permitido.get(self._clase, 0)
        kg_extra = max(0, self._peso_equipaje - kg_permitidos)
        if kg_extra == 0:
            self._costo_equipaje_adicional = 0
        else:
            if self._clase == 'economica':
                self._costo_equipaje_adicional = 5000 * kg_extra
            elif self._clase == 'ejecutiva':
                self._costo_equipaje_adicional = 10000 * kg_extra
            elif self._clase == 'premium':
                self._costo_equipaje_adicional = (self._valor_tiquete * 0.01) * kg_extra
            else:
                self._costo_equipaje_adicional = 0
        return self._costo_equipaje_adicional

    def costo_cargas_especiales(self):
        total = 0
        for carga in self._cargas_especiales.recorrer():
            total += carga.costo()
        return total

    def precio_con_descuento_infante(self):
        if 0 <= self._edad <= 13:
            return self._valor_tiquete * 0.93
        return self._valor_tiquete

    def costo_total(self):
        base = self.precio_con_descuento_infante()
        equipaje = self.calcular_costo_equipaje_adicional()
        cargas = self.costo_cargas_especiales()
        return base + equipaje + cargas




class Vuelo:
    def __init__(self, origen, destino):
        self._origen = origen
        self._destino = destino
        self._pasajeros = ListaEnlazada()

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    def agregar_pasajero(self, pasajero):
        self._pasajeros.agregar_final(pasajero)

    def eliminar_pasajero_por_nombre(self, nombre):
        return self._pasajeros.eliminar_por_condicion(lambda p: p.nombre == nombre)

    def buscar_pasajero(self, nombre):
        return self._pasajeros.buscar_por_condicion(lambda p: p.nombre == nombre)

    def total_recaudo(self):
        total = 0
        for p in self._pasajeros.recorrer():
            total += p.costo_total()
        return total

    def contar_por_genero(self):
        hombres = 0
        mujeres = 0
        for p in self._pasajeros.recorrer():
            if p.genero == 'hombre':
                hombres += 1
            elif p.genero == "mujer":
                mujeres += 1
        return hombres, mujeres

    def cantidad_pasajeros(self):
        return self._pasajeros.tamanio()






class Aerolinea:
    def __init__(self):
        self._vuelos = ListaEnlazada()
        self._recaudo_tiquetes = 0
        self._recaudo_equipaje = 0

    def crear_vuelo(self, origen, destino):
        if self.buscar_vuelo(origen, destino):
            raise ValueError("Ya existe el vuelo con ese trayecto")
        vuelo = Vuelo(origen, destino)
        self._vuelos.agregar_final(vuelo)

    def buscar_vuelo(self, origen, destino):
        return self._vuelos.buscar_por_condicion(lambda v: v.origen == origen and v.destino == destino)

    def vender_tiquete(self, origen, destino, nombre, genero, edad, clase, peso_equipaje, cargas_especiales=[]):
        vuelo = self.buscar_vuelo(origen, destino)
        if not vuelo:
            raise ValueError("Vuelo no encontrado")
        valor_tiquete_base = 200000  # fijo o podría ser variable

        pasajero = Pasajero(nombre, genero, edad, clase, valor_tiquete_base)
        pasajero.set_peso_equipaje(peso_equipaje)

        for carga_info in cargas_especiales:
            if carga_info['tipo'] == 'bicicleta':
                bici = Bicicleta(carga_info['peso'], carga_info['costo_por_kilo'])
                pasajero.agregar_carga_especial(bici)
            elif carga_info['tipo'] == 'mascota':
                mascota = Mascota(carga_info['especie'], valor_tiquete_base)
                pasajero.agregar_carga_especial(mascota)

        vuelo.agregar_pasajero(pasajero)
        self._recaudo_tiquetes += pasajero.precio_con_descuento_infante()
        self._recaudo_equipaje += pasajero.calcular_costo_equipaje_adicional()
        self._recaudo_equipaje += pasajero.costo_cargas_especiales()

    def devolver_tiquete(self, origen, destino, nombre):
        vuelo = self.buscar_vuelo(origen, destino)
        if not vuelo:
            raise ValueError("Vuelo no encontrado")
        pasajero = vuelo.buscar_pasajero(nombre)
        if not pasajero:
            raise ValueError("Pasajero no encontrado")
        vuelo.eliminar_pasajero_por_nombre(nombre)
        self._recaudo_tiquetes -= pasajero.precio_con_descuento_infante()
        self._recaudo_equipaje -= pasajero.calcular_costo_equipaje_adicional()
        self._recaudo_equipaje -= pasajero.costo_cargas_especiales()

    def trayecto_mas_recaudo(self):
        max_recaudo = 0
        mejor_trayecto = None
        for vuelo in self._vuelos.recorrer():
            recaudado = vuelo.total_recaudo()
            if recaudado > max_recaudo:
                max_recaudo = recaudado
                mejor_trayecto = (vuelo.origen, vuelo.destino)
        return mejor_trayecto, max_recaudo

    def viajeros_por_genero_destino(self, destino):
        hombres = 0
        mujeres = 0
        for vuelo in self._vuelos.recorrer():
            if vuelo.destino == destino:
                h, m = vuelo.contar_por_genero()
                hombres += h
                mujeres += m
        return hombres, mujeres

    def costo_promedio_tiquete_por_trayecto(self):
        datos = {}
        for vuelo in self._vuelos.recorrer():
            key = (vuelo.origen, vuelo.destino)
            total = 0
            cant = 0
            for p in vuelo._pasajeros.recorrer():
                total += p._valor_tiquete
                cant += 1
            datos[key] = total / cant if cant > 0 else 0
        return datos

    def recaudo_total_tiquetes(self):
        return self._recaudo_tiquetes

    def recaudo_total_equipaje_extra(self):
        return self._recaudo_equipaje





def main():
    aerolinea = Aerolinea()
    while True:
        print("\n--- Menú Aerolínea ---")
        print("1. Crear vuelo")
        print("2. Vender tiquete")
        print("3. Devolver tiquete")
        print("4. Trayecto más recaudado")
        print("5. Viajeros por género a un destino")
        print("6. Costo promedio tiquete por trayecto")
        print("7. Recaudo total tiquetes")
        print("8. Recaudo total equipaje extra")
        print("9. Salir")
        opcion = input("Ingrese opción: ")
        try:
            if opcion == "1":
                origen = input("Ciudad origen: ")
                destino = input("Ciudad destino: ")
                aerolinea.crear_vuelo(origen, destino)
                print("Vuelo creado.")
            elif opcion == "2":
                origen = input("Ciudad origen: ")
                destino = input("Ciudad destino: ")
                nombre = input("Nombre pasajero: ")
                genero = input("Género (hombre/mujer): ")
                edad = int(input("Edad: "))
                clase = input("Clase (economica/ejecutiva/premium): ")
                peso_equipaje = float(input("Peso equipaje (kg): "))
                cargas_especiales = []
                while True:
                    c = input("Agregar carga especial? (bicicleta/mascota/no): ").strip().lower()
                    if c == "no":
                        break
                    if c == "bicicleta":
                        peso_bic = float(input("Peso bicicleta (kg): "))
                        costo_kilo = float(input("Costo por kilo bicicleta: "))
                        cargas_especiales.append({'tipo':'bicicleta','peso':peso_bic,'costo_por_kilo':costo_kilo})
                    elif c == "mascota":
                        especie = input("Especie mascota (perro/gato): ")
                        cargas_especiales.append({'tipo':'mascota','especie':especie})
                    else:
                        print("Carga especial inválida.")
                aerolinea.vender_tiquete(origen,destino,nombre,genero,edad,clase,peso_equipaje,cargas_especiales)
                print("Tiquete vendido.")
            elif opcion == "3":
                origen = input("Ciudad origen: ")
                destino = input("Ciudad destino: ")
                nombre = input("Nombre pasajero a devolver: ")
                aerolinea.devolver_tiquete(origen,destino,nombre)
                print("Tiquete devuelto.")
            elif opcion == "4":
                trayecto, monto = aerolinea.trayecto_mas_recaudo()
                print(f"Trayecto más recaudado: {trayecto} - {monto}")
            elif opcion == "5":
                destino = input("Destino: ")
                h,m = aerolinea.viajeros_por_genero_destino(destino)
                print(f"Hombres: {h}, Mujeres: {m}")
            elif opcion == "6":
                promedios = aerolinea.costo_promedio_tiquete_por_trayecto()
                for k,v in promedios.items():
                    print(f"{k}: {v}")
            elif opcion == "7":
                print(f"Recaudo total tiquetes: {aerolinea.recaudo_total_tiquetes()}")
            elif opcion == "8":
                print(f"Recaudo total equipaje extra: {aerolinea.recaudo_total_equipaje_extra()}")
            elif opcion == "9":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
