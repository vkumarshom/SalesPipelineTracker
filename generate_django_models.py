import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metamystic.settings')
django.setup()

# Import all models from astrology app
from astrology.models import *
from django.apps import apps
from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField

def generate_model_schema():
    with open('db_schema_django.sql', 'w') as f:
        f.write("-- MetaMystic Database Schema (Generated from Django Models)\n\n")
        
        # Get all models from astrology app
        app_models = apps.get_app_config('astrology').get_models()
        
        for model in app_models:
            model_name = model.__name__
            table_name = model._meta.db_table
            
            f.write(f"-- Model: {model_name} (Table: {table_name})\n")
            f.write("CREATE TABLE IF NOT EXISTS ")
            f.write(f"\"{table_name}\" (\n")
            
            # Get all fields
            fields = []
            for field in model._meta.fields:
                field_def = f"    \"{field.column}\" "
                
                # Determine field type
                if isinstance(field, models.AutoField):
                    field_def += "serial "
                elif isinstance(field, models.BigAutoField):
                    field_def += "bigserial "
                elif isinstance(field, models.CharField) or isinstance(field, models.TextField):
                    max_length = getattr(field, 'max_length', None)
                    if max_length and isinstance(field, models.CharField):
                        field_def += f"varchar({max_length}) "
                    else:
                        field_def += "text "
                elif isinstance(field, models.IntegerField):
                    field_def += "integer "
                elif isinstance(field, models.BooleanField):
                    field_def += "boolean "
                elif isinstance(field, models.DateField):
                    field_def += "date "
                elif isinstance(field, models.DateTimeField):
                    field_def += "timestamp with time zone "
                elif isinstance(field, models.TimeField):
                    field_def += "time "
                elif isinstance(field, models.DecimalField):
                    field_def += f"decimal({field.max_digits}, {field.decimal_places}) "
                elif isinstance(field, models.FloatField):
                    field_def += "double precision "
                elif isinstance(field, models.FileField) or isinstance(field, models.ImageField):
                    field_def += "varchar(100) "
                elif isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                    field_def += "integer "
                else:
                    field_def += "text "  # Default to text for unknown types
                
                # Add NULL constraint
                if not field.null:
                    field_def += "NOT NULL "
                
                # Add primary key constraint
                if field.primary_key:
                    field_def += "PRIMARY KEY "
                
                fields.append(field_def)
            
            # Add foreign key constraints
            for field in model._meta.fields:
                if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                    related_model = field.related_model
                    related_table = related_model._meta.db_table
                    fk_def = f"    CONSTRAINT \"{table_name}_{field.column}_fkey\" "
                    fk_def += f"FOREIGN KEY (\"{field.column}\") "
                    fk_def += f"REFERENCES \"{related_table}\" (\"id\") "
                    
                    # Add ON DELETE behavior
                    if field.remote_field.on_delete == models.CASCADE:
                        fk_def += "ON DELETE CASCADE "
                    elif field.remote_field.on_delete == models.SET_NULL:
                        fk_def += "ON DELETE SET NULL "
                    elif field.remote_field.on_delete == models.PROTECT:
                        fk_def += "ON DELETE RESTRICT "
                    
                    fields.append(fk_def)
            
            # Join all field definitions
            f.write(",\n".join(fields))
            f.write("\n);\n\n")
            
            # Add table comment
            if model.__doc__:
                doc = model.__doc__.replace("'", "''") if model.__doc__ else ""
                f.write(f"COMMENT ON TABLE \"{table_name}\" IS '{doc}';\n\n")
        
        # Add a summary
        f.write("\n-- Database Summary:\n")
        f.write(f"-- Total Models/Tables: {len(list(app_models))}\n")

if __name__ == "__main__":
    generate_model_schema()
    print("Django model schema has been exported to db_schema_django.sql")