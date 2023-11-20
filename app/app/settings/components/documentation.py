SPECTACULAR_SETTINGS = {
    'TITLE': 'Egnite',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATION_PARAMETERS': False,
    
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Api-Key"
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], }],
}