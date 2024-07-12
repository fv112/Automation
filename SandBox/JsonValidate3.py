from jsonschema import validate

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
  "TokenAdminRequest": {
    "type": "object",
    "properties": {
      "admin": {
        "$ref": "#/components/schemas/Admin"
      },
      "user": {
        "$ref": "#/components/schemas/Admin"
      }
    },
    "additionalProperties": False
  },
  "TokenDealerRequest": {
    "type": "object",
    "properties": {
      "admin": {
        "$ref": "#/components/schemas/Admin"
      },
      "dealer": {
        "$ref": "#/components/schemas/DealerAntigo"
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


#JSON Válido
validate({"DealerAntigo": {"dealerCode": '324231'}}, schema)
