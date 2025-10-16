from flasgger import Swagger
template = {
        "openapi": "3.0.2",
        "info": {
            "title": "Library API",
            "description": "Simple Library Management API with JWT Auth",
            "version": "1.0.0"
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"BearerAuth": []}]
    }