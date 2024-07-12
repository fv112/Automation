import jsonschema
from jsonschema import validate, ValidationError

# Esquema JSON fornecido
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

# Exemplo de JSON a ser validado
json_data = {
  "dealerCode": '123',
}

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

# Validando o JSON
try:
    for schema_item in resolved_schema.keys():
      #print(schema_item)

      #validate(instance=json_data, schema=resolved_schema['DealerAntigo'])
      validate(instance=json_data, schema=resolved_schema[schema_item])
      print("JSON válido.")
except ValidationError as e:
    print("JSON inválido:", e.message)
