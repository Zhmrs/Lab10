from database.DB_connect import DBConnect
from model.hub import Hub
class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @ staticmethod
    def leggi_hub(): # nodi
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = " SELECT * FROM hub "
        try:
            cursor.execute(query)
            for row in cursor:
                hub=Hub(row['id'],
                        row['codice'],
                        row['nome'],
                        row['citta'],
                        row['stato'],
                        row['latitudine'],
                        row['longitudine'])
                result.append(hub)
        except Exception as e:
            print(f"Errore durante la query leggi_hub: {e}")
            result = None
        finally:
            cursor.close()
            conn.close()

        return result


    @ staticmethod
    def get_spedizioni_media():
        conn = DBConnect.get_connection()
        result=[]
        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT LEAST(id_hub_origine, id_hub_destinazione) AS origine, 
                           GREATEST(id_hub_origine, id_hub_destinazione) AS destinazione,
                           SUM(valore_merce) AS somma_valore_merce,
                           COUNT(*) AS num_spedizioni
                    FROM spedizione 
                    GROUP BY LEAST(id_hub_origine, id_hub_destinazione),
                             GREATEST(id_hub_origine, id_hub_destinazione)"""

                # LEAST restituisce il più piccolo tra i due valori
                # GREATEST restituisce il più grande tra i due valori
                # esempio: (2,5) e (5,2) finiscono nello stesso gruppo, perché LEAST(2,5)=2 e GREATEST(2,5)=5.
                # In questo modo tratti la coppia come non orientata (cioè (A,B) ≡ (B,A)).
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row)
        except Exception as e:
            print(f"Errore durante la query readSpedizione: {e}")
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

