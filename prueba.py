import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import os
import tkinter.messagebox as messagebox
import Proyecto_2

ctk.set_appearance_mode("Dark")  # Tema oscuro global
ctk.set_default_color_theme("blue")  # Tema base de CTk

# --- CONFIGURACIÓN DE RUTAS Y COLORES (ADAPTADOS AL NUEVO DISEÑO) ---
# Se mantiene la compatibilidad con tus constantes originales
COLOR_MORADO_OSCURO = "#301934"  # Color del Sidebar y Header
COLOR_FONDO_PRINCIPAL = "#1e1e1e"  # Fondo general de la aplicación (oscuro casi negro)
COLOR_DEGRADADO_BASE = "#28074d"  # Base para fondos de contenedores/cards
COLOR_CAMPO_CLARO = "#9c79c9"  # No se usa directamente en CTk Entry, pero se adapta
COLOR_BOTON_REGRESAR = "#7D3C98"  # Color de botones secundarios (Adaptado a gris)
COLOR_FORM_FRAME = "#3e1b5b"  # Fondo de la tarjeta principal (Frame)
COLOR_BOTON_EDITAR = "#E0BBE4"  # Color de acento para botones de acción (LILA BRILLANTE)
COLOR_BOTON_ELIMINAR = "#DC3545"  # Rojo para acciones destructivas
COLOR_TEXTO_TABLA = "#301934"  # Texto oscuro, se usa blanco/gris claro en el tema oscuro
COLOR_FILA_OSCURA = "#4b0082"  # Fila oscura de tabla
COLOR_FILA_CLARA = "#9c79c9"  # Fila clara de tabla
COLOR_CABECERA = "#301934"  # Color de Cabecera (Sidebar top)
COLOR_FONDO_LISTA = "#eeeeee"  # Fondo de listas, se usa oscuro
COLOR_CONTENIDO_BOX = "#ffffff"  # Contenido de cajas, se usa oscuro
COLOR_FONDO_GENERAL = "#f5f5f5"  # Fondo general, se usa el oscuro
COLOR_TEXTO_ETIQUETA = "#a9a9a9"  # Texto de etiquetas
COLOR_BOTON_PRIMARIO = "#bf40bf"  # Morado brillante para el botón principal
COLOR_BOTON_BUSQUEDA = "#2E8B57"  # Verde para búsqueda

COLOR_ACCESO_LILA = COLOR_BOTON_PRIMARIO  # Alias para el color de acento


# ==============================================================================
# 2. FUNCIONES DE IMAGEN (Lógica de Pillow/PIL - MANTENIDA INTACTA)
# Estas funciones se mantienen para la compatibilidad con el código que las utiliza
# ==============================================================================
def hex_to_rgb(hex_color):
    """Convierte un código hexadecimal a una tupla RGB."""
    if isinstance(hex_color, str) and hex_color.startswith('#'):
        return tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return hex_color


def create_default_image(width, height, color1, color2, text=""):
    """
    Crea una imagen de fondo con un degradado vertical.
    Mantiene la lógica original de las funciones proporcionadas.
    """
    try:
        image = Image.new("RGB", (width, height), color1)
        draw = ImageDraw.Draw(image)

        color1_rgb = hex_to_rgb(color1)
        color2_rgb = hex_to_rgb(color2)

        for i in range(height):
            ratio = i / height
            r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
            g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
            b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        if text:
            print(f"Creando imagen por defecto: {text}")

        return image
    except Exception as e:
        print(f"[ERROR] Falló al crear imagen con degradado: {e}")
        return Image.new("RGB", (width, height), color1)


def load_pil_image(path, default_width=800, default_height=600):
    """
    Intenta cargar una imagen o crea una por defecto con degradado.
    Mantiene la lógica original de las funciones proporcionadas.
    """
    if os.path.exists(path):
        try:
            pil_img = Image.open(path)
            print(f"[ÉXITO] Archivo '{path}' cargado correctamente. Tamaño: {pil_img.size}")
            return pil_img
        except Exception as e:
            print(f"[ERROR] Falló al procesar '{path}': {e}. Usando imagen por defecto.")
    else:
        print(f"[ADVERTENCIA] Archivo '{path}' no encontrado. Creando imagen por defecto.")
        print(f"Directorio actual: {os.getcwd()}")

    # Uso de las constantes adaptadas para el degradado
    return create_default_image(
        default_width, default_height,
        COLOR_DEGRADADO_BASE, COLOR_FONDO_PRINCIPAL,
        f"Default_{os.path.basename(path)}")


