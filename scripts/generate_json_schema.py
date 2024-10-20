from query_generator.schemas import QueryConfig
import json
from pathlib import Path

main_model_schema = QueryConfig.model_json_schema()
out = json.dumps(main_model_schema, indent=2)

project_path = Path(__file__).parent.parent
file_path = project_path / "static" / "query_json_schema.json"

with open(file_path, "w") as f:
    f.write(out)
