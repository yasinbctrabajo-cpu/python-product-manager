from tkinter import *
from tkinter import ttk
import sqlite3


class VentanaPrincipal:

    def __init__(self, root):

        # Guardo la ventana principal para poder usarla en toda la clase
        self.ventana = root

        # Pongo el título que se verá arriba en la ventana
        self.ventana.title("App Gestor de Productos")

        # Permito que la ventana se pueda hacer más grande o más pequeña
        self.ventana.resizable(1, 1)

        # Creo un marco para meter dentro el formulario de nuevo producto
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Creo la etiqueta y la caja para escribir el nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)

        self.nombre = Entry(frame)
        self.nombre.grid(row=1, column=1)

        # Creo la etiqueta y la caja para escribir el precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)

        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Creo el botón para guardar un producto nuevo
        self.boton_aniadir = ttk.Button(
            frame,
            text="Guardar Producto",
            command=self.add_producto
        )
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W + E)

        # Creo el botón para eliminar el producto seleccionado
        self.boton_eliminar = ttk.Button(
            text="ELIMINAR",
            command=self.del_producto
        )
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E)

        # Creo el botón para editar el producto seleccionado
        self.boton_editar = ttk.Button(
            text="EDITAR",
            command=self.edit_producto
        )
        self.boton_editar.grid(row=5, column=1, sticky=W + E)

        # Doy un poco de estilo a la tabla
        style = ttk.Style()

        style.configure(
            "mystyle.Treeview",
            highlightthickness=0,
            bd=0,
            font=('Calibri', 11)
        )

        style.configure(
            "mystyle.Treeview.Heading",
            font=('Calibri', 13, 'bold')
        )

        style.layout(
            "mystyle.Treeview",
            [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]
        )

        # Creo la tabla donde se van a mostrar los productos
        self.tabla = ttk.Treeview(
            height=10,
            columns=2,
            style="mystyle.Treeview"
        )

        self.tabla.grid(row=4, column=0, columnspan=2)

        # Pongo los nombres de las columnas de la tabla
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)

        # Cargo los productos de la base de datos nada más abrir la app
        self.get_productos()

    def validacion(self):

        # Compruebo que el nombre y el precio no estén vacíos
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

    def add_producto(self):

        # Si los campos tienen datos, guardo el producto
        if self.validacion():

            consulta = 'INSERT INTO producto VALUES(NULL, ?, ?)'

            parametros = (self.nombre.get(), self.precio.get())

            # Ejecuto la consulta para insertar el producto en la base de datos
            self.ejecutar_consulta(consulta, parametros)

            # Actualizo la tabla para que aparezca el producto nuevo
            self.get_productos()

            # Limpio los campos después de guardar
            self.nombre.delete(0, END)
            self.precio.delete(0, END)

    def del_producto(self):

        # Cojo el nombre del producto que está seleccionado en la tabla
        nombre = self.tabla.item(self.tabla.selection())['text']

        consulta = 'DELETE FROM producto WHERE nombre = ?'

        # Borro el producto de la base de datos
        self.ejecutar_consulta(consulta, (nombre,))

        # Actualizo la tabla para que desaparezca el producto borrado
        self.get_productos()

    def edit_producto(self):

        # Cojo los datos del producto seleccionado
        nombre = self.tabla.item(self.tabla.selection())['text']
        precio = self.tabla.item(self.tabla.selection())['values'][0]

        # Abro una nueva ventana para editar ese producto
        VentanaEditarProducto(self, nombre, precio)

    def ejecutar_consulta(self, consulta, parametros=()):

        # Me conecto a la base de datos
        with sqlite3.connect('database/productos.db') as conexion:

            cursor = conexion.cursor()

            # Ejecuto la consulta SQL que le pase al método
            resultado = cursor.execute(consulta, parametros)

            # Guardo los cambios en la base de datos
            conexion.commit()

        return resultado

    def get_productos(self):

        # Primero borro lo que haya en la tabla para no duplicar datos
        registros_tabla = self.tabla.get_children()

        for elemento in registros_tabla:
            self.tabla.delete(elemento)

        # Consulta para sacar todos los productos ordenados por nombre
        consulta = 'SELECT * FROM producto ORDER BY nombre DESC'

        db_filas = self.ejecutar_consulta(consulta)

        # Recorro los productos y los meto en la tabla
        for fila in db_filas:
            self.tabla.insert('', 0, text=fila[1], values=fila[2])


class VentanaEditarProducto:

    def __init__(self, ventana_principal, nombre, precio):

        # Guardo la referencia de la ventana principal para poder actualizarla luego
        self.ventana_principal = ventana_principal

        # Guardo el nombre y precio antiguos del producto
        self.nombre = nombre
        self.precio = precio

        # Creo una ventana nueva para editar
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creo un marco para organizar los campos de edición
        frame = LabelFrame(
            self.ventana_editar,
            text="Editar el siguiente Producto"
        )
        frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Muestro el nombre antiguo, pero no dejo modificarlo
        Label(frame, text="Nombre antiguo: ").grid(row=1, column=0)

        Entry(
            frame,
            textvariable=StringVar(
                self.ventana_editar,
                value=nombre
            ),
            state="readonly"
        ).grid(row=1, column=1)

        # Caja para escribir el nombre nuevo
        Label(frame, text="Nombre nuevo: ").grid(row=2, column=0)

        self.input_nombre_nuevo = Entry(frame)
        self.input_nombre_nuevo.grid(row=2, column=1)

        # Muestro el precio antiguo, pero no dejo modificarlo
        Label(frame, text="Precio antiguo: ").grid(row=3, column=0)

        Entry(
            frame,
            textvariable=StringVar(
                self.ventana_editar,
                value=precio
            ),
            state="readonly"
        ).grid(row=3, column=1)

        # Caja para escribir el precio nuevo
        Label(frame, text="Precio nuevo: ").grid(row=4, column=0)

        self.input_precio_nuevo = Entry(frame)
        self.input_precio_nuevo.grid(row=4, column=1)

        # Botón que actualiza el producto
        ttk.Button(
            frame,
            text="Actualizar Producto",
            command=self.actualizar
        ).grid(row=5, columnspan=2, sticky=W + E)

    def actualizar(self):

        # Si no escribo un nombre nuevo, se queda el antiguo
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre

        # Si no escribo un precio nuevo, se queda el antiguo
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        consulta = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'

        parametros = (
            nuevo_nombre,
            nuevo_precio,
            self.nombre
        )

        # Actualizo el producto en la base de datos
        self.ventana_principal.ejecutar_consulta(
            consulta,
            parametros
        )

        # Cierro la ventana de edición
        self.ventana_editar.destroy()

        # Refresco la tabla principal para ver el cambio
        self.ventana_principal.get_productos()


if __name__ == '__main__':

    # Creo la ventana principal de Tkinter
    root = Tk()

    # Creo la aplicación usando mi clase principal
    app = VentanaPrincipal(root)

    # Mantengo la ventana abierta
    root.mainloop()