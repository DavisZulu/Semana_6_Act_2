# usuarios.py
# Semana 6 - Quantum Wallet: codigo a MODELAR en UML.
#
# Integra el codigo original de la actividad, publicado en el enunciado de
# Canvas y en el repositorio del curso (FUNDAMENTOS-DE-SOFTWARE,
# MisProyectosPython/Semana_6/usuarios.py), y CONSERVA todas sus clases,
# atributos y metodos. Para enriquecer el ejercicio se adicionaron elementos,
# marcados con  [AGREGADO].
#
# Clases:  Wallet, Usuario, UsuarioEmpresa        (codigo original de la actividad)
#          Transaccion, Empleado                   [AGREGADO] clases adicionadas
#
# Integracion con el patron Singleton: Wallet obtiene la moneda y valida el
# limite por transaccion consultando al BancoCentral (banco_central.py).
#
# Para ejecutar:  python3 usuarios.py

from datetime import datetime

from banco_central import BancoCentral   # [AGREGADO] dependencia del Singleton


# ============================================================
# CLASE NUEVA: Transaccion (un movimiento de la billetera)      [AGREGADO]
# ============================================================
# COMPOSICION: cada Transaccion la crea la Wallet dentro de recargar();
# no existe por fuera de su Wallet.  En UML: Wallet 1 <>---- 0..* Transaccion
class Transaccion:
    # Atributo de CLASE (estatico) con UN guion bajo -> PROTEGIDO.
    # En UML:  # contador: int   (subrayado por ser estatico)
    _contador = 0

    def __init__(self, tipo, monto, saldo_resultante):
        Transaccion._contador += 1
        self.__id = Transaccion._contador          # - id: int
        self.__tipo = tipo                         # - tipo: str
        self.__monto = monto                       # - monto: float
        self.__fecha = datetime.now()              # - fecha: datetime
        self.__saldo_resultante = saldo_resultante # - saldo_resultante: float

    def obtener_monto(self):                       # + obtener_monto(): float
        return self.__monto

    def descripcion(self):                         # + descripcion(): str
        return (f"#{self.__id:03d} {self.__fecha:%Y-%m-%d %H:%M} "
                f"{self.__tipo:<8} {self.__monto:>12,.0f}  saldo {self.__saldo_resultante:>12,.0f}")


# ============================================================
# CLASE 1: Wallet (la billetera)
# ============================================================
class Wallet:
    def __init__(self, saldo_inicial=0.0):
        # __saldo lleva DOBLE guion bajo -> es PRIVADO.  En UML:  - saldo: float
        self.__saldo = saldo_inicial
        self.__id_billetera = "W-" + str(id(self))   # PRIVADO  ->  - id_billetera: str
        # [AGREGADO]  - moneda: str  (la define la configuracion global del BancoCentral)
        self.__moneda = BancoCentral().obtener_moneda()
        self.__historial = []          # [AGREGADO]  - historial: list[Transaccion]

    # Metodos PUBLICOS.  En UML:  + consultar_saldo()
    def consultar_saldo(self):
        return self.__saldo

    def recargar(self, monto):        # + recargar()
        BancoCentral().validar_monto(monto)   # [AGREGADO] limite global por transaccion
        self.__saldo += monto
        # [AGREGADO] cada movimiento queda registrado en el historial
        tipo = "RECARGA" if monto >= 0 else "PAGO"
        self.__historial.append(Transaccion(tipo, abs(monto), self.__saldo))
        return self.__saldo

    def obtener_historial(self):      # [AGREGADO]  + obtener_historial(): list[Transaccion]
        return list(self.__historial)  # copia: el historial original no se expone

    def obtener_moneda(self):         # [AGREGADO]  + obtener_moneda(): str
        return self.__moneda


# ============================================================
# CLASE 2: Usuario (el dueno de la billetera)
# ============================================================
class Usuario:
    # email y cedula son opcionales para que Usuario("Ana") siga funcionando
    def __init__(self, nombre, email="", cedula=""):
        # 'nombre' es simple -> es PUBLICO.  En UML:  + nombre: str
        self.nombre = nombre
        self.email = email             # PUBLICO  ->  + email: str
        self.__cedula = cedula         # [AGREGADO]  - cedula: str

        # COMPOSICION: el Usuario "es dueno" de una Wallet, que se crea DENTRO de
        # su constructor. Si se borra el Usuario, su Wallet deja de existir.
        # __wallet lleva doble guion bajo -> PRIVADO.  En UML:  - wallet: Wallet
        self.__wallet = Wallet()

    # Metodo PUBLICO.  En UML:  + realizar_pago()
    def realizar_pago(self, monto):
        saldo = self.__wallet.consultar_saldo()
        if monto > saldo:
            raise ValueError("saldo insuficiente")
        self.__wallet.recargar(-monto)   # descuenta el pago
        return self.__wallet.consultar_saldo()

    def recargar_wallet(self, monto):
        return self.__wallet.recargar(monto)

    def consultar_saldo(self):         # [AGREGADO]  + consultar_saldo(): float
        return self.__wallet.consultar_saldo()

    def transferir(self, destino, monto):   # [AGREGADO]  + transferir(destino: Usuario, monto: float): float
        self.realizar_pago(monto)            # valida el saldo y descuenta
        destino.recargar_wallet(monto)       # abona en la Wallet del otro usuario
        return self.consultar_saldo()

    def ver_movimientos(self):         # [AGREGADO]  + ver_movimientos(): list[str]
        return [t.descripcion() for t in self.__wallet.obtener_historial()]

    def obtener_cedula(self):          # [AGREGADO]  + obtener_cedula(): str
        return self.__cedula


