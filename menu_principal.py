# Importa la librería principal para renderizar el menú, la barra de estado y los botones
import wx
from gestion_productos import VentanaGestionProducto
from registro_ventas import VentanaRegistroVenta
from ver_stock import VentanaVerStock
# Permite capturar la hora del sistema en tiempo real para mostrarla abajo en la barra de estado
from datetime import datetime

# VENTANA 1: MENÚ PRINCIPAL

class VentanaMenuPrincipal(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Control de Stock", size=(600, 450))
        self.SetMinSize((600, 450))
        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(245, 245, 245))

        #Barra de Menú superior para acceder a las opciones del sistema
        menu_bar = wx.MenuBar()
        #Pestaña Archivo
        menu_archivo = wx.Menu()
        item_m_gestionar = menu_archivo.Append(wx.ID_ANY, "Gestionar productos")
        item_m_ventas = menu_archivo.Append(wx.ID_ANY, "Registrar ventas")
        item_m_stock = menu_archivo.Append(wx.ID_ANY, "Ver stock")

        menu_archivo.AppendSeparator()

        menu_guardar = menu_archivo.Append(wx.ID_SAVE, "Guardar")
        menu_archivo.Append(wx.ID_ANY, "Configuración")

        menu_archivo.AppendSeparator()

        menu_salir = menu_archivo.Append(wx.ID_EXIT, "Salir")
        #Pestaña Ayuda
        menu_ayuda = wx.Menu()
        item_manual = menu_ayuda.Append(wx.ID_ANY, "Manual de Uso")
        item_acerca_de = menu_ayuda.Append(wx.ID_ABOUT, "Acerca de...")
        #Agregamos las pestañas a la barra superior prncipal
        menu_bar.Append(menu_archivo, "Archivo")
        menu_bar.Append(menu_ayuda, "Ayuda")
        self.SetMenuBar(menu_bar)

        # Binds de la barra de menú
        self.Bind(wx.EVT_MENU, self.OnSalir, menu_salir)
        self.Bind(wx.EVT_MENU, self.OnGuardar, menu_guardar)
        self.Bind(wx.EVT_MENU, self.OnMostrarCreditos, item_acerca_de)
        self.Bind(wx.EVT_MENU, self.OnAbrirGestion, item_m_gestionar)
        self.Bind(wx.EVT_MENU, self.OnAbrirVentas, item_m_ventas)
        self.Bind(wx.EVT_MENU, self.OnAbrirStock, item_m_stock)
        self.Bind(wx.EVT_MENU, self.OnMostrarManual, item_manual) 

        # 2. Diseño de la Interfaz (Sizer)
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        #Texto del nombre de la aplicación 
        lbl_logo = wx.StaticText(panel, label="\nCONTROL\nDE STOCK", style=wx.ALIGN_CENTER)
        lbl_logo.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_logo.SetForegroundColour(wx.Colour(20, 40, 80))
        sizer_principal.Add(lbl_logo, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Botones Principales para navegar entre las distintas ventanas
        color_boton = wx.Colour(255, 180, 180)
        btn_gestionar = wx.Button(panel, label="Gestionar productos", size=(250, 40))
        btn_ventas = wx.Button(panel, label="Registrar ventas", size=(250, 40))
        btn_stock = wx.Button(panel, label="Ver stock", size=(250, 40))
        btn_salir = wx.Button(panel, label="Salir", size=(250, 40))

        for btn in [btn_gestionar, btn_ventas, btn_stock, btn_salir]:
            btn.SetBackgroundColour(color_boton)
            btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            sizer_principal.Add(btn, 0, wx.ALIGN_CENTER | wx.TOP, 12)

        # Binds de los botones principales 
        btn_gestionar.Bind(wx.EVT_BUTTON, self.OnAbrirGestion)
        btn_ventas.Bind(wx.EVT_BUTTON, self.OnAbrirVentas)
        btn_stock.Bind(wx.EVT_BUTTON, self.OnAbrirStock)
        btn_salir.Bind(wx.EVT_BUTTON, self.OnSalir)

        panel.SetSizer(sizer_principal)

        # Barra de Estado inferior donde se muestra un mensaje junto con la fecha y hora actual
        self.statusbar = self.CreateStatusBar(1)
        fecha_hora = datetime.now().strftime("%d/%m/%Y    %H:%M:%S")
        self.statusbar.SetStatusText(   f"Bienvenidos al sistema de control de stock        {fecha_hora}")
    
    def OnAbrirGestion(self, event):
        #Abre la ventana 2 
        ventana_gestion = VentanaGestionProducto(self)
        ventana_gestion.Show()

    def OnAbrirStock(self, event):
        #Abre la ventana 4
        ventana = VentanaVerStock(self)
        ventana.Show()

    def OnAbrirVentas(self, event):
        #Abre la ventana 3
        ventana_ventas = VentanaRegistroVenta(self)
        ventana_ventas.Show()

    def OnGuardar(self, event):
        wx.MessageBox("¡Los datos del sistema se han guardado con éxito!", "Guardado", wx.OK | wx.ICON_INFORMATION)

    def OnMostrarCreditos(self, event):
        wx.MessageBox("Sistema de Control de Stock v1.0\n\nDesarrollado por Melany Caballero y Alejandra Macedo\n\nMateria:Programación Orientada a Objetos\n\nProfesor:Javier Castrillo\n Año: 2026", "Créditos", wx.OK | wx.ICON_INFORMATION)

    def OnSalir(self, event):
        #Cierra la aplicación 
        self.Close()

    #Muestra el manual de uso en la pestaña Ayuda
    def OnMostrarManual(self, event):
        texto_manual = (
            "MANUAL DE USO\n"
            "====================================================================\n\n"
            "1. GESTIÓN DE PRODUCTOS:\n"
            "   - Permite dar de alta, modificar precios o eliminar productos.\n"
            "   - IMPORTANTE: Al ingresar la fecha de vencimiento, use estrictamente el formato DD/MM/AAAA (ej: 25/12/2026).\n\n"

            "2. REGISTRO DE VENTAS:\n"
            "   - Seleccione el producto, indique la cantidad y agréguelo al carrito.\n"
            "   - El stock real del sistema NO se modificará hasta que presione 'Confirmar Venta'.\n\n"

            "3. CONTROL DE STOCK (CÓDIGO DE COLORES):\n"
            "   En la ventana de Ver Stock, las filas se pintarán automáticamente según su urgencia de vencimiento:\n"
            "   - ROJO: El producto ya venció o vencerá en menos de 7 días. ¡Requiere atención urgente!\n"
            "   - AMARILLO: Vencimiento intermedio (vence entre 7 y 30 días).\n"
            "   - VERDE: Producto seguro (le queda más de un mes de margen para su venta).\n"
            "=====================================================================\n\n")
        
        wx.MessageBox(texto_manual, "Manual de Uso del Sistema", wx.OK | wx.ICON_INFORMATION)