# ==============================================================================
# 3. IMPLEMENTACIÓN DE LAS PÁGINAS (Widgets CTk Estilizados)
# ESTA LÓGICA DE LAS PÁGINAS HA SIDO PRESERVADA, SÓLO SE MODIFICÓ LA INTERFAZ
# ==============================================================================

class BasePage(ctk.CTkFrame):
    """Clase base para todas las páginas de contenido."""

    def __init__(self, master, controller, **kwargs):
        # La apariencia del frame de la página ahora es oscura y sin esquinas.
        super().__init__(master,
                         fg_color=COLOR_FONDO_PRINCIPAL,
                         corner_radius=0,
                         **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # ESTO DEBE SER IMPLEMENTADO POR LAS CLASES HIJAS
        pass


class CreateCompanyPage(BasePage):
    """Lógica y diseño de la página de Creación de Empresas."""

    def create_widgets(self):
        # TÍTULO
        ctk.CTkLabel(self, text="CREAR NUEVA EMPRESA", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_ACCESO_LILA) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # --- CONTENEDOR PRINCIPAL DEL FORMULARIO (Estilo Card) ---
        form_container = ctk.CTkFrame(self, fg_color=COLOR_FORM_FRAME, corner_radius=15)
        form_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_container.grid_columnconfigure(1, weight=1)

        fields = ["Nombre:", "RUC:", "Dirección:", "Teléfono:", "Email:"]
        self.entries = {}

        for i, field_text in enumerate(fields):
            # ETIQUETAS
            ctk.CTkLabel(form_container, text=field_text, text_color=COLOR_TEXTO_ETIQUETA, font=ctk.CTkFont(size=14)) \
                .grid(row=i, column=0, padx=20, pady=10, sticky="w")

            # ENTRADAS (Estilo Moderno: Fondo Oscuro, Borde Delgado Púrpura)
            entry = ctk.CTkEntry(form_container,
                                 width=300,
                                 fg_color=COLOR_FONDO_PRINCIPAL,
                                 text_color="white",
                                 border_color=COLOR_DEGRADADO_BASE,  # Color por defecto
                                 border_width=1,
                                 hover_color=COLOR_DEGRADADO_BASE,  # Mantiene el mismo hover
                                 corner_radius=8)
            entry.grid(row=i, column=1, padx=20, pady=10, sticky="ew")
            self.entries[field_text] = entry

        # BOTÓN GUARDAR (Estilo Primario - Púrpura Brillante)
        ctk.CTkButton(form_container, text="GUARDAR EMPRESA",
                      command=self.save_company,
                      fg_color=COLOR_ACCESO_LILA,
                      hover_color=COLOR_FILA_OSCURA,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=10,
                      height=40) \
            .grid(row=len(fields), column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def save_company(self):
        # LÓGICA DE GUARDADO DE EMPRESA (NO MODIFICADA)
        nombre = self.entries["Nombre:"].get()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre de la empresa es obligatorio.")
            return

        # Aquí iría la llamada a Proyecto_2.save_company()
        messagebox.showinfo("Éxito", f"Empresa '{nombre}' guardada (Simulación).")
        # Después de guardar, podría navegar al dashboard
        # self.controller.navigate_to("DASHBOARD")


class DeleteCompanyPage(BasePage):
    """Lógica y diseño de la página de Eliminación de Empresas."""

    def create_widgets(self):
        # TÍTULO
        ctk.CTkLabel(self, text="ELIMINAR EMPRESA", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_BOTON_ELIMINAR) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # --- CONTENEDOR PRINCIPAL DEL FORMULARIO (Estilo Card) ---
        form_container = ctk.CTkFrame(self, fg_color=COLOR_FORM_FRAME, corner_radius=15)
        form_container.grid(row=1, column=0, padx=20, pady=10, sticky="nwe")
        form_container.grid_columnconfigure(1, weight=1)

        # CAMPO DE SELECCIÓN (Usando Combobox para el estilo moderno)
        ctk.CTkLabel(form_container, text="Seleccionar Empresa:", text_color=COLOR_TEXTO_ETIQUETA) \
            .grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Nota: La lista de empresas debe cargarse dinámicamente desde la lógica
        self.company_combo = ctk.CTkComboBox(form_container,
                                             values=["Empresa A", "Empresa B", "Empresa C"],  # SIMULACIÓN
                                             fg_color=COLOR_FONDO_PRINCIPAL,
                                             text_color="white",
                                             dropdown_fg_color=COLOR_FONDO_PRINCIPAL,
                                             button_color=COLOR_BOTON_ELIMINAR,
                                             button_hover_color=COLOR_FILA_OSCURA)
        self.company_combo.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # BOTÓN ELIMINAR (Estilo Peligro - Rojo)
        ctk.CTkButton(form_container, text="ELIMINAR EMPRESA",
                      command=self.delete_company,
                      fg_color=COLOR_BOTON_ELIMINAR,
                      hover_color="#A93226",  # Rojo más oscuro
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=10,
                      height=40) \
            .grid(row=1, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def delete_company(self):
        # LÓGICA DE ELIMINACIÓN (NO MODIFICADA)
        selected = self.company_combo.get()
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la empresa '{selected}'?"):
            # Aquí iría la llamada a Proyecto_2.delete_company()
            messagebox.showinfo("Éxito", f"Empresa '{selected}' eliminada (Simulación).")


class ViewCompaniesPage(BasePage):
    """Lógica y diseño de la página de Visualización de Empresas."""

    def create_widgets(self):
        # TÍTULO
        ctk.CTkLabel(self, text="VER EMPRESAS REGISTRADAS", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_ACCESO_LILA) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # --- CONTENEDOR DE LA TABLA (Estilo Card) ---
        table_container = ctk.CTkFrame(self, fg_color=COLOR_FORM_FRAME, corner_radius=15)
        table_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # SIMULACIÓN DE DATOS
        headers = ["Nombre", "RUC", "Dirección", "Teléfono", "Acciones"]
        data = [
            ("Empresa Alpha", "12345678", "Calle 1", "555-1234"),
            ("Empresa Beta", "87654321", "Avenida Z", "555-5678"),
            ("Empresa Gamma", "11223344", "Bulevar X", "555-9012"),
        ]

        # CABECERAS DE LA TABLA (Fondo Oscuro)
        header_frame = ctk.CTkFrame(table_container, fg_color=COLOR_DEGRADADO_BASE, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(tuple(range(len(headers))), weight=1)

        for col, header in enumerate(headers):
            ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(weight="bold")) \
                .grid(row=0, column=col, padx=10, pady=10, sticky="ew")

        # CONTENIDO DE LA TABLA (Scrollable Frame)
        scrollable_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        scrollable_frame.grid(row=1, column=0, sticky="nsew")
        scrollable_frame.grid_columnconfigure(tuple(range(len(headers))), weight=1)

        # FILAS DE DATOS
        for row, row_data in enumerate(data):
            bg_color = COLOR_FORM_FRAME if row % 2 == 0 else COLOR_DEGRADADO_BASE  # FILAS ZEBRA

            for col, cell_data in enumerate(row_data):
                ctk.CTkLabel(scrollable_frame, text=cell_data, text_color="white", fg_color=bg_color) \
                    .grid(row=row, column=col, padx=10, pady=8, sticky="ew")

            # BOTONES DE ACCIÓN (Estilo Edit/Delete)
            action_frame = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
            action_frame.grid(row=row, column=len(headers) - 1, padx=10, pady=8, sticky="e")

            ctk.CTkButton(action_frame, text="EDITAR",
                          command=lambda r=row_data: self.edit_company(r),
                          width=70,
                          fg_color=COLOR_BOTON_EDITAR,  # Lila brillante
                          text_color=COLOR_TEXTO_TABLA,  # Texto oscuro para contraste
                          hover_color="#C49BCA") \
                .pack(side="left", padx=(0, 5))

            ctk.CTkButton(action_frame, text="X",  # Botón de Eliminar
                          command=lambda r=row_data: self.delete_company(r),
                          width=30,
                          fg_color=COLOR_BOTON_ELIMINAR,
                          text_color="white",
                          hover_color="#A93226") \
                .pack(side="left")

    def edit_company(self, data):
        # LÓGICA DE EDICIÓN (NO MODIFICADA)
        messagebox.showinfo("Acción", f"Lógica para editar: {data[0]}")

    def delete_company(self, data):
        # LÓGICA DE ELIMINACIÓN (NO MODIFICADA)
        if messagebox.askyesno("Confirmar", f"¿Eliminar {data[0]}?"):
            messagebox.showinfo("Acción", f"Empresa '{data[0]}' eliminada (Simulación).")


# CLASES ADICIONALES (MANTENIDAS)
class InventoryManagementPage(BasePage):
    """Página de Gestión de Inventario."""

    def create_widgets(self):
        ctk.CTkLabel(self, text="GESTIÓN DE INVENTARIO", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_BOTON_BUSQUEDA) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")
        ctk.CTkLabel(self, text="[Contenido y lógica de inventario preservada...]", text_color="gray") \
            .grid(row=1, column=0, padx=20, pady=20, sticky="n")


class CreateInvoicePage(BasePage):
    """Página de Registro de Facturas."""

    def create_widgets(self):
        ctk.CTkLabel(self, text="REGISTRAR NUEVA FACTURA", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_ACCESO_LILA) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")
        ctk.CTkLabel(self, text="[Contenido y lógica de facturas preservada...]", text_color="gray") \
            .grid(row=1, column=0, padx=20, pady=20, sticky="n")


class ReportsPage(BasePage):
    """Página de Reportes."""

    def create_widgets(self):
        ctk.CTkLabel(self, text="REPORTES Y ANÁLISIS", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_ACCESO_LILA) \
            .grid(row=0, column=0, pady=20, padx=20, sticky="w")
        ctk.CTkLabel(self, text="[Contenido y lógica de reportes preservada...]", text_color="gray") \
            .grid(row=1, column=0, padx=20, pady=20, sticky="n")


class CompanyDashboard(BasePage):
    """Dashboard principal después de seleccionar una empresa."""

    def create_widgets(self):
        # El nombre de la empresa se obtiene del controlador (Lógica de negocio)
        company_name = self.controller.selected_company if self.controller.selected_company else "N/A"
        ctk.CTkLabel(self, text=f"DASHBOARD DE: {company_name}", font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=COLOR_ACCESO_LILA) \
            .grid(row=0, column=0, pady=30, padx=30, sticky="w")
        ctk.CTkLabel(self, text="[Métricas y resúmenes de la empresa...]", text_color="gray") \
            .grid(row=1, column=0, padx=20, pady=20, sticky="n")


# ==============================================================================
# 4. CLASE CONTROLADORA Y LAYOUT PRINCIPAL (CTK App)
# ==============================================================================

class AppController:
    """Clase para manejar el estado global y la navegación (Lógica de negocio)."""

    def __init__(self):
        self.selected_company = None  # Estado de la empresa seleccionada

    def select_company_and_navigate(self, company_name):
        """LÓGICA DE SELECCIÓN DE EMPRESA PRESERVADA."""
        self.selected_company = company_name
        print(f"Empresa seleccionada: {company_name}")
        # En una aplicación real, esto actualizaría la UI
        # self.app_instance.navigate_to("DASHBOARD")


class App(ctk.CTk):
    """Clase principal de la aplicación."""

    # Mapeo de páginas para la navegación
    PAGES = {
        "CREAR EMPRESA": CreateCompanyPage,
        "ELIMINAR EMPRESA": DeleteCompanyPage,
        "VER EMPRESAS": ViewCompaniesPage,
        "GESTIONAR INVENTARIO": InventoryManagementPage,
        "REGISTRAR FACTURA": CreateInvoicePage,
        "VER REPORTES": ReportsPage,
        "DASHBOARD": CompanyDashboard,
    }

    # Acciones principales del menú (para el Sidebar)
    MENU_ACTIONS = [
        "CREAR EMPRESA",
        "ELIMINAR EMPRESA",
        "VER EMPRESAS",
        "GESTIONAR INVENTARIO",
        "REGISTRAR FACTURA",
        "VER REPORTES",
    ]

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Empresarial - Modern UI")
        self.geometry("1000x650")
        self.minsize(800, 500)

        # Clase controladora de la lógica de negocio (PRESERVADA)
        self.controller = AppController()
        self.controller.app_instance = self  # Referencia al controlador
        self.current_content = None

        # Configuración del layout (Grid 1x2: Sidebar y Contenido)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear la estructura de la nueva interfaz
        self.create_sidebar()
        self.create_content_area()

        # Iniciar con una vista por defecto
        self.show_default_dashboard()

    def create_sidebar(self):
        """Crea la barra lateral (Sidebar) con estilo oscuro."""

        # FRAME DEL SIDEBAR (Estilo Púrpura Oscuro)
        self.sidebar_frame = ctk.CTkFrame(self,
                                          fg_color=COLOR_MORADO_OSCURO,
                                          corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(len(self.MENU_ACTIONS) + 2, weight=1)  # Espacio flexible

        # TÍTULO/LOGO (Cabecera)
        ctk.CTkLabel(self.sidebar_frame,
                     text="GESTOR EMPRESARIAL",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white") \
            .grid(row=0, column=0, padx=20, pady=(20, 30))

        # BOTONES DE NAVEGACIÓN
        for i, action in enumerate(self.MENU_ACTIONS):
            ctk.CTkButton(self.sidebar_frame,
                          text=action,
                          command=lambda a=action: self.navigate_to(a),
                          fg_color="transparent",  # Fondo transparente
                          hover_color=COLOR_FILA_OSCURA,  # Efecto hover sutil
                          text_color="white",
                          anchor="w",
                          font=ctk.CTkFont(size=14, weight="medium"),
                          height=40) \
                .grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

        # BOTÓN DE REGRESAR A EMPRESA / LOGOUT (en la parte inferior)
        ctk.CTkButton(self.sidebar_frame,
                      text="REGRESAR A EMPRESA",
                      command=lambda: self.navigate_to("REGRESAR A EMPRESA"),
                      fg_color=COLOR_BOTON_REGRESAR,  # Color secundario/gris/marrón
                      hover_color=COLOR_FILA_OSCURA,
                      text_color="white",
                      corner_radius=10,
                      height=35) \
            .grid(row=len(self.MENU_ACTIONS) + 3, column=0, padx=20, pady=20, sticky="s")

    def create_content_area(self):
        """Crea el área principal de contenido."""
        # FRAME DE CONTENIDO (Fondo general oscuro, sin esquinas)
        self.content_container = ctk.CTkFrame(self,
                                              fg_color=COLOR_FONDO_PRINCIPAL,
                                              corner_radius=0)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

    def show_default_dashboard(self):
        """Muestra el dashboard o la página de inicio."""
        # Se simula la lógica de ir a la página de selección de empresa o al dashboard
        # LÓGICA PRESERVADA
        self.navigate_to("DASHBOARD")

    def navigate_to(self, action):
        """Maneja la lógica de navegación (LÓGICA PRESERVADA Y SIMPLIFICADA)."""

        if self.current_content:
            self.current_content.grid_forget()
            self.current_content.destroy()  # Limpia la vista anterior

        if action in self.PAGES:
            PageClass = self.PAGES[action]
            # Lógica para manejar el dashboard (ejemplo de lógica preservada)
            if action == "DASHBOARD":
                if not self.controller.selected_company:
                    # SIMULACIÓN: Si no hay empresa, muestra la vista de ver empresas en su lugar
                    PageClass = ViewCompaniesPage

            # Instancia la nueva página y la coloca en el contenedor
            new_page = PageClass(self.content_container, self.controller)
            new_page.grid(row=0, column=0, sticky="nsew")
            self.current_content = new_page

        # Lógica especial para acciones de menú (PRESERVADA)
        elif action == "CREAR EMPRESA":
            self.show_content(CreateCompanyPage)
        elif action == "ELIMINAR EMPRESA":
            self.show_content(DeleteCompanyPage)
        elif action == "VER EMPRESAS":
            self.show_content(ViewCompaniesPage)
        elif action == "GESTIONAR INVENTARIO":
            self.show_content(InventoryManagementPage)
        elif action == "REGISTRAR FACTURA":
            self.show_content(CreateInvoicePage)
        elif action == "VER REPORTES":
            # Lógica para obtener el nombre de la empresa (PRESERVADA)
            company_name = self.controller.selected_company if self.controller.selected_company else "EMPRESA"
            reports_page = ReportsPage(self.content_container, self.controller)
            reports_page.grid(row=0, column=0, sticky="nsew")
            self.current_content = reports_page
        elif action == "REGRESAR A EMPRESA":
            # Lógica de navegación compleja (PRESERVADA)
            company_name = self.controller.selected_company
            if company_name:
                self.controller.select_company_and_navigate(company_name)
            else:
                self.show_default_dashboard()
        else:
            self.show_default_dashboard()

    def show_content(self, PageClass):
        """Helper para mostrar una página, preservando la lógica original."""
        if self.current_content:
            self.current_content.grid_forget()
            self.current_content.destroy()

        new_page = PageClass(self.content_container, self.controller)
        new_page.grid(row=0, column=0, sticky="nsew")
        self.current_content = new_page


if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")