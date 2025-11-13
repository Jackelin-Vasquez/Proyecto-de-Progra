import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import os
import tkinter.messagebox as messagebox
import Proyecto_2

# --- NUEVA CONFIGURACIÓN DE COLORES ---
PURPLE_DARK = "#4D148C"  # Morado Oscuro Intenso (Sidebar y Header)
PURPLE_BRIGHT = "#5E18B5"  # Morado del Formulario y botón de menú seleccionado
PURPLE_ENTRY = "#7D33CF"  # Morado de los campos de entrada
MAGENTA_SAVE = "#E83375"  # Botón GUARDAR (Rosa/Magenta)
TEXT_LIGHT_GRAY = "#D0D0D0"  # Gris muy claro para títulos
TEXT_DARK_GRAY = "#6C6C6C"  # Gris para textos de apoyo
BG_WHITE = "white"  # Fondo blanco puro

# Reemplazar las constantes anteriores con las nuevas
COLOR_MORADO_OSCURO = PURPLE_DARK
COLOR_FONDO_PRINCIPAL = BG_WHITE
COLOR_DEGRADADO_BASE = PURPLE_DARK
COLOR_CAMPO_CLARO = PURPLE_ENTRY
COLOR_BOTON_REGRESAR = "white"
COLOR_FORM_FRAME = PURPLE_BRIGHT
COLOR_BOTON_EDITAR = PURPLE_BRIGHT
COLOR_BOTON_ELIMINAR = MAGENTA_SAVE
COLOR_TEXTO_TABLA = "black"
COLOR_FILA_OSCURA = "#F0F0F0"
COLOR_FILA_CLARA = BG_WHITE
COLOR_CABECERA = PURPLE_DARK
COLOR_FONDO_LISTA = BG_WHITE
COLOR_CONTENIDO_BOX = BG_WHITE
COLOR_FONDO_GENERAL = BG_WHITE
COLOR_TEXTO_ETIQUETA = TEXT_DARK_GRAY
COLOR_BOTON_PRIMARIO = PURPLE_BRIGHT
COLOR_BOTON_BUSQUEDA = MAGENTA_SAVE

PATH_BG = "fondologincompe.png"
PATH_LOGO = "fondologincompe.png"
PATH_FROG = "fondologincompe.png.png"


def create_default_image(width, height, color1, color2, text=""):
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)

    def hex_to_rgb(hex_color):
        if isinstance(hex_color, str) and hex_color.startswith('#'):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        elif isinstance(hex_color, str) and hex_color.lower() == "white":
            return (255, 255, 255)
        elif isinstance(hex_color, str) and hex_color.lower() == "black":
            return (0, 0, 0)
        return hex_color

    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    # Asegurarse de que son tuplas de 3 elementos
    if not isinstance(color1_rgb, tuple) or len(color1_rgb) != 3:
        color1_rgb = (0, 0, 0)  # Negro por defecto
    if not isinstance(color2_rgb, tuple) or len(color2_rgb) != 3:
        color2_rgb = (255, 255, 255)  # Blanco por defecto

    for i in range(height):
        ratio = i / height
        r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
        g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
        b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    if text:
        print(f"Creando imagen por defecto: {text}")

    return image


def load_pil_image(path, default_width=800, default_height=600):
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

    return create_default_image(
        default_width, default_height,
        COLOR_DEGRADADO_BASE, COLOR_FONDO_PRINCIPAL,
        f"Default_{os.path.basename(path)}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        print(f"¿Existe PATH_BG ({PATH_BG})? {os.path.exists(PATH_BG)}")
        print(f"¿Existe PATH_LOGO ({PATH_LOGO})? {os.path.exists(PATH_LOGO)}")
        print(f"¿Existe PATH_FROG ({PATH_FROG})? {os.path.exists(PATH_FROG)}")
        print(f"Directorio actual: {os.getcwd()}")

        # Variables de usuario
        self.current_user = None
        self.user_role = None
        self.selected_company = None

        self.title("- Sistema de Gestión Contable")
        self.geometry("1200x800")
        self.minsize(1000, 600)

        # FORZAR FONDO BLANCO en toda la aplicación
        self.configure(fg_color=BG_WHITE)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color=BG_WHITE)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.original_bg_image = load_pil_image(PATH_BG, 1000, 700)
        self.original_logo_image = load_pil_image(PATH_LOGO, 50, 30)

        self.frames[LoginPage] = LoginPage(parent=container, controller=self,
                                           bg_image=self.original_bg_image, logo_image=self.original_logo_image)

        # DashboardPage se creará después de la autenticación
        self.frames[DashboardPage] = None

        self.pages = {
            LoginPage: LoginPage,
            DashboardPage: DashboardPage,
            CreateUserPage: CreateUserPage,
            ModifyUsersPage: ModifyUsersPage,
            DeleteUsersPage: DeleteUsersPage,
            CreateClientPage: CreateClientPage,
            CreateCompanyPage: CreateCompanyPage,
            ModifyCompanyPage: ModifyCompanyPage,
            DeleteCompanyPage: DeleteCompanyPage,
            ViewCompaniesPage: ViewCompaniesPage,
            CompanyHomePage: CompanyHomePage,
            InventoryManagementPage: InventoryManagementPage,
            CreateInvoicePage: CreateInvoicePage,
            ReportsPage: ReportsPage
        }

        self.show_frame(LoginPage)

        # Verificar y crear admin si no existe
        self.initialize_system()

    def initialize_system(self):
        """Inicializa el sistema y crea usuario admin si no existe"""
        try:
            # Verificar conexión y crear admin
            Proyecto_2.verificar_y_crear_admin()
            Proyecto_2.crear_usuario_admin()
            print("Sistema inicializado correctamente")
        except Exception as e:
            print(f"Error en inicialización: {e}")

    def show_frame(self, cont):
        if cont == DashboardPage and self.frames[cont] is None:
            # Crear DashboardPage solo cuando sea necesario y después de la autenticación
            self.frames[DashboardPage] = DashboardPage(parent=self.frames[LoginPage].master, controller=self)

        if cont in self.frames and self.frames[cont] is not None:
            frame = self.frames[cont]
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

    def authenticate_user(self, username, password):
        """Verifica las credenciales en la base de datos MySQL y almacena el rol"""
        try:
            resultado = Proyecto_2.inicio_sesion(username, password)

            if resultado == "salir":
                return False
            elif resultado:
                self.current_user = resultado
                self.user_role = resultado.get('rol', 'empleado')

                # Crear DashboardPage después de la autenticación
                self.frames[DashboardPage] = DashboardPage(parent=self.frames[LoginPage].master, controller=self)
                self.show_frame(DashboardPage)
                return True
            return False
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False

    def select_company_and_navigate(self, company_name):
        self.selected_company = company_name
        if self.frames[DashboardPage]:
            self.frames[CompanyHomePage] = CompanyHomePage(parent=self.frames[DashboardPage].content_container,
                                                           controller=self.frames[DashboardPage],
                                                           company_name=company_name)
            self.frames[DashboardPage].show_content(CompanyHomePage)

    def is_admin(self):
        """Verifica si el usuario actual es administrador"""
        return self.user_role and self.user_role.lower() in ['admin', 'administrador']


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller, bg_image, logo_image):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.original_bg_image = bg_image
        self.original_logo_image = logo_image

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.background_label = ctk.CTkLabel(self, text="")
        self.background_label.grid(row=0, column=0, sticky="nsew")

        self.setup_background()
        self._setup_header()

        self.login_frame = ctk.CTkFrame(
            self, width=350, height=350, corner_radius=15,
            fg_color="white", bg_color="transparent", border_width=0)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ctk.CTkLabel(self.login_frame, text="Inicio de Sesión",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_MORADO_OSCURO).pack(pady=(40, 30), padx=10)

        self.username_entry = ctk.CTkEntry(self.login_frame,
                                           placeholder_text="Usuario",
                                           width=250, height=40,
                                           corner_radius=10,
                                           fg_color="#f0f0f0",
                                           text_color="black",
                                           border_width=0)
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, "admin")

        self.password_entry = ctk.CTkEntry(self.login_frame,
                                           placeholder_text="Contraseña",
                                           show="•",
                                           width=250, height=40,
                                           corner_radius=10,
                                           fg_color="#f0f0f0",
                                           text_color="black",
                                           border_width=0)
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, "admin123")

        ctk.CTkButton(self.login_frame, text="Ingresar",
                      command=self.login_action,
                      width=200, height=40,
                      corner_radius=10,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#4B0082").pack(pady=(30, 20))

        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack()

        self.password_entry.bind("<Return>", lambda e: self.login_action())

    def setup_background(self):
        if self.original_bg_image:
            initial_width = self.winfo_width() if self.winfo_width() > 1 else 1000
            initial_height = self.winfo_height() if self.winfo_height() > 1 else 700

            self.ctk_bg_image = ctk.CTkImage(
                light_image=self.original_bg_image,
                dark_image=self.original_bg_image,
                size=(initial_width, initial_height))
            self.background_label.configure(image=self.ctk_bg_image)
        else:
            self.background_label.configure(fg_color=COLOR_MORADO_OSCURO)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if hasattr(self, 'original_bg_image') and self.original_bg_image:
            if event.width > 50 and event.height > 50:
                try:
                    original_width, original_height = self.original_bg_image.size
                    ratio = min(event.width / original_width, event.height / original_height)
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)

                    resized_bg = self.original_bg_image.resize((new_width, new_height), Image.LANCZOS)

                    self.ctk_bg_image = ctk.CTkImage(
                        light_image=resized_bg,
                        dark_image=resized_bg,
                        size=(new_width, new_height)
                    )
                    self.background_label.configure(image=self.ctk_bg_image)

                except Exception as e:
                    print(f"Error al redimensionar fondo: {e}")

    def _setup_header(self):
        ctk.CTkLabel(self, text="Oficina Contable SK",
                     font=ctk.CTkFont(size=16, weight="normal"),
                     text_color="white", bg_color="transparent").place(x=20, y=10)

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.controller.authenticate_user(username, password):
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.error_label.configure(text="")



class CreateUserPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        # Cambiar color de texto a NEGRO para el lado izquierdo (fuera del formulario)
        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Crear nuevo\nusuario",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="black",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text="Aquí puedes crear un nuevo usuario para el sistema.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=2, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="black",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Completa todos los campos requeridos.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=4, column=0, sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=35, corner_radius=10,
                      fg_color="white",
                      hover_color="#A948C9",
                      border_width=1,
                      border_color="gray",
                      text_color="black").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=150, pady=50)
        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        # Mantener BLANCO el título dentro del formulario morado
        ctk.CTkLabel(form_frame, text="Usuario",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        fields = [
            ("DPI", "text"),
            ("NOMBRE_COMPLETO", "text"),
            ("CORREO", "text"),
            ("PUESTO", "text"),
            ("USUARIO", "text"),
            ("CONTRASEÑA", "password"),
            ("ROL", "text")
        ]

        self.entries = {}
        for field, field_type in fields:
            # Mantener BLANCO las etiquetas dentro del formulario morado
            ctk.CTkLabel(form_frame, text=field.replace("_", " "),
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            if field_type == "password":
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40, show="•",
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")

            entry.pack(fill="x", padx=40)
            self.entries[field] = entry

        ctk.CTkButton(form_frame, text="CREAR\nUSUARIO",
                      command=self.create_user_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold"),
                      text_color="white").pack(pady=(30, 40))

    def create_user_action(self):
        dpi = self.entries["DPI"].get()
        nombre = self.entries["NOMBRE_COMPLETO"].get()
        correo = self.entries["CORREO"].get()
        puesto = self.entries["PUESTO"].get()
        usuario = self.entries["USUARIO"].get()
        contrasena = self.entries["CONTRASEÑA"].get()
        rol = self.entries["ROL"].get()

        if not all([dpi, nombre, usuario, contrasena, rol, correo, puesto]):
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
            return

        auditor = Proyecto_2.Auditor(nombre, dpi, correo, usuario, contrasena)
        success = auditor.crear_usuario(nombre, dpi, correo, puesto, usuario, contrasena, rol)

        if success:
            messagebox.showinfo("Éxito", f"Usuario {usuario} creado correctamente")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario")

class CreateClientPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Crear nuevo\ncliente",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="black",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text="Aquí puedes crear un nuevo cliente.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=2, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="black",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Solo NIT y Nombre son obligatorios.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black").grid(row=4, column=0, sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=35, corner_radius=10,
                      fg_color="white",
                      hover_color="#A948C9",
                      border_width=1,
                      border_color="gray",
                      text_color="black").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        ctk.CTkLabel(form_frame, text="Cliente",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        # Campos modificados - nombre_negocio ahora es opcional
        fields = [
            ("NIT *", "NIT"),
            ("NOMBRE *", "NOMBRE"),
            ("TELÉFONO", "TELEFONO"),
            ("CORREO", "CORREO"),
            ("DIRECCIÓN", "DIRECCION"),
            ("DPI", "DPI"),
            ("FECHA NACIMIENTO", "FECHA_NACIMIENTO"),
            ("NOMBRE NEGOCIO (Opcional)", "NOMBRE_NEGOCIO")  # Ahora es opcional
        ]

        self.entries = {}
        for field_label, field_key in fields:
            ctk.CTkLabel(form_frame, text=field_label,
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                 corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            entry.pack(fill="x", padx=40)
            self.entries[field_key] = entry

        # Agregar nota sobre campos obligatorios
        ctk.CTkLabel(form_frame, text="* Campos obligatorios",
                     font=ctk.CTkFont(size=10), text_color="yellow").pack(pady=(10, 0))

        ctk.CTkButton(form_frame, text="CREAR\nCLIENTE",
                      command=self.create_client_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def create_client_action(self):
        nit = self.entries["NIT"].get().strip()
        nombre = self.entries["NOMBRE"].get().strip()
        telefono = self.entries["TELEFONO"].get().strip()
        correo = self.entries["CORREO"].get().strip()
        direccion = self.entries["DIRECCION"].get().strip()
        dpi = self.entries["DPI"].get().strip()
        fecha_nacimiento = self.entries["FECHA_NACIMIENTO"].get().strip()
        nombre_negocio = self.entries["NOMBRE_NEGOCIO"].get().strip()

        # Solo validar campos obligatorios
        if not all([nit, nombre]):
            messagebox.showerror("Error", "Por favor complete los campos obligatorios: NIT y Nombre")
            return

        try:
            # Si nombre_negocio está vacío, se pasa como string vacío (será NULL en BD)
            nombre_negocio_value = nombre_negocio if nombre_negocio else ""

            cliente = Proyecto_2.Cliente(nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento,
                                         nombre_negocio_value)
            success = cliente.guardar()

            if success:
                messagebox.showinfo("Éxito", f"Cliente {nombre} creado correctamente")
                # Limpiar todos los campos
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo crear el cliente. Puede que el NIT ya exista.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")


class CreateCompanyPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_WHITE)
        self.controller = controller
        self.selected_client = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header morado
        self.title_header_frame = ctk.CTkFrame(self, fg_color=PURPLE_DARK, height=60, corner_radius=0)
        self.title_header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=0, pady=0)
        self.title_header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.title_header_frame, text="CREAR NUEVA EMPRESA",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="white")
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        main_container = ctk.CTkFrame(self, fg_color=BG_WHITE)
        main_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=14), text_color=TEXT_DARK_GRAY).grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Crear nueva\nempresa",
                     font=ctk.CTkFont(size=40, weight="bold"), text_color=TEXT_LIGHT_GRAY,
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text="Primero selecciona un cliente, luego crea la empresa.",
                     font=ctk.CTkFont(size=14), text_color=TEXT_DARK_GRAY).grid(row=2, column=0, sticky="nw")

        # Separador horizontal corto
        self.short_separator = ctk.CTkFrame(left_frame, width=50, height=2, fg_color=TEXT_DARK_GRAY)
        self.short_separator.grid(row=3, column=0, sticky="w", pady=(0, 20))

        ctk.CTkLabel(left_frame, text="La empresa se creará bajo el NIT del cliente seleccionado.",
                     font=ctk.CTkFont(size=14), text_color=TEXT_DARK_GRAY).grid(row=4, column=0, sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=35, corner_radius=10,
                      fg_color="white",
                      hover_color="#A948C9",
                      border_width=1,
                      border_color="gray",
                      text_color="black").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        # Frame para lista de clientes
        self.client_list_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=15,
                                                        fg_color=PURPLE_BRIGHT, width=400, height=300)
        self.client_list_frame.pack(expand=True, fill="both", pady=(0, 20))

        ctk.CTkLabel(self.client_list_frame, text="SELECCIONAR CLIENTE",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=(20, 15))

        self.client_list_container = ctk.CTkFrame(self.client_list_frame, fg_color="transparent")
        self.client_list_container.pack(fill="both", expand=True, padx=20)

        # Frame para formulario de empresa (inicialmente oculto)
        self.company_form_frame = ctk.CTkFrame(right_frame, corner_radius=15,
                                               fg_color=PURPLE_BRIGHT, width=400)

        self.load_clients()

    def load_clients(self):
        """Carga la lista de TODOS los clientes desde la base de datos"""
        try:
            # Limpiar lista anterior
            for widget in self.client_list_container.winfo_children():
                widget.destroy()

            auditor = Proyecto_2.Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "password")
            clientes = auditor.obtener_clientes_disponibles()

            if not clientes:
                ctk.CTkLabel(self.client_list_container,
                             text="No hay clientes disponibles\nCrea clientes primero",
                             font=ctk.CTkFont(size=14),
                             text_color="white").pack(pady=20)
                return

            for i, cliente in enumerate(clientes):
                client_frame = ctk.CTkFrame(self.client_list_container,
                                            fg_color=PURPLE_ENTRY,
                                            corner_radius=10)
                client_frame.pack(fill="x", pady=5, padx=10)

                # Mostrar información del cliente (nombre_negocio puede ser NULL)
                nombre_negocio = cliente['nombre_negocio'] if cliente['nombre_negocio'] else "Sin negocio registrado"
                client_info = f"{cliente['nombre']}\nNIT: {cliente['nit']}\nNegocio: {nombre_negocio}"

                ctk.CTkButton(client_frame,
                              text=client_info,
                              command=lambda c=cliente: self.select_client(c),
                              fg_color="transparent",
                              hover_color="#7D3C98",
                              font=ctk.CTkFont(size=12),
                              height=60,
                              anchor="w",
                              text_color="white").pack(fill="x", padx=10, pady=5)

        except Exception as e:
            ctk.CTkLabel(self.client_list_container,
                         text=f"Error al cargar clientes: {str(e)}",
                         font=ctk.CTkFont(size=14),
                         text_color="red").pack(pady=20)

    def select_client(self, cliente):
        """Selecciona un cliente y muestra el formulario de empresa"""
        self.selected_client = cliente

        # Ocultar lista de clientes
        self.client_list_frame.pack_forget()

        # Mostrar formulario de empresa
        self.show_company_form(cliente)

    def show_company_form(self, cliente):
        """Muestra el formulario para crear la empresa"""
        self.company_form_frame.pack(expand=True, fill="both", pady=(0, 20))

        ctk.CTkLabel(self.company_form_frame, text="CREAR EMPRESA",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(pady=(20, 10))

        nombre_negocio = cliente['nombre_negocio'] if cliente['nombre_negocio'] else "Sin negocio registrado"
        client_info = f"Cliente: {cliente['nombre']}\nNIT: {cliente['nit']}\nNegocio registrado: {nombre_negocio}"
        ctk.CTkLabel(self.company_form_frame, text=client_info,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="white").pack(pady=(0, 20))

        ctk.CTkLabel(self.company_form_frame, text="NOMBRE EMPRESA *",
                     font=ctk.CTkFont(size=12), text_color="white", anchor="w").pack(fill="x", padx=30,
                                                                                     pady=(15, 0))

        self.nombre_empresa_entry = ctk.CTkEntry(self.company_form_frame,
                                                 placeholder_text="Ingrese el nombre de la empresa", height=40,
                                                 corner_radius=10, fg_color=PURPLE_ENTRY, border_width=0,
                                                 text_color="white", placeholder_text_color="white")
        self.nombre_empresa_entry.pack(fill="x", padx=30, pady=(5, 15))

        ctk.CTkLabel(self.company_form_frame, text="DIRECCIÓN (Opcional)",
                     font=ctk.CTkFont(size=12), text_color="white", anchor="w").pack(fill="x", padx=30,
                                                                                     pady=(5, 0))

        self.direccion_entry = ctk.CTkEntry(self.company_form_frame, placeholder_text="Ingrese la dirección", height=40,
                                            corner_radius=10, fg_color=PURPLE_ENTRY, border_width=0,
                                            text_color="white", placeholder_text_color="white")
        self.direccion_entry.pack(fill="x", padx=30, pady=(5, 20))

        button_frame = ctk.CTkFrame(self.company_form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="CANCELAR",
                      command=self.back_to_client_list,
                      width=140, height=40, corner_radius=10,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black",
                      font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=(0, 10), sticky="w")

        ctk.CTkButton(button_frame, text="GUARDAR",
                      command=self.create_company_action,
                      width=140, height=40, corner_radius=10,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63",
                      font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=(10, 0), sticky="e")

    def back_to_client_list(self):
        """Vuelve a la lista de clientes"""
        self.company_form_frame.pack_forget()
        self.selected_client = None
        self.client_list_frame.pack(expand=True, fill="both", pady=(0, 20))

    def create_company_action(self):
        """Crea la empresa con el cliente seleccionado"""
        if not self.selected_client:
            messagebox.showerror("Error", "No hay cliente seleccionado")
            return

        nombre_empresa = self.nombre_empresa_entry.get().strip()
        direccion = self.direccion_entry.get().strip()

        if not nombre_empresa:
            messagebox.showerror("Error", "Por favor ingrese el nombre de la empresa")
            return

        try:
            auditor = Proyecto_2.Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "password")
            success = auditor.crear_empresa(nombre_empresa, self.selected_client['nit'], direccion)

            if success:
                messagebox.showinfo("Éxito",
                                    f"Empresa '{nombre_empresa}' creada correctamente para el cliente {self.selected_client['nombre']}")
                # Limpiar formulario y regresar a lista de clientes
                self.nombre_empresa_entry.delete(0, tk.END)
                self.direccion_entry.delete(0, tk.END)
                self.back_to_client_list()
            else:
                messagebox.showerror("Error",
                                     "No se pudo crear la empresa. Puede que ya exista una empresa con ese nombre.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la empresa: {str(e)}")


