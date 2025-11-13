import mysql.connector
from datetime import date

DB_Sistema = "sistema_empresa.db"

# Métodos de Búsqueda
def busqueda_binaria(lista, indice, valor):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio][indice] == valor:
            return lista[medio]
        elif lista[medio][indice] < valor:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

def busqueda_secuencial(lista, indice, valor):
    for x in lista:
        if x[indice] == valor:
            return x
    return -1

# Métodos de ordenamiento
def metodo_bubble_sort(lista, indice=1):
    datos = list(lista)
    numero = len(datos)
    for i in range(numero):
        cambio = False
        for j in range(0, numero - i - 1):
            if datos[j][indice] > datos[j + 1][indice]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                cambio = True
        if not cambio:
            break
    return datos

def metodo_quick_sort(lista, indice=1):
    if len(lista) <= 1:
        return list(lista)
    pivote = lista[len(lista) // 2][indice]
    menores = [x for x in lista if x[indice] < pivote]
    iguales = [x for x in lista if x[indice] == pivote]
    mayores = [x for x in lista if x[indice] > pivote]
    return metodo_quick_sort(menores, indice) + iguales + metodo_quick_sort(mayores, indice)

def metodo_selection_sort(lista, indice=1):
    lista_ordenar = list(lista)
    for i in range(len(lista_ordenar) - 1):
        menor = i
        for j in range(i + 1, len(lista_ordenar)):
            if lista_ordenar[j][indice] < lista_ordenar[menor][indice]:
                menor = j
        aux = lista_ordenar[i]
        lista_ordenar[i] = lista_ordenar[menor]
        lista_ordenar[menor] = aux
    return lista_ordenar

# Clase base de datos
class BasedeDatos:
    @staticmethod
    def conectar():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rufisbb7",
            database="prueba2",
            port=3306
        )
        return conn
# Clase base
class Usuario:
    def __init__(self,nombre,dpi,correo,puesto,usuario,contrasena,rol):
        self.__nombre= nombre
        self.__dpi= dpi
        self._correo= correo
        self._puesto= puesto
        self.__usuario= usuario
        self.__contrasena= contrasena
        self._rol= rol
        Usuario._conn()

    @staticmethod
    def _conn():
        cursor = None
        conn = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    dpi VARCHAR(50),
                    correo VARCHAR(255),
                    puesto VARCHAR(50),
                    usuario VARCHAR(255) UNIQUE NOT NULL,
                    contrasena VARCHAR(255) NOT NULL,
                    rol VARCHAR(50) NOT NULL
                );
            """)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Ocurrio un error en la base de datos {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @property
    def nombre(self):
        return self.__nombre

    def puesto(self):
        return self._puesto

    @property
    def correo(self):
        return self._correo
    @correo.setter
    def correo(self,correo_nuevo):
        if "@" in correo_nuevo:
            self._correo = correo_nuevo
        else:
            print("Correo no válido..")

    @property
    def rol(self):
        return self._rol

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (self.__usuario,))
            if cursor.fetchone():
                print(f"Usuario {self.__usuario} ya existe.")
                return False
            cursor.execute("""INSERT INTO usuarios (nombre, dpi, correo, puesto, usuario, contrasena, rol) VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (self.__nombre, self.__dpi, self._correo, self._puesto, self.__usuario, self.__contrasena, self._rol))
            conn.commit()
            print(f"Usuario {self.__usuario} guardado.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar usuario: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mostrar_info(self):
        print(f"{self.nombre} ({self.puesto}) - Rol:{self.rol}")

    @staticmethod
    def listar_todos():
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, usuario, rol, puesto FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
        except mysql.connector.Error as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def eliminar(usuario):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            if not cursor.fetchone():
                print(f"El usuario '{usuario}' no existe.")
                return False

            cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (usuario,))
            conn.commit()

            print(f"Usuario {usuario} eliminado correctamente.")
            return True

        except mysql.connector.Error as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def actualizar_usuario(usuario_actual, nuevo_dpi, nuevo_nombre, nuevo_correo, nuevo_puesto, nuevo_usuario,nueva_contrasena, nuevo_rol):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            # Verificamos si el usuario existe
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario_actual,))
            if not cursor.fetchone():
                print(f"Usuario {usuario_actual} no existe.")
                return False
            # Verificamos si el nuevo nombre de usuario ya existe
            if usuario_actual != nuevo_usuario:
                cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (nuevo_usuario,))
                if cursor.fetchone():
                    print(f"El usuario {nuevo_usuario} ya existe.")
                    return False

            # Ya podemos actulizar el usuario
            if nueva_contrasena:  # Si se proporciona nueva contraseña
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre=%s, dpi=%s, correo=%s, puesto=%s, usuario=%s, contrasena=%s, rol=%s 
                    WHERE usuario=%s""", (nuevo_nombre, nuevo_dpi, nuevo_correo, nuevo_puesto, nuevo_usuario, nueva_contrasena, nuevo_rol,usuario_actual))
            else:  # Mantener la contraseña actual
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre=%s, dpi=%s, correo=%s, puesto=%s, usuario=%s, rol=%s 
                    WHERE usuario=%s""", (nuevo_nombre, nuevo_dpi, nuevo_correo, nuevo_puesto, nuevo_usuario, nuevo_rol, usuario_actual))
            conn.commit()
            print(f"Usuario {usuario_actual} actualizado correctamente.")
            return True

        except mysql.connector.Error as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

