import pandas as pd
import numpy as np

def limpiar_dataset():
    archivo_entrada = './normalizacion/normalizado_standar.csv' 
    print("Cargando datos desde {archivo_entrada}...")
    df = pd.read_csv(archivo_entrada)

    # 2. Eliminar filas duplicadas exactas
    df = df.drop_duplicates()
    
    # 3. Revertir la estandarización de los estratos (Mapeo a valores reales 0-6)
    estratos_map = {
        -2.761216: 0,
        -1.445046: 1,
        -0.128877: 2,
         1.187292: 3,
         2.503462: 4,
         3.819631: 5,
         5.135800: 6
    }
    df['id_estrato'] = df['id_estrato'].round(6).map(estratos_map)
    # Llenar valores no mapeados con -1 por seguridad y convertir a entero
    df['id_estrato'] = df['id_estrato'].fillna(-1).astype(int)

    # 4. Limpieza de textos y formato profesional (Title Case)
    cols_texto = [
        'barrio', 'comuna', 'ciudad_nacimiento', 'pais_nacimiento', 
        'ciudad_nacimiento_1', 'nombre_programa', 'sexo', 'tipo_inscripcion', 
        'sede', 'facultad', 'area_conocimiento', 'institucion', 'colegio', 
        'modalidad', 'tipo_programa'
    ]

    print("🧹 Limpiando textos y aplicando formato Title Case...")
    for col in cols_texto:
        # Convertir a texto por si hay valores numéricos nulos camuflados
        df[col] = df[col].astype(str)
        
        # Reemplazar valores de sistema (ej: "** seleccionar**", "** desconocida **")
        df[col] = df[col].replace(
            to_replace=[r'\*\*.*seleccionar.*\*\*', r'\*\*.*desconocid.*\*\*'], 
            value='No reportado', 
            regex=True
        )
        
        # Aplicar mayúsculas iniciales (Title Case) 
        # (ej: "ingenieria de sistemas" -> "Ingenieria De Sistemas")
        df[col] = df[col].str.title()

    # 5. Exportar el dataset limpio
    archivo_salida = 'dataset_limpio.csv'
    df.to_csv(archivo_salida, index=False)
    
    print("Normalización exitosa")
    print("Archivo guardado como: {archivo_salida}")
    print("Total de registros listos para el grafo: {len(df)}")

if __name__ == "__main__":
    limpiar_dataset()