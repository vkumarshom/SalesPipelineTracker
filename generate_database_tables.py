import os
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metamystic.settings')
django.setup()

def generate_database_tables():
    """Generate a list of all database tables with their schema"""
    
    with open('database_tables.md', 'w') as f:
        f.write("# MetaMystic Database Tables\n\n")
        
        # Get a list of all tables
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tablename 
                FROM pg_catalog.pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """)
            tables = cursor.fetchall()
        
        # Write the table of contents
        f.write("## Table of Contents\n\n")
        for table in tables:
            table_name = table[0]
            # Create an anchor tag for the TOC
            f.write(f"- [{table_name}](#{table_name})\n")
        
        f.write("\n")
        
        # For each table, get the schema information
        for table in tables:
            table_name = table[0]
            
            f.write(f"## {table_name}\n\n")
            
            # Get columns
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT 
                        column_name, 
                        data_type, 
                        character_maximum_length,
                        column_default,
                        is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, [table_name])
                columns = cursor.fetchall()
            
            # Write column information
            f.write("### Columns\n\n")
            f.write("| Column Name | Data Type | Length | Default | Nullable |\n")
            f.write("|------------|-----------|--------|---------|----------|\n")
            
            for column in columns:
                col_name, data_type, max_length, default, nullable = column
                max_length_str = str(max_length) if max_length is not None else '-'
                default_str = str(default) if default is not None else '-'
                nullable_str = 'YES' if nullable == 'YES' else 'NO'
                
                f.write(f"| {col_name} | {data_type} | {max_length_str} | {default_str} | {nullable_str} |\n")
            
            # Get primary key information
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                        AND tc.table_name = %s;
                """, [table_name])
                pk_columns = cursor.fetchall()
            
            if pk_columns:
                f.write("\n### Primary Key\n\n")
                pk_cols = [col[0] for col in pk_columns]
                f.write(f"- {', '.join(pk_cols)}\n")
            
            # Get foreign key information
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_name = %s;
                """, [table_name])
                fk_columns = cursor.fetchall()
            
            if fk_columns:
                f.write("\n### Foreign Keys\n\n")
                for fk in fk_columns:
                    col_name, foreign_table, foreign_col = fk
                    f.write(f"- `{col_name}` → `{foreign_table}.{foreign_col}`\n")
            
            # Get indexes
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT
                        i.relname AS index_name,
                        a.attname AS column_name,
                        ix.indisunique AS is_unique
                    FROM
                        pg_class t,
                        pg_class i,
                        pg_index ix,
                        pg_attribute a
                    WHERE
                        t.oid = ix.indrelid
                        AND i.oid = ix.indexrelid
                        AND a.attrelid = t.oid
                        AND a.attnum = ANY(ix.indkey)
                        AND t.relkind = 'r'
                        AND t.relname = %s
                    ORDER BY
                        i.relname;
                """, [table_name])
                indexes = cursor.fetchall()
            
            if indexes:
                f.write("\n### Indexes\n\n")
                current_index = ""
                index_columns = []
                is_unique = False
                
                for idx in indexes:
                    idx_name, col_name, unique = idx
                    
                    if current_index != idx_name:
                        if current_index:
                            unique_str = "UNIQUE " if is_unique else ""
                            f.write(f"- {unique_str}INDEX `{current_index}` ({', '.join(index_columns)})\n")
                        
                        current_index = idx_name
                        index_columns = [col_name]
                        is_unique = unique
                    else:
                        index_columns.append(col_name)
                
                if current_index:
                    unique_str = "UNIQUE " if is_unique else ""
                    f.write(f"- {unique_str}INDEX `{current_index}` ({', '.join(index_columns)})\n")
            
            f.write("\n---\n\n")
    
    print("Database tables information generated: database_tables.md")

if __name__ == "__main__":
    generate_database_tables()