import wx
# Trae funciones personalizadas desde datos.py para interactuar con el JSON
from datos import cargar_productos, guardar_productos
# Permite trabajar con fechas (lo usamos para validar que el vencimiento sea DD/MM/AAAA)
from datetime import datetime

# VENTANA 2: GESTIÓN DE PRODUCTO
class VentanaGestionProducto(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Gestión de productos", size=(750, 550)) # Aumentado el alto
        # Cargamos los productos guardados previamente
        self.productos = cargar_productos()
        self.InitUI()
        self.Centre()

    # Creamos todos los componentes visuales 
    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        #sSizer para acomodar los elementos de forma ordenada 
        sizer_global = wx.BoxSizer(wx.VERTICAL)
        sizer_superior = wx.BoxSizer(wx.HORIZONTAL)

        # Acá el usuario ingresa los datos del producto
        caja_datos = wx.StaticBox(panel, label="Datos del producto")
        sizer_form = wx.StaticBoxSizer(caja_datos, wx.VERTICAL)
        
        fgs = wx.FlexGridSizer(5, 2, 10, 10)
        #Etiquetas del formulario
        lbl_nombre = wx.StaticText(panel, label="Nombre:")
        self.txt_nombre = wx.TextCtrl(panel, size=(200, -1))
        lbl_precio = wx.StaticText(panel, label="Precio:")
        self.txt_precio = wx.TextCtrl(panel, size=(200, -1))
        lbl_stock = wx.StaticText(panel, label="Stock:")
        self.txt_stock = wx.TextCtrl(panel, size=(200, -1))
        lbl_cat = wx.StaticText(panel, label="Categoría:")
        self.cb_categoria = wx.ComboBox(panel, choices=["Bebidas", "Golosinas", "Snack", "Lácteos", "Despensa", "Libreria", "Limpieza", "Higiene Personal"], size=(200, -1))
        
        # Campo para la Fecha de Vencimiento
        lbl_venc = wx.StaticText(panel, label="Vencimiento (DD/MM/AAAA):")
        self.txt_venc = wx.TextCtrl(panel, size=(200, -1))

        # Agregar los elementos usando AddMany
        fgs.AddMany([lbl_nombre, self.txt_nombre, lbl_precio, self.txt_precio, lbl_stock, self.txt_stock, lbl_cat, self.cb_categoria,lbl_venc, self.txt_venc])
        fgs.AddGrowableCol(1, 1)
        sizer_form.Add(fgs, 1, wx.ALL | wx.EXPAND, 10)

        # Botones Laterales
        sizer_botones_acciones = wx.BoxSizer(wx.VERTICAL)
        btn_agregar = wx.Button(panel, label="+ Agregar", size=(120, 35))
        btn_agregar.SetBackgroundColour(wx.Colour(144, 238, 144))
        btn_modificar = wx.Button(panel, label=" Modificar", size=(120, 35))
        btn_modificar.SetBackgroundColour(wx.Colour(255, 200, 100))
        btn_eliminar = wx.Button(panel, label="Eliminar", size=(120, 35))
        btn_eliminar.SetBackgroundColour(wx.Colour(240, 128, 128))
        
        #Acomodamos los botones uno abajo del otro 
        sizer_botones_acciones.Add(btn_agregar, 0, wx.BOTTOM, 8)
        sizer_botones_acciones.Add(btn_modificar, 0, wx.BOTTOM, 8)
        sizer_botones_acciones.Add(btn_eliminar, 0, wx.BOTTOM, 8)

        sizer_superior.Add(sizer_form, 1, wx.EXPAND | wx.ALL, 10)
        sizer_superior.Add(sizer_botones_acciones, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)

        # Tabla donde se muestra todos los productos registrados
        self.lista_productos = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista_productos.InsertColumn(0, 'ID', width=50)
        self.lista_productos.InsertColumn(1, 'Producto', width=150)
        self.lista_productos.InsertColumn(2, 'Precio', width=100)
        self.lista_productos.InsertColumn(3, 'Stock', width=80)
        self.lista_productos.InsertColumn(4, 'Categoría', width=120)
        self.lista_productos.InsertColumn(5, 'F. Vencimiento', width=120) 

        # Binds de acciones
        btn_agregar.Bind(wx.EVT_BUTTON, self.OnAgregarProducto)
        btn_modificar.Bind(wx.EVT_BUTTON, self.OnModificarProducto)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.OnEliminarProducto)
        self.lista_productos.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnProductoSeleccionado)

        # Footer y botón volver
        sizer_inferior = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_status = wx.StaticText(panel, label="Datos guardados")
        self.lbl_status.SetForegroundColour(wx.Colour(34, 139, 34))
        self.lbl_status.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        btn_volver = wx.Button(panel, label="Volver", size=(100, 30))
        btn_volver.SetBackgroundColour(wx.Colour(255, 200, 200))
        btn_volver.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        sizer_inferior.Add(self.lbl_status, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 15)
        sizer_inferior.Add(btn_volver, 0, wx.RIGHT | wx.BOTTOM, 10)
        #Armamos el diseño de la pantalla
        sizer_global.Add(sizer_superior, 0, wx.EXPAND)
        sizer_global.Add(self.lista_productos, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        sizer_global.Add(sizer_inferior, 0, wx.EXPAND | wx.TOP, 15)

        panel.SetSizer(sizer_global)
        self.cargar_lista()

    def cargar_lista(self):
        #Limpia la tabla y vuelve a cargar todos los productos del JSON 
        self.lista_productos.DeleteAllItems()
        for producto in self.productos:
            # Trae la fecha si existe, sino pone vacío
            f_venc = producto.get("fecha_vencimiento", "")
            self.lista_productos.Append([
                str(producto["id"]),
                producto["nombre"],
                f"${int(producto['precio']):,}".replace(",", "."),
                str(producto["stock"]),
                producto["categoria"],
                f_venc
            ])
          
    def OnProductoSeleccionado(self, event):
        #Cuando el usuario hace click en un producto de la lista
        #pasa los datos de la fila al formulario
        idx = event.GetIndex()
        self.txt_nombre.SetValue(self.lista_productos.GetItemText(idx, 1))
        self.txt_precio.SetValue(self.lista_productos.GetItemText(idx, 2).replace("$", ""))
        self.txt_stock.SetValue(self.lista_productos.GetItemText(idx, 3))
        self.cb_categoria.SetValue(self.lista_productos.GetItemText(idx, 4))
        self.txt_venc.SetValue(self.lista_productos.GetItemText(idx, 5))

    def OnAgregarProducto(self, event):
        #Toma los datos del formulario, los valida y guarda el producto nuevo
        nombre = self.txt_nombre.GetValue().strip()
        precio_raw = self.txt_precio.GetValue().strip()
        stock_raw = self.txt_stock.GetValue().strip()
        categoria = self.cb_categoria.GetValue()
        fecha_venc = self.txt_venc.GetValue().strip() # Captura la fecha

        if not (nombre and precio_raw and stock_raw and categoria and fecha_venc):
            wx.MessageBox("Completa todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Validar y convertir números y fechas de forma segura
        try:
            precio = float(precio_raw)
            stock = int(stock_raw)
            datetime.strptime(fecha_venc, "%d/%m/%Y")
        except ValueError:
            wx.MessageBox("Precio/Stock deben ser numéricos, y la fecha debe tener el formato DD/MM/AAAA.", "Error de tipos", wx.OK | wx.ICON_ERROR)
            return

        # Calcular nuevo ID
        nuevo_id = max([p["id"] for p in self.productos], default=0) + 1

        # Construimos el diccionario con todos los campos
        nuevo_producto = { 
            "id": nuevo_id,
            "nombre": nombre,
            "precio": precio,
            "stock": stock, 
            "categoria": categoria, 
            "fecha_vencimiento": fecha_venc }
        self.productos.append(nuevo_producto)

        # Guardamos los cambios en el archivo JSON
        guardar_productos(self.productos)
        self.cargar_lista()
        self.lbl_status.SetLabel("Producto agregado con éxito")

        # Limpia el formulario para dejarlo listo para otra carga
        self.txt_nombre.Clear()
        self.txt_precio.Clear()
        self.txt_stock.Clear()
        self.txt_venc.Clear()
        self.cb_categoria.SetSelection(wx.NOT_FOUND)

    def OnModificarProducto(self, event):
        #Modifica el precio del producto 
        seleccionado = self.lista_productos.GetFirstSelected()
        if seleccionado != -1:
            id_prod = int(self.lista_productos.GetItemText(seleccionado, 0))
            for prod in self.productos:
                if prod["id"] == id_prod:
                    dlg = wx.TextEntryDialog(self, f"Modificar precio para {prod['nombre']}:", "Modificar", str(prod['precio']))
                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            prod['precio'] = float(dlg.GetValue())
                            guardar_productos(self.productos)
                            self.cargar_lista()
                            self.lbl_status.SetLabel(" Producto modificado")
                        except ValueError:
                            wx.MessageBox("Por favor ingresa un número válido.", "Error")
                    dlg.Destroy()
                    break
        else:
            wx.MessageBox("Selecciona un producto de la lista.", "Aviso", wx.OK | wx.ICON_WARNING)

    def OnEliminarProducto(self, event):
        #Saca el producto de la lista y lo borra del archivo JSON 
        seleccionado = self.lista_productos.GetFirstSelected()
        if seleccionado != -1:
            if wx.MessageBox("¿Eliminar producto?", "Confirmar", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                id_prod = int(self.lista_productos.GetItemText(seleccionado, 0))
                self.productos = [p for p in self.productos if p["id"] != id_prod]
                guardar_productos(self.productos)
                self.cargar_lista()
                self.lbl_status.SetLabel(" Producto eliminado")
        else:
            wx.MessageBox("Selecciona un producto de la lista.", "Aviso", wx.OK | wx.ICON_WARNING)