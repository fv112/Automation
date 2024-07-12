from jsonschema import validate

schema = {
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

#JSON Válido
validate({"cnpj": 324231}, schema)
