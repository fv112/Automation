import json
import yaml

# Função para carregar o arquivo Swagger
def load_swagger(file_path):
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(f)
        else:
            raise ValueError("O arquivo deve ser .json ou .yaml/.yml")

# Função para extrair e salvar as definições e esquemas relevantes para JSON Schema
def extract_jsonschema_relevant_data(swagger_data, output_file):
    # Extraindo a seção `definitions` (Swagger 2.0) ou `components/schemas` (OpenAPI 3.0)
    if 'definitions' in swagger_data:
        relevant_data = swagger_data['definitions']
    elif 'components' in swagger_data and 'schemas' in swagger_data['components']:
        relevant_data = swagger_data['components']['schemas']
    else:
        relevant_data = {}

    # Salvando os dados extraídos em um novo arquivo JSON
    with open(output_file, 'w') as f:
        json.dump(relevant_data, f, indent=2)

# Caminho para o arquivo Swagger
swagger_file_path = 'C:\\QA-Automation-Files\\swagger.json'  # ou 'swagger.yaml'

# Carregar o esquema Swagger
swagger_data = load_swagger(swagger_file_path)

# Extrair dados relevantes para JSON Schema e salvar como JSON
output_file = 'jsonschema_definitions.json'
extract_jsonschema_relevant_data(swagger_data, output_file)

print(f"Dados relevantes para JSON Schema extraídos e salvos como {output_file}")
