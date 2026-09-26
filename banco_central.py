# banco_central.py
# Quantum Core - Patron de diseno SINGLETON: Banco Central.
#
# Integra el codigo original de la actividad, publicado en el enunciado de
# Canvas y en el repositorio del curso (FUNDAMENTOS-DE-SOFTWARE,
# MisProyectosPython/Semana_6/banco_central.py). Para enriquecer el ejercicio
# se adiciono la configuracion global del sistema, marcada con  [AGREGADO].
#
# Problema: en la Fintech Quantum Core NO queremos que se cree un "Banco Central"
# nuevo cada vez que alguien hace un pago (eso causaria caos con los saldos y
# gastaria memoria). Necesitamos UNA sola instancia en todo el sistema.
#
# Solucion: el patron Singleton garantiza una unica instancia y un punto de
# acceso global a ella.
#
# Para ejecutar:  python3 banco_central.py


class BancoCentral:
    """Singleton: por mas veces que lo crees, SIEMPRE es el mismo objeto."""

    # Atributo de CLASE (estatico): guarda la unica copia del banco.
    # Doble guion bajo -> PRIVADO.  En UML:  - instancia: BancoCentral  (subrayado)
    __instancia = None

    # __new__ se ejecuta ANTES que __init__ y es quien CREA el objeto.
    # Aqui interceptamos la creacion: si ya existe una instancia, la devolvemos;
    # si no, la creamos una sola vez.
    def __new__(cls):
        if cls.__instancia is None:
            print("Creando el Banco Central por única vez...")
            cls.__instancia = super(BancoCentral, cls).__new__(cls)
            cls.__instancia.fondos_totales = 1000000   # + fondos_totales: float
            cls.__instancia.reservas = 0               # + reservas: float
            # [AGREGADO] configuracion global compartida por todo el sistema
            cls.__instancia.__configuracion = {        # - configuracion: dict
                "moneda": "COP",
                "limite_transaccion": 50000000,
            }
        return cls.__instancia

    def emitir_moneda(self, cantidad):
        self.reservas += cantidad
        return self.reservas

    # ----------------------------------------------------------------
    # [AGREGADO] Acceso controlado a la configuracion global
    # ----------------------------------------------------------------
    def obtener_moneda(self):
        """Devuelve la moneda oficial del sistema."""
        return self.__configuracion["moneda"]

    def obtener_limite(self):
        """Devuelve el monto maximo permitido por transaccion."""
        return self.__configuracion["limite_transaccion"]

    def validar_monto(self, monto):
        """Lanza ValueError si el monto supera el limite por transaccion."""
        if abs(monto) > self.obtener_limite():
            raise ValueError("el monto supera el limite por transaccion")


# ============================================================
# Demostracion: aunque creemos "varios", es el MISMO objeto
# ============================================================
if __name__ == "__main__":
    # --- Prueba del enunciado (Canvas) ---
    banco1 = BancoCentral()
    banco2 = BancoCentral()
    print(f"Es el mismo banco? {banco1 is banco2}")      # True

    # --- Demostracion del repositorio del curso ---
    banco_a = BancoCentral()
    banco_b = BancoCentral()

    print("id(banco_a):", id(banco_a))
    print("id(banco_b):", id(banco_b))
    print("Son el mismo objeto?:", banco_a is banco_b)   # True

    # Aunque intentemos crear 100 en un bucle, siempre es la misma instancia:
    ultimo = None
    for _ in range(100):
        ultimo = BancoCentral()
        print("id(ultimo):", id(ultimo))
    print("El #100 es el mismo?:", ultimo is banco_a)     # True

    banco_a.emitir_moneda(1000)
    banco_b.emitir_moneda(500)
    # Como son el mismo objeto, las reservas se comparten:
    print("Reservas totales (compartidas):", banco_b.reservas)   # 1500

    # --- [AGREGADO] Configuracion global ---
    print("Moneda del sistema:", banco_a.obtener_moneda())
    print("Limite por transaccion:", banco_b.obtener_limite())
