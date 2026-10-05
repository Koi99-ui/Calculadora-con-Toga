# -*- coding: utf-8 -*-
"""
Calculadora simple (Toga)
-------------------------
Permite sumar, restar, multiplicar y dividir.
Controla la división entre cero y muestra el historial
de las últimas cinco operaciones.
Creado por Jhudith Romero - 2026
"""

from collections import deque

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER


class CalculadoraApp(toga.App):
    def startup(self):
        self.historial = deque(maxlen=5)  # últimas cinco operaciones
        self.operando = None              # primer número guardado
        self.operacion = None             # operación pendiente
        self.nuevo_numero = True          # indica si el próximo dígito inicia número

        # Título
        self.titulo = toga.Label(
            "Calculadora Simple",
            style=Pack(text_align=CENTER, font_size=18, font_weight="bold",
                       padding=10),
        )

        # Pantalla
        self.pantalla = toga.TextInput(
            value="0", readonly=True,
            style=Pack(padding=10, font_size=22),
        )

        # Teclado
        teclas = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "⌫", "%", "±"],
        ]
        self.filas_teclado = []
        for fila in teclas:
            botones = []
            for texto in fila:
                boton = toga.Button(
                    texto,
                    on_press=self.pulsar,
                    style=Pack(padding=5, flex=1, font_size=15),
                )
                boton.text = texto  # guarda el símbolo
                botones.append(boton)
            self.filas_teclado.append(botones)

        # Historial
        self.etiqueta_hist = toga.Label(
            "Historial (últimas 5 operaciones):",
            style=Pack(padding=(10, 5), font_weight="bold"),
        )
        self.lista_historial = toga.MultilineTextInput(
            readonly=True,
            style=Pack(padding=5, height=110),
        )

        # Pie de página
        self.pie = toga.Label(
            "Creado por Jhudith Romero - 2026",
            style=Pack(text_align=CENTER, padding=8, font_style="italic"),
        )

        # Contenedor principal
        caja = toga.Box(style=Pack(direction=COLUMN, padding=10))
        caja.add(self.titulo)
        caja.add(self.pantalla)
        for fila in self.filas_teclado:
            fila_box = toga.Box(style=Pack(direction=ROW))
            for boton in fila:
                fila_box.add(boton)
            caja.add(fila_box)
        caja.add(self.etiqueta_hist)
        caja.add(self.lista_historial)
        caja.add(self.pie)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = caja
        self.main_window.show()

    # --------------------------- Lógica ---------------------------
    def pulsar(self, widget):
        texto = widget.text

        if texto.isdigit():
            self.escribir_digito(texto)
        elif texto == ".":
            self.escribir_punto()
        elif texto == "C":
            self.limpiar()
        elif texto == "⌫":
            actual = self.pantalla.value
            self.pantalla.value = actual[:-1] if len(actual) > 1 else "0"
        elif texto == "%":
            self.pantalla.value = self.formatear(float(self.pantalla.value) / 100)
        elif texto == "±":
            valor = float(self.pantalla.value)
            self.pantalla.value = self.formatear(-valor)
        elif texto == "=":
            self.calcular()
        else:  # operadores
            self.guardar_operando(texto)

    def escribir_digito(self, digito):
        if self.nuevo_numero:
            self.pantalla.value = digito
            self.nuevo_numero = False
        else:
            actual = self.pantalla.value
            self.pantalla.value = digito if actual == "0" else actual + digito

    def escribir_punto(self):
        if self.nuevo_numero:
            self.pantalla.value = "0."
            self.nuevo_numero = False
        elif "." not in self.pantalla.value:
            self.pantalla.value = self.pantalla.value + "."

    def guardar_operando(self, simbolo):
        # Si ya hay operación pendiente, calcula primero (encadenar)
        if self.operacion is not None and not self.nuevo_numero:
            self.calcular()
        self.operando = float(self.pantalla.value)
        self.operacion = simbolo
        self.nuevo_numero = True

    def calcular(self):
        if self.operacion is None or self.operando is None:
            return
        try:
            b = float(self.pantalla.value)
        except ValueError:
            return

        a = self.operando
        if self.operacion == "+":
            resultado = a + b
        elif self.operacion == "-":
            resultado = a - b
        elif self.operacion == "×":
            resultado = a * b
        else:  # ÷
            if b == 0:
                self.pantalla.value = "0"
                self.ventana_error("Error: No se puede dividir entre cero.")
                self.limpiar()
                return
            resultado = a / b

        self.pantalla.value = self.formatear(resultado)
        self.historial.appendleft(
            f"{self.formatear(a)} {self.operacion} {self.formatear(b)} = {self.formatear(resultado)}"
        )
        self.lista_historial.value = "\n".join(self.historial)

        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    def ventana_error(self, mensaje):
        import asyncio
        async def mostrar():
            await self.main_window.error_dialog("Error", mensaje)
        try:
            asyncio.ensure_future(mostrar())
        except Exception:
            pass

    def limpiar(self):
        self.pantalla.value = "0"
        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    @staticmethod
    def formatear(valor):
        return str(int(valor)) if isinstance(valor, float) and valor == int(valor) else str(valor)


def main():
    return CalculadoraApp("Calculadora2", "org.jhudith.calculadora2")


if __name__ == "__main__":
    main().main_loop()