class TableBasePage(ctk.CTkFrame):
    def __init__(self, parent, controller, action_text, action_color, action_hover_color, action_command,
                 data_type="user", title_text=""):
        super().__init__(parent, fg_color=BG_WHITE)

        self.controller = controller
        self.action_text = action_text
        self.action_color = action_color
        self.action_hover_color = action_hover_color
        self.action_command = action_command
        self.data_type = data_type
        self.title_text = title_text

        # Variables para búsqueda y ordenamiento
        self.datos_originales = []
        self.datos_filtrados = []
        self.campo_busqueda = "Nombre"  # Campo por defecto para búsqueda
        self.metodo_ordenamiento = "bubble"  # Método por defecto

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header morado
        self.title_header_frame = ctk.CTkFrame(self, fg_color=PURPLE_DARK, height=60, corner_radius=0)
        self.title_header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=0, pady=0)
        self.title_header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.title_header_frame, text=title_text,
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="white")
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Cargar datos
        if data_type == "user":
            self.datos_originales = self._load_users_from_db()
        elif data_type == "company":
            self.datos_originales = self._load_companies_from_db()
        elif data_type == "inventory":
            self.datos_originales = self._load_inventory_from_db()

        self.datos_filtrados = self.datos_originales.copy()

        self._setup_top_bar()
        self._setup_table()

    def _load_users_from_db(self):
        """Carga usuarios reales desde la base de datos"""
        try:
            usuarios = Proyecto_2.Usuario.listar_todos()
            # Adaptar formato para la tabla
            formatted_users = []
            for usuario in usuarios:
                formatted_users.append({
                    "ID": usuario.get('id', ''),
                    "Nombre": usuario.get('nombre', ''),
                    "Usuario": usuario.get('usuario', ''),
                    "ROL": usuario.get('rol', ''),
                    "Puesto": usuario.get('puesto', '')
                })
            return formatted_users
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            return []

    def _load_companies_from_db(self):
        """Carga empresas reales desde la base de datos"""
        try:
            empresas = Proyecto_2.Empresa.listar()
            formatted_companies = []
            for empresa in empresas:
                formatted_companies.append({
                    "ID": empresa.get('id', ''),
                    "Nombre": empresa.get('nombre', ''),
                    "NIT": empresa.get('nit_cliente', ''),
                    "DIRECCIÓN": empresa.get('direccion', '')
                })
            return formatted_companies
        except Exception as e:
            print(f"Error cargando empresas: {e}")
            return []

    def _load_inventory_from_db(self):
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                return []

            inventario = Proyecto_2.Inventario.listar(empresa_nombre)
            formatted_inventory = []
            for item in inventario:
                formatted_inventory.append({
                    "ID_Producto": item.get('id', ''),
                    "Nombre": item.get('producto', ''),
                    "Cantidad": item.get('cantidad', 0),
                    "Precio": item.get('precio', 0)
                })
            return formatted_inventory
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            return []

    def _get_data(self):
        return self.datos_filtrados

    def _get_columns(self):
        if self.data_type == "company":
            return ["ID", "Nombre", "NIT", "DIRECCIÓN", "Acción"]
        elif self.data_type == "inventory":
            return ["PRODUCTO", "CANTIDAD", "PRECIO", "Acción"]
        return ["ID", "Nombre", "Usuario", "ROL", "Acción"]

    def _setup_top_bar(self):
        top_bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_bar_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(40, 20))
        top_bar_frame.grid_columnconfigure(1, weight=1)

        # Botón de ordenamiento con dropdown
        self.ordenar_btn = ctk.CTkButton(top_bar_frame, text="Ordenar ▾",
                                         width=120, height=45, corner_radius=25,
                                         fg_color=PURPLE_BRIGHT,
                                         hover_color="#6A5ACD",
                                         text_color="white",
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         command=self._mostrar_opciones_ordenamiento)
        self.ordenar_btn.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # Campo de búsqueda
        self.buscar_entry = ctk.CTkEntry(top_bar_frame, placeholder_text="Buscar...",
                                         width=400, height=45, corner_radius=25,
                                         fg_color="white", text_color="black",
                                         font=ctk.CTkFont(size=14))
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=15)
        self.buscar_entry.bind("<KeyRelease>", self._realizar_busqueda)

        # Botón de búsqueda avanzada
        ctk.CTkButton(top_bar_frame, text="Buscar",
                      command=self._buscar_avanzada,
                      width=100, height=45, corner_radius=25,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63",
                      font=ctk.CTkFont(size=14, weight="bold")
                      ).grid(row=0, column=2, padx=(15, 0), sticky="e")

        ctk.CTkButton(top_bar_frame, text="Regresar",
                      command=lambda: self._handle_back_action(),
                      width=100, height=45, corner_radius=25,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black",
                      font=ctk.CTkFont(size=14, weight="bold")
                      ).grid(row=0, column=3, padx=(15, 0), sticky="e")

    def _mostrar_opciones_ordenamiento(self):
        menu = tk.Menu(self, tearoff=0)

        # Métodos de ordenamiento
        menu.add_command(label="Burbuja", command=lambda: self._aplicar_ordenamiento("bubble"))
        menu.add_command(label="Quick Sort", command=lambda: self._aplicar_ordenamiento("quick"))
        menu.add_command(label="Selección", command=lambda: self._aplicar_ordenamiento("selection"))

        menu.add_separator()

        # Campos para ordenar
        if self.data_type == "user":
            menu.add_command(label="Por Nombre", command=lambda: self._ordenar_por_campo("Nombre"))
            menu.add_command(label="Por Usuario", command=lambda: self._ordenar_por_campo("Usuario"))
            menu.add_command(label="Por Rol", command=lambda: self._ordenar_por_campo("ROL"))
        elif self.data_type == "company":
            menu.add_command(label="Por Nombre", command=lambda: self._ordenar_por_campo("Nombre"))
            menu.add_command(label="Por NIT", command=lambda: self._ordenar_por_campo("NIT"))
        elif self.data_type == "inventory":
            menu.add_command(label="Por Producto", command=lambda: self._ordenar_por_campo("Nombre"))
            menu.add_command(label="Por Cantidad", command=lambda: self._ordenar_por_campo("Cantidad"))
            menu.add_command(label="Por Precio", command=lambda: self._ordenar_por_campo("Precio"))

        # Mostrar menú cerca del botón
        try:
            menu.tk_popup(self.ordenar_btn.winfo_rootx(),
                          self.ordenar_btn.winfo_rooty() + self.ordenar_btn.winfo_height())
        finally:
            menu.grab_release()

    def _ordenar_por_campo(self, campo):
        """Ordena por un campo específico usando el método actual CORREGIDO"""
        self.campo_busqueda = campo

        # Mapear nombres de campos de visualización a campos de datos reales
        campo_mapeo = self._mapear_campo_ordenamiento(campo)
        self.campo_busqueda = campo_mapeo

        self._aplicar_ordenamiento(self.metodo_ordenamiento)

    def _mapear_campo_ordenamiento(self, campo_visual):
        """Mapea nombres de columnas de tabla a campos reales en los datos"""
        mapeo = {
            # Para usuarios
            "Nombre": "Nombre",
            "Usuario": "Usuario",
            "ROL": "ROL",
            "Puesto": "Puesto",
            # Para empresas
            "Nombre": "Nombre",
            "NIT": "NIT",
            "DIRECCIÓN": "DIRECCIÓN",
            # Para inventario
            "PRODUCTO": "Nombre",
            "Cantidad": "Cantidad",
            "Precio": "Precio"
        }
        return mapeo.get(campo_visual, "Nombre")

    def _adaptar_datos_para_ordenamiento(self, datos, campo_ordenar):
        """Convierte lista de diccionarios a lista de tuplas para ordenamiento"""
        datos_adaptados = []
        for item in datos:
            valor_ordenar = item.get(campo_ordenar, '')
            # Para ordenamiento numérico si el campo es Cantidad o Precio
            if campo_ordenar in ["Cantidad", "Precio"]:
                try:
                    valor_ordenar = float(valor_ordenar) if valor_ordenar else 0.0
                except ValueError:
                    valor_ordenar = 0.0
            datos_adaptados.append((valor_ordenar, item))
        return datos_adaptados

    def _aplicar_ordenamiento(self, metodo):
        """Aplica el método de ordenamiento seleccionado CORREGIDO"""
        self.metodo_ordenamiento = metodo
        self.ordenar_btn.configure(text=f"Ordenar ({metodo}) ▾")

        if not self.datos_filtrados:
            return

        # Adaptar datos para ordenamiento
        datos_para_ordenar = self._adaptar_datos_para_ordenamiento(
            self.datos_filtrados, self.campo_busqueda
        )

        # Aplicar ordenamiento usando los métodos de Proyecto_2
        # Los métodos ahora reciben lista de tuplas (valor, diccionario)
        if metodo == "bubble":
            resultados = Proyecto_2.metodo_bubble_sort(datos_para_ordenar, 0)  # Índice 0 = valor
        elif metodo == "quick":
            resultados = Proyecto_2.metodo_quick_sort(datos_para_ordenar, 0)
        elif metodo == "selection":
            resultados = Proyecto_2.metodo_selection_sort(datos_para_ordenar, 0)
        else:
            resultados = datos_para_ordenar

        #  CORREGIDO: Extraer solo los diccionarios originales en orden
        self.datos_filtrados = [item[1] for item in resultados]

        self._actualizar_tabla()


    def _adaptar_busqueda_binaria(self, lista, campo, valor):
        if not lista:
            return -1

        # Convertir la lista a una lista de valores del campo específico
        lista_valores = [(i, str(item.get(campo, '')).lower()) for i, item in enumerate(lista)]
        lista_ordenada = sorted(lista_valores, key=lambda x: x[1])

        # Realizar búsqueda binaria
        resultado = Proyecto_2.busqueda_binaria([x[1] for x in lista_ordenada], 0, str(valor).lower())

        if resultado != -1:
            # Encontrar el índice original
            for i, (idx, val) in enumerate(lista_ordenada):
                if val == resultado:
                    return lista[idx]
        return -1

    def _adaptar_busqueda_secuencial(self, lista, campo, valor):
        """Adapta la búsqueda secuencial para trabajar con diccionarios"""
        if not lista:
            return -1

        valor_busqueda = str(valor).lower()
        resultados = []

        for item in lista:
            valor_item = str(item.get(campo, '')).lower()
            if valor_busqueda in valor_item:
                resultados.append(item)

        return resultados if resultados else -1

    def _realizar_busqueda(self, event=None):
        """Búsqueda en tiempo real"""
        texto_busqueda = self.buscar_entry.get().strip()

        if not texto_busqueda:
            self.datos_filtrados = self.datos_originales.copy()
            self._actualizar_tabla()
            return

        # Usar búsqueda secuencial adaptada para diccionarios
        resultados = self._adaptar_busqueda_secuencial(self.datos_originales, self.campo_busqueda, texto_busqueda)

        if resultados == -1:
            self.datos_filtrados = []
        else:
            self.datos_filtrados = resultados

        self._actualizar_tabla()

    def _buscar_avanzada(self):
        """Búsqueda avanzada con selección de método"""
        texto_busqueda = self.buscar_entry.get().strip()

        if not texto_busqueda:
            messagebox.showinfo("Búsqueda", "Ingrese un término de búsqueda")
            return
        dialog = BusquedaAvanzadaDialog(self, self.data_type)
        self.wait_window(dialog)

        if dialog.metodo_seleccionado and dialog.campo_seleccionado:
            self.campo_busqueda = dialog.campo_seleccionado

            if dialog.metodo_seleccionado == "secuencial":
                resultados = self._adaptar_busqueda_secuencial(self.datos_originales, self.campo_busqueda,
                                                               texto_busqueda)
            else:  # binaria
                resultado_binario = self._adaptar_busqueda_binaria(self.datos_originales, self.campo_busqueda,
                                                                   texto_busqueda)
                resultados = [resultado_binario] if resultado_binario != -1 else []

            if not resultados or resultados == -1:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados")
                self.datos_filtrados = []
            else:
                self.datos_filtrados = resultados
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} resultado(s)")

            self._actualizar_tabla()

    def _actualizar_tabla(self):
        # Limpiar tabla actual
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) == 2:
                widget.destroy()
        # Recrear la tabla
        self._setup_table()

    def _handle_back_action(self):
        if self.data_type == "inventory":
            if self.controller.controller.selected_company:
                company_name = self.controller.controller.selected_company
                self.controller.controller.select_company_and_navigate(company_name)
            else:
                self.controller.show_default_dashboard()
        else:
            self.controller.show_default_dashboard()

    def _setup_table(self):
        table_container = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        table_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        data = self._get_data()
        cols = self._get_columns()

        num_cols = len(cols)
        for i in range(num_cols):
            table_container.grid_columnconfigure(i, weight=1 if i < num_cols - 1 else 1)

        header_font = ctk.CTkFont(size=16, weight="bold")
        for i, col_name in enumerate(cols):
            header_cell = ctk.CTkLabel(table_container, text=col_name.upper(),
                                       fg_color=PURPLE_DARK, text_color="white", font=header_font, height=50,
                                       corner_radius=0)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

        row_font = ctk.CTkFont(size=14)
        if self.data_type == "user":
            display_keys = ["Nombre", "Usuario", "ROL"]
            id_key = "ID"
        elif self.data_type == "company":
            display_keys = ["Nombre", "NIT", "DIRECCIÓN"]
            id_key = "ID"
        elif self.data_type == "inventory":
            display_keys = ["Cantidad", "Precio"]
            id_key = "Nombre"
        else:
            display_keys = []
            id_key = ""

        for r, item in enumerate(data):
            row_index = r + 1
            bg_color = COLOR_FILA_CLARA if r % 2 == 0 else COLOR_FILA_OSCURA
            text_color = COLOR_TEXTO_TABLA

            ctk.CTkLabel(table_container, text=item[id_key], fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=0,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))
            current_col = 1
            for key in display_keys:
                value = item.get(key)
                if key == "Precio":
                    display_value = f"Q {float(value):.2f}" if value else "Q 0.00"
                else:
                    display_value = str(value) if value else ""
                cell = ctk.CTkLabel(table_container, text=display_value, fg_color=bg_color, text_color=text_color,
                                    font=row_font, height=60, corner_radius=0, anchor="w", padx=15)
                cell.grid(row=row_index, column=current_col, sticky="nsew", padx=(1, 1), pady=(1, 1))
                current_col += 1

            action_col_idx = num_cols - 1
            edit_button_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            edit_button_frame.grid(row=row_index, column=action_col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))
            edit_button_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(edit_button_frame, text=self.action_text,
                          command=lambda u=item: self.action_command(u),
                          width=80, height=35, corner_radius=10,
                          fg_color=self.action_color,
                          hover_color=self.action_hover_color,
                          text_color="white",
                          font=ctk.CTkFont(size=14, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class BusquedaAvanzadaDialog(ctk.CTkToplevel):
    def __init__(self, parent, data_type):
        super().__init__(parent)
        self.title("Búsqueda Avanzada")
        self.geometry("500x500")
        self.resizable(False, False)

        self.metodo_seleccionado = None
        self.campo_seleccionado = None

        main_frame = ctk.CTkFrame(self, fg_color=PURPLE_BRIGHT, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="BÚSQUEDA AVANZADA", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white").pack(pady=(15, 20))

        ctk.CTkLabel(main_frame, text="Método de búsqueda:",
                     font=ctk.CTkFont(size=12), text_color="white").pack(anchor="w", padx=20)

        self.metodo_var = tk.StringVar(value="secuencial")
        ctk.CTkRadioButton(main_frame, text="Búsqueda Secuencial",
                           variable=self.metodo_var, value="secuencial",
                           text_color="white").pack(anchor="w", padx=30, pady=5)
        ctk.CTkRadioButton(main_frame, text="Búsqueda Binaria",
                           variable=self.metodo_var, value="binaria",
                           text_color="white").pack(anchor="w", padx=30, pady=5)
        ctk.CTkLabel(main_frame, text="Campo de búsqueda:",
                     font=ctk.CTkFont(size=12), text_color="white").pack(anchor="w", padx=20, pady=(10, 0))

        if data_type == "user":
            campos = ["Nombre", "Usuario", "ROL", "Puesto"]
        elif data_type == "company":
            campos = ["Nombre", "NIT", "DIRECCIÓN"]
        elif data_type == "inventory":
            campos = ["Nombre", "Cantidad", "Precio"]
        else:
            campos = ["Nombre"]

        self.campo_combobox = ctk.CTkComboBox(main_frame, values=campos, state="readonly",
                                              fg_color=PURPLE_ENTRY, text_color="white")
        self.campo_combobox.pack(fill="x", padx=20, pady=5)
        self.campo_combobox.set(campos[0])
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=15)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy,
                      width=100, height=35, corner_radius=10,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black").grid(row=0, column=0, padx=(0, 10), sticky="w")

        ctk.CTkButton(button_frame, text="Aplicar", command=self.aplicar_busqueda,
                      width=100, height=35, corner_radius=10,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63").grid(row=0, column=1, padx=(10, 0), sticky="e")

    def aplicar_busqueda(self):
        self.metodo_seleccionado = self.metodo_var.get()
        self.campo_seleccionado = self.campo_combobox.get()
        self.destroy()


class ModifyUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Editar",
            action_color=PURPLE_BRIGHT,
            action_hover_color="#6A5ACD",
            action_command=self.edit_user_action,
            data_type="user",
            title_text="MODIFICAR USUARIOS"
        )

    def edit_user_action(self, user):
        print(f"Editando usuario: ID={user['ID']}, Nombre={user['Nombre']}")

        # Crear y mostrar diálogo de edición
        dialog = EditUserDialog(self, user)
        self.wait_window(dialog)

        if dialog.result:
            # Recargar la tabla para reflejar cambios
            self.datos_originales = self._load_users_from_db()
            self.datos_filtrados = self.datos_originales.copy()
            self._actualizar_tabla()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
class EditUserDialog(ctk.CTkToplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.title("Editar Usuario")
        self.geometry("450x500")
        self.resizable(False, True)

        # Hacer que la ventana se abra por delante
        self.lift()  # Traer al frente
        self.focus_force()  # Forzar el foco
        self.grab_set()  # Hacerla modal (capturar todos los eventos)

        self.user_data = user_data
        self.result = None

        # Frame principal con scroll
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame scrollable
        self.scrollable_frame = ctk.CTkScrollableFrame(main_container, fg_color=PURPLE_BRIGHT, corner_radius=15)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.scrollable_frame, text="EDITAR USUARIO",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(20, 30))

        # Campos de edición
        fields = [
            ("DPI", "DPI"),
            ("NOMBRE COMPLETO", "NOMBRE_COMPLETO"),
            ("CORREO", "CORREO"),
            ("PUESTO", "PUESTO"),
            ("USUARIO", "USUARIO"),
            ("CONTRASEÑA", "CONTRASEÑA"),
            ("ROL", "ROL")
        ]

        self.entries = {}
        for field_label, field_key in fields:
            # Frame para cada campo
            field_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            field_frame.pack(fill="x", padx=40, pady=(5, 0))

            ctk.CTkLabel(field_frame, text=field_label,
                         font=ctk.CTkFont(size=12, weight="normal"),
                         text_color="white", anchor="w").pack(fill="x", pady=(0, 5))

            entry = ctk.CTkEntry(field_frame, placeholder_text="", height=35,
                                 corner_radius=10, fg_color=PURPLE_ENTRY,
                                 border_width=0, text_color="white",
                                 placeholder_text_color="white")
            entry.pack(fill="x", pady=(0, 10))
            self.entries[field_key] = entry

        # Cargar datos actuales del usuario
        self._load_current_user_data()

        # Frame para botones (fuera del scrollable frame para que sean siempre visibles)
        button_container = ctk.CTkFrame(main_container, fg_color="transparent")
        button_container.pack(fill="x", padx=20, pady=(10, 5))

        button_frame = ctk.CTkFrame(button_container, fg_color="transparent")
        button_frame.pack(fill="x")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy,
                      width=120, height=40, corner_radius=10,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black").grid(row=0, column=0, padx=(0, 10), sticky="w")

        ctk.CTkButton(button_frame, text="Guardar Cambios",
                      command=self.save_changes,
                      width=120, height=40, corner_radius=10,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63").grid(row=0, column=1, padx=(10, 0), sticky="e")

        # Ajustar el tamaño mínimo para mejor visualización
        self.minsize(450, 400)

        # Asegurar que esté al frente después de que todos los widgets estén creados
        self.after(100, self._ensure_front)

    def _ensure_front(self):
        """Asegura que la ventana esté al frente"""
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

    def _load_current_user_data(self):
        """Carga los datos actuales del usuario en los campos"""
        # Mapeo de campos del formulario a campos de la base de datos
        field_mapping = {
            'dpi': 'dpi',
            'nombre': 'nombre',
            'correo': 'correo',
            'puesto': 'puesto',
            'usuario': 'usuario',
            'rol': 'rol'
        }

        for field_key, data_key in field_mapping.items():
            if data_key in self.user_data:
                # Insertar el valor actual en el campo
                current_value = str(self.user_data[data_key]) if self.user_data[data_key] else ""
                self.entries[field_key].insert(0, current_value)

        # Para el campo de contraseña, dejarlo vacío por seguridad
        self.entries["CONTRASEÑA"].insert(0, "")
        # Agregar placeholder para indicar que es opcional
        self.entries["CONTRASEÑA"].configure(placeholder_text="Dejar vacío para mantener actual")

    def save_changes(self):
        """Guarda los cambios del usuario en la base de datos llamando al método correspondiente"""
        try:
            # Obtener datos de los campos
            dpi = self.entries["DPI"].get().strip()
            nombre = self.entries["NOMBRE_COMPLETO"].get().strip()
            correo = self.entries["CORREO"].get().strip()
            puesto = self.entries["PUESTO"].get().strip()
            usuario = self.entries["USUARIO"].get().strip()
            contrasena = self.entries["CONTRASEÑA"].get().strip()
            rol = self.entries["ROL"].get().strip()

            # Validar campos obligatorios
            if not all([dpi, nombre, usuario, rol]):
                messagebox.showerror("Error", "Por favor complete los campos obligatorios: DPI, Nombre, Usuario y Rol")
                return

            # Validar formato de correo
            if correo and "@" not in correo:
                messagebox.showerror("Error", "Por favor ingrese un correo electrónico válido")
                return

            # Obtener el usuario actual para la actualización
            usuario_actual = self.user_data.get('usuario') or self.user_data.get('USUARIO') or self.user_data.get(
                'Usuario')
            if not usuario_actual:
                messagebox.showerror("Error",
                                     f"No se pudo identificar el usuario a actualizar. Datos: {self.user_data}")
                return

            print(f"Actualizando usuario: {usuario_actual} -> {usuario}")  # Debug

            # Llamar al método de actualización de la clase Usuario
            success = Proyecto_2.Usuario.actualizar_usuario(
                usuario_actual=usuario_actual,
                nuevo_dpi=dpi,
                nuevo_nombre=nombre,
                nuevo_correo=correo,
                nuevo_puesto=puesto,
                nuevo_usuario=usuario,
                nueva_contrasena=contrasena if contrasena else None,  # Si no hay nueva contraseña, mantener la actual
                nuevo_rol=rol
            )

            if success:
                messagebox.showinfo("Éxito", f"Usuario {usuario} actualizado correctamente")
                self.result = {
                    'dpi': dpi,
                    'nombre': nombre,
                    'correo': correo,
                    'puesto': puesto,
                    'usuario': usuario,
                    'rol': rol
                }
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario. Verifique los datos.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class EditCompanyDialog(ctk.CTkToplevel):
    def __init__(self, parent, company_data):
        super().__init__(parent)
        self.title("Editar Empresa")
        self.geometry("500x600")
        self.resizable(False, False)

        self.company_data = company_data
        self.result = None

        main_frame = ctk.CTkFrame(self, fg_color=PURPLE_BRIGHT, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="EDITAR EMPRESA", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(20, 30))
        # Campos de edición
        fields = [
            ("NOMBRE EMPRESA", "NOMBRE"),
            ("NIT CLIENTE", "NIT"),
            ("DIRECCIÓN", "DIRECCION")]

        self.entries = {}
        for field_label, field_key in fields:
            ctk.CTkLabel(main_frame, text=field_label,
                         font=ctk.CTkFont(size=12, weight="normal"),
                         text_color="white", anchor="w").pack(fill="x", padx=40, pady=(10, 0))

            entry = ctk.CTkEntry(main_frame, placeholder_text="", height=35,
                                 corner_radius=10, fg_color=PURPLE_ENTRY,
                                 border_width=0, text_color="white", placeholder_text_color="white")
            entry.pack(fill="x", padx=40, pady=(5, 10))
            self.entries[field_key] = entry

        # Cargar datos actuales de la empresa
        self._load_current_company_data()

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy,
                      width=120, height=40, corner_radius=10,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black").grid(row=0, column=0, padx=(0, 10), sticky="w")

        ctk.CTkButton(button_frame, text="Guardar Cambios",
                      command=self.save_changes,
                      width=120, height=40, corner_radius=10,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63").grid(row=0, column=1, padx=(10, 0), sticky="e")

    def _load_current_company_data(self):
        """Carga los datos actuales de la empresa en los campos"""
        field_mapping = {
            'NOMBRE': 'Nombre',
            'NIT': 'NIT',
            'DIRECCION': 'DIRECCIÓN'
        }

        for field_key, table_key in field_mapping.items():
            if table_key in self.company_data:
                self.entries[field_key].insert(0, str(self.company_data[table_key]))

    def save_changes(self):
        """Guarda los cambios de la empresa"""
        try:
            nombre = self.entries["NOMBRE"].get().strip()
            nit = self.entries["NIT"].get().strip()
            direccion = self.entries["DIRECCION"].get().strip()

            if not all([nombre, nit]):
                messagebox.showerror("Error", "Por favor complete los campos obligatorios: Nombre y NIT")
                return

            nombre_actual = self.company_data['Nombre']

            # Llamar al método de actualización
            success = Proyecto_2.Empresa.actualizar_empresa(
                nombre_actual, nombre, nit, direccion
            )

            if success:
                messagebox.showinfo("Éxito", f"Empresa {nombre} actualizada correctamente")
                self.result = {
                    'nombre': nombre,
                    'nit': nit,
                    'direccion': direccion
                }
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la empresa. Verifique los datos.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")


class DeleteUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Eliminar",
            action_color=MAGENTA_SAVE,
            action_hover_color="#C42A63",
            action_command=self.delete_user_action,
            data_type="user",
            title_text="ELIMINAR USUARIOS"
        )

    def delete_user_action(self, user):
        """Elimina un usuario usando Proyecto_2"""
        try:
            success = Proyecto_2.Usuario.eliminar(user['Usuario'])
            if success:
                messagebox.showinfo("Éxito", f"Usuario {user['Nombre']} eliminado correctamente")
                self.datos_originales = self._load_users_from_db()
                self.datos_filtrados = self.datos_originales.copy()
                self._actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")


class ModifyCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Editar",
            action_color=PURPLE_BRIGHT,
            action_hover_color="#6A5ACD",
            action_command=self.edit_company_action,
            data_type="company",
            title_text="MODIFICAR EMPRESAS"
        )

    def edit_company_action(self, company):
        """Abre el diálogo para editar empresa"""
        print(f"Editando empresa: ID={company['ID']}, Nombre={company['Nombre']}")

        # Crear y mostrar diálogo de edición
        dialog = EditCompanyDialog(self, company)
        self.wait_window(dialog)

        if dialog.result:
            # Recargar la tabla para reflejar cambios
            self.datos_originales = self._load_companies_from_db()
            self.datos_filtrados = self.datos_originales.copy()
            self._actualizar_tabla()


class DeleteCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Eliminar",
            action_color=MAGENTA_SAVE,
            action_hover_color="#C42A63",
            action_command=self.delete_company_action,
            data_type="company",
            title_text="ELIMINAR EMPRESAS"
        )

    def delete_company_action(self, company):
        """Elimina una empresa usando Proyecto_2"""
        try:
            success = Proyecto_2.Empresa.eliminar(company['Nombre'])
            if success:
                messagebox.showinfo("Éxito", f"Empresa {company['Nombre']} eliminada correctamente")
                self.datos_originales = self._load_companies_from_db()
                self.datos_filtrados = self.datos_originales.copy()
                self._actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la empresa")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la empresa: {e}")


