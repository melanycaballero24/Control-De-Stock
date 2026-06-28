import wx
# Trae las funciones para leer los precios y descontar el stock en el JSON
from datos import cargar_productos, guardar_productos
#Se encarga de enviar el texto del ticket a la impresora o generador PDF
class TicketPrintout(wx.Printout):

    def __init__(self, texto):
        super().__init__()
        self.texto = texto
    
    def OnPrintPage(self, page):
        #Dibuja el contenido del ticket línea por línea
        dc = self.GetDC()

        dc.DrawText("TICKET DE VENTA", 100, 100)

        y = 140
        for linea in self.texto.split("\n"):
            dc.DrawText(linea, 100, y)
            y += 25

        return True

    def HasPage(self, page):
        return page == 1

    def GetPageInfo(self):
        return (1, 1, 1, 1)
    
# VENTANA 3: REGISTRO DE VENTA
class VentanaRegistroVenta(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Registro de venta", size=(800, 550))
        #Cargamos los productos guardados para utilizarlos en la venta 
        self.productos = cargar_productos()
        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(245, 245, 245))

        sizer_global = wx.BoxSizer(wx.VERTICAL)

        # Zona Superior Selector
        caja_agregar = wx.StaticBox(panel, label="Agregar productos")
        sizer_agregar = wx.StaticBoxSizer(caja_agregar, wx.HORIZONTAL)

        lbl_prod = wx.StaticText(panel, label="Producto: ")
        #Creamos una lista con los productos para mostrarlos en el ComboBox
        nombres_productos = []

        for producto in self.productos:
           nombres_productos.append(producto["nombre"])
  
        self.cb_prod = wx.ComboBox(panel, choices=nombres_productos, size=(150, -1)) 
        
        lbl_cant = wx.StaticText(panel, label="Cantidad: ")
        self.spin_cant = wx.SpinCtrl(panel, value="0", size=(60, -1), min=1, max=100)
        #Acá se mostrará un aviso del stock disponible
        self.lbl_stock_aviso = wx.StaticText(panel,label="",size=(180,30),style=wx.ALIGN_CENTER)
        self.lbl_stock_aviso.SetBackgroundColour(wx.Colour(220, 245, 220))
        self.lbl_stock_aviso.SetForegroundColour(wx.Colour(0, 100, 0))
        self.lbl_stock_aviso.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        btn_carrito = wx.Button(panel, label="+ Agregar al carrito", size=(150, 35))
        btn_carrito.SetBackgroundColour(wx.Colour(255, 180, 180))
        #Acomodamos los elementos del sizer de la zona superior
        sizer_agregar.Add(lbl_prod, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        sizer_agregar.Add(self.cb_prod, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer_agregar.Add(lbl_cant, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 15)
        sizer_agregar.Add(self.spin_cant, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer_agregar.Add(self.lbl_stock_aviso, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        sizer_agregar.Add(btn_carrito, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        # Zona Media Carrito y Total
        sizer_medio = wx.BoxSizer(wx.HORIZONTAL)
        #Acá se muestra la tabla de los productos agregados al carrito
        self.lista_carrito = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista_carrito.InsertColumn(0, 'Producto', width=140)
        self.lista_carrito.InsertColumn(1, 'Cantidad', width=70)
        self.lista_carrito.InsertColumn(2, 'Precio Unit.', width=90)
        self.lista_carrito.InsertColumn(3, 'Subtotal', width=90)

        btn_quitar = wx.Button(panel, label="Quitar", size=(80, 35))
        btn_quitar.SetBackgroundColour(wx.Colour(210, 50, 50))
        btn_quitar.SetForegroundColour(wx.WHITE)
        #Panel que resalta el monto total de la compra 
        panel_total = wx.Panel(panel,size=(180, 120), style=wx.BORDER_THEME)
        panel_total.SetBackgroundColour(wx.Colour(240, 240, 240))
        sizer_total_box = wx.BoxSizer(wx.VERTICAL)
        lbl_total_t = wx.StaticText(panel_total, label="TOTAL:", style=wx.ALIGN_CENTER)
        lbl_total_t.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.lbl_total_num = wx.StaticText(panel_total, label="$0", style=wx.ALIGN_CENTER)
        self.lbl_total_num.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_total_num.SetForegroundColour(wx.Colour(0, 128, 0))

        sizer_total_box.Add(lbl_total_t, 0, wx.EXPAND | wx.TOP, 15)
        sizer_total_box.Add(self.lbl_total_num, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        panel_total.SetSizer(sizer_total_box)

        sizer_medio.Add(self.lista_carrito, 1, wx.EXPAND | wx.ALL, 10)
        sizer_medio.Add(btn_quitar, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer_medio.Add(panel_total, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        # Acciones inferiores
        sizer_inferior_botones = wx.BoxSizer(wx.HORIZONTAL)
        btn_confirmar = wx.Button(panel, label="Confirmar Venta", size=(150, 35))
        btn_confirmar.SetBackgroundColour(wx.Colour(46, 139, 87))
        btn_confirmar.SetForegroundColour(wx.WHITE)
        
        btn_cancelar = wx.Button(panel, label="Cancelar", size=(120, 35))
        btn_cancelar.SetBackgroundColour(wx.Colour(255, 200, 100))
        
        btn_pdf = wx.Button(panel, label="Imprimir PDF", size=(150, 35))
        btn_pdf.SetBackgroundColour(wx.Colour(70, 130, 180))
        btn_pdf.SetForegroundColour(wx.WHITE)

        sizer_inferior_botones.Add(btn_confirmar, 0, wx.LEFT, 10)
        sizer_inferior_botones.Add(btn_cancelar, 0, wx.LEFT, 10)
        sizer_inferior_botones.AddStretchSpacer()
        sizer_inferior_botones.Add(btn_pdf, 0, wx.RIGHT, 10)

        lbl_nota = wx.StaticText(panel, label="Importante: el stock se actualizará al confirmar la venta.")
        lbl_nota.SetBackgroundColour(wx.Colour(230, 242, 255))
        lbl_nota.SetForegroundColour(wx.Colour(25, 75, 140))

        # Asociamos cada evento con su función correspondiente 
        self.cb_prod.Bind(wx.EVT_COMBOBOX, self.OnCambiarProducto)
        btn_carrito.Bind(wx.EVT_BUTTON, self.OnAgregarAlCarrito)
        btn_quitar.Bind(wx.EVT_BUTTON, self.OnQuitarDelCarrito)
        btn_confirmar.Bind(wx.EVT_BUTTON, self.OnConfirmarVenta)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.OnCancelarVenta)
        btn_pdf.Bind(wx.EVT_BUTTON, self.OnImprimirPDF)

        sizer_global.Add(sizer_agregar, 0, wx.EXPAND | wx.ALL, 10)
        sizer_global.Add(wx.StaticText(panel, label="Carrito de compra"), 0, wx.LEFT, 15)
        sizer_global.Add(sizer_medio, 1, wx.EXPAND)
        sizer_global.Add(sizer_inferior_botones, 0, wx.EXPAND | wx.BOTTOM, 15)
        sizer_global.Add(lbl_nota, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer_global)

    def OnCambiarProducto(self,event):
        #Obtenemos el producto elegido por el usuario
        producto_seleccionado = self.cb_prod.GetValue()
        #Buscamos el producto dentro de la lista cargada 
        for producto in self.productos:

         if producto["nombre"] == producto_seleccionado:
 
            self.lbl_stock_aviso.SetLabel(f" Stock disponible: {producto['stock']} unidades")
            return
         self.lbl_stock_aviso.SetLabel(
         "Stock disponible: 0 unidades" )

    def RecalcularTotal(self):

        total = 0
        #Recorremos todos los productos agregados al carrito
        for i in range(self.lista_carrito.GetItemCount()):

         subtotal_texto = self.lista_carrito.GetItemText(i, 3)

         subtotal_limpio = subtotal_texto.replace("$", "").strip()

         total += float(subtotal_limpio)

        self.lbl_total_num.SetLabel(f"${int(total)}")

    def OnAgregarAlCarrito(self, event):
        #Obtenemos el producto y la cantidad elegidos
        producto = self.cb_prod.GetValue()
        cantidad = self.spin_cant.GetValue()

        if producto:
            #Cargamos los productos para obtener su precio actual
            productos = cargar_productos()
            precio_unit = 0
            #Buscamos el precio del producto 
            for p in productos:
                if p["nombre"] == producto:
                    precio_unit = float(p["precio"])
                    break

            subtotal = precio_unit * cantidad
            #Lo agregamos a la lista visual del carrito
            self.lista_carrito.Append([
                producto,
                str(cantidad),
                f"${int(precio_unit)}",
                f"${int(subtotal)}"
            ])

            self.RecalcularTotal()

        else:
            wx.MessageBox(
                "Selecciona un producto.","Error",wx.OK | wx.ICON_ERROR)
        
    def OnQuitarDelCarrito(self, event):
        seleccionado = self.lista_carrito.GetFirstSelected()
        if seleccionado != -1:
            self.lista_carrito.DeleteItem(seleccionado)
            self.RecalcularTotal()
        else:
            wx.MessageBox("Selecciona un elemento para quitar.", "Aviso", wx.OK | wx.ICON_WARNING)

    def OnConfirmarVenta(self, event):
        if wx.MessageBox("¿Confirmar venta?", "Venta", wx.YES_NO | wx.ICON_QUESTION) != wx.YES:
          return
          
        # Cargamos nuevamente los productos para actualizar el stock
        productos = cargar_productos()
        # Creamos el texto que funcionará como ticket de compra 
        ticket = "VENTA REALIZADA\n\n"
        #Recorremos cada articulo que se agrego al carrito
        for i in range(self.lista_carrito.GetItemCount()):
            nombre_producto = self.lista_carrito.GetItemText(i, 0)
            cantidad_vendida = int(self.lista_carrito.GetItemText(i, 1))
            #Descontamos el stock en nustra lista de datos
            for producto in productos:
              if producto["nombre"] == nombre_producto:
                 producto["stock"] -= cantidad_vendida
                 subtotal = self.lista_carrito.GetItemText(i, 3)
                 ticket += (f"{nombre_producto} x{cantidad_vendida}" f" = {subtotal}\n" )
                 break
                 
        # Guardamos el stock en el archivo JSON 
        guardar_productos(productos)

        ticket += f"\nTOTAL: {self.lbl_total_num.GetLabel()}"

        # Mostramos el ticket de venta pero preguntando si desea imprimirlo
        mensaje_pregunta = f"{ticket}\n\n¿Desea imprimir el ticket de venta?"
        
        # Guardamos la respuesta del usuario (wx.YES o wx.NO)
        respuesta = wx.MessageBox(mensaje_pregunta, "Ticket de Venta", wx.YES_NO | wx.ICON_INFORMATION)
        
        # Si el usuario responde que SÍ, llamamos internamente a la función de imprimir
        if respuesta == wx.YES:
            self.OnImprimirPDF(event=None) 

        # Limpiamos el carrito para la próxima venta
        self.lista_carrito.DeleteAllItems()
        self.RecalcularTotal()

        self.Close()

    def OnCancelarVenta(self, event):
        if wx.MessageBox("¿Cancelar venta actual?", "Cancelar", wx.YES_NO) == wx.YES:
            self.Close()
            
    #Guardamos el ticket en PDF
    def OnImprimirPDF(self, event):

     ticket = "VENTA REALIZADA\n\n"

     for i in range(self.lista_carrito.GetItemCount()):

        producto = self.lista_carrito.GetItemText(i, 0)
        cantidad = self.lista_carrito.GetItemText(i, 1)
        subtotal = self.lista_carrito.GetItemText(i, 3)

        ticket += f"{producto} x{cantidad} = {subtotal}\n"

     ticket += f"\nTOTAL: {self.lbl_total_num.GetLabel()}"

     printout = TicketPrintout(ticket)

     printer = wx.Printer()

     if not printer.Print(self, printout, True):
        wx.MessageBox( "No se pudo imprimir.","Error", wx.OK | wx.ICON_ERROR  )
     
     printout.Destroy()