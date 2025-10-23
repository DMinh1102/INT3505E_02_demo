from flasgger import Swagger

template = {
    "openapi": "3.0.2",
    "info": {
        "title": "Library API",
        "description": "Simple Library Management API with JWT Authentication",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@example.com"
        }
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer <your_jwt_token>'"
            }
        },
        "schemas": {
            "Error": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message"
                    },
                    "message": {
                        "type": "string", 
                        "description": "Detailed error description"
                    }
                }
            }
        },
        "responses": {
            "Unauthorized": {
                "description": "Missing or invalid JWT token",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/Error"
                        }
                    }
                }
            },
            "Forbidden": {
                "description": "Valid JWT but insufficient permissions",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/Error"
                        }
                    }
                }
            }
        }
    },
    "security": [{"BearerAuth": []}]
}