class EditInventoryDialog(ctk.CTkToplevel):
    def __init__(self, parent, product_data, empresa_nombre):
        super().__init__(parent)
        self.title("Editar Producto")
        self.geometry("500x400")
        self.resizable(False, False)

        self.product_data = product_data
        self.empresa_nombre = empresa_nombre
        self.result = None

        main_frame = ctk.CTkFrame(self, fg_color=PURPLE_BRIGHT, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="EDITAR PRODUCTO",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(20, 30))

        # Campos de edición
        fields = [
            ("PRODUCTO", "PRODUCTO"),
            ("CANTIDAD", "CANTIDAD"),
            ("PRECIO", "PRECIO")]

        self.entries = {}
        for field_label, field_key in fields:
            ctk.CTkLabel(main_frame, text=field_label, font=ctk.CTkFont(size=12, weight="normal"), text_color="white",
                         anchor="w").pack(fill="x", padx=40, pady=(10, 0))

            entry = ctk.CTkEntry(main_frame, placeholder_text="", height=35, corner_radius=10, fg_color=PURPLE_ENTRY,
                                 border_width=0, text_color="white", placeholder_text_color="white")
            entry.pack(fill="x", padx=40, pady=(5, 10))
            self.entries[field_key] = entry

        # Cargar datos actuales del producto
        self._load_current_product_data()

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, width=120, height=40, corner_radius=10,
                      fg_color="white", hover_color="#E0E0E0", text_color="black").grid(row=0, column=0, padx=(0, 10),
                                                                                        sticky="w")

        ctk.CTkButton(button_frame, text="Guardar Cambios", command=self.save_changes, width=120, height=40,
                      corner_radius=10, fg_color=MAGENTA_SAVE, hover_color="#C42A63").grid(row=0, column=1,
                                                                                           padx=(10, 0), sticky="e")

    def _load_current_product_data(self):
        """Carga los datos actuales del producto en los campos"""
        # El nombre del producto no se puede editar (es la clave primaria)
        self.entries["PRODUCTO"].insert(0, self.product_data['Nombre'])
        self.entries["PRODUCTO"].configure(state="disabled")  # No editable

        self.entries["CANTIDAD"].insert(0, str(self.product_data['Cantidad']))
        self.entries["PRECIO"].insert(0, str(self.product_data['Precio']))

    def save_changes(self):
        """Guarda los cambios del producto en la base de datos"""
        try:
            producto = self.entries["PRODUCTO"].get().strip()
            cantidad_text = self.entries["CANTIDAD"].get().strip()
            precio_text = self.entries["PRECIO"].get().strip()

            if not all([producto, cantidad_text, precio_text]):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            try:
                cantidad = int(cantidad_text)
                precio = float(precio_text)

                if cantidad < 0:
                    messagebox.showerror("Error", "La cantidad no puede ser negativa")
                    return
                if precio < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo")
                    return

            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal")
                return

            # Obtener información actual del producto
            producto_info_actual = Proyecto_2.Inventario.obtener_informacion_producto(
                self.empresa_nombre, producto
            )

            if not producto_info_actual:
                messagebox.showerror("Error", "No se pudo encontrar el producto en la base de datos")
                return
            if (int(producto_info_actual['cantidad']) == cantidad and
                    float(producto_info_actual['precio']) == precio):
                messagebox.showinfo("Información", "No se detectaron cambios para guardar")
                self.destroy()
                return

            conn = None
            cursor = None
            try:
                conn = Proyecto_2.BasedeDatos.conectar()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE inventario_general 
                    SET cantidad = %s, precio = %s 
                    WHERE empresa_nombre = %s AND producto = %s""",
                               (cantidad, precio, self.empresa_nombre, producto))

                conn.commit()

                messagebox.showinfo("Éxito", f"Producto {producto} actualizado correctamente")
                self.result = {
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio
                }
                self.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar producto: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")


class InventoryManagementPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_WHITE)
        self.controller = controller
        self.datos_originales = []
        self.datos_filtrados = []
        self.campo_busqueda = "Nombre"

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header morado
        self.title_header_frame = ctk.CTkFrame(self, fg_color=PURPLE_DARK, height=60, corner_radius=0)
        self.title_header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=0, pady=0)
        self.title_header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.title_header_frame, text="GESTIÓN DE INVENTARIO",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="white")
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Cargar datos del inventario
        self.datos_originales = self._load_inventory_from_db()
        self.datos_filtrados = self.datos_originales.copy()

        self._setup_top_bar()
        self._setup_table()

    def _load_inventory_from_db(self):
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                return []

            inventario = Proyecto_2.Inventario.listar(empresa_nombre)
            formatted_inventory = []
            for item in inventario:
                formatted_inventory.append({
                    "ID_Producto": item.get('id_producto', ''),
                    "Nombre": item.get('producto', ''),
                    "Cantidad": item.get('cantidad', 0),
                    "Precio": item.get('precio', 0)
                })
            return formatted_inventory
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            return []

    def _setup_top_bar(self):
        top_bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_bar_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(40, 20))
        top_bar_frame.grid_columnconfigure(1, weight=1)

        # Botón de Agregar Producto
        ctk.CTkButton(top_bar_frame, text="Agregar Producto",
                      command=self.add_inventory_action,
                      width=140, height=45, corner_radius=25,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63",
                      font=ctk.CTkFont(size=14, weight="bold")
                      ).grid(row=0, column=0, padx=(0, 15), sticky="w")

        # Campo de búsqueda
        self.buscar_entry = ctk.CTkEntry(top_bar_frame, placeholder_text="Buscar...",
                                         width=400, height=45, corner_radius=25,
                                         fg_color="white", text_color="black",
                                         font=ctk.CTkFont(size=14))
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=15)
        self.buscar_entry.bind("<KeyRelease>", self._realizar_busqueda)

        # Botón de búsqueda avanzada
        ctk.CTkButton(top_bar_frame, text="Buscar",
                      command=self._buscar_avanzada,
                      width=100, height=45, corner_radius=25,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63",
                      font=ctk.CTkFont(size=14, weight="bold")
                      ).grid(row=0, column=2, padx=(15, 0), sticky="e")

        # Botón de regresar
        ctk.CTkButton(top_bar_frame, text="Regresar",
                      command=self._handle_back_action,
                      width=100, height=45, corner_radius=25,
                      fg_color="white", hover_color="#E0E0E0", text_color="black",
                      font=ctk.CTkFont(size=14, weight="bold")
                      ).grid(row=0, column=3, padx=(15, 0), sticky="e")

    def _realizar_busqueda(self, event=None):
        texto_busqueda = self.buscar_entry.get().strip()

        if not texto_busqueda:
            self.datos_filtrados = self.datos_originales.copy()
            self._actualizar_tabla()
            return

        # Búsqueda secuencial simple
        resultados = []
        for item in self.datos_originales:
            if texto_busqueda.lower() in str(item.get('Nombre', '')).lower():
                resultados.append(item)

        self.datos_filtrados = resultados
        self._actualizar_tabla()

    def _buscar_avanzada(self):
        texto_busqueda = self.buscar_entry.get().strip()

        if not texto_busqueda:
            messagebox.showinfo("Búsqueda", "Ingrese un término de búsqueda")
            return

        dialog = BusquedaInventarioDialog(self)
        self.wait_window(dialog)

        if dialog.campo_seleccionado:
            self.campo_busqueda = dialog.campo_seleccionado
            resultados = []

            for item in self.datos_originales:
                valor_item = str(item.get(self.campo_busqueda, '')).lower()
                if texto_busqueda.lower() in valor_item:
                    resultados.append(item)

            if not resultados:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados")
                self.datos_filtrados = []
            else:
                self.datos_filtrados = resultados
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} resultado(s)")

            self._actualizar_tabla()

    def _handle_back_action(self):
        if self.controller.controller.selected_company:
            company_name = self.controller.controller.selected_company
            self.controller.controller.select_company_and_navigate(company_name)
        else:
            self.controller.show_default_dashboard()

    def _setup_table(self):
        table_container = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        table_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        data = self.datos_filtrados
        cols = ["PRODUCTO", "CANTIDAD", "PRECIO", "Editar", "Eliminar"]

        num_cols = len(cols)
        for i in range(num_cols):
            table_container.grid_columnconfigure(i, weight=1)

        # Encabezados de la tabla
        header_font = ctk.CTkFont(size=16, weight="bold")
        for i, col_name in enumerate(cols):
            header_cell = ctk.CTkLabel(table_container, text=col_name.upper(),
                                       fg_color=PURPLE_DARK, text_color="white", font=header_font, height=50,
                                       corner_radius=0)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

        # Filas de datos
        row_font = ctk.CTkFont(size=14)
        for r, item in enumerate(data):
            row_index = r + 1
            bg_color = COLOR_FILA_CLARA if r % 2 == 0 else COLOR_FILA_OSCURA
            text_color = COLOR_TEXTO_TABLA

            # Columna Producto
            ctk.CTkLabel(table_container, text=item['Nombre'], fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=0,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))

            # Columna Cantidad
            ctk.CTkLabel(table_container, text=str(item['Cantidad']), fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=1,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))

            # Columna Precio
            precio_text = f"Q {float(item['Precio']):.2f}" if item['Precio'] else "Q 0.00"
            ctk.CTkLabel(table_container, text=precio_text, fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=2,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))

            # Columna Editar
            edit_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            edit_frame.grid(row=row_index, column=3, sticky="nsew", padx=(1, 1), pady=(1, 1))
            ctk.CTkButton(edit_frame, text="Editar",
                          command=lambda u=item: self.edit_inventory_action(u),
                          width=70, height=35, corner_radius=10,
                          fg_color=PURPLE_BRIGHT,
                          hover_color="#6A5ACD",
                          text_color="white",
                          font=ctk.CTkFont(size=12, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            # Columna Eliminar
            delete_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            delete_frame.grid(row=row_index, column=4, sticky="nsew", padx=(1, 1), pady=(1, 1))
            ctk.CTkButton(delete_frame, text="Eliminar",
                          command=lambda u=item: self.delete_inventory_action(u),
                          width=70, height=35, corner_radius=10,
                          fg_color=MAGENTA_SAVE,
                          hover_color="#C42A63",
                          text_color="white",
                          font=ctk.CTkFont(size=12, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _actualizar_tabla(self):
        # Limpiar tabla actual
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) == 2:
                widget.destroy()
        self._setup_table()

    def add_inventory_action(self):
        """Abre el diálogo para agregar nuevo producto al inventario"""
        dialog = AddInventoryDialog(self)
        self.wait_window(dialog)
        # Recargar los datos después de agregar un producto
        self.datos_originales = self._load_inventory_from_db()
        self.datos_filtrados = self.datos_originales.copy()
        self._actualizar_tabla()

    def edit_inventory_action(self, item):
        """Abre diálogo para editar producto del inventario"""
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                messagebox.showerror("Error", "No hay empresa seleccionada")
                return
            dialog = EditInventoryDialog(self, item, empresa_nombre)
            self.wait_window(dialog)

            if dialog.result:
                self.datos_originales = self._load_inventory_from_db()
                self.datos_filtrados = self.datos_originales.copy()
                self._actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"Error al editar producto: {str(e)}")

    def delete_inventory_action(self, item):
        """Elimina un ítem del inventario"""
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                messagebox.showerror("Error", "No hay empresa seleccionada")
                return

            # Confirmar eliminación
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de que quieres eliminar el producto '{item['Nombre']}'?"
            )

            if not respuesta:
                return

            success = Proyecto_2.Inventario.eliminar_de_inventario(empresa_nombre, item['Nombre'])
            if success:
                messagebox.showinfo("Éxito", f"Producto {item['Nombre']} eliminado correctamente")
                # Recargar datos después de eliminar
                self.datos_originales = self._load_inventory_from_db()
                self.datos_filtrados = self.datos_originales.copy()
                self._actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")


class BusquedaInventarioDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Búsqueda en Inventario")
        self.geometry("500x500")
        self.resizable(False, False)

        self.campo_seleccionado = None

        main_frame = ctk.CTkFrame(self, fg_color=PURPLE_BRIGHT, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="BUSCAR POR:",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white").pack(pady=(15, 20))

        campos = ["Nombre", "Cantidad", "Precio"]

        for campo in campos:
            ctk.CTkButton(main_frame, text=campo,
                          command=lambda c=campo: self.seleccionar_campo(c),
                          width=200, height=35, corner_radius=10,
                          fg_color=PURPLE_ENTRY,
                          hover_color="#6A5ACD",
                          text_color="white").pack(pady=5)

    def seleccionar_campo(self, campo):
        self.campo_seleccionado = campo
        self.destroy()


class AddInventoryDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Producto al Inventario")
        self.geometry("500x600")
        self.resizable(False, False)

        self.parent = parent

        main_frame = ctk.CTkFrame(self, fg_color=PURPLE_BRIGHT, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="AGREGAR PRODUCTO",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=(20, 30))

        self.entries = {}
        fields = ["PRODUCTO", "CANTIDAD", "PRECIO"]

        for field in fields:
            ctk.CTkLabel(main_frame, text=field,
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(10, 0))

            entry = ctk.CTkEntry(main_frame, placeholder_text="", height=35,
                                 corner_radius=10, fg_color=PURPLE_ENTRY, border_width=0,
                                 text_color="white", placeholder_text_color="white")
            entry.pack(fill="x", padx=40, pady=(5, 10))
            self.entries[field] = entry

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy,
                      width=120, height=40, corner_radius=10,
                      fg_color="white",
                      hover_color="#E0E0E0",
                      text_color="black").grid(row=0, column=0, padx=(0, 10), sticky="w")

        ctk.CTkButton(button_frame, text="Agregar", command=self.add_product,
                      width=120, height=40, corner_radius=10,
                      fg_color=MAGENTA_SAVE,
                      hover_color="#C42A63").grid(row=0, column=1, padx=(10, 0), sticky="e")

    def add_product(self):
        producto = self.entries["PRODUCTO"].get().strip()
        cantidad = self.entries["CANTIDAD"].get().strip()
        precio = self.entries["PRECIO"].get().strip()

        if not all([producto, cantidad, precio]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        empresa_nombre = self.parent.controller.controller.selected_company
        if not empresa_nombre:
            messagebox.showerror("Error", "No hay empresa seleccionada")
            return

        try:
            # Convertir a números
            cantidad_int = int(cantidad)
            precio_float = float(precio)

            if cantidad_int <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            if precio_float <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return

            # Crear el objeto inventario y guardar
            inventario = Proyecto_2.Inventario(empresa_nombre, producto, cantidad_int, precio_float)
            success = inventario.guardar()

            if success:
                messagebox.showinfo("Éxito", f"Producto {producto} agregado correctamente")
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto")

        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")


class ViewCompaniesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_WHITE)
        self.controller = controller.controller

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header morado
        self.title_header_frame = ctk.CTkFrame(self, fg_color=PURPLE_DARK, height=60, corner_radius=0)
        self.title_header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=0, pady=0)
        self.title_header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.title_header_frame, text="EMPRESAS",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="white")
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.companies = self._load_companies_from_db()
        self._setup_company_list()

    def _load_companies_from_db(self):
        """Carga empresas desde la base de datos"""
        try:
            empresas = Proyecto_2.Empresa.listar()
            return [empresa['nombre'] for empresa in empresas] if empresas else []
        except Exception as e:
            print(f"Error cargando empresas: {e}")
            return []

    def _setup_company_list(self):
        list_frame = ctk.CTkFrame(self, fg_color=BG_WHITE, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=100, pady=50)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollable_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable_list.pack(fill="both", expand=True, padx=40, pady=40)
        scrollable_list.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(scrollable_list, text="LISTA DE EMPRESAS",
                     font=ctk.CTkFont(family="Courier", size=24, weight="bold"), text_color="black").grid(row=0,
                                                                                                          column=0,
                                                                                                          pady=(20, 30),
                                                                                                          sticky="n")
        list_font = ctk.CTkFont(family="Courier", size=20)
        for i, company_name in enumerate(self.companies):
            company_button = ctk.CTkButton(scrollable_list,
                                           text=f"{i + 1}. {company_name}",
                                           command=lambda name=company_name: self.select_company(name),
                                           fg_color="transparent",
                                           hover_color="#cccccc",
                                           anchor="w",
                                           font=list_font,
                                           height=40,
                                           text_color="black")
            company_button.grid(row=i + 1, column=0, sticky="ew", pady=5, padx=20)

    def select_company(self, company_name):
        print(f"Empresa seleccionada: {company_name}")
        self.controller.select_company_and_navigate(company_name)


class CompanyHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller, company_name):
        super().__init__(parent, fg_color=BG_WHITE)
        self.controller = controller
        self.company_name = company_name

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header morado
        self.title_header_frame = ctk.CTkFrame(self, fg_color=PURPLE_DARK, height=60, corner_radius=0)
        self.title_header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=0, pady=0)
        self.title_header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.title_header_frame, text=f"{self.company_name} - PANEL PRINCIPAL",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="white")
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self._setup_options_list()

    def _setup_options_list(self):
        list_frame = ctk.CTkFrame(self, fg_color=BG_WHITE, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=100, pady=50)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollable_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable_list.pack(fill="both", expand=True, padx=40, pady=40)
        scrollable_list.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(scrollable_list, text="OPCIONES", font=ctk.CTkFont(family="Courier", size=24, weight="normal"),
                     text_color="black").pack(pady=(20, 30), anchor="n")

        options = ["GESTIONAR INVENTARIO", "VER REPORTES", "REGISTRAR FACTURA"]

        list_font_normal = ctk.CTkFont(family="Courier", size=20)
        for i, option_name in enumerate(options):
            command = lambda name=option_name: self.controller.nav_action(name)

            option_button = ctk.CTkButton(scrollable_list,
                                          text=f"{i + 1}. {option_name}",
                                          command=command,
                                          fg_color="transparent",
                                          hover_color="#cccccc",
                                          anchor="w",
                                          font=list_font_normal,
                                          height=40,
                                          text_color="black")
            option_button.pack(fill="x", pady=5, padx=20)

    def nav_action(self, action):
        """Redirige la acción al controlador del dashboard"""
        self.controller.nav_action(action)

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller
        self.company_name = self.controller.controller.selected_company
        self.año_seleccionado = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_header()
        self._setup_reports()

    def _setup_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_MORADO_OSCURO, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="new")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header_frame, text=f"REPORTES - {self.company_name}",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="white").grid(
            row=0, column=0, padx=20, pady=10, sticky="w")

        # Selector de año
        año_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        año_frame.grid(row=0, column=1, padx=20, sticky="e")

        ctk.CTkLabel(año_frame, text="Año:",
                     font=ctk.CTkFont(size=12),
                     text_color="white").pack(side="left", padx=(0, 5))

        self.año_combobox = ctk.CTkComboBox(año_frame,
                                            values=["2025", "2026", "2027"],
                                            width=80,
                                            command=self.cambiar_año)
        self.año_combobox.pack(side="left", padx=(0, 10))
        self.año_combobox.set("2025")  # Año por defecto
        self.año_seleccionado = 2024

        ctk.CTkButton(header_frame, text="Regresar",
                      command=lambda: self.controller.nav_action("REGRESAR A EMPRESA"),
                      width=100, height=35, corner_radius=10,
                      fg_color="white", hover_color="#cccccc", text_color="black"
                      ).grid(row=0, column=2, padx=20, sticky="e")

    def cambiar_año(self, choice):
        """Cambia el año seleccionado para los reportes"""
        try:
            self.año_seleccionado = int(choice)
            # Refrescar el reporte actual
            if hasattr(self, 'reporte_actual'):
                self.show_report(self.reporte_actual)
        except ValueError:
            pass

    def _setup_reports(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=30)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Botones de tipos de reportes
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        report_types = ["FACTURAS EMITIDAS", "FACTURAS CANCELADAS", "VENTAS TOTALES", "VENTAS POR MES"]
        for i, report_type in enumerate(report_types):
            ctk.CTkButton(button_frame, text=report_type,
                          command=lambda rt=report_type: self.show_report(rt),
                          width=150, height=40, corner_radius=10,
                          fg_color=COLOR_BOTON_PRIMARIO,
                          hover_color="#5D3FD3").grid(row=0, column=i, padx=5)

        # Área de reportes
        self.report_frame = ctk.CTkScrollableFrame(main_frame, fg_color=COLOR_CONTENIDO_BOX)
        self.report_frame.grid(row=1, column=0, sticky="nsew")

        # Mostrar reporte por defecto
        self.show_report("FACTURAS EMITIDAS")

    def show_report(self, report_type):
        # Limpiar frame anterior
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        self.reporte_actual = report_type

        ctk.CTkLabel(self.report_frame, text=f"{report_type} - Año {self.año_seleccionado}",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=20)

        try:
            if report_type == "FACTURAS EMITIDAS":
                self.mostrar_facturas_emitidas()
            elif report_type == "FACTURAS CANCELADAS":
                self.mostrar_facturas_canceladas()
            elif report_type == "VENTAS TOTALES":
                self.mostrar_ventas_totales()
            elif report_type == "VENTAS POR MES":
                self.mostrar_ventas_por_mes()
            else:
                data = []

            if not self.report_frame.winfo_children():
                ctk.CTkLabel(self.report_frame, text="No hay datos disponibles",
                             font=ctk.CTkFont(size=16), text_color=COLOR_TEXTO_ETIQUETA).pack(pady=50)

        except Exception as e:
            ctk.CTkLabel(self.report_frame, text=f"Error al cargar reporte: {str(e)}",
                         font=ctk.CTkFont(size=16), text_color="red").pack(pady=50)

    def mostrar_facturas_emitidas(self):
        try:
            data = Proyecto_2.Reporte.facturas_emitidas(self.company_name)

            if not data:
                self.mostrar_sin_datos()
                return

            # Crear tabla
            table_frame = ctk.CTkFrame(self.report_frame, fg_color="transparent")
            table_frame.pack(fill="x", padx=20, pady=10)

            # Encabezados
            headers = ["No. FACTURA", "NIT CLIENTE", "MONTO", "FECHA", "EMPRESA"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"),
                             text_color="black").grid(row=0, column=i, padx=5, pady=5, sticky="w")

            # Datos
            for i, factura in enumerate(data, 1):
                ctk.CTkLabel(table_frame, text=factura.get('no_factura', ''),
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=0, padx=5, pady=2,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=factura.get('nit_cliente', ''),
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=1, padx=5, pady=2,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=f"Q {float(factura.get('monto', 0)):.2f}",
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=2, padx=5, pady=2,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=str(factura.get('fecha', '')),
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=3, padx=5, pady=2,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=factura.get('empresa_nombre', ''),
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=4, padx=5, pady=2,
                                                                                 sticky="w")
        except Exception as e:
            self.mostrar_error(str(e))

    def mostrar_facturas_canceladas(self):
        try:
            data = Proyecto_2.Reporte.facturas_canceladas_mes(self.company_name, self.año_seleccionado)

            if not data:
                ctk.CTkLabel(self.report_frame, text="No hay facturas canceladas para este período",
                             font=ctk.CTkFont(size=14), text_color=COLOR_TEXTO_ETIQUETA).pack(pady=20)
                return

            # Crear tabla
            table_frame = ctk.CTkFrame(self.report_frame, fg_color="transparent")
            table_frame.pack(fill="x", padx=20, pady=10)

            # Encabezados
            headers = ["MES", "FACTURAS CANCELADAS", "MONTO CANCELADO"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(table_frame, text=header,
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=COLOR_TEXTO_ETIQUETA).grid(row=0, column=i, padx=10, pady=5, sticky="w")

            # Datos
            nombres_meses = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }

            total_cancelado = 0
            for i, item in enumerate(data, 1):
                mes_num = item['mes']
                mes_nombre = nombres_meses.get(mes_num, f"Mes {mes_num}")
                cantidad = item['cantidad']
                total = item['total'] if item['total'] else 0
                total_cancelado += total

                ctk.CTkLabel(table_frame, text=mes_nombre,
                             font=ctk.CTkFont(size=12)).grid(row=i, column=0, padx=10, pady=3, sticky="w")
                ctk.CTkLabel(table_frame, text=str(cantidad),
                             font=ctk.CTkFont(size=12)).grid(row=i, column=1, padx=10, pady=3, sticky="w")
                ctk.CTkLabel(table_frame, text=f"Q {total:.2f}",
                             font=ctk.CTkFont(size=12)).grid(row=i, column=2, padx=10, pady=3, sticky="w")

            # Total cancelado
            ctk.CTkLabel(table_frame, text="TOTAL CANCELADO:",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLOR_TEXTO_ETIQUETA).grid(row=len(data) + 1, column=1, padx=10, pady=10,
                                                               sticky="e")
            ctk.CTkLabel(table_frame, text=f"Q {total_cancelado:.2f}",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLOR_TEXTO_ETIQUETA).grid(row=len(data) + 1, column=2, padx=10, pady=10,
                                                               sticky="w")

        except Exception as e:
            ctk.CTkLabel(self.report_frame, text=f"Error: {str(e)}",
                         font=ctk.CTkFont(size=14), text_color="red").pack(pady=20)

    def mostrar_ventas_totales(self):
        try:
            data = Proyecto_2.Reporte.total_ventas_empresa(self.company_name)
            if not data:
                ctk.CTkLabel(self.report_frame, text="No hay datos de ventas", font=ctk.CTkFont(size=14),
                             text_color=COLOR_TEXTO_ETIQUETA).pack(pady=20)
                return

            info_frame = ctk.CTkFrame(self.report_frame, fg_color=COLOR_FILA_CLARA, corner_radius=10)
            info_frame.pack(fill="x", padx=50, pady=20)

            for item in data:
                ctk.CTkLabel(info_frame, text=f"Empresa: {item['empresa_nombre']}",
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color="black").pack(pady=10)

                ctk.CTkLabel(info_frame, text=f"Total Facturas Emitidas: {item['facturas']}",
                             font=ctk.CTkFont(size=14),
                             text_color="black").pack(pady=5)

                ctk.CTkLabel(info_frame, text=f"Ventas Totales: Q {float(item['total']):.2f}",
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=COLOR_MORADO_OSCURO).pack(pady=10)

        except Exception as e:
            ctk.CTkLabel(self.report_frame, text=f"Error: {str(e)}", font=ctk.CTkFont(size=14), text_color="red").pack(
                pady=20)

    def mostrar_ventas_por_mes(self):
        """Muestra reporte detallado de ventas por mes"""
        try:
            data = Proyecto_2.Reporte.facturas_por_mes(self.company_name, self.año_seleccionado)

            if not data:
                ctk.CTkLabel(self.report_frame, text="No hay datos de ventas por mes", font=ctk.CTkFont(size=14),
                             text_color=COLOR_TEXTO_ETIQUETA).pack(pady=20)
                return

            # Crear tabla
            table_frame = ctk.CTkFrame(self.report_frame, fg_color="transparent")
            table_frame.pack(fill="x", padx=20, pady=10)
            headers = ["MES", "FACTURAS", "VENTAS TOTALES"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(table_frame, text=header,
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=COLOR_TEXTO_ETIQUETA).grid(row=0, column=i, padx=10, pady=5, sticky="w")

            # Datos
            nombres_meses = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }

            ventas_totales = 0
            facturas_totales = 0

            for i, item in enumerate(data, 1):
                mes_num = item['mes']
                mes_nombre = nombres_meses.get(mes_num, f"Mes {mes_num}")
                cantidad_facturas = item['cuantas_facturas']
                ventas_mes = item['cuanto_dinero'] if item['cuanto_dinero'] else 0
                ventas_totales += ventas_mes
                facturas_totales += cantidad_facturas

                ctk.CTkLabel(table_frame, text=mes_nombre,
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=0, padx=10, pady=3,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=str(cantidad_facturas),
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=1, padx=10, pady=3,
                                                                                 sticky="w")
                ctk.CTkLabel(table_frame, text=f"Q {ventas_mes:.2f}",
                             font=ctk.CTkFont(size=12), text_color="black").grid(row=i, column=2, padx=10, pady=3,
                                                                                 sticky="w")

            resumen_frame = ctk.CTkFrame(self.report_frame, fg_color=COLOR_FILA_CLARA, corner_radius=10)
            resumen_frame.pack(fill="x", padx=50, pady=20)

            ctk.CTkLabel(resumen_frame, text="RESUMEN ANUAL", font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=COLOR_TEXTO_TABLA).pack(pady=10)

            ctk.CTkLabel(resumen_frame, text=f"Total Facturas: {facturas_totales}", font=ctk.CTkFont(size=14),
                         text_color=COLOR_TEXTO_TABLA).pack(pady=2)

            ctk.CTkLabel(resumen_frame, text=f"Ventas Totales: Q {ventas_totales:.2f}",
                         font=ctk.CTkFont(size=14),
                         text_color=COLOR_TEXTO_TABLA).pack(pady=2)
        except Exception as e:
            ctk.CTkLabel(self.report_frame, text=f"Error: {str(e)}",
                         font=ctk.CTkFont(size=14), text_color="red").pack(pady=20)

    def mostrar_sin_datos(self):
        ctk.CTkLabel(self.report_frame, text="No hay datos disponibles",
                     font=ctk.CTkFont(size=16), text_color=COLOR_TEXTO_ETIQUETA).pack(pady=50)

    def mostrar_error(self, mensaje):
        ctk.CTkLabel(self.report_frame, text=f"Error: {mensaje}",
                     font=ctk.CTkFont(size=14), text_color="red").pack(pady=20)

class CreateInvoicePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller
        self.productos_factura = []
        self.productos_disponibles = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(6, weight=1)

        company_name = self.controller.controller.selected_company if self.controller.controller.selected_company else "Empres Conta"
        ctk.CTkLabel(left_frame, text=company_name,
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Registrar\nFactura",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="black",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text=f"Aquí puedes registrar una nueva  de factura{company_name}.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black", justify="left").grid(row=2,
                                                                                                          column=0,
                                                                                                          sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="black",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Selecciona productos del inventario disponible.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black", justify="left").grid(row=4,
                                                                                                          column=0,
                                                                                                          sticky="nw")
        ctk.CTkLabel(left_frame, text="El inventario se actualizará automáticamente.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="black", justify="left").grid(row=5,
                                                                                                          sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.nav_action("REGRESAR A EMPRESA"),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="black").grid(row=6, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30, fg_color=COLOR_FORM_FRAME, width=450)
        form_frame.pack(expand=False, fill="y", side="right")

        ctk.CTkLabel(form_frame, text="Factura",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        # Campos básicos de la factura
        basic_fields = ["NIT CLIENTE", "NUMERO FACTURA", "FECHA DE COMPRA"]
        self.entries = {}
        for field in basic_fields:
            ctk.CTkLabel(form_frame, text=field.replace("_", " "),
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            if field == "FECHA DE COMPRA":
                entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=40,
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40, corner_radius=10,
                                     fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            entry.pack(fill="x", padx=40)
            self.entries[field] = entry

        # Sección para seleccionar productos
        ctk.CTkLabel(form_frame, text="SELECCIONAR PRODUCTOS",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(pady=(30, 10), padx=40)
        product_selection_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        product_selection_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(product_selection_frame, text="Producto Disponible",
                     font=ctk.CTkFont(size=12), text_color="white").pack(anchor="w")

        self.producto_combobox = ctk.CTkComboBox(product_selection_frame,
                                                 values=[],
                                                 state="readonly",
                                                 height=40,
                                                 corner_radius=10,
                                                 fg_color=COLOR_CAMPO_CLARO,
                                                 text_color="white",
                                                 dropdown_fg_color=COLOR_FORM_FRAME,
                                                 button_color=COLOR_MORADO_OSCURO)
        self.producto_combobox.pack(fill="x", pady=(5, 10))
        self.producto_combobox.set("Seleccione un producto")
        # Información del producto seleccionado
        self.producto_info_label = ctk.CTkLabel(product_selection_frame, text="Stock: - | Precio: Q -",
                                                font=ctk.CTkFont(size=11), text_color="yellow")
        self.producto_info_label.pack(anchor="w", pady=(0, 10))

        # Frame para cantidad
        cantidad_frame = ctk.CTkFrame(product_selection_frame, fg_color="transparent")
        cantidad_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(cantidad_frame, text="Cantidad a vender",
                     font=ctk.CTkFont(size=12), text_color="white").pack(anchor="w")

        self.cantidad_entry = ctk.CTkEntry(cantidad_frame,
                                           placeholder_text="Cantidad",
                                           height=40,
                                           corner_radius=10,
                                           fg_color=COLOR_CAMPO_CLARO,
                                           text_color="white")
        self.cantidad_entry.pack(fill="x", pady=(5, 10))
        # Botón para agregar producto
        ctk.CTkButton(form_frame, text="Agregar Producto a Factura",
                      command=self.agregar_producto_action,
                      width=200, height=40, corner_radius=10,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3").pack(pady=(10, 20))

        # Lista de productos agregados a la factura
        ctk.CTkLabel(form_frame, text="PRODUCTOS EN FACTURA",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=(10, 5), padx=40)

        self.productos_listbox = tk.Listbox(form_frame,
                                            bg=COLOR_CAMPO_CLARO,
                                            fg="white",
                                            font=("Arial", 10),
                                            height=6,
                                            selectmode=tk.SINGLE)
        self.productos_listbox.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkButton(form_frame, text="Eliminar Producto Seleccionado",
                      command=self.eliminar_producto_action,
                      width=200, height=35, corner_radius=8,
                      fg_color=COLOR_BOTON_ELIMINAR,
                      hover_color="#8B0000").pack(pady=(0, 20))

        # Total de la factura
        self.total_label = ctk.CTkLabel(form_frame, text="TOTAL: Q 0.00", font=ctk.CTkFont(size=18, weight="bold"),
                                        text_color="yellow")
        self.total_label.pack(pady=(10, 20))
        ctk.CTkButton(form_frame, text="REGISTRAR\nFACTURA",
                      command=self.register_invoice_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 40))
        self.cargar_productos_disponibles()
        self.producto_combobox.configure(command=self.actualizar_info_producto)
        self.cantidad_entry.bind("<KeyRelease>", self.actualizar_info_producto)

    def cargar_productos_disponibles(self):
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                messagebox.showerror("Error", "No hay empresa seleccionada")
                return

            auditor = Proyecto_2.Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "password")
            self.productos_disponibles = auditor.obtener_productos_empresa(empresa_nombre)

            if not self.productos_disponibles:
                self.producto_combobox.configure(values=["No hay productos disponibles"])
                self.producto_combobox.set("No hay productos disponibles")
                return
            nombres_productos = [f"{prod['producto']} (Stock: {prod['cantidad']})" for prod in
                                 self.productos_disponibles]
            self.producto_combobox.configure(values=nombres_productos)
            self.producto_combobox.set("Seleccione un producto")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")

    def actualizar_info_producto(self, event=None):
        """Actualiza la información del producto seleccionado"""
        producto_seleccionado = self.producto_combobox.get()

        if producto_seleccionado in ["Seleccione un producto", "No hay productos disponibles"]:
            self.producto_info_label.configure(text="Stock: - | Precio: Q -")
            return
        nombre_producto = producto_seleccionado.split(" (Stock: ")[0]
        producto_info = next((prod for prod in self.productos_disponibles if prod['producto'] == nombre_producto), None)

        if producto_info:
            stock = producto_info['cantidad']
            precio = producto_info['precio']

            cantidad_text = self.cantidad_entry.get().strip()
            if cantidad_text:
                try:
                    cantidad = int(cantidad_text)
                    if cantidad > stock:
                        self.producto_info_label.configure(
                            text=f"Stock: {stock} | Precio: Q {precio:.2f} | Stock insuficiente",
                            text_color="red")
                    else:
                        subtotal = cantidad * precio
                        self.producto_info_label.configure(
                            text=f"Stock: {stock} | Precio: Q {precio:.2f} | Subtotal: Q {subtotal:.2f}",
                            text_color="yellow")
                except ValueError:
                    self.producto_info_label.configure(text=f"Stock: {stock} | Precio: Q {precio:.2f}",
                                                       text_color="yellow")
            else:
                self.producto_info_label.configure(text=f"Stock: {stock} | Precio: Q {precio:.2f}", text_color="yellow")

    def agregar_producto_action(self):
        producto_seleccionado = self.producto_combobox.get()
        cantidad_text = self.cantidad_entry.get().strip()

        if producto_seleccionado in ["Seleccione un producto", "No hay productos disponibles"]:
            messagebox.showerror("Error", "Por favor seleccione un producto")
            return
        if not cantidad_text:
            messagebox.showerror("Error", "Por favor ingrese la cantidad")
            return
        try:
            cantidad = int(cantidad_text)
            if cantidad <= 0:
                messagebox.showerror("Error", "La catidad debe ser mayor a 0")
                return
            nombre_producto = producto_seleccionado.split(" (Stock: ")[0]
            # Busca información del producto
            producto_info = next((prod for prod in self.productos_disponibles if prod['producto'] == nombre_producto),
                                 None)

            if not producto_info:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            if cantidad > producto_info['cantidad']:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto_info['cantidad']}")
                return
            for prod in self.productos_factura:
                if prod['producto'] == nombre_producto:
                    messagebox.showerror("Error", f"El producto {nombre_producto} ya está en la factura")
                    return
            # Agregar producto a la factura
            producto_factura = {
                'producto': nombre_producto,
                'cantidad': cantidad,
                'precio_unitario': producto_info['precio'],
                'subtotal': cantidad * producto_info['precio']
            }
            self.productos_factura.append(producto_factura)
            self.actualizar_lista_productos()
            self.cantidad_entry.delete(0, tk.END)
            self.producto_combobox.set("Seleccione un producto")
            self.producto_info_label.configure(text="Stock: - | Precio: Q -")

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")

    def eliminar_producto_action(self):
        seleccion = self.productos_listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione un producto para eliminar")
            return

        indice = seleccion[0]
        producto_eliminado = self.productos_factura.pop(indice)

        self.actualizar_lista_productos()
        messagebox.showinfo("Éxito", f"Producto {producto_eliminado['producto']} eliminado de la factura")

    def actualizar_lista_productos(self):
        """Actualiza la lista visual de productos y el total"""
        # Limpiar lista
        self.productos_listbox.delete(0, tk.END)

        # Agregar productos
        total_factura = 0
        for prod in self.productos_factura:
            display_text = f"{prod['producto']} - {prod['cantidad']} x Q{prod['precio_unitario']:.2f} = Q{prod['subtotal']:.2f}"
            self.productos_listbox.insert(tk.END, display_text)
            total_factura += prod['subtotal']

        # Actualizar total
        self.total_label.configure(text=f"TOTAL: Q {total_factura:.2f}")

    def register_invoice_action(self):
        """Registra la factura completa con todos los productos"""
        nit_cliente = self.entries["NIT CLIENTE"].get().strip()
        numero_factura = self.entries["NUMERO FACTURA"].get().strip()
        fecha_compra = self.entries["FECHA DE COMPRA"].get().strip()

        if not all([nit_cliente, numero_factura, fecha_compra]):
            messagebox.showerror("Error", "Por favor complete los campos obligatorios de la factura")
            return

        if not self.productos_factura:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la factura")
            return

        empresa_nombre = self.controller.controller.selected_company
        if not empresa_nombre:
            messagebox.showerror("Error", "No hay empresa seleccionada")
            return

        try:
            monto_total = sum(prod['subtotal'] for prod in self.productos_factura)
            # Crear factura
            factura = Proyecto_2.Factura(numero_factura, nit_cliente, monto_total, self.productos_factura, fecha_compra)
            success = factura.guardar(empresa_nombre)

            if success:
                messagebox.showinfo("Éxito",
                                    f"Factura {numero_factura} registrada correctamente\n"f"Inventario actualizado automáticamente\n"f"Total: Q {monto_total:.2f}")
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
                self.productos_listbox.delete(0, tk.END)
                self.productos_factura.clear()
                self.total_label.configure(text="TOTAL: Q 0.00")
                self.cargar_productos_disponibles()
            else:
                messagebox.showerror("Error", "No se pudo registrar la factura. Verifique el stock diponible.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar factura: {str(e)}")

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_WHITE)
        self.controller = controller

        self.content_container = ctk.CTkFrame(self, fg_color=BG_WHITE)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.user_menu_open = False
        self.company_menu_open = False
        self.client_menu_open = False

        # Sidebar con nuevo color
        self.sidebar_frame = ctk.CTkFrame(
            self, width=220, corner_radius=0,
            fg_color=PURPLE_DARK
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # Logo
        ctk.CTkLabel(self.sidebar_frame, text="CONTABILIDAD EMPRESARIAL V.G.",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")

        # Separador
        separator_top = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="white")
        separator_top.grid(row=0, column=0, padx=0, pady=(60, 0), sticky="ew")

        self.nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.nav_frame.grid(row=1, column=0, sticky="nwe", padx=0, pady=(0, 20))

        # Mostrar información del usuario
        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        user_info = f"BIENVENIDO!\n({user_role.upper()})"
        ctk.CTkLabel(self.nav_frame, text=user_info, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white", justify="left").pack(pady=(20, 30), padx=20, anchor="w")

        self._setup_navigation()

        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", command=self.logout_action,
                      fg_color=MAGENTA_SAVE, hover_color="#C42A63").grid(row=2, column=0, sticky="s", padx=20, pady=20)

        self.current_content = None
        self.show_default_dashboard()

    def _create_nav_button(self, text, command, is_selected=False):
        bg_color = PURPLE_BRIGHT if is_selected else "transparent"
        return ctk.CTkButton(
            self.nav_frame,
            text=text,
            command=command,
            fg_color=bg_color,
            hover_color=PURPLE_BRIGHT,
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=0,
            text_color="white"
        )

    def _create_sub_menu(self, parent_frame, sub_item_text):
        return ctk.CTkButton(
            parent_frame,
            text=f"• {sub_item_text}",
            command=lambda val=sub_item_text: self.nav_action(val),
            fg_color="transparent",
            hover_color="#6A5ACD",
            anchor="w",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            text_color="white"
        )

    def _setup_navigation(self):
        # Solo mostrar gestión de usuarios si es administrador
        if self.controller.is_admin():
            self.btn_usuarios = self._create_nav_button("GESTIONAR USUARIOS ▾",
                                                        lambda: self.toggle_menu('user'))
            self.btn_usuarios.pack(fill="x", padx=0, pady=(10, 0))
            self.user_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
            self._create_sub_menu(self.user_menu_frame, "CREAR USUARIO").pack(fill="x")
            self._create_sub_menu(self.user_menu_frame, "MODIFICAR USUARIOS").pack(fill="x")
            self._create_sub_menu(self.user_menu_frame, "ELIMINAR USUARIOS").pack(fill="x")

        # Solo mostrar gestión de clientes si es administrador
        if self.controller.is_admin():
            self.btn_clientes = self._create_nav_button("GESTIONAR CLIENTES ▾",
                                                        lambda: self.toggle_menu('client'))
            self.btn_clientes.pack(fill="x", padx=0, pady=(10, 0))
            self.client_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
            self._create_sub_menu(self.client_menu_frame, "CREAR CLIENTE").pack(fill="x")

        # Solo mostrar gestión de empresa si es administrador
        if self.controller.is_admin():
            self.btn_empresa = self._create_nav_button("GESTIONAR EMPRESA ▾",
                                                       lambda: self.toggle_menu('company'))
            self.btn_empresa.pack(fill="x", padx=0, pady=(10, 0))
            self.company_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
            self._create_sub_menu(self.company_menu_frame, "CREAR EMPRESA").pack(fill="x")
            self._create_sub_menu(self.company_menu_frame, "MODIFICAR INFORMACIÓN EMPRESA").pack(fill="x")
            self._create_sub_menu(self.company_menu_frame, "ELIMINAR EMPRESA").pack(fill="x")

        # Todos los usuarios pueden ver empresas
        self.btn_view_companies = self._create_nav_button("VER EMPRESAS",
                                                          lambda: self.nav_action("VER EMPRESAS"))
        self.btn_view_companies.pack(fill="x", padx=0, pady=(10, 0))

        self.repack_navigation()

    def repack_navigation(self):
        # Limpiar todos los widgets
        for widget in self.nav_frame.winfo_children():
            widget.pack_forget()

        # Mostrar información del usuario de forma segura
        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        user_info = f"BIENVENIDO!\n({user_role.upper()})"
        ctk.CTkLabel(self.nav_frame, text=user_info, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white", justify="left").pack(pady=(20, 30), padx=20, anchor="w")

        # Reconstruir navegación según permisos
        if self.controller.is_admin() and hasattr(self, 'btn_usuarios'):
            self.btn_usuarios.pack(fill="x", padx=0, pady=(10, 0))
            if self.user_menu_open:
                self.user_menu_frame.pack(fill="x", padx=20, pady=(0, 10))

        if self.controller.is_admin() and hasattr(self, 'btn_clientes'):
            self.btn_clientes.pack(fill="x", padx=0, pady=(10, 0))
            if self.client_menu_open:
                self.client_menu_frame.pack(fill="x", padx=20, pady=(0, 10))

        if self.controller.is_admin() and hasattr(self, 'btn_empresa'):
            self.btn_empresa.pack(fill="x", padx=0, pady=(10, 0))
            if self.company_menu_open:
                self.company_menu_frame.pack(fill="x", padx=20, pady=(0, 10))

        if hasattr(self, 'btn_view_companies'):
            self.btn_view_companies.pack(fill="x", padx=0, pady=(10, 0))

        self.nav_frame.update_idletasks()

    def toggle_menu(self, menu_type):
        if menu_type == 'user' and self.controller.is_admin():
            self.user_menu_open = not self.user_menu_open
            if self.user_menu_open:
                self.company_menu_open = False
                self.client_menu_open = False
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▴")
                if hasattr(self, 'btn_empresa'):
                    self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")
                if hasattr(self, 'btn_clientes'):
                    self.btn_clientes.configure(text="GESTIONAR CLIENTES ▾")
            else:
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")

        elif menu_type == 'client' and self.controller.is_admin():
            self.client_menu_open = not self.client_menu_open
            if self.client_menu_open:
                self.user_menu_open = False
                self.company_menu_open = False
                self.btn_clientes.configure(text="GESTIONAR CLIENTES ▴")
                if hasattr(self, 'btn_usuarios'):
                    self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")
                if hasattr(self, 'btn_empresa'):
                    self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")
            else:
                self.btn_clientes.configure(text="GESTIONAR CLIENTES ▾")

        elif menu_type == 'company' and self.controller.is_admin():
            self.company_menu_open = not self.company_menu_open
            if self.company_menu_open:
                self.user_menu_open = False
                self.client_menu_open = False
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▴")
                if hasattr(self, 'btn_usuarios'):
                    self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")
                if hasattr(self, 'btn_clientes'):
                    self.btn_clientes.configure(text="GESTIONAR CLIENTES ▾")
            else:
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")

        self.repack_navigation()

    def show_content(self, content_frame_class):
        if self.current_content:
            self.current_content.destroy()

        if content_frame_class == CompanyHomePage:
            self.current_content = self.controller.frames.get(CompanyHomePage)
        elif content_frame_class == ViewCompaniesPage:
            self.current_content = ViewCompaniesPage(self.content_container, self)
        else:
            page_class = self.controller.pages.get(content_frame_class) or content_frame_class
            self.current_content = page_class(self.content_container, self)

        if self.current_content:
            self.current_content.grid(row=0, column=0, sticky="nsew")

    def show_default_dashboard(self):
        if self.current_content:
            self.current_content.destroy()

        default_frame = ctk.CTkFrame(self.content_container, fg_color=BG_WHITE)
        default_frame.grid(row=0, column=0, sticky="nsew")

        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        welcome_text = f"Bienvenido al sistema de CONTABILIDAD EMPRESARIAL V.G.\nRol: {user_role.upper()}"
        ctk.CTkLabel(default_frame, text=welcome_text,
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=TEXT_LIGHT_GRAY).pack(pady=100)

        self.current_content = default_frame

    def nav_action(self, action):
        print(f"Navegando a: {action}")

        # Verificar permisos para acciones de administrador
        if action in ["CREAR USUARIO", "MODIFICAR USUARIOS", "ELIMINAR USUARIOS",
                      "CREAR EMPRESA", "MODIFICAR INFORMACIÓN EMPRESA", "ELIMINAR EMPRESA",
                      "CREAR CLIENTE"]:
            if not self.controller.is_admin():
                messagebox.showwarning("Acceso Denegado",
                                       "No tienes permisos para acceder a esta función.")
                return

        if action == "CREAR USUARIO":
            self.show_content(CreateUserPage)
        elif action == "MODIFICAR USUARIOS":
            self.show_content(ModifyUsersPage)
        elif action == "ELIMINAR USUARIOS":
            self.show_content(DeleteUsersPage)
        elif action == "CREAR CLIENTE":
            self.show_content(CreateClientPage)
        elif action == "CREAR EMPRESA":
            self.show_content(CreateCompanyPage)
        elif action == "MODIFICAR INFORMACIÓN EMPRESA":
            self.show_content(ModifyCompanyPage)
        elif action == "ELIMINAR EMPRESA":
            self.show_content(DeleteCompanyPage)
        elif action == "VER EMPRESAS":
            self.show_content(ViewCompaniesPage)
        elif action == "GESTIONAR INVENTARIO":
            self.show_content(InventoryManagementPage)
        elif action == "REGISTRAR FACTURA":
            self.show_content(CreateInvoicePage)
        elif action == "VER REPORTES":
            company_name = self.controller.selected_company if self.controller.selected_company else "EMPRESA"
            reports_page = ReportsPage(self.content_container, self)
            reports_page.grid(row=0, column=0, sticky="nsew")
            self.current_content = reports_page
        elif action == "REGRESAR A EMPRESA":
            company_name = self.controller.selected_company
            if company_name:
                self.controller.select_company_and_navigate(company_name)
            else:
                self.show_default_dashboard()
        else:
            self.show_default_dashboard()

    def logout_action(self):
        self.controller.current_user = None
        self.controller.user_role = None
        self.controller.selected_company = None
        self.controller.show_frame(LoginPage)


if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    app = App()
    app.mainloop()