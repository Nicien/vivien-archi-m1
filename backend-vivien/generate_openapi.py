import yaml
import logging
from fastapi.openapi.utils import get_openapi
from main import app

# Generate OpenAPI schema from app
openapi_schema = get_openapi(
    title=app.title,
    version=app.version,
    description=app.description,
    routes=app.routes,
)

# Write to openapi.yml
with open("openapi.yml", "w") as f:
    yaml.dump(openapi_schema, f, sort_keys=False)
logging.info("openapi.yml written")
