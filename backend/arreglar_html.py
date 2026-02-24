import os

# Contenido HTML LIMPIO (Partículas pequeñas + Icono SVG + Sin errores de tildes)
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servicio Suspendido</title>
    <style>
        body, html { height: 100%; margin: 0; font-family: 'Segoe UI', sans-serif; background-color: #111827; overflow: hidden; }
        #particles-js { position: absolute; width: 100%; height: 100%; z-index: 1; }
        .container { position: relative; z-index: 2; display: flex; justify-content: center; align-items: center; height: 100%; padding: 20px; }
        .card { background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 20px; text-align: center; max-width: 420px; width: 100%; border-top: 6px solid #ef4444; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); }
        .icon-svg { width: 64px; height: 64px; color: #ef4444; margin-bottom: 20px; }
        h1 { color: #1f2937; margin-bottom: 15px; font-size: 28px; font-weight: 800; }
        p { color: #4b5563; margin-bottom: 25px; line-height: 1.6; font-size: 16px; }
        .btn { background: linear-gradient(to right, #2563eb, #4f46e5); color: white; padding: 15px 30px; text-decoration: none; border-radius: 12px; font-weight: bold; display: inline-block; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .footer { margin-top: 30px; color: #9ca3af; font-size: 14px; }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div class="container">
        <div class="card">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
            </svg>
            
            <h1>Servicio Suspendido</h1>
            <p>Estimado cliente, su servicio ha sido pausado por falta de pago.</p>
            <p>Realice su pago para restablecer la conexi&oacute;n inmediatamente.</p>
            
            <a href="https://wa.me/584241792456" class="btn">Reportar Pago al WhatsApp</a>
            <div class="footer">Kingsystem Solutions</div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
        /* Particulas ajustadas a tamaño 2 (pequeñas) */
        particlesJS("particles-js", {"particles":{"number":{"value":60},"color":{"value":"#ffffff"},"shape":{"type":"circle"},"opacity":{"value":0.5},"size":{"value":2},"line_linked":{"enable":true,"distance":150,"color":"#ffffff","opacity":0.4,"width":1},"move":{"enable":true,"speed":2}}});
    </script>
</body>
</html>"""

# Ruta correcta: Directamente en la carpeta templates que está aquí
file_path = os.path.join("templates", "suspended.html")

# Escribir el archivo forzando UTF-8
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Archivo REPARADO exitosamente en: {file_path}")
