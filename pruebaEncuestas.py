from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
import time
import os
from datetime import datetime

# Variables globales
desarrollador = ""
fecha_inicio = ""
fecha_fin = ""
ruta_base = 'C:\\Users\\Usuario\\Downloads\\RESULTADOS_ENCUESTA\\'
evidencias = []

DATOS_PRUEBA = [
    {
        "email": "acruz116@alumnos.uaq.mx",
        "nombre": "Alejandra",
        "asistencia": "Si, allí estaré",
        "recomendacion": "Todo ha estado muy bien profesor, gracias",
        "edad": "Entre 15 y 18 años",
        "propuestas": ["Artículos de investigación", "Sesiones en línea"]
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

def configurar_desarrollador():
    global desarrollador
    desarrollador = input("Por favor, ingresa tu nombre: ")
    print(f"Hola {desarrollador}! Iniciando prueba automatizada...")

def crear_carpeta_resultados():
    global ruta_base
    carpeta_prueba = time.strftime("%Y-%m-%d_%H-%M-%S")
    ruta_Reporte = os.path.join(ruta_base, carpeta_prueba)
    if not os.path.exists(ruta_Reporte):
        os.makedirs(ruta_Reporte)
    return ruta_Reporte

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

def llenar_encuesta(driver, datos_persona, numero_persona, ruta_Reporte):
    try:
        driver.get("https://forms.gle/E25iWovVTz3KroXt9")
        time.sleep(2)
        driver.save_screenshot(os.path.join(ruta_Reporte, f"persona{numero_persona}_inicio.png"))

        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i1 i4']"))
            )
            email_input.send_keys(datos_persona['email'])
        except Exception as e:
            evidencias.append(f"Error al ingresar email para persona {numero_persona}: {e}")

        try:
            nombre_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i6 i9']"))
            )
            nombre_input.send_keys(datos_persona['nombre'])
        except Exception as e:
            evidencias.append(f"Error al ingresar nombre para persona {numero_persona}: {e}")

        try:
            opcion_asistencia = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{datos_persona['asistencia']}')]"))
            )
            opcion_asistencia.click()
        except Exception as e:
            evidencias.append(f"Error al seleccionar asistencia para persona {numero_persona}: {e}")

        try:
            recomendacion_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='i22 i25']"))
            )
            recomendacion_input.send_keys(datos_persona['recomendacion'])
        except Exception as e:
            evidencias.append(f"Error al ingresar recomendación para persona {numero_persona}: {e}")

        for propuesta in datos_persona['propuestas']:
            try:
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{propuesta}')]"))
                )
                checkbox.click()
            except Exception as e:
                evidencias.append(f"Error al seleccionar propuesta '{propuesta}' para persona {numero_persona}: {e}")

        try:
            listbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']"))
            )
            listbox.click()
            opcion_edad = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{datos_persona['edad']}')]"))
            )
            opcion_edad.click()
        except Exception as e:
            evidencias.append(f"Error al seleccionar edad para persona {numero_persona}: {e}")

        try:
            boton_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enviar')]"))
            )
            boton_enviar.click()
        except Exception as e:
            evidencias.append(f"Error al enviar formulario para persona {numero_persona}: {e}")

    except Exception as e:
        evidencias.append(f"Error general para persona {numero_persona}: {e}")

def generar_reporte(ruta_Reporte):
    with open(os.path.join(ruta_Reporte, "reporte_encuesta.txt"), "w", encoding="utf-8") as archivo:
        archivo.write(f"Desarrollador de la prueba: {desarrollador}\n")
        archivo.write(f"Fecha de inicio: {fecha_inicio}\n")
        archivo.write(f"Fecha de fin: {fecha_fin}\n")
        archivo.write("\nEvidencias de la prueba:\n")
        for evidencia in evidencias:
            archivo.write(f"- {evidencia}\n")
    print("Reporte generado.")

def ejecutar_prueba_automatizada():
    global fecha_inicio, fecha_fin
    fecha_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
    ruta_Reporte = crear_carpeta_resultados()
    driver = iniciar_navegador()

    try:
        for i, datos_persona in enumerate(DATOS_PRUEBA, 1):
            llenar_encuesta(driver, datos_persona, i, ruta_Reporte)
            time.sleep(2)
    finally:
        driver.quit()
        fecha_fin = time.strftime("%Y-%m-%d %H:%M:%S")
        generar_reporte(ruta_Reporte)

if __name__ == "__main__":
    configurar_desarrollador()
    ejecutar_prueba_automatizada()