reportes = {}
facturas = {}
inventario = {}

class Auditor(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre,dpi,correo,"Auditor",usuario,contrasena,"Admin")

    def mostrar_info(self):
        pass

    def crear_usuario(self, nombre, dpi, correo, puesto, usuario, contrasena, rol):
        u = Usuario(nombre, dpi, correo, puesto, usuario, contrasena, rol)
        return u.guardar()

    def crear_cliente(self,nit,nombre,telefono="",correo="",direccion="",dpi="",fecha_nacimiento="",nombre_negocio=""):
        cliente = Cliente(nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio)
        return cliente.guardar()

    def crear_empresa(self, nombre_empresa, nit_cliente, direccion=""):
        empresa = Empresa(nombre_empresa, nit_cliente, direccion)
        guardar = empresa.guardar()
        if guardar:
            if nombre_empresa not in reportes:
                reportes[nombre_empresa] = []
            if nombre_empresa not in facturas:
                facturas[nombre_empresa] = []
            if nombre_empresa not in inventario:
                inventario[nombre_empresa] = []
        return guardar

    def listar_empresas(self):
        return Empresa.listar()

    def listar_clientes(self):
        return Cliente.listar()

    def ver_inventario(self,nombre_empresa):
        return Inventario.listar(nombre_empresa)

    def modificar_inventario(self,nombre_empresa,producto,cantidad,precio):
        inventari = Inventario(nombre_empresa,producto,cantidad,precio)
        guardar = inventari.guardar()
        return guardar

    def reporte_facturas_emitidas(self,empresa):
        return Reporte.facturas_emitidas(empresa)

    def reporte_facturas_canceladas(self,empresa):
        return Reporte.facturas_anuladas(empresa)

    def reporte_ventas(self,empresa):
        return Reporte.total_ventas_empresa(empresa)

    def registrar_factura(self,numero_factura,nit_cliente,empresa_nombre,monto,productos=None,fecha=None):
        factura = Factura(numero_factura,nit_cliente,monto,productos,fecha)
        guardar = factura.guardar(empresa_nombre)
        if guardar:
            if empresa_nombre not in facturas:
                facturas[empresa_nombre] = []
            facturas[empresa_nombre].append(factura)
        return guardar

    def eliminar_usuario(self, usuario):
        return Usuario.eliminar(usuario)

    def eliminar_empresa(self, nombre_empresa):
        return Empresa.eliminar(nombre_empresa)

    def listar_usuarios(self):
        return Usuario.listar_todos()

    def obtener_clientes_disponibles(self):
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.nit, c.nombre, c.nombre_negocio 
                FROM clientes c
                ORDER BY c.nombre
            """)
            clientes = cursor.fetchall()
            cursor.close()
            conn.close()
            return clientes
        except mysql.connector.Error as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def obtener_productos_empresa(self,empresa_nombre):
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT producto, cantidad, precio 
                FROM inventario_general 
                WHERE empresa_nombre = %s AND cantidad > 0
                ORDER BY producto""", (empresa_nombre,))
            productos = cursor.fetchall()
            cursor.close()
            conn.close()
            return productos
        except mysql.connector.Error as e:
            print(f"Existio un error en la base de datos :(: {e}")
            return []

