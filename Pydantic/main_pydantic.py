import sys
from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional
from datetime import datetime
import csv
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class User(BaseModel):
    id: int = Field(description="identifiant de l'utilisateur", le=1235)
    name: str = Field(description="nom de l'utilisateur", max_length=5)
    last_name: str = Field(description="Prenom de l'utilisateur", max_length=300)
    email: EmailStr = Field(description="email de l'utilisateur")
    date_validate: Optional[datetime] = datetime.now()


class Parc(BaseModel):
    num_du_parc: str
    parc: str
    arrdt: int
    insertion_date: datetime
    date_validate: Optional[datetime] = datetime.now()


def load_csv(filepath, delimiter=','):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        data = [row for row in reader]
    return data


def validate_data(data, Model):
    print("\nSI LE SCRIPT NE RENVOIE RIEN C'EST QUE LES DONNEES SONT VALIDEES.")
    validated_data = []
    for index, item in enumerate(data):
        try:
            validated_data.append(Model(**item))
        except ValidationError as e:
            print(f"\nErreur sur les données de la ligne: {index + 2}:\n {e}\n\n")
            colonne_error = [error['loc'] for error in e.errors()]
            print(f"Ce qu'il faut changer à la :\n>>> ligne : {index + 2}\n>>> colonne: {colonne_error}\n>>> Données: {item}")
    return validated_data


def save_data_validate_to_csv(filepath, data):
    fieldnames = data[0].dict().keys()
    with open(filepath, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for item in data:
            writer.writerow(item.dict())

    # Output to stdout
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for item in data:
        writer.writerow(item.dict())

    # Save to Parquet
    data_csv = pd.read_csv(filepath, delimiter=";")
    table = pa.Table.from_pandas(data_csv)
    pq.write_table(table, 'to.parquet')


# Main script execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_pydantic.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    data = load_csv(csv_file_path, delimiter=';')
    validated_data = validate_data(data, Parc)
    if validated_data:
        validated_csv = 'validated_data.csv'
        save_data_validate_to_csv(validated_csv, validated_data)
        print("Validated data has been saved to 'validated_data.csv' and 'to.parquet'.")

# you can run the script with the following command: python main_pydantic.py codification_parc.csv