# ============================================================
# CLASE NUEVA: Empleado (HEREDA de Usuario)                     [AGREGADO]
# ============================================================
# HERENCIA: un Empleado ES UN Usuario (tiene nombre, cedula y su propia Wallet)
# y agrega su cargo y su salario.
class Empleado(Usuario):
    def __init__(self, nombre, cedula, cargo, salario):
        super().__init__(nombre, cedula=cedula)
        self.__cargo = cargo           # - cargo: str
        self.__salario = salario       # - salario: float

    def obtener_salario(self):         # + obtener_salario(): float
        return self.__salario

    def ficha(self):                   # + ficha(): str
        return f"{self.nombre} (CC {self.obtener_cedula()}) - {self.__cargo}"


# ============================================================
# CLASE 3: UsuarioEmpresa (HEREDA de Usuario)
# ============================================================
# HERENCIA: UsuarioEmpresa(Usuario) -> hereda TODO de Usuario y agrega lo suyo.
# En UML: una flecha con TRIANGULO HUECO que apunta al padre (Usuario).
class UsuarioEmpresa(Usuario):
    def __init__(self, nombre, nit, email=""):
        super().__init__(nombre, email)   # reutiliza el constructor del padre
        # __nit lleva doble guion bajo -> PRIVADO.  En UML:  - nit: str
        self.__nit = nit
        # [AGREGADO] AGREGACION: la empresa agrupa empleados que se crean AFUERA
        # y siguen existiendo aunque la empresa desaparezca.
        # En UML: UsuarioEmpresa <>---- 0..* Empleado  (rombo HUECO)
        self.__empleados = []          # - empleados: list[Empleado]

    # Metodo PUBLICO propio.  En UML:  + generar_factura()
    def generar_factura(self):
        return f"Factura de {self.nombre} (NIT: {self.__nit})"

    def agregar_empleado(self, empleado):   # [AGREGADO]  + agregar_empleado(empleado: Empleado)
        self.__empleados.append(empleado)

    def contar_empleados(self):        # [AGREGADO]  + contar_empleados(): int
        return len(self.__empleados)

    def pagar_nomina(self):            # [AGREGADO]  + pagar_nomina(): float
        total = sum(e.obtener_salario() for e in self.__empleados)
        if total > self.consultar_saldo():
            raise ValueError("saldo insuficiente para la nomina")
        for empleado in self.__empleados:
            self.transferir(empleado, empleado.obtener_salario())
        return total


# ============================================================
# Demostracion (opcional)
# ============================================================
if __name__ == "__main__":
    # --- Demostracion del codigo original (sin cambios) ---
    ana = Usuario("Ana")
    ana.recargar_wallet(100000)
    print("Saldo tras pagar 30000:", ana.realizar_pago(30000))

    bancolombia = UsuarioEmpresa("Bancolombia", "900123456-7")
    bancolombia.recargar_wallet(500000)
    print(bancolombia.generar_factura())
    print("Saldo empresa:", bancolombia.realizar_pago(200000))

    # --- [AGREGADO] Demostracion de los elementos adicionados ---
    print("\n--- Version ampliada ---")
    quantum = UsuarioEmpresa("Quantum SAS", "901555222-1")
    quantum.recargar_wallet(10000000)

    laura = Empleado("Laura Gomez", "1036123456", "Desarrolladora", 4500000)
    pedro = Empleado("Pedro Rios", "1017987654", "Analista", 3200000)
    quantum.agregar_empleado(laura)
    quantum.agregar_empleado(pedro)

    print("Empleados:", quantum.contar_empleados())
    print("Nomina pagada:", quantum.pagar_nomina())
    print("Saldo empresa:", quantum.consultar_saldo())
    print("Saldo de", laura.ficha() + ":", laura.consultar_saldo())

    print("Movimientos de Quantum SAS:")
    for linea in quantum.ver_movimientos():
        print("  ", linea)
