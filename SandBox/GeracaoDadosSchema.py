import json
from faker import Faker
import random

# Inicializar Faker
fake = Faker()

# Função para gerar dados fictícios de tipos diferentes com base no tipo do esquema
def generate_data(schema, definitions):
    if 'type' not in schema:
        return None

    data = []

    # Função para adicionar variações de tipos de dados
    def add_variations(base_type, value):
        if base_type == 'string':
            data.extend([
                value,  # Original value
                fake.random_int(),  # Integer variation
                fake.pyfloat(left_digits=5, right_digits=2),  # Float variation
                fake.boolean()  # Boolean variation
            ])
        elif base_type == 'integer':
            data.extend([
                value,  # Original value
                fake.word(),  # String variation
                fake.pyfloat(left_digits=5, right_digits=2),  # Float variation
                fake.boolean()  # Boolean variation
            ])
        elif base_type == 'number':
            data.extend([
                value,  # Original value
                fake.word(),  # String variation
                fake.random_int(),  # Integer variation
                fake.boolean()  # Boolean variation
            ])
        elif base_type == 'boolean':
            data.extend([
                value,  # Original value
                fake.word(),  # String variation
                fake.random_int(),  # Integer variation
                fake.pyfloat(left_digits=5, right_digits=2)  # Float variation
            ])

    # Gerar dados com base no tipo do esquema
    if schema['type'] == 'string':
        value = fake.word() if not (schema.get('nullable', False) and random.choice([True, False])) else None
        add_variations('string', value)
    elif schema['type'] == 'number':
        value = fake.pyfloat(left_digits=5, right_digits=2) if not (schema.get('nullable', False) and random.choice([True, False])) else None
        add_variations('number', value)
    elif schema['type'] == 'integer':
        value = fake.random_int() if not (schema.get('nullable', False) and random.choice([True, False])) else None
        add_variations('integer', value)
    elif schema['type'] == 'boolean':
        value = fake.boolean() if not (schema.get('nullable', False) and random.choice([True, False])) else None
        add_variations('boolean', value)
    elif schema['type'] == 'array':
        if not (schema.get('nullable', False) and random.choice([True, False])):
            array_data = [generate_data(schema['items'], definitions) for _ in range(3)]
            if array_data not in data:
                data.append(array_data)
    elif schema['type'] == 'object':
        if not (schema.get('nullable', False) and random.choice([True, False])):
            obj = {}
            for prop, prop_schema in schema.get('properties', {}).items():
                if '$ref' in prop_schema:
                    ref = prop_schema['$ref'].split('/')[-1]
                    obj[prop] = generate_data(definitions[ref], definitions)#, include_variations=False)
                else:
                    obj[prop] = generate_data(prop_schema, definitions)#, include_variations=False)
            if obj not in data:
                data.append(obj)
    return data

# Definição do esquema fornecido
schema = {
  "DealerAntigo": {
    "type": "object",
    "properties": {
      "dealerCode": {
        "type": "string",
        "nullable": True
      },
      "cnpj": {
        "type": "string",
        "nullable": True
      },
      "dms": {
        "type": "string",
        "nullable": True
      }
    },
    "additionalProperties": False
  },
  "Admin": {
    "type": "object",
    "properties": {
      "adminCode": {
        "type": "string",
        "nullable": True
      },
      "adminName": {
        "type": "string",
        "nullable": True
      }
    },
    "additionalProperties": False
  },
  "TokenAdminRequest": {
    "type": "object",
    "properties": {
      "admin": {
        "$ref": "#/Admin"
      },
      "user": {
        "$ref": "#/Admin"
      }
    },
    "additionalProperties": False
  },
  "TokenDealerRequest": {
    "type": "object",
    "properties": {
      "admin": {
        "$ref": "#/Admin"
      },
      "dealer": {
        "$ref": "#/DealerAntigo"
      }
    },
    "additionalProperties": False
  },
  "UploadFileModelRequest": {
    "type": "object",
    "properties": {
      "cnpj": {
        "type": "string",
        "nullable": True
      },
      "dealerCode": {
        "type": "string",
        "nullable": True
      },
      "fileName": {
        "type": "string",
        "nullable": True
      },
      "file": {
        "type": "string",
        "nullable": True
      }
    },
    "additionalProperties": False
  }
}

# Gerar e imprimir dados fictícios para cada definição no esquema
for definition_name, definition_schema in schema.items():
    data_list = generate_data(definition_schema, schema)
    print(f"Dados gerados para {definition_name}:")
    for data in data_list:
        print(json.dumps(data, indent=2))
    print("-" * 80)
