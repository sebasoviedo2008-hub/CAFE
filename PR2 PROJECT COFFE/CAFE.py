import ttkbootstrap as ttk


class Cafe:

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


class Monedero:

    def __init__(self):
        self.permitidas = [0.5, 1.0, 2.0, 5.0]
        self.saldo = 0.0

    def validar(self, moneda):
        return moneda in self.permitidas

    def ingresar(self, moneda):
        if self.validar(moneda):
            self.saldo += moneda
            return True
        return False

    def limpiar(self):
        acumulado = self.saldo
        self.saldo = 0.0
        return acumulado


class MaquinaCafe:

    def __init__(self):
        self.lista_cafes = [
            Cafe("Expresso", 5.0),
            Cafe("Macchiato", 5.0),
            Cafe("Capuchino", 5.0),
            Cafe("Latte", 5.0),
        ]
        self.cafe_seleccionado = None
        self.monedero = Monedero()
        self.preparando = False

    def elegir_cafe(self, cafe):
        if not self.preparando:
            self.cafe_seleccionado = cafe

    def meter_moneda(self, moneda):
        if self.preparando:
            return False, "Proceso en curso. Por favor espere."

        if self.cafe_seleccionado == None:
            return False, "Seleccione un producto antes de ingresar dinero."

        if self.monedero.ingresar(moneda):
            return True, "Moneda aceptada."
        return False, "Denominacion no permitida."

    def listo(self):
        if self.cafe_seleccionado != None:
            return self.monedero.saldo >= self.cafe_seleccionado.precio
        return False

    def cancelar(self):
        if self.preparando:
            return 0.0
        devuelto = self.monedero.limpiar()
        self.cafe_seleccionado = None
        return devuelto