class Empleado(Usuario):
    def __init__(self, nombre, dpi, correo, usuario, contrasena):
        super().__init__(nombre, dpi, correo, "Empleado", usuario, contrasena, "Usuario")

    def mostrar_info(self):
        pass

class Cliente:
    def __init__(self,nit,nombre,telefono="",correo="",direccion="",dpi="",fecha_nacimiento=None,nombre_negocio=""):
        self._nit = nit
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion
        self._dpi = dpi
        self._fecha_nacimiento = fecha_nacimiento
        self.__nombre_negocio = nombre_negocio  # Ahora es opcional
        self._conn()

    @staticmethod
    def _conn():
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nit VARCHAR(50) UNIQUE NOT NULL,
                    nombre VARCHAR(255) NOT NULL,
                    telefono VARCHAR(20),
                    correo VARCHAR(255),
                    direccion TEXT,
                    dpi VARCHAR(50),
                    fecha_nacimiento DATE,
                    nombre_negocio VARCHAR(255)  -- Ahora es opcional
            );
            """)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al crear la tabla clientes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    @property
    def nit(self):
        return self._nit

    @property
    def nombre(self):
        return self._nombre

    @property
    def nombre_negocio(self):
        return self.__nombre_negocio

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE nit=%s", (self._nit,))
            if cursor.fetchone():
                print(f"⚠ Cliente con NIT {self._nit} ya existe.")
                return False

            cursor.execute("""INSERT INTO clientes (nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio) 
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                           (self._nit, self._nombre, self._telefono, self._correo, self._direccion, self._dpi,
                            self._fecha_nacimiento, self.__nombre_negocio if self.__nombre_negocio else None))
            conn.commit()
            print(f"Cliente {self._nombre} guardado.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar cliente: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    @staticmethod
    def listar():
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def eliminar(nit):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM clientes WHERE nit = %s", (nit,))
            if not cursor.fetchone():
                print(f" El cliente con NIT '{nit}' no existe.")
                return False
            cursor.execute("SELECT * FROM empresas WHERE nit_cliente = %s", (nit,))
            if cursor.fetchone():
                print(f"No se puede eliminar el cliente. Está asociado a una empresa.")
                return False

            cursor.execute("SELECT * FROM facturas_general WHERE nit_cliente = %s", (nit,))
            if cursor.fetchone():
                print(f" No se puede eliminar el cliente. Tiene facturas asociadas.")
                return False
            cursor.execute("DELETE FROM clientes WHERE nit = %s", (nit,))
            conn.commit()

            print(f"Cliente con NIT {nit} eliminado correctamente.")
            return True

        except mysql.connector.Error as e:
            print(f" Error al eliminar cliente: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mostrar_informacion(self):
        print(f"{self.nit} - {self.nombre} ({self.nombre_negocio})")

# Normalizar nombre para guardar en base de datos
def normalizar_nombre(nombre):
    nombre_empresa = nombre.strip().lower()
    nombre_empresa = "_".join(nombre_empresa.split())
    resultado = ""
    for x in nombre_empresa:
        if ("a" <= x <= "z") or ("0" <= x <= "9") or x == "_":
            resultado += x
    if not resultado:
        resultado = "empresa"
    return resultado[:50]

class Empresa:
    def __init__(self, nombre, nit_cliente, direccion=""):
        self._nombre = nombre
        self._nit_cliente = nit_cliente
        self._direccion = direccion
        self.tabla_inventario = "inventario_" + normalizar_nombre(nombre)
        self.tabla_facturas = "facturas_" + normalizar_nombre(nombre)
        self._crear_tabla()

    #Se crea tanto tabla de empresas, como inventario y facturas
    def _crear_tabla(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empresas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(200) UNIQUE NOT NULL,
                    nit_cliente VARCHAR(60),
                    direccion VARCHAR(255),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (nit_cliente) REFERENCES clientes(nit) ON DELETE SET NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventario_general (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empresa_nombre VARCHAR(200) NOT NULL,
                    producto VARCHAR(200) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_empresa (empresa_nombre),
                    INDEX idx_producto (producto)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas_general (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empresa_nombre VARCHAR(200) NOT NULL,
                    no_factura VARCHAR(50) NOT NULL,
                    nit_cliente VARCHAR(50) NOT NULL,
                    monto DECIMAL(10,2) NOT NULL,
                    fecha DATE NOT NULL,
                    estado VARCHAR(20) DEFAULT 'Emitida',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY uk_factura_empresa (empresa_nombre, no_factura),
                    INDEX idx_empresa (empresa_nombre),
                    INDEX idx_fecha (fecha),
                    INDEX idx_cliente (nit_cliente)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalle_facturas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empresa_nombre VARCHAR(200) NOT NULL,
                    no_factura VARCHAR(50) NOT NULL,
                    producto VARCHAR(200) NOT NULL,
                    cantidad INT NOT NULL,
                    precio_unitario DECIMAL(10,2) NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (empresa_nombre, no_factura) REFERENCES facturas_general(empresa_nombre, no_factura) ON DELETE CASCADE,
                    INDEX idx_factura (empresa_nombre, no_factura),
                    INDEX idx_producto (producto)
                );""")
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al crear tablas unificadas: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM empresas WHERE nombre=%s", (self._nombre,))
            if cursor.fetchone():
                print(f"Empresa {self._nombre} ya existe.")
                return False
            cursor.execute("INSERT INTO empresas (nombre, nit_cliente, direccion) VALUES (%s,%s,%s)",
                           (self._nombre, self._nit_cliente, self._direccion))
            conn.commit()
            print(f"Empresa {self._nombre} guardada.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar empresa: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def eliminar(nombre_empresa):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empresas WHERE nombre = %s", (nombre_empresa,))
            if not cursor.fetchone():
                print(f"La empresa '{nombre_empresa}' no existe.")
                return False

            cursor.execute("DELETE FROM detalle_facturas WHERE empresa_nombre = %s", (nombre_empresa,))
            cursor.execute("DELETE FROM inventario_general WHERE empresa_nombre = %s", (nombre_empresa,))

            cursor.execute("DELETE FROM facturas_general WHERE empresa_nombre = %s", (nombre_empresa,))
            cursor.execute("DELETE FROM empresas WHERE nombre = %s", (nombre_empresa,))

            conn.commit()

            if nombre_empresa in reportes:
                del reportes[nombre_empresa]
            if nombre_empresa in facturas:
                del facturas[nombre_empresa]
            if nombre_empresa in inventario:
                del inventario[nombre_empresa]

            print(f"Empresa '{nombre_empresa}' y todos sus datos eliminados correctamente.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al eliminar empresa: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar(nit_cliente=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        if nit_cliente:
            cursor.execute(
                "SELECT id, nombre, nit_cliente, direccion FROM empresas WHERE nit_cliente=%s",
                (nit_cliente,))
        else:
            cursor.execute(
                "SELECT id, nombre, nit_cliente, direccion FROM empresas")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def actualizar_empresa(nombre_actual, nuevo_nombre, nuevo_nit_cliente, nueva_direccion):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            # Verificamos si la empresa existe
            cursor.execute("SELECT * FROM empresas WHERE nombre=%s", (nombre_actual,))
            if not cursor.fetchone():
                print(f"Empresa {nombre_actual} no existe.")
                return False
            # Verificamos si el nuevo nombre ya existe
            if nombre_actual != nuevo_nombre:
                cursor.execute("SELECT * FROM empresas WHERE nombre=%s", (nuevo_nombre,))
                if cursor.fetchone():
                    print(f"La empresa {nuevo_nombre} ya existe.")
                    return False
            # Actualizar la empresa
            cursor.execute("""
                UPDATE empresas 
                SET nombre=%s, nit_cliente=%s, direccion=%s 
                WHERE nombre=%s""", (nuevo_nombre, nuevo_nit_cliente, nueva_direccion, nombre_actual))
            conn.commit()
            print(f"Empresa {nombre_actual} actualizada correctamente.")
            return True

        except mysql.connector.Error as e:
            print(f"Error al actualizar empresa: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

class Factura:
    def __init__(self, no_factura, nit_cliente, monto, productos=None, fecha=None, estado="Emitida"):
        self.__no_factura = no_factura
        self.__nit_cliente = nit_cliente
        self._monto = monto
        self._fecha = fecha if fecha else date.today()
        self._estado = estado
        self.productos = productos or []  # Lista de productos que fya fueron vendidos

    def agregar_producto(self, producto, cantidad, precio_unitario):
        self.productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'subtotal': cantidad * precio_unitario})
        self._monto = sum(prod['subtotal'] for prod in self.productos)

    def informacion(self):
        print(f"Factura: {self.no_factura} | Cliente: {self.nit_cliente} | Monto: {self.monto} | fecha: {self.fecha} | Estado:{self.estado}")

    def guardar(self, empresa_nombre):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            for producto in self.productos:
                if not Inventario.verificar_stock(empresa_nombre, producto['producto'], producto['cantidad']):
                    print(f"Stock insuficiente para {producto['producto']}")
                    return False
            cursor.execute("""
                INSERT INTO facturas_general (empresa_nombre, no_factura, nit_cliente, monto, fecha, estado) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                           (empresa_nombre, self.__no_factura, self.__nit_cliente, self._monto, self._fecha,self._estado))

            for producto in self.productos:
                cursor.execute("""
                    INSERT INTO detalle_facturas (empresa_nombre, no_factura, producto, cantidad, precio_unitario, subtotal)VALUES (%s, %s, %s, %s, %s, %s)""",
                               (empresa_nombre, self.__no_factura, producto['producto'], producto['cantidad'],producto['precio_unitario'], producto['subtotal']))

                cursor.execute("""
                    UPDATE inventario_general 
                    SET cantidad = cantidad - %s 
                    WHERE empresa_nombre = %s AND producto = %s""",
                               (producto['cantidad'], empresa_nombre, producto['producto']))

                if cursor.rowcount == 0:
                    print(f"Error: Producto {producto['producto']} no encontrado en inventario")
                    conn.rollback()
                    return False

            conn.commit()
            print(f"Factura {self.__no_factura} guardada e inventario actualizado")
            return True

        except mysql.connector.Error as e:
            print("Error al guardar factura:", e)
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar_por_empresa(empresa_nombre):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT 
                facturas_general.no_factura,
                facturas_general.nit_cliente,
                clientes.nombre as nombre_cliente,
                facturas_general.monto,
                facturas_general.fecha,
                facturas_general.estado
            FROM facturas_general
            INNER JOIN clientes ON facturas_general.nit_cliente = clientes.nit
            WHERE facturas_general.empresa_nombre = %s
            ORDER BY facturas_general.fecha DESC""",
                       (empresa_nombre,))
        datos_filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return datos_filas

    @staticmethod
    def obtener_detalle_factura(empresa_nombre, no_factura):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT producto, cantidad, precio_unitario, subtotal
            FROM detalle_facturas
            WHERE empresa_nombre = %s AND no_factura = %s""",
                       (empresa_nombre, no_factura))
        detalles = cursor.fetchall()
        cursor.close()
        conn.close()
        return detalles

    @property
    def estado(self):
        return self._estado

    def cambiar_estado(self,nuevo_estado):
        self._estado =nuevo_estado

    @property
    def no_factura(self):
        return self.__no_factura

    @property
    def nit_cliente(self):
        return self.__nit_cliente
    @property
    def monto(self):
        return self._monto

    @property
    def fecha(self):
        return self._fecha

class Reporte:
    def __init__(self, total_clientes, total_facturas):
        self.total_clientes = total_clientes
        self.total_facturas = total_facturas

    @staticmethod
    def facturas_emitidas(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT no_factura, nit_cliente, monto, fecha, empresa_nombre
            FROM facturas_general 
            WHERE estado = 'Emitida' AND empresa_nombre = %s""",
                       (empresa,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    @staticmethod
    def facturas_anuladas(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT no_factura, nit_cliente, monto, fecha, empresa_nombre
            FROM facturas_general 
            WHERE estado = 'Anulada' AND empresa_nombre = %s""", (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def total_ventas_empresa(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT empresa_nombre, COUNT(*) as facturas, SUM(monto) as total
            FROM facturas_general 
            WHERE estado = 'Emitida' AND empresa_nombre = %s
            GROUP BY empresa_nombre""",
                       (empresa,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    @staticmethod
    def facturas_por_mes(empresa, año_deseado=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)

        if año_deseado: #Si dan año
            cursor.execute("""
                SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cuantas_facturas,
                    SUM(monto) as cuanto_dinero
                FROM facturas_general 
                WHERE empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes
            """, (empresa, año_deseado))
        else:  #Si no dan año y solo empresa
            cursor.execute("""SELECT 
                    YEAR(fecha) as año, 
                    MONTH(fecha) as mes,
                    COUNT(*) as cuantas_facturas,
                    SUM(monto) as cuanto_dinero
                FROM facturas_general 
                WHERE empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))

        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def facturas_emitidas_mes(empresa, año=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)

        if año: #si dan año
            cursor.execute("""SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Emitida' AND empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes
            """,
                           (empresa, año))
        else: #si no dan año y solo nombre de empresa
            cursor.execute("""SELECT 
                    YEAR(fecha) as año,
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Emitida' AND empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def facturas_canceladas_mes(empresa, año=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        if año:
            cursor.execute("""SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Anulada' AND empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes""",
                           (empresa, año))
        else:
            cursor.execute("""
                SELECT 
                    YEAR(fecha) as año,
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Anulada' AND empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def hacer_reporte_emitidas(empresa, año_seleccionado=None):
        datos = Reporte.facturas_emitidas_mes(empresa, año_seleccionado)
        if not datos:
            return "No hay facturas emitidas"

        nombres_meses = {
            1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
            5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
            9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
        }

        reporte = "FACTURAS EMITIDAS\n"
        reporte += "=" * 30 + "\n\n"

        for dato in datos:
            año = dato.get("año", "2024")
            mes_num = dato["mes"]
            mes_nombre = nombres_meses.get(mes_num, f"MES {mes_num}")

            reporte += f"{mes_nombre}: {dato['cantidad']}\n"
        return reporte

    @staticmethod
    def hacer_reporte_anuladas(empresa, año_seleccionado=None):
        datos = Reporte.facturas_canceladas_mes(empresa, año_seleccionado)
        if not datos:
            return "No hay facturas anuladas"

        nombres_meses = {
            1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
            5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
            9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
        }
        reporte = "FACTURAS ANULADAS\n"
        reporte += "=" * 30 + "\n"
        for dato in datos:
            año = dato.get("año", "2024")
            mes_num = dato["mes"]
            mes_nombre = nombres_meses.get(mes_num, f"MES {mes_num}")
            reporte += f"{mes_nombre}: {dato['cantidad']}\n"
        return reporte

class Inventario:
    def __init__(self, empresa_nombre, producto, cantidad, precio):
        self._empresa_nombre = empresa_nombre
        self._producto = producto
        self._cantidad = cantidad
        self._precio = precio

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cantidad, precio FROM inventario_general 
                WHERE empresa_nombre = %s AND producto = %s""",
                           (self._empresa_nombre, self._producto))
            existente = cursor.fetchone()

            if existente:
                # Actualizar cantidad existente sumando la nueva cantidad
                nueva_cantidad = existente[0] + self._cantidad
                cursor.execute("""
                    UPDATE inventario_general 
                    SET cantidad = %s, precio = %s 
                    WHERE empresa_nombre = %s AND producto = %s""",
                               (nueva_cantidad, self._precio, self._empresa_nombre, self._producto))
            else:
                # Insertar nuevo producto
                cursor.execute("""
                    INSERT INTO inventario_general (empresa_nombre, producto, cantidad, precio) 
                    VALUES (%s, %s, %s, %s)""",
                               (self._empresa_nombre, self._producto, self._cantidad, self._precio))

            conn.commit()
            print(f"Producto {self._producto} actualizado en inventario de {self._empresa_nombre}")
            return True
        except mysql.connector.Error as e:
            print("Error al guardar inventario", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar(nombre_empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT producto, cantidad, precio 
            FROM inventario_general 
            WHERE empresa_nombre = %s
            ORDER BY producto""", (nombre_empresa,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def verificar_stock(empresa_nombre, producto, cantidad_requerida):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT cantidad FROM inventario_general 
            WHERE empresa_nombre = %s AND producto = %s""", (empresa_nombre, producto))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        if resultado and resultado['cantidad'] >= cantidad_requerida:
            return True
        return False

    @staticmethod
    def eliminar_de_inventario(empresa_nombre, producto):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()

            cursor.execute("""DELETE FROM inventario_general 
                    WHERE empresa_nombre = %s AND producto = %s
                """, (empresa_nombre, producto))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Producto '{producto}' eliminado del inventario de {empresa_nombre}.")
                return True
            else:
                print(f"Producto '{producto}' no encontrado en el inventario de {empresa_nombre}.")
                return False

        except mysql.connector.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def obtener_informacion_producto(empresa_nombre, producto):
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT producto, cantidad, precio 
                FROM inventario_general 
                WHERE empresa_nombre = %s AND producto = %s""", (empresa_nombre, producto))
            producto_info = cursor.fetchone()
            cursor.close()
            conn.close()
            return producto_info
        except mysql.connector.Error as e:
            print(f"Ocurrio un error en base de datos :(: {e}")
            return None

def inicio_sesion(usuario, contrasena):
    try:
        if usuario == "contador" and contrasena == "contador123":
            return {"rol": "Contador", "nombre": "Administrador"}

        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s",
                       (usuario, contrasena))
        usuario_db = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario_db:
            return usuario_db
        elif usuario == "0" and contrasena == "0":
            return "salir"
        else:
            return None

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

def crear_usuario_admin():
    """Crea un usuario admin por defecto si no existe"""
    try:
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)

        # Verificar si ya existe usuario
        cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
        if cursor.fetchone():
            print("Usuario admin ya existe")
            return True

        # Crear usuario admin
        admin = Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "admin123")
        success = admin.crear_usuario("Administrador", "123456789", "admin@empresa.com", "Administrador", "admin","admin123", "Admin")

        if success:
            print(" Usuario admin creado exitosamente")
            print(" Credenciales: admin / admin123")
        else:
            print(" No se pudo crear el usuario admin")

        return success

    except Exception as e:
        print(f"Error creando usuario admin: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def verificar_y_crear_admin():
    try:
        admin = Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "admin123")

        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")

        if cursor.fetchone():
            print("Sistema listo - Usuario admin existe")
        else:
            success = admin.crear_usuario("Administrador", "123456789", "admin@empresa.com",
                                          "Administrador", "admin", "admin123", "Admin")
            if success:
                print("Usuario admin creado exitosamente")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error inicializando: {e}")
        return False

# Ejecutar verificación
verificar_y_crear_admin()
crear_usuario_admin()
