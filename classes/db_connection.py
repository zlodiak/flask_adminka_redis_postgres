import psycopg2

class DB_connection:   
    def __enter__(self):
        self.connection = psycopg2.connect(
            dbname='flask_adminka',  
            user='flask_admin', 
            password='flask_admin',
            host='localhost'
        )
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'connection'):
            self.connection.close()   
