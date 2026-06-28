import wx
# Módulo avanzado de wxPython, fundamental para poder usar el componente de pantalla 
# de bienvenida (SplashScreen)
import wx.adv
# Conecta el Menú Principal para mostrarlo automáticamente cuando termine de verse el logo
from menu_principal import VentanaMenuPrincipal

# CONFIGURACIÓN DEL ARRANQUE DE LA APLICACIÓN (CON SPLASH SCREEN)
if __name__ == "__main__":
    #Inicializamos la aplicación una sola vez
    app = wx.App(False)
    
    # Intentamos cargar el logo
    try:
        imagen_logo = wx.Image("logo.png", wx.BITMAP_TYPE_PNG)
        
        # Ajustamos el tamaño para el logo
        ancho_deseado = 450
        alto_deseado = 350
        imagen_redimensionada = imagen_logo.Scale(ancho_deseado, alto_deseado, wx.IMAGE_QUALITY_HIGH)
        
        # Convertimos a Bitmap
        bitmap_logo = wx.Bitmap(imagen_redimensionada)
        
        # Creamos el Splash Screen (2.5 segundos)
        splash = wx.adv.SplashScreen(
            bitmap_logo, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,  2500,  None, -1)
        splash.Show()
        
    except Exception as e:
        print(f"Aviso: No se pudo mostrar el Splash Screen ({e})")
        splash = None

    #Inicializamos la Ventana Principal de fondo (espera oculta)
    frame_principal = VentanaMenuPrincipal()
    
    #Función encargada de mostrar el menú cuando el Splash termine
    def AlCerrarSplash(event):
        frame_principal.Show()
        if splash:
            splash.Destroy()
            
    #Controlamos el flujo según si la imagen cargó o no
    if splash:
        splash.Bind(wx.EVT_CLOSE, AlCerrarSplash)
    else:
        frame_principal.Show()
    
    #Arranca el bucle único de la aplicación
    app.MainLoop()