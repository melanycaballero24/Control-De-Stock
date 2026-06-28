import wx
from datos import cargar_productos
#Lo usamos para validar el vencimiento
from datetime import datetime

# VENTANA 4: VER STOCK
class VentanaVerStock(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Ver Stock", size=(800, 450)) # Más ancho para la columna de fechas
        self.productos = cargar_productos()
        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Tabla de stock
        self.lista_stock = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        
        # Columnas de la tabla
        self.lista_stock.InsertColumn(0, "ID", width=50)
        self.lista_stock.InsertColumn(1, "Producto", width=150)
        self.lista_stock.InsertColumn(2, "Precio", width=100)
        self.lista_stock.InsertColumn(3, "Stock", width=80)
        self.lista_stock.InsertColumn(4, "Categoría", width=120)
        self.lista_stock.InsertColumn(5, "F. Vencimiento", width=120) # Columna de fecha

        btn_volver = wx.Button(panel, label="Volver", size=(100, 30))
        btn_volver.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        
        # Fecha actual del sistema para comparar plazos
        hoy = datetime.now()

        # Recorremos todos los productos cargados y los agregamos a la tabla del stock 
        for producto in self.productos:
            # Obtenemos la fecha
            fecha_venc_str = producto.get("fecha_vencimiento", "")
            
            # Agregamos la fila a la tabla y guardamos el índice 
            index = self.lista_stock.Append([
                str(producto["id"]),
                producto["nombre"],
                f"${int(producto['precio'])}",
                str(producto["stock"]),
                producto["categoria"],
                fecha_venc_str
            ])

            # LÓGICA DE COLORES DE CONTROL
            if fecha_venc_str:
                try:
                    # Pasamos el string de la fecha a un objeto datetime real
                    fecha_venc = datetime.strptime(fecha_venc_str, "%d/%m/%Y")
                    # Restamos las fechas para obtener la diferencia en días continuos
                    dias_restantes = (fecha_venc - hoy).days

                    # Clasificación por colores
                    if dias_restantes < 7:
                        # Rojo suave para productos vencidos o a menos de 7 días de vencer
                        color_fondo = wx.Colour(255, 200, 200) 
                    elif dias_restantes <= 30:
                        # Amarillo suave para vencimiento medio (entre 7 y 30 días)
                        color_fondo = wx.Colour(255, 255, 200) 
                    else:
                        # Verde suave si le queda más de un mes de margen
                        color_fondo = wx.Colour(200, 255, 200)

                    # Pintamos la fila correspondiente
                    self.lista_stock.SetItemBackgroundColour(index, color_fondo)

                except ValueError:
                    pass

        sizer.Add(self.lista_stock, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_volver, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        panel.SetSizer(sizer)