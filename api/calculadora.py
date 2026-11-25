
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape


# Productos disponibles
PRODUCTOS = {
    "45000": "Sérum facial hidratante",
    "28000": "Labial mate larga duración",
    "65000": "Paleta de sombras"
}


# Código de descuento de ejemplo
CODIGO_DESCUENTO = "AURA10"
PORCENTAJE_DESCUENTO = 10


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        # 1. Recibir los datos del formulario
        longitud = int(self.headers.get("Content-Length", 0))
        datos = self.rfile.read(longitud).decode("utf-8")

        formulario = parse_qs(datos)

        precio = formulario.get("producto", [""])[0]
        cantidad = formulario.get("cantidad", ["0"])[0]
        descuento = formulario.get("descuento", [""])[0].strip().upper()

        # 2. Validar la información
        if precio not in PRODUCTOS:
            self.responder("Error: selecciona un producto válido.")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            self.responder("Error: ingresa una cantidad válida.")
            return

        if cantidad < 1:
            self.responder("Error: la cantidad debe ser mayor que cero.")
            return

        # 3. Calcular el pedido
        precio = int(precio)
        producto = PRODUCTOS[str(precio)]

        subtotal = precio * cantidad
        valor_descuento = 0

        # 4. Aplicar descuento si el código es correcto
        if descuento == CODIGO_DESCUENTO:
            valor_descuento = subtotal * PORCENTAJE_DESCUENTO / 100

        total = subtotal - valor_descuento

        # 5. Construir el resultado
        resultado = f"""
        <h1>Resumen de tu pedido</h1>

        <p><strong>Producto:</strong> {escape(producto)}</p>
        <p><strong>Cantidad:</strong> {cantidad}</p>
        <p><strong>Subtotal:</strong> ${subtotal:,.0f}</p>
        <p><strong>Descuento:</strong> ${valor_descuento:,.0f}</p>

        <h2>Total a pagar: ${total:,.0f}</h2>

        <p>¡Gracias por elegir Aura Belleza!</p>
        """

        self.responder(resultado)

    # 6. Enviar la respuesta al navegador
    def responder(self, contenido):

        pagina = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resultado de tu pedido - Aura Belleza</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #fff0f5;
                    padding: 30px;
                    text-align: center;
                }}

                .resultado {{
                    background: white;
                    max-width: 500px;
                    margin: 40px auto;
                    padding: 30px;
                    border-radius: 15px;
                }}

                h1, h2 {{
                    color: #b34f78;
                }}

                p {{
                    margin: 15px;
                }}

                a {{
                    display: inline-block;
                    background: #b34f78;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                }}
            </style>
        </head>

        <body>
            <div class="resultado">
                {contenido}

                <a href="/">Volver a la tienda</a>
            </div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(pagina.encode("utf-8"))
