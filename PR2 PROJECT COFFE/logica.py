from datos import CATALOGO_CAFES


class Cafe:
    """clase cafe para guardar el nombre y precio"""

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


class Monedero:
    """clase monedero para llevar el dinero y las monedas que acepta"""

    def __init__(self):
        self.permitidas = [0.5, 1.0, 2.0, 5.0]
        self.saldo = 0.0

    def validar(self, moneda):
        """revisa si la moneda sirve o no"""
        return moneda in self.permitidas

    def ingresar(self, moneda):
        """mete la moneda si es valida y suma al saldo"""
        if self.validar(moneda):
            self.saldo += moneda
            return True
        return False

    def limpiar(self):
        """saca todo el dinero y deja el saldo en cero"""
        acumulado = self.saldo
        self.saldo = 0.0
        return acumulado


class MaquinaCafe:
    """clase de la maquina de cafe principal"""

    def __init__(self):
        """inicializa la maquina con los cafecitos"""
        self.lista_cafes = [
            Cafe(nombre, precio) for nombre, precio in CATALOGO_CAFES
        ]
        self.cafe_seleccionado = None
        self.monedero = Monedero()
        self.preparando = False

    def elegir_cafe(self, cafe):
        """aqui el usuario elige su cafe"""
        if not self.preparando:
            self.cafe_seleccionado = cafe

    def meter_moneda(self, moneda):
        """mete una moneda a la maquina si se puede"""
        if self.preparando:
            return False, "Proceso en curso. Por favor espere."

        if self.cafe_seleccionado == None:
            return False, "Seleccione un producto antes de ingresar dinero."

        if self.monedero.ingresar(moneda):
            return True, "Moneda aceptada."
        return False, "Denominacion no permitida."

    def listo(self):
        """fija si ya alcanza la plata para el cafe"""
        if self.cafe_seleccionado != None:
            return self.monedero.saldo >= self.cafe_seleccionado.precio
        return False

    def cancelar(self):
        """cancela todo y devuelve la plata"""
        if self.preparando:
            return 0.0
        devuelto = self.monedero.limpiar()
        self.cafe_seleccionado = None
        return devuelto