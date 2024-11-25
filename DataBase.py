import sqlite3

class DataBase:
    def __init__(self, bdName="Flashcards.db"):
        self.conn = None
        try:
            self.conector = sqlite3.connect(bdName)
            self.TablaCarpeta()
        except KeyError as e:
            print(f"Error al conectar con SQLite: {e}")
        
    def TablaCarpeta(self):
        try:
            cursor = self.conector.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carpetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    color VARCHAR(20),
                    img VARCHAR(100)
                );
            """)

            self.conector.commit()
        except KeyError as e:
            print(f"Error al crear las tablas: {e}")

    def CrearCarpeta(self, nombre, colorCarpeta, colorMarcador):
        try:
            cursor = self.conector.cursor()
            # Inserta el nombre en la tabla carpetas
            cursor.execute("""
                INSERT INTO carpetas (nombre, color, img)
                VALUES (?, ?, ?);
            """, (nombre, colorCarpeta, colorMarcador))
            
            id = cursor.lastrowid  # Obtén el ID de la última carpeta creada

            # Crea una tabla asociada para la nueva carpeta
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS carpeta_{id} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CONCEPTO VARCHAR(300),
                    RESPUESTA VARCHAR(300),
                    COMENTARIO VARCHAR(500), 
                    FOTOS VARCHAR(100)
                );
            """)
            self.conector.commit()
            print(f"Se ha creado la carpeta '{nombre}' y su tabla asociada (ID: {id}) correctamente.")
        except sqlite3.Error as e:
            print(f"Error al crear la carpeta: {e}")

    def CrearFlashCard(self, idTabla, concepto, respuesta, comentario, foto):
        try:
            cursor = self.conector.cursor()
            cursor.execute(f"""
                INSERT INTO carpeta_{idTabla} (CONCEPTO, RESPUESTA, COMENTARIO, FOTOS)
                VALUES (?, ?, ?, ?);
            """, (concepto, respuesta, comentario, foto))
            self.conector.commit()
            print(f"se ha creado una flashcard correctamente en la tabla carpeta_{idTabla}")
        except KeyError as e:
            print(f"Error al conectar con SQLite: {e}")


    def ObtenerCarpetas(self):
        try:
            cursor = self.conector.cursor()
            cursor.execute("""
                SELECT * FROM carpetas;
            """)
            data = cursor.fetchall()
            self.conector.commit()
            print("Se ha obtenido la informacion correctamente")
            return data
        except:
            pass
            
    def ObtenerFlashCards(self, idTabla):
        try:
            cursor = self.conector.cursor()
            cursor.execute(f"""
                SELECT * FROM carpeta_{idTabla};
            """)
            data = cursor.fetchall()
            self.conector.commit()
            print("Se ha obtenido la informacion correctamente")
            print(data)
            return data
        except KeyError as e:
            print(f"error en ObtenerFlashCards: ", e)

    def EliminarFlashCard(self, idTabla, id):
        try:
            cursor = self.conector.cursor()
            cursor.execute(f"""
                DELETE FROM carpeta_{idTabla} WHERE ID = ?;
            """, id)
            self.conector.commit()
            print("Se ha eliminado la flashcard correctamente")
        except:
            pass

    def EliminarCarpeta(self, id):
        try:
            cursor = self.conector.cursor()
            cursor.execute("""
                DELETE FROM carpetas WHERE id = ?;
            """, id)

            print("Se ha eliminado la carpeta correctamente")

            cursor.execute(f"""
                DROP TABLE carpeta_{id};
            """)

            print("Se ha eliminado la tabla correctamente")

            self.conector.commit()
        except:
            pass

    def EditarFlashCard(self, idTable, id, concepto, respuesta, comentario, foto):
        cursor = self.conector.cursor()
        cursor.execute(f"""
            UPDATE carpeta_{idTable} WHERE ID = ?
            SET CONCEPTO = ?,
            SET RESPUESTA = ?,
            SET COMENTARIO = ?,
            SET FOTOS = ? 
        """, (id, concepto, respuesta, comentario, foto))

    def Cerrar(self):
        if self.conector:
            self.conector.close()
            print("La conexion se ha cerrado")

