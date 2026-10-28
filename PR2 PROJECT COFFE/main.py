import tkinter as tk
import cv2
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import pygame
from logica import MaquinaCafe


class CafeteriaApp:
    """controlador principal de la interfaz grafica"""

    def __init__(self):
        """configura la ventana principal inicia la musica y carga la intro"""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("musica.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        except:
            pass

        self.ventana = ttk.Window(
            title="Entralgo Coffee Maquina de Cafe",
            themename="gruvbox-dark",
            size=(820, 520),
            resizable=(False, False),
        )

        self.imagenes_ref = []
        self.contenedor = ttk.Frame(self.ventana)
        self.contenedor.pack(fill="both", expand=True)

        self.video_path = "intro.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        self.delay = int((1000 / fps) / 2.8)

        self.lbl_video = tk.Label(self.contenedor, bg="black")
        self.lbl_video.place(x=0, y=0, width=820, height=520)

        self.reproducir_video()

    def reproducir_video(self):
        """reproduce el video de intro frame por frame eliminando marcas de agua"""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            frame = frame[
                int(h * 0.03) : int(h * 0.93), int(w * 0.03) : int(w * 0.97)
            ]
            frame = cv2.resize(frame, (820, 520))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_video.imgtk = imgtk
            self.lbl_video.configure(image=imgtk)
            self.ventana.after(self.delay, self.reproducir_video)
        else:
            self.cap.release()
            self.mostrar_cartel_bienvenida()

    def mostrar_cartel_bienvenida(self):
        """muestra el cartel flotante de bienvenida sobre el video congelado"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        card = ttk.Frame(self.contenedor, padding=15, bootstyle="secondary")
        card.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        ttk.Label(
            card,
            text="El cafe es el regalo de Dios a la humanidad",
            font=("Georgia", 10, "italic"),
            bootstyle="light",
            anchor="center",
        ).pack(pady=(0, 2), fill="x")

        ttk.Label(
            card,
            text="ENTRALGO COFFEE",
            font=("Georgia", 18, "bold"),
            bootstyle="inverse-secondary",
            anchor="center",
        ).pack(pady=(2, 2), fill="x")

        ttk.Label(
            card,
            text="Bienvenido a nuestro sistema de autoservicio",
            font=("Segoe UI", 10),
            bootstyle="inverse-secondary",
            anchor="center",
        ).pack(pady=2, fill="x")

        ttk.Label(
            card,
            text="Franquicia de Johan Sebastian Oviedo Entralgo C I 32307911",
            font=("Segoe UI", 9, "bold"),
            bootstyle="warning",
            anchor="center",
        ).pack(pady=(2, 8), fill="x")

        btn_historia = ttk.Button(
            card,
            text="Historia del Cafe",
            bootstyle="outline-light",
            command=self.mostrar_historia_en_pantalla,
        )
        btn_historia.pack(ipadx=15, ipady=4, pady=6)

        btn_cont = ttk.Button(
            card,
            text="INICIAR PEDIDO",
            bootstyle="warning",
            command=self.mostrar_seleccion_cafe,
        )
        btn_cont.pack(ipadx=20, ipady=6, pady=6)
        btn_cont.configure(font=("Segoe UI", 11, "bold"))

    def mostrar_historia_en_pantalla(self):
        """muestra la imagen de la historia del cafe en la ventana principal"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        frame_h = ttk.Frame(self.contenedor, padding=20)
        frame_h.pack(fill="both", expand=True)

        ttk.Label(
            frame_h,
            text="HISTORIA Y ORIGEN DEL CAFE",
            font=("Georgia", 18, "bold"),
            bootstyle="light",
            anchor="center",
        ).pack(pady=(5, 10))

        try:
            pil_img = Image.open("historia.png")
            pil_img = pil_img.resize((650, 320), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_img)
            self.imagenes_ref.append(tk_img)

            lbl_img = ttk.Label(frame_h, image=tk_img, bootstyle="secondary")
            lbl_img.pack(pady=(0, 15))
        except:
            ttk.Label(
                frame_h,
                text="No se encontro el archivo historia png en la carpeta",
                font=("Segoe UI", 10),
                bootstyle="danger",
            ).pack(pady=40)

        btn_volver = ttk.Button(
            frame_h,
            text="Volver al Menu Principal",
            bootstyle="warning",
            command=self.mostrar_cartel_bienvenida,
        )
        btn_volver.pack(ipadx=20, ipady=6)

    def mostrar_seleccion_cafe(self):
        """carga la cuadricula con los cafes fotos grandes y precios grandes"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        self.maquina = MaquinaCafe()

        self.frame_seleccion = ttk.Frame(self.contenedor, padding=20)
        self.frame_seleccion.pack(fill="both", expand=True)

        top_bar = ttk.Frame(self.frame_seleccion)
        top_bar.pack(fill="x", pady=(0, 10))

        ttk.Label(
            top_bar,
            text="SELECCIONA TU CAFE",
            font=("Georgia", 18, "bold"),
            bootstyle="light",
        ).pack(side="left")

        btn_volver_menu = ttk.Button(
            top_bar,
            text="Volver al Menu Principal",
            bootstyle="outline-secondary",
            command=self.mostrar_cartel_bienvenida,
        )
        btn_volver_menu.pack(side="right")

        ttk.Label(
            self.frame_seleccion,
            text="Todas las opciones tienen un costo de 50 UM",
            font=("Segoe UI", 10),
            bootstyle="secondary",
        ).pack(anchor="w", pady=(0, 15))

        grid_cafes = ttk.Frame(self.frame_seleccion)
        grid_cafes.pack(fill="both", expand=True)

        fotos_mapa = {
            "Expresso": "espresso.png",
            "Macchiato": "macchiato.png",
            "Capuchino": "capuchino.png",
            "Latte": "latte.png",
        }

        for idx, cafe in enumerate(self.maquina.lista_cafes):
            card_cafe = ttk.Frame(
                grid_cafes, padding=15, bootstyle="secondary"
            )
            card_cafe.grid(
                row=idx // 2, column=idx % 2, padx=12, pady=8, sticky="nsew"
            )

            contenido_card = ttk.Frame(card_cafe, bootstyle="secondary")
            contenido_card.pack(fill="both", expand=True, pady=(0, 8))

            nombre_archivo = fotos_mapa.get(cafe.nombre, "")
            try:
                pil_img = Image.open(nombre_archivo)
                pil_img = pil_img.resize((88, 88), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                self.imagenes_ref.append(tk_img)

                lbl_foto = ttk.Label(
                    contenido_card, image=tk_img, bootstyle="secondary"
                )
                lbl_foto.pack(side="left", padx=(0, 15))
            except:
                pass

            info_frame = ttk.Frame(contenido_card, bootstyle="secondary")
            info_frame.pack(side="left", fill="both", expand=True)

            ttk.Label(
                info_frame,
                text=cafe.nombre.upper(),
                font=("Georgia", 15, "bold"),
                bootstyle="light",
            ).pack(anchor="w", pady=(4, 6))

            ttk.Label(
                info_frame,
                text=(
                    f"${cafe.precio}0 UM"
                    if cafe.precio == 5
                    else f"${cafe.precio} UM"
                ),
                font=("Georgia", 14, "bold"),
                bootstyle="warning",
            ).pack(anchor="w", pady=(0, 4))

            btn_elegir = ttk.Button(
                card_cafe,
                text="Elegir este cafe",
                bootstyle="warning",
                command=lambda c=cafe: self.ir_a_pago(c),
            )
            btn_elegir.pack(fill="x", ipady=6, pady=(4, 0))

        grid_cafes.columnconfigure(0, weight=1)
        grid_cafes.columnconfigure(1, weight=1)
        grid_cafes.rowconfigure(0, weight=1)
        grid_cafes.rowconfigure(1, weight=1)

    def ir_a_pago(self, cafe):
        """guarda el cafe seleccionado y pasa a la pantalla de monedas"""
        self.maquina.elegir_cafe(cafe)
        self.mostrar_pantalla_pago()

    def mostrar_pantalla_pago(self):
        """muestra la seccion para insertar monedas y ver el saldo"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        self.frame_pago = ttk.Frame(self.contenedor, padding=25)
        self.frame_pago.pack(fill="both", expand=True)

        top_bar = ttk.Frame(self.frame_pago)
        top_bar.pack(fill="x", pady=(0, 15))

        ttk.Label(
            top_bar,
            text=(
                "SELECCIONADO"
                f" {self.maquina.cafe_seleccionado.nombre.upper()}"
            ),
            font=("Georgia", 18, "bold"),
            bootstyle="light",
        ).pack(side="left")

        btn_volver = ttk.Button(
            top_bar,
            text="Cambiar cafe",
            bootstyle="outline-secondary",
            command=self.regresar_seleccion,
        )
        btn_volver.pack(side="right")

        self.card_led = ttk.Frame(
            self.frame_pago, padding=20, bootstyle="secondary"
        )
        self.card_led.pack(fill="x", pady=10)

        self.lbl_msg = ttk.Label(
            self.card_led,
            text=(
                f"Precio ${self.maquina.cafe_seleccionado.precio} UM Inserta tus"
                " monedas por favor"
            ),
            font=("Segoe UI", 11, "bold"),
            bootstyle="inverse-secondary",
        )
        self.lbl_msg.pack(anchor="w", pady=2)

        self.lbl_saldo = ttk.Label(
            self.card_led,
            text="Monto ingresado 0 UM",
            font=("Georgia", 14, "bold"),
            bootstyle="warning",
        )
        self.lbl_saldo.pack(anchor="w", pady=(8, 2))

        self.frame_acciones = ttk.Frame(self.frame_pago)
        self.frame_acciones.pack(fill="x", pady=15)

        ttk.Label(
            self.frame_acciones,
            text="INGRESAR MONEDAS",
            font=("Segoe UI", 11, "bold"),
            bootstyle="light",
        ).pack(anchor="w", pady=(5, 10))

        grid_monedas = ttk.Frame(self.frame_acciones)
        grid_monedas.pack(fill="x", pady=(0, 10))

        for idx, valor in enumerate(self.maquina.monedero.permitidas):
            btn_m = ttk.Button(
                grid_monedas,
                text=f"${valor} UM",
                bootstyle="light",
                command=lambda v=valor: self.click_moneda(v),
            )
            btn_m.grid(row=0, column=idx, padx=5, sticky="ew", ipady=8)
            grid_monedas.columnconfigure(idx, weight=1)

        self.btn_canc = ttk.Button(
            self.frame_pago,
            text="Cancelar y Retirar Dinero",
            bootstyle="outline-danger",
            command=self.click_cancelar,
        )
        self.btn_canc.pack(fill="x", side="bottom", pady=5)

    def regresar_seleccion(self):
        """permite volver atras si no se esta preparando nada"""
        if not self.maquina.preparando:
            self.maquina.cancelar()
            self.mostrar_seleccion_cafe()

    def click_moneda(self, valor):
        """procesa la moneda que el usuario le mete a la maquina"""
        ok, msg = self.maquina.meter_moneda(valor)
        if not ok:
            self.lbl_msg.config(text=msg)
        else:
            self.actualizar_saldo_pantalla()
            if self.maquina.listo():
                self.hacer_cafe()

    def click_cancelar(self):
        """cancela la transaccion y devuelve el dinero"""
        if self.maquina.preparando:
            self.lbl_msg.config(
                text="No puedes cancelar mientras se prepara el cafe"
            )
        else:
            recuperado = self.maquina.cancelar()
            self.actualizar_saldo_pantalla()
            if recuperado > 0:
                self.lbl_msg.config(
                    text=f"Cancelado Se te devuelven {recuperado} UM"
                )

    def hacer_cafe(self):
        """inicia el proceso reproduciendo el video corto de preparacion con mensaje"""
        self.maquina.preparando = True
        self.vuelto_actual = (
            self.maquina.monedero.saldo - self.maquina.cafe_seleccionado.precio
        )
        self.nombre_cafe_actual = self.maquina.cafe_seleccionado.nombre
        self.maquina.monedero.saldo = 0.0

        for widget in self.contenedor.winfo_children():
            widget.destroy()

        frame_prep = ttk.Frame(self.contenedor, padding=15)
        frame_prep.pack(fill="both", expand=True)

        ttk.Label(
            frame_prep,
            text="PREPARANDO SU CAFE",
            font=("Georgia", 18, "bold"),
            bootstyle="warning",
            anchor="center",
        ).pack(pady=(5, 10))

        self.lbl_video_prep = tk.Label(frame_prep, bg="black")
        self.lbl_video_prep.pack(fill="both", expand=True, pady=(0, 5))

        self.cap_prep = cv2.VideoCapture("preparacion.mp4")
        fps = self.cap_prep.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        self.delay_prep = int(1000 / fps)

        self.reproducir_video_preparacion()

    def reproducir_video_preparacion(self):
        """reproduce el video de preparacion frame por frame eliminando marcas de agua"""
        ret, frame = self.cap_prep.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            frame = frame[
                int(h * 0.03) : int(h * 0.93), int(w * 0.03) : int(w * 0.97)
            ]
            frame = cv2.resize(frame, (760, 380))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_video_prep.imgtk = imgtk
            self.lbl_video_prep.configure(image=imgtk)
            self.ventana.after(
                self.delay_prep, self.reproducir_video_preparacion
            )
        else:
            self.cap_prep.release()
            for widget in self.contenedor.winfo_children():
                widget.destroy()
            self.mostrar_mensaje_cafe_listo(
                self.nombre_cafe_actual, self.vuelto_actual
            )

    def mostrar_mensaje_cafe_listo(self, nombre_cafe, vuelto):
        """muestra el mensaje de cafe listo y la opcion de calificar con estrellas"""
        self.maquina.preparando = False
        self.maquina.cafe_seleccionado = None

        frame_listo = ttk.Frame(
            self.contenedor, padding=25, bootstyle="secondary"
        )
        frame_listo.place(
            relx=0.5, rely=0.5, anchor="center", width=580, height=380
        )

        ttk.Label(
            frame_listo,
            text="CAFE LISTO",
            font=("Georgia", 18, "bold"),
            bootstyle="light",
            anchor="center",
        ).pack(pady=(10, 5), fill="x")

        mensaje = f"Disfrute su delicioso {nombre_cafe}"
        if vuelto > 0:
            mensaje += f" Cambio entregado {vuelto} UM"

        ttk.Label(
            frame_listo,
            text=mensaje,
            font=("Segoe UI", 11),
            bootstyle="inverse-secondary",
            anchor="center",
        ).pack(pady=5, fill="x")

        ttk.Label(
            frame_listo,
            text="Calificanos",
            font=("Segoe UI", 11, "bold"),
            bootstyle="warning",
            anchor="center",
        ).pack(pady=(10, 5), fill="x")

        frame_estrellas = ttk.Frame(frame_listo, bootstyle="secondary")
        frame_estrellas.pack(pady=5)

        def registrar_calificacion(estrellas):
            for widget in frame_listo.winfo_children():
                widget.destroy()

            ttk.Label(
                frame_listo,
                text=f"Gracias por tu calificacion de {estrellas} estrellas",
                font=("Segoe UI", 11, "bold"),
                bootstyle="warning",
                anchor="center",
            ).pack(pady=60, fill="x")

            self.ventana.after(1500, self.mostrar_cartel_bienvenida)

        for i in range(1, 6):
            btn_est = ttk.Button(
                frame_estrellas,
                text=f"{i} Estrellas",
                bootstyle="outline-light",
                command=lambda val=i: registrar_calificacion(val),
            )
            btn_est.pack(side="left", padx=5, ipadx=8, ipady=6)

        btn_omitir = ttk.Button(
            frame_listo,
            text="Omitir y Volver al Menu",
            bootstyle="outline-secondary",
            command=self.mostrar_cartel_bienvenida,
        )
        btn_omitir.pack(pady=(15, 0), ipadx=10, ipady=3)

    def actualizar_saldo_pantalla(self):
        """refresca los textos del saldo actual en la interfaz"""
        self.lbl_saldo.config(
            text=f"Monto ingresado ${self.maquina.monedero.saldo} UM"
        )
        falta = (
            self.maquina.cafe_seleccionado.precio
            - self.maquina.monedero.saldo
        )
        if falta > 0:
            self.lbl_msg.config(
                text=(
                    f"Faltan {falta} UM para tu"
                    f" {self.maquina.cafe_seleccionado.nombre}"
                )
            )
        else:
            self.lbl_msg.config(text="Procesando pago y preparando")


if __name__ == "__main__":
    app = CafeteriaApp()
    app.ventana.mainloop()