class interfaz:

    def __init__(self):
        self.maquina = MaquinaCafe()
        self.progreso = 0

        self.ventana = ttk.Window(
            title="MAQUINA DE CAFECITO",
            themename="minty",
            size=(760, 440),
            resizable=(False, False),
        )

        main_box = ttk.Frame(self.ventana, padding=20)
        main_box.pack(fill="both", expand=True)

        col_izquierda = ttk.Frame(main_box, padding=10)
        col_izquierda.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(
            col_izquierda,
            text="ESTADO DEL PEDIDO",
            font=("Helvetica", 11, "bold"),
            bootstyle="secondary",
        ).pack(anchor="w", pady=(0, 10))

        card_pantalla = ttk.Frame(col_izquierda, padding=15, bootstyle="light")
        card_pantalla.pack(fill="x", pady=5)

        self.lbl_msg = ttk.Label(
            card_pantalla,
            text="Bienvenido. Seleccione una bebida.",
            font=("Helvetica", 10),
            wraplength=280,
            justify="left",
        )
        self.lbl_msg.pack(anchor="w", fill="x")

        self.lbl_saldo = ttk.Label(
            col_izquierda,
            text="Monto ingresado: 0.0 UM",
            font=("Helvetica", 11, "bold"),
            bootstyle="dark",
        )
        self.lbl_saldo.pack(anchor="w", pady=(15, 5))

        self.barra = ttk.Progressbar(
            col_izquierda, maximum=100, bootstyle="info-striped"
        )
        self.barra.pack(fill="x", pady=(5, 20))

        self.btn_canc = ttk.Button(
            col_izquierda,
            text="Cancelar y Devolver Dinero",
            bootstyle="outline-danger",
            command=self.click_cancelar,
        )
        self.btn_canc.pack(fill="x", side="bottom")

        sep = ttk.Separator(main_box, orient="vertical")
        sep.pack(side="left", fill="y", padx=10)

        col_derecha = ttk.Frame(main_box, padding=10)
        col_derecha.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ttk.Label(
            col_derecha,
            text="SELECCIONE SU BEBIDA (5.0 UM)",
            font=("Helvetica", 11, "bold"),
            bootstyle="secondary",
        ).pack(anchor="w", pady=(0, 10))

        grid_cafes = ttk.Frame(col_derecha)
        grid_cafes.pack(fill="x", pady=(0, 20))

        for idx, cafe in enumerate(self.maquina.lista_cafes):
            btn = ttk.Button(
                grid_cafes,
                text=cafe.nombre,
                bootstyle="outline-dark",
                command=lambda c=cafe: self.click_cafe(c),
            )
            btn.grid(
                row=idx // 2,
                column=idx % 2,
                padx=5,
                pady=5,
                sticky="ew",
                ipady=5,
            )

        grid_cafes.columnconfigure(0, weight=1)
        grid_cafes.columnconfigure(1, weight=1)

        ttk.Label(
            col_derecha,
            text="DEPOSITAR MONEDAS",
            font=("Helvetica", 11, "bold"),
            bootstyle="secondary",
        ).pack(anchor="w", pady=(0, 10))

        grid_monedas = ttk.Frame(col_derecha)
        grid_monedas.pack(fill="x")

        for idx, valor in enumerate(self.maquina.monedero.permitidas):
            btn_m = ttk.Button(
                grid_monedas,
                text=str(valor) + " UM",
                bootstyle="secondary",
                command=lambda v=valor: self.click_moneda(v),
            )
            btn_m.grid(row=0, column=idx, padx=3, pady=5, sticky="ew", ipady=3)
            grid_monedas.columnconfigure(idx, weight=1)

    def click_cafe(self, cafe):
        if not self.maquina.preparando:
            self.maquina.elegir_cafe(cafe)
            self.actualizar()

    def click_moneda(self, valor):
        ok, msg = self.maquina.meter_moneda(valor)
        if not ok:
            self.lbl_msg.config(text=msg)
        else:
            if self.maquina.listo():
                self.hacer_cafe()
            else:
                self.actualizar()

    def click_cancelar(self):
        if self.maquina.preparando:
            self.lbl_msg.config(
                text="No es posible cancelar mientras se prepara la bebida."
            )
        else:
            recuperado = self.maquina.cancelar()
            self.actualizar()
            if recuperado > 0:
                self.lbl_msg.config(
                    text="Operacion cancelada. Se han devuelto "
                    + str(recuperado)
                    + " UM."
                )

    def hacer_cafe(self):
        self.maquina.preparando = True
        vuelto = (
            self.maquina.monedero.saldo - self.maquina.cafe_seleccionado.precio
        )
        self.maquina.monedero.saldo = 0.0

        self.lbl_msg.config(
            text="Preparando su "
            + self.maquina.cafe_seleccionado.nombre
            + ". Por favor espere..."
        )
        self.progreso = 0
        self.animacion(vuelto)

    def animacion(self, vuelto):
        if self.progreso <= 100:
            self.barra["value"] = self.progreso
            self.progreso += 5
            self.ventana.after(50, lambda: self.animacion(vuelto))
        else:
            txt = (
                "Su "
                + self.maquina.cafe_seleccionado.nombre
                + " esta listo. Puede retirarlo."
            )
            if vuelto > 0:
                txt = txt + " Se entregan " + str(vuelto) + " UM de cambio."

            self.lbl_msg.config(text=txt)
            self.maquina.preparando = False
            self.maquina.cafe_seleccionado = None
            self.lbl_saldo.config(text="Monto ingresado: 0.0 UM")

    def actualizar(self):
        if self.maquina.cafe_seleccionado == None:
            self.lbl_msg.config(
                text="Seleccione una bebida de la lista para iniciar."
            )
        else:
            falta = (
                self.maquina.cafe_seleccionado.precio
                - self.maquina.monedero.saldo
            )
            if falta > 0:
                self.lbl_msg.config(
                    text="Bebida: "
                    + self.maquina.cafe_seleccionado.nombre
                    + " | Pendiente: "
                    + str(falta)
                    + " UM"
                )
            else:
                self.lbl_msg.config(text="Procesando despacho...")

        self.lbl_saldo.config(
            text="Monto ingresado: "
            + str(self.maquina.monedero.saldo)
            + " UM"
        )


if __name__ == "__main__":
    app = interfaz()
    app.ventana.mainloop()