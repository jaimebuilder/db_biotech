import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_3a():
    """
    Opción 3.a: Pide el nombre de una enfermedad (de la tabla disease_code) 
    y muestra los fármacos asociados.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 3.a: Fármacos para una Enfermedad ---")
        disease_name_input = input("Introduce el nombre de la enfermedad (p.ej., ASPERGILLOSIS): ").strip()
        
        if not disease_name_input:
            print(" El nombre de la enfermedad no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f" Buscando fármacos asociados a: {disease_name_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL CORREGIDA (Ruta más directa: drug -> drug_disease -> disease_code)
        consulta = """
        SELECT DISTINCT
            d.drug_id,
            d.drug_name
        FROM drug d
        JOIN drug_disease dd ON d.drug_id = dd.drug_id
        JOIN disease_code dc ON dd.code_id = dc.code_id  -- <--- CORRECCIÓN CLAVE: Usamos dd.code_id
        WHERE dc.name = %s;
        """
        
        # Ejecutar la consulta
        cursor.execute(consulta, (disease_name_input,))
        
        resultados = cursor.fetchall()

        # 4. PROCESAMIENTO Y SALIDA
        if resultados:
            print(f"\n Fármacos asociados a '{disease_name_input}':")
            print("ID de Fármaco (ChEMBL) | Nombre del Fármaco")
            # Mostrar los fármacos
            for fila in resultados:
                print(f"   {fila[0]} | {fila[1]}")
        else:
            # Comprobación de existencia (Verificamos si la enfermedad existe en disease_code)
            cursor.execute("SELECT COUNT(*) FROM disease_code WHERE name = %s", (disease_name_input,))
            existe_enfermedad = cursor.fetchone()[0] > 0
            
            if existe_enfermedad:
                print(f"\n La enfermedad '{disease_name_input}' fue encontrada, pero no tiene fármacos asociados registrados.")
            else:
                print(f"\n Enfermedad no encontrada: No existe ningún código de enfermedad con el nombre '{disease_name_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")
ejecutar_opcion_3a()

import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_3b():
    """
    Opción 3.b: Muestra el fármaco y la enfermedad con el mayor 'inferred_score'.
    """
    conexion = None
    cursor = None
    
    try:
        print("\n--- Opción 3.b: Mayor Score de Asociación ---")
        
        # 1. CONEXIÓN
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        print("Conexión establecida.")
        
        # 2. CONSULTA SQL OPTIMIZADA
        # Busca el registro con el MAX(inferred_score), uniendo las tres tablas necesarias.
        consulta = """
        SELECT 
            d.drug_name,
            dc.name,
            dd.inferred_score
        FROM drug_disease dd
        JOIN drug d ON dd.drug_id = d.drug_id
        JOIN disease_code dc ON dd.code_id = dc.code_id
        ORDER BY dd.inferred_score DESC
        LIMIT 1;
        """
        
        cursor.execute(consulta)
        
        resultado = cursor.fetchone()

        # 3. PROCESAMIENTO Y SALIDA
        if resultado:
            drug_name, disease_name, score = resultado
            
            print("\n Par Fármaco-Enfermedad con el MAYOR Score de Asociación:")
            print(f"   Score (inferred_score): **{score}**")
            print(f"   Fármaco:                **{drug_name}**")
            print(f"   Enfermedad (Código):    **{disease_name}**")
        else:
            print("\n No se encontraron registros con 'inferred_score' para procesar.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")

ejecutar_opcion_3b()