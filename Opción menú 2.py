import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_2a():
    """
    Opción 2.a: Pide un drug_id y muestra su nombre, tipo molecular, estructura química e InChI-key.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 2.a: Información de un Fármaco Dado ---")
        drug_id_input = input("Introduce el identificador de ChEMBL del fármaco (drug_id): ").strip()
        
        if not drug_id_input:
            print(" El identificador no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f" Buscando información para el drug_id: {drug_id_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL
        # Se pide: drug_name, molecular_type, chemical_structure, inchi_key
        consulta = """
        SELECT drug_name, molecular_type, chemical_structure, inchi_key
        FROM drug
        WHERE drug_id = %s;
        """
        
        # Ejecutar la consulta con el ID proporcionado
        cursor.execute(consulta, (drug_id_input,))
        
        resultado = cursor.fetchone()

        # 4. PROCESAMIENTO Y SALIDA
        if resultado:
            # Desempaquetar los resultados para una presentación clara
            drug_name, molecular_type, chemical_structure, inchi_key = resultado
            
            print("\n Información del Fármaco encontrada:")
            print(f"   Nombre: {drug_name}")
            print(f"   Tipo Molecular: {molecular_type}")
            print(f"   Estructura Química: {chemical_structure}")
            print(f"   InChI-key: {inchi_key}")
        else:
            # No se encuentra el ID (comprobación de existencia)
            print(f"\n Fármaco no encontrado: No existe ningún registro para el drug_id '{drug_id_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")

ejecutar_opcion_2a()

import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA (para que sea autónoma) ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_2b():
    """
    Opción 2.b: Dado el nombre de un fármaco, muestra sus sinónimos.
    Busca en la tabla 'synonymous' usando el 'drug_id' obtenido de la tabla 'drug'.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 2.b: Sinónimos de un Fármaco Dado ---")
        drug_name_input = input("Introduce el nombre del fármaco: ").strip().upper() 
        
        if not drug_name_input:
            print(" El nombre del fármaco no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f" Buscando sinónimos para el fármaco: {drug_name_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL ÚNICA OPTIMIZADA
        # Se usa un JOIN para relacionar el nombre (drug.drug_name) con los sinónimos (synonymous.synonymous_name)
        consulta = """
        SELECT s.synonymous_name
        FROM drug d
        JOIN synonymous s ON d.drug_id = s.drug_id
        WHERE d.drug_name = %s;
        """
        
        cursor.execute(consulta, (drug_name_input,))
        
        resultados = cursor.fetchall()

        # 4. PROCESAMIENTO Y SALIDA
        if resultados:
            print(f"\n Sinónimos encontrados para '{drug_name_input}':")
            # Mostrar los sinónimos
            for i, fila in enumerate(resultados, 1):
                print(f"   {i}. {fila[0]}")
        else:
            # Comprobación de existencia. Puede significar que no existe el fármaco O no tiene sinónimos.
            
            # Buscamos si el fármaco existe
            cursor.execute("SELECT COUNT(*) FROM drug WHERE drug_name = %s", (drug_name_input,))
            existe_farmaco = cursor.fetchone()[0] > 0
            
            if existe_farmaco:
                print(f"\n El fármaco '{drug_name_input}' fue encontrado, pero no tiene sinónimos registrados en la BD.")
            else:
                print(f"\n Fármaco no encontrado: No existe ningún registro para el nombre '{drug_name_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")

ejecutar_opcion_2b()

import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA (para que sea autónoma) ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_2c():
    """
    Opción 2.c: Pide un drug_id y muestra sus códigos ATC asociados.
    Muestra un mensaje claro si no se encuentra ningún código.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 2.c: Código ATC de un Fármaco Dado ---")
        drug_id_input = input("Introduce el identificador de ChEMBL del fármaco (drug_id): ").strip()
        
        if not drug_id_input:
            print(" El identificador no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f" Buscando códigos ATC para el drug_id: {drug_id_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL ÚNICA OPTIMIZADA
        # Se asume que la tabla ATC_code enlaza directamente con drug_id para simplificar,
        # como se sugiere en la descripción.
        consulta = """
        SELECT atc.ATC_code_id
        FROM ATC_code atc
        WHERE atc.drug_id = %s;
        """
        
        # Ejecutar la consulta con el ID proporcionado
        cursor.execute(consulta, (drug_id_input,))
        
        resultados = cursor.fetchall()

        # 4. PROCESAMIENTO Y SALIDA (Comprobación de existencia ATC)
        if resultados:
            print(f"\n Códigos ATC encontrados para el drug_id '{drug_id_input}':")
            # Mostrar los códigos ATC
            for i, fila in enumerate(resultados, 1):
                print(f"   {i}. {fila[0]}")
        else:
            # Si no hay resultados ATC, primero verificamos si el fármaco existe
            cursor.execute("SELECT drug_name FROM drug WHERE drug_id = %s", (drug_id_input,))
            farmaco_existe = cursor.fetchone()
            
            if farmaco_existe:
                # El fármaco existe, pero no tiene códigos ATC asociados (Requisito del enunciado)
                print(f"\n El fármaco '{farmaco_existe[0]}' (drug_id: {drug_id_input}) fue encontrado,")
                print("   pero la base de datos no tiene guardado un código ATC para dicho fármaco.")
            else:
                # El fármaco no existe en la base de datos principal
                print(f"\n Fármaco no encontrado: No existe ningún registro para el drug_id '{drug_id_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")

ejecutar_opcion_2c()

