import os
import sqlalchemy
from sqlalchemy import MetaData, inspect, Table, create_engine
from sqlalchemy.schema import CreateTable

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
metadata = MetaData()

# Open file to write schema
with open('db_schema_structured.sql', 'w') as f:
    f.write("-- MetaMystic Database Schema\n\n")
    
    # Get all schemas
    schemas = inspector.get_schema_names()
    
    for schema in schemas:
        if schema == 'public':  # We only care about the public schema
            f.write(f"-- Schema: {schema}\n\n")
            
            # Get all tables in schema
            for table_name in inspector.get_table_names(schema=schema):
                # Reflect the table
                table = Table(table_name, metadata, autoload_with=engine)
                
                # Get the CreateTable statement
                create_table_statement = str(CreateTable(table).compile(engine))
                
                # Write the statement
                f.write(f"-- Table: {table_name}\n")
                f.write(create_table_statement + ";\n\n")
                
                # Get primary keys
                pk_constraint = inspector.get_pk_constraint(table_name, schema=schema)
                if pk_constraint and pk_constraint.get('constrained_columns'):
                    f.write(f"-- Primary Key for {table_name}: {', '.join(pk_constraint['constrained_columns'])}\n\n")
                
                # Get foreign keys
                fk_constraints = inspector.get_foreign_keys(table_name, schema=schema)
                if fk_constraints:
                    f.write(f"-- Foreign Keys for {table_name}:\n")
                    for fk in fk_constraints:
                        f.write(f"--   {', '.join(fk['constrained_columns'])} -> {fk['referred_table']}.{', '.join(fk['referred_columns'])}\n")
                    f.write("\n")
                
                # Get indexes
                indexes = inspector.get_indexes(table_name, schema=schema)
                if indexes:
                    f.write(f"-- Indexes for {table_name}:\n")
                    for index in indexes:
                        f.write(f"--   {index['name']}: {', '.join(index['column_names'])} (unique: {index['unique']})\n")
                    f.write("\n")
                
                f.write("\n")
    
    # Add a summary
    f.write("\n-- Database Summary:\n")
    table_count = len(inspector.get_table_names(schema='public'))
    f.write(f"-- Total Tables: {table_count}\n")

print("Database schema has been exported to db_schema_structured.sql")