"""
Automatización Front Ejercicio 2 prueba KATA banco de bogota
Autor: Andres Rincon
Fecha: Marzo de 2025
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Constantes de configuración
LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
VALID_USER = "Admin"
VALID_PASS = "admin123"

# Localizadores (objetos de la pagina)
class Locators:
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, ".oxd-alert-content")
    REQUIRED_MSGS = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

def setup_driver():
    # Inicializa y configura el WebDriver de Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def perform_login(driver, username, password):
    # Realiza el proceso de login con las credenciales proporcionadas
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.USERNAME))
    
    driver.find_element(*Locators.USERNAME).send_keys(username)
    driver.find_element(*Locators.PASSWORD).send_keys(password)
    driver.find_element(*Locators.LOGIN_BTN).click()

def test_credenciales_invalidas(driver):
    # Prueba de login con credenciales inválidas
    perform_login(driver, "AdminIncorrecto", "admin12345")
    error = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(Locators.ERROR_MSG))
    assert "Invalid credentials" in error.text, "¡El mensaje de error no apareció!"
    print("✅ Prueba 1: Mensaje de credenciales inválidas validado")

def test_username_vacio(driver):
    # Prueba con username vacío y contraseña válida
    perform_login(driver, "", VALID_PASS)
    required_msg = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(Locators.REQUIRED_MSGS))
    assert "Required" in required_msg.text, "¡El mensaje de requerido no apareció!"
    print("✅ Prueba 2: Mensaje de campo requerido validado")

def test_campos_vacios(driver):
    # Prueba con ambos campos vacíos
    perform_login(driver, "", "")
    required_msgs = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(Locators.REQUIRED_MSGS))
    assert len(required_msgs) == 2, "¡No se mostraron ambos mensajes de requerido!"
    print("✅ Prueba 3: Mensajes de campos requeridos validados")

def test_validacion_login(driver):
    # Prueba de login exitoso
    perform_login(driver, VALID_USER, VALID_PASS)
    WebDriverWait(driver, 10).until(EC.url_contains("index"))
    assert "index" in driver.current_url, "¡No se redireccionó correctamente!"
    print("✅ Prueba 4: Login correcto realizado")

if __name__ == "__main__":
    driver = setup_driver()
    
    try:
        # Ejecutar pruebas secuencialmente
        test_credenciales_invalidas(driver)
        time.sleep(3)
        test_username_vacio(driver)
        time.sleep(3)
        test_campos_vacios(driver)
        time.sleep(3)
        test_validacion_login(driver)
        
    except AssertionError as e:
        print(f"❌ Error en pruebas: {str(e)}")
        
    finally:
        input("\nPresiona Enter para cerrar el navegador...")
        driver.quit()