# comprobacion_singleton.py
# Script de apoyo para el informe (no hace parte del modelo).
# Comprueba el comportamiento del Singleton BancoCentral y lo compara con una
# clase comun, para evidenciar el riesgo de NO usar el patron.
# Para ejecutar:  python3 comprobacion_singleton.py

from banco_central import BancoCentral
from usuarios import Usuario, Wallet


class BancoSinSingleton:
    """Clase comun: cada llamada crea un objeto nuevo (solo para comparar)."""

    def __init__(self):
        self.fondos_totales = 1000000
        self.reservas = 0

    def emitir_moneda(self, cantidad):
        self.reservas += cantidad
        return self.reservas


print("1. INSTANCIA UNICA")
a = BancoCentral()
b = BancoCentral()
print("   a is b:", a is b, "| id(a) == id(b):", id(a) == id(b))
ids = {id(BancoCentral()) for _ in range(100)}
print("   Objetos distintos tras 100 intentos:", len(ids))

print("2. ATRIBUTO ESTATICO PRIVADO")
print("   'instancia' pertenece a la clase:", "_BancoCentral__instancia" in vars(BancoCentral))
try:
    BancoCentral.__instancia
except AttributeError:
    print("   Acceso directo a BancoCentral.__instancia -> AttributeError (privado)")

print("3. DATOS GLOBALES COMPARTIDOS")
a.emitir_moneda(1000)
b.emitir_moneda(500)
print("   Reservas vistas desde a:", a.reservas, "| desde b:", b.reservas)
billetera1 = Wallet()
billetera2 = Wallet()
print("   Moneda de dos billeteras distintas:", billetera1.obtener_moneda(), "y", billetera2.obtener_moneda())
ana = Usuario("Ana")
try:
    ana.recargar_wallet(60000000)
except ValueError as error:
    print("   Recarga de 60.000.000 ->", "ValueError:", error)

print("4. SIN SINGLETON (comparacion)")
x = BancoSinSingleton()
y = BancoSinSingleton()
x.emitir_moneda(1000)
y.emitir_moneda(500)
print("   x is y:", x is y)
print("   Reservas en x:", x.reservas, "| en y:", y.reservas, "-> datos inconsistentes")
ids_comunes = {id(o) for o in [BancoSinSingleton() for _ in range(100)]}
print("   Objetos distintos tras 100 intentos:", len(ids_comunes))
