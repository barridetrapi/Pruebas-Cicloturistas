import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "CicloNorte Mobile"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # Base de datos en memoria (Marzo - Agosto)
    carreras = [
        {"nombre": "Occident Bilbao-Bilbao", "fecha": "2027-03-14", "comunidad": "País Vasco", "distancia": 115, "desnivel": 1200, "precio": 45.0, "participantes": 6000},
        {"nombre": "Itzulia Basque Challenge", "fecha": "2027-04-11", "comunidad": "País Vasco", "distancia": 138, "desnivel": 2500, "precio": 78.0, "participantes": 1000},
        {"nombre": "La Cantabrona", "fecha": "2027-05-08", "comunidad": "Cantabria", "distancia": 170, "desnivel": 3364, "precio": 62.0, "participantes": 2000},
        {"nombre": "Quebrantahuesos GF", "fecha": "2027-06-19", "comunidad": "Aragón", "distancia": 200, "desnivel": 3500, "precio": 98.0, "participantes": 11000},
    ]

    # Componentes de la interfaz
    lista_vista = ft.ListView(expand=1, spacing=10, padding=10)

    # FUNCIÓN SOLICITADA: Borrar registros individualmente
    def borrar_prueba(nombre_objetivo):
        for c in carreras:
            if c["nombre"] == nombre_objetivo:
                carreras.remove(c)
                break
        actualizar_lista()

    def actualizar_lista():
        lista_vista.controls.clear()
        # Ordenar estrictamente por fecha
        carreras_ordenadas = sorted(carreras, key=lambda x: x["fecha"])
        
        for c in carreras_ordenadas:
            lista_vista.controls.add(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(c["nombre"], weight=ft.FontWeight.BOLD, size=16, expand=True),
                                # Icono de papelera para borrar
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_600,
                                    on_click=lambda e, name=c["nombre"]: borrar_prueba(name)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"📅 {c['fecha']} | 📍 {c['comunidad']}", size=14, color=ft.Colors.GREY_700),
                            ft.Row([
                                ft.Text(f"📏 {c['distancia']} km"),
                                ft.Text(f"⛰️ +{c['desnivel']} m"),
                                ft.Text(f"💰 {c['precio']} €"),
                                ft.Text(f"👥 {c['participantes']}"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ])
                    )
                )
            )
        page.update()

    # FUNCIÓN SOLICITADA: Botón de actualización automática
    def actualizar_nuevas_pruebas(e):
        nuevas = [
            {"nombre": "Clásica Castro-Castro", "fecha": "2027-04-18", "comunidad": "Cantabria", "distancia": 99, "desnivel": 1200, "precio": 42.0, "participantes": 1200},
            {"nombre": "TotalEnergies Lagos de Covadonga", "fecha": "2027-06-05", "comunidad": "Asturias", "distancia": 111, "desnivel": 2340, "precio": 65.0, "participantes": 3000}
        ]
        contador = 0
        nombres_existentes = [c["nombre"] for c in carreras]
        for n in nuevas:
            if n["nombre"] not in nombres_existentes:
                carreras.append(n)
                contador += 1
        
        actualizar_lista()
        # Notificación en pantalla
        texto_aviso = f"¡Actualizado! +{contador} marchas." if contador > 0 else "Ya está actualizado."
        page.open(ft.SnackBar(ft.Text(texto_aviso)))
        page.update()

    # Formulario para añadir marchas manualmente
    input_nombre = ft.TextField(label="Nombre de la prueba")
    input_fecha = ft.TextField(label="Fecha (AAAA-MM-DD)", placeholder="Ej: 2027-04-15")
    input_comunidad = ft.Dropdown(
        label="Comunidad",
        options=[
            ft.dropdown.Option("País Vasco"), ft.dropdown.Option("Cantabria"),
            ft.dropdown.Option("Asturias"), ft.dropdown.Option("Galicia"),
            ft.dropdown.Option("Navarra"), ft.dropdown.Option("Aragón")
        ]
    )
    input_distancia = ft.TextField(label="Distancia (km)", keyboard_type=ft.KeyboardType.NUMBER)
    input_desnivel = ft.TextField(label="Desnivel (+m)", keyboard_type=ft.KeyboardType.NUMBER)
    input_precio = ft.TextField(label="Precio con Seguro (€)", keyboard_type=ft.KeyboardType.NUMBER)
    input_participantes = ft.TextField(label="Participantes", keyboard_type=ft.KeyboardType.NUMBER)

    def guardar_prueba(e):
        if input_nombre.value and input_fecha.value:
            carreras.append({
                "nombre": input_nombre.value,
                "fecha": input_fecha.value,
                "comunidad": input_comunidad.value if input_comunidad.value else "Norte",
                "distancia": int(input_distancia.value) if input_distancia.value else 0,
                "desnivel": int(input_desnivel.value) if input_desnivel.value else 0,
                "precio": float(input_precio.value) if input_precio.value else 0.0,
                "participantes": int(input_participantes.value) if input_participantes.value else 0
            })
            # Limpiar campos
            input_nombre.value = ""
            input_fecha.value = ""
            input_distancia.value = ""
            input_desnivel.value = ""
            input_precio.value = ""
            input_participantes.value = ""
            
            # Cierre seguro del diálogo
            dialogo_añadir.open = False
            actualizar_lista()

    # Ventana emergente (Modal) corregida para compatibilidad móvil
    dialogo_añadir = ft.AlertDialog(
        title=ft.Text("Añadir Prueba Manual"),
        content=ft.Column([
            input_nombre, input_fecha, input_comunidad, 
            ft.Row([input_distancia, input_desnivel]),
            ft.Row([input_precio, input_participantes])
        ], tight=True, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_añadir)),
            ft.ElevatedButton("Guardar", on_click=guardar_prueba)
        ]
    )

    # Botón flotante para abrir el formulario
    page.fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD, 
        on_click=lambda e: page.open(dialogo_añadir),
        bgcolor=ft.Colors.BLUE_600,
        content_color=ft.Colors.WHITE
    )

    # Barra superior con el botón de actualización sincronizado
    page.add(
        ft.AppBar(
            title=ft.Text("🚴‍♂️ CicloNorte Datos"), 
            bgcolor=ft.Colors.BLUE_600, 
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(ft.Icons.REFRESH, on_click=actualizar_nuevas_pruebas, tooltip="Actualizar")
            ]
        ),
        lista_vista
    )
    
    actualizar_lista()

# Comando limpio de ejecución final compatible con GitHub Actions
ft.app(target=main)
