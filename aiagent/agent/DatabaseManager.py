import requests
import os
from typing import List, Any
import psycopg2
import urllib.parse
import sqlite3
import json


# def get_table_schema(self, table_name: str) -> list:
#     """Retrieve the schema of a specific table."""
#     try:
#         with psycopg2.connect(self.connection_string) as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         column_name, 
#                         data_type, 
#                         is_nullable, 
#                         column_default 
#                     FROM 
#                         information_schema.columns 
#                     WHERE 
#                         table_name = %s;
#                 """, (table_name,))
#                 return cursor.fetchall()  # Return list of column details
#     except Exception as e:
#         raise Exception(f"Error fetching schema for table {table_name}: {str(e)}")
    

class DatabaseManager:
    def __init__(self):
        self.endpoint_url = os.getenv("DB_ENDPOINT_URL")
        username = "postgres"
        hostname = "localhost"
        database = "mysiteDB"
        port = "5432"
        encoded_password = urllib.parse.quote('Niharikaa@0823')

        # Add connection parameters
        self.connection_string = f"postgresql+psycopg2://{username}:{encoded_password}@{hostname}:{port}/{database}"


    def get_schema(self, uuid: str) -> str:
        """Retrieve the database schema."""
        try:
            db_path = f"./uploadsDir/{uuid}.db"
            if not os.path.exists(db_path):
                raise Exception("Database not found")
            
            try:
                db = sqlite3.connect(db_path)
                cursor = db.cursor()
                cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                schema = []

                for table_name, create_statement in tables:
                    schema.append(f"Table: {table_name}")
                    schema.append(f"CREATE statement: {create_statement}\n")

                    cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 3;")
                    rows = cursor.fetchall()

                    if rows:
                        schema.append("Example rows:")
                        for row in rows:
                            schema.append(json.dumps(row))
                    schema.append("") # add a blank line between tables

                db.close()

                return {'schema': "\n".join(schema)}
            except Exception as e:
                raise Exception(f"Error fetching schema: {str(e)}")
        except requests.RequestException as e:
            raise Exception(f"Database not found {str(e)}")

    # def get_schema(self, uuid: str) -> str:
    #     """Retrieve the database schema."""
    #     try:
    #         # Connect to the local PostgreSQL database
    #         with psycopg2.connect(self.connection_string) as conn:
    #             with conn.cursor() as cursor:
    #                 cursor.execute("SELECT schema_name FROM information_schema.schemata;")
    #                 schemas = cursor.fetchall()
    #                 return [schema[0] for schema in schemas]  # Return list of schemas
    #     except Exception as e:
    #         raise Exception(f"Error fetching schema: {str(e)}")

    def execute_query(self, uuid: str, query: str) -> List[Any]:
        """Execute SQL query on the local SQLite database and return results."""
        try:
            db_path = f"./uploadsDir/{uuid}.db"
            if not os.path.exists(db_path):
                raise Exception("Database not found")

            db = sqlite3.connect(db_path)
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            db.close()

            return rows  # Return the fetched results
        except sqlite3.Error as e:
            raise Exception(f"Error executing query: {str(e)}")