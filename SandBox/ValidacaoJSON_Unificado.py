import os.path
import subprocess
import json
from faker import Faker
import random
from jsonschema import validate, ValidationError

import Automation.modules.automationAux as Aux

# ---- Extract only the definition content from the JSON Swagger file --------------------------------------------------

swagger_link = None
swagger_file = 'swagger.json'


def load_swagger(file_path):
    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError("O arquivo deve ser .json ou .yaml/.yml")


def extract_jsonschema_relevant_data(swagger_data, output_file):
    if 'definitions' in swagger_data:
        relevant_data = swagger_data['definitions']
    elif 'components' in swagger_data and 'schemas' in swagger_data['components']:
        relevant_data = swagger_data['components']['schemas']
    else:
        relevant_data = {}

    #with open(os.path.join(Aux.directories['SwaggerFolder'], swagger_file), 'w') as f:
    with open(os.path.join('C:\\QA-Automation-Files\\Repository\\Automation\\Swagger', swagger_file), 'w') as f: ### Atualizar.
        json.dump(relevant_data, f, indent=2)


# --- Preparing the file, directory and Swagger file download.

# Aux.Main.createDirectory(path_folder=Aux.directories['SwaggerFolder'])
Aux.Main.createDirectory(path_folder='C:\\QA-Automation-Files\\Repository\\Automation\\Swagger') ### Atualizar
#if os.path.isfile(Aux.directories['SwaggerFolder']): ### Descomentar
#    f = open(os.path.join(Aux.directories['SwaggerFolder'],swagger_file), 'w') ### Descomentar

# Download the swagger file.

swagger_link = 'https://api-after-sales-hml.mbcv-online.com/swagger/../swagger/v1/swagger.json' ### Atualizar com o valor do passo.

subprocess.run(['curl', '-o', 'C:\QA-Automation-Files\Repository\Automation\Swagger\\' + swagger_file, swagger_link]) ### Atualizar
#subprocess.run(['curl', '-o', os.path.join(Aux.directories['SwaggerFolder'],output_file), swagger_link])

# swagger_file_path = os.path.join(Aux.directories['SwaggerFolder'], 'swagger.json') ###
#swagger_file_path = os.path.join('C:\\QA-Automation-Files\\Repository\\Automation\\Swagger', 'swagger.json') ### Atualizar

#swagger_data = load_swagger(Aux.directories['SwaggerFolder'], output_file)
swagger_data = load_swagger(os.path.join('C:\\QA-Automation-Files\\Repository\\Automation\\Swagger', swagger_file)) ### Atualizar

extract_jsonschema_relevant_data(swagger_data, swagger_file)

print(f"Dados relevantes para JSON Schema extraídos e salvos como {swagger_file}")

#schema = open(os.path.join(Aux.directories['SwaggerFolder'], swagger_file), 'r')
file = open(os.path.join('C:\\QA-Automation-Files\\Repository\\Automation\\Swagger', swagger_file), 'r') ### Atualizar.
schema = json.load(file)

# ------------------------------------- Generate the fake dataa to the API fields --------------------------------------

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

# Gerar e imprimir dados fictícios para cada definição no esquema
for definition_name, definition_schema in schema.items():
    data_list = generate_data(definition_schema, schema)
    print(f"Dados gerados para {definition_name}:")
    for data in data_list:
        print(json.dumps(data, indent=2))
    print("-" * 80)

# ------------------------------------- Teste de API fields for each schema tag ----------------------------------------

# Função para resolver referências no esquema.
def resolve_refs(schema, definitions):
    if isinstance(schema, dict):
        if '$ref' in schema:
            ref = schema['$ref'].split('/')[-1]
            return resolve_refs(definitions[ref], definitions)
        else:
            return {k: resolve_refs(v, definitions) for k, v in schema.items()}
    elif isinstance(schema, list):
        return [resolve_refs(item, definitions) for item in schema]
    else:
        return schema


# Resolvendo as referências no esquema.
resolved_schema = {k: resolve_refs(v, schema) for k, v in schema.items()}


def run_validation(json_data):

    errors = []

    try:
        # for count, json_data_items in enumerate(data.keys()):
        #     print(data[json_data_items][count])

        ### JSON data é o valor a se alterar.
        for schema_item in resolved_schema.keys():
            validate(instance=json_data, schema=resolved_schema[schema_item])
        print("JSON válido.")

    except ValidationError as e:
        print("JSON inválido:", e.message)
        errors.append((e.message))

    return errors


for key, values in data.items():
    result = []
    for value in values:
        print(f"Key: {key}, Value: {value}")
        json_data = {key: value}
        result = run_validation(json_data)

    print("-" * 90)
    print(result)



# if os.path.isfile(Aux.directories['SwaggerFolder']): ### Descomentar
#     Aux.Main.deleteFiles(exact_file=swagger_file) ### Descomentar
