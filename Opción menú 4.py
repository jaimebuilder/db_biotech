import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_4a():
    """
    Opción 4.a: Pide un drug_id y muestra los efectos fenotípicos categorizados 
    como INDICACIONES para ese fármaco.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 4.a: Indicaciones de un Fármaco Dado ---")
        drug_id_input = input("Introduce el identificador de ChEMBL del fármaco (drug_id): ").strip()
        
        if not drug_id_input:
            print("El identificador no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f" Buscando indicaciones para el drug_id: {drug_id_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL ÚNICA
        # Filtra por el campo 'phenotype_type' igual a 'INDICATION'.
        consulta = """
        SELECT DISTINCT
            pe.phenotype_id,
            pe.phenotype_name
        FROM phenotype_effect pe
        JOIN drug_phenotype_effect dpe ON pe.phenotype_id = dpe.phenotype_id
        WHERE dpe.drug_id = %s
          AND dpe.phenotype_type = 'INDICATION';
        """
        
        cursor.execute(consulta, (drug_id_input,))
        
        resultados = cursor.fetchall()

        # 4. PROCESAMIENTO Y SALIDA
        if resultados:
            print(f"\n Indicaciones encontradas para el drug_id '{drug_id_input}':")
            print("ID Fenotípico | Nombre del Efecto")
            # Mostrar las indicaciones
            for fila in resultados:
                print(f"   {fila[0]} | {fila[1]}")
        else:
            # Comprobación de existencia del fármaco
            cursor.execute("SELECT drug_name FROM drug WHERE drug_id = %s", (drug_id_input,))
            farmaco_existe = cursor.fetchone()
            
            if farmaco_existe:
                print(f"\n El fármaco '{farmaco_existe[0]}' fue encontrado, pero no tiene indicaciones registradas.")
            else:
                print(f"\n Fármaco no encontrado: No existe ningún registro para el drug_id '{drug_id_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")
ejecutar_opcion_4a()

import mysql.connector

# --- CONFIGURACIÓN DE ACCESO INTEGRADA ---
config = {
    'host' : '127.0.0.1', 
    'port' : 3306,
    'user' : 'disnet_user',
    'password' : 'disnet_pwd',
    'database' : 'disnet_drugslayer'
}

def ejecutar_opcion_4b():
    """
    Opción 4.b: Pide un drug_id y muestra los efectos fenotípicos categorizados 
    como EFECTOS SECUNDARIOS, ordenados por score descendente.
    """
    conexion = None
    cursor = None
    
    try:
        # 1. ENTRADA DE DATOS POR TECLADO
        print("\n--- Opción 4.b: Efectos Secundarios de un Fármaco Dado ---")
        drug_id_input = input("Introduce el identificador de ChEMBL del fármaco (drug_id): ").strip()
        
        if not drug_id_input:
            print("El identificador no puede estar vacío.")
            return

        # 2. CONEXIÓN
        print(f"Buscando efectos secundarios para el drug_id: {drug_id_input}...")
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # 3. CONSULTA SQL ÚNICA
        # Filtra por 'SIDE EFFECT' y ordenamos por 'score' descendente.
        consulta = """
        SELECT 
            pe.phenotype_id,
            pe.phenotype_name,
            dpe.score 
        FROM phenotype_effect pe
        JOIN drug_phenotype_effect dpe ON pe.phenotype_id = dpe.phenotype_id
        WHERE dpe.drug_id = %s
          AND dpe.phenotype_type = 'SIDE EFFECT'
        ORDER BY dpe.score DESC; 
        """
        
        cursor.execute(consulta, (drug_id_input,))
        
        resultados = cursor.fetchall()

        # 4. PROCESAMIENTO Y SALIDA
        if resultados:
            print(f"\n Efectos secundarios encontrados (ordenados por score) para '{drug_id_input}':")
            print("Score | ID Fenotípico | Nombre del Efecto")
            # Mostrar los efectos
            for fila in resultados:
                # fila[2] es el score, fila[0] es el ID, fila[1] es el nombre
                print(f"{fila[2]:<5.4f} | {fila[0]} | {fila[1]}") 
        else:
            # Comprobación de existencia del fármaco
            cursor.execute("SELECT drug_name FROM drug WHERE drug_id = %s", (drug_id_input,))
            farmaco_existe = cursor.fetchone()
            
            if farmaco_existe:
                print(f"\n El fármaco '{farmaco_existe[0]}' fue encontrado, pero no tiene efectos secundarios registrados.")
            else:
                print(f"\n Fármaco no encontrado: No existe ningún registro para el drug_id '{drug_id_input}'.")
            
        print("-----------------------------------------------------")

    except mysql.connector.Error as e:
        print(f"\n ERROR de Conexión o Consulta MySQL: {e}")
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")
ejecutar_opcion_4b()