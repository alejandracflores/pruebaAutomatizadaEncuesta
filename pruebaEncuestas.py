from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import os
from datetime import datetime

# Variables globales
desarrollador = ""  # Se configurará mediante input del usuario
fecha_inicio = ""
fecha_fin = ""
ruta_base = 'C:\\Users\\Usuario\\Downloads\\RESULTADOS_ENCUESTA\\'
evidencias = []

# Datos de prueba
DATOS_PRUEBA = [
    {
        "email": "acruz116@alumnos.uaq.mx",
        "nombre": "Alejandra",
        "asistencia": "Si,  allí estaré",
        "recomendacion": "Todo ha estado muy bien profesor, gracias",
        "edad": "Entre 15 y 18 años",
        "propuestas": ["Artículos de investigación", "Sesiones enlínea"]
    },
    {
        "email": "est.alejandram.cruz@unimilitar.edu.co",
        "nombre": "María",
        "asistencia": "No, no puedo asistir",
        "recomendacion": "Todo ha estado muy bien profesor, gracias :)",
        "propuestas": ["Grabaciones", "Foros"],
        "edad": "Más de 35 años"
    }
]

# Solicitar el nombre del desarrollador
def configurar_desarrollador():
    global desarrollador
    desarrollador = input("Por favor, ingresa tu nombre: ")
    print(f"Hola {desarrollador}! Iniciando prueba automatizada...")

# Crear carpeta para guardar resultados de la prueba
def crear_carpeta_resultados():
    global ruta_base
    carpeta_prueba = time.strftime("%Y-%m-%d_%H-%M-%S")
    ruta_Reporte = os.path.join(ruta_base, carpeta_prueba)
    os.makedirs(ruta_Reporte, exist_ok=True)
    return ruta_Reporte

# Inicializar el navegador
def iniciar_navegador():
    try:
        driver_path = "C:\\Users\\Usuario\\Downloads\\Instaladores y Programas\\chromedriver.exe"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        return driver
    except WebDriverException as e:
        evidencias.append(f"Error al iniciar el navegador: {e}")
        print(f"Error al iniciar el navegador: {e}")
        exit(1)

# Llenar el formulario con los datos proporcionados
def llenar_encuesta(driver, datos_persona, numero_persona, ruta_Reporte):
    try:
        # Navegar a la URL del formulario
        driver.get("https://forms.gle/E25iWovVTz3KroXt9")
        time.sleep(2)
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_inicio.png"))
        evidencias.append(f"Persona {numero_persona} - Inicio de formulario: Correcto")

        # 1. Ingresar email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i1 i4']"))
        )
        email_input.send_keys(datos_persona['email'])
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_correo.png"))
        evidencias.append(f"Persona {numero_persona} - Email ingresado: Correcto")

        # 2. Ingresar nombre
        nombre_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i6 i9']"))
        )
        nombre_input.send_keys(datos_persona['nombre'])
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_nombre.png"))
        evidencias.append(f"Persona {numero_persona} - Nombre ingresado: Correcto")

        # 3. Seleccionar asistencia
        opcion_asistencia = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{datos_persona['asistencia']}')]"))
        )
        opcion_asistencia.click()
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_asistencia.png"))
        evidencias.append(f"Persona {numero_persona} - Asistencia seleccionada: Correcto")

        # 4. Ingresar recomendación
        recomendacion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i22 i25']"))
        )
        recomendacion_input.send_keys(datos_persona['recomendacion'])
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_recomendacion.png"))
        evidencias.append(f"Persona {numero_persona} - Recomendación ingresada: Correcto")

        # 5. Seleccionar propuestas
        for propuesta in datos_persona['propuestas']:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{propuesta}')]"))
            )
            checkbox.click()
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_propuestas.png"))
        evidencias.append(f"Persona {numero_persona} - Propuestas seleccionadas: Correcto")

        # 6. Seleccionar edad
        listbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']"))
        )
        listbox.click()
        opcion_edad = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{datos_persona['edad']}')]"))
        )
        opcion_edad.click()
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_edad.png"))
        evidencias.append(f"Persona {numero_persona} - Edad seleccionada: Correcto")

        # 7. Enviar el formulario
        boton_enviar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enviar')]"))
        )
        boton_enviar.click()
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_final.png"))
        evidencias.append(f"Persona {numero_persona} - Formulario enviado: Correcto")

    except Exception as e:
        evidencias.append(f"Error para persona {numero_persona}: {e}")
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_error.png"))

# Generar un reporte con las evidencias recopiladas
def generar_reporte(ruta_Reporte):
    with open(os.path.join(ruta_Reporte, "reporte_encuesta.txt"), "w", encoding="utf-8") as archivo:
        archivo.write(f"Desarrollador: {desarrollador}\nFecha inicio: {fecha_inicio}\nFecha fin: {fecha_fin}\n")
        archivo.write("\nEvidencias:\n")
        for evidencia in evidencias:
            archivo.write(f"- {evidencia}\n")

def ejecutar_prueba_automatizada():
    global fecha_inicio, fecha_fin
    fecha_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
    ruta_Reporte = crear_carpeta_resultados()
    driver = iniciar_navegador()

    try:
        for i, datos in enumerate(DATOS_PRUEBA, 1):
            llenar_encuesta(driver, datos, i, ruta_Reporte)
            time.sleep(2)
    finally:
        driver.quit()
        fecha_fin = time.strftime("%Y-%m-%d %H:%M:%S")
        generar_reporte(ruta_Reporte)

if __name__ == "__main__":
    configurar_desarrollador()
    ejecutar_prueba_automatizada()

