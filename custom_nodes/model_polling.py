import requests
from comfy_api.latest import ComfyExtension, io

KNOWN_ENDPOINTS = [
    "/models",
    "/api/models",
    "/v1/models",
    "/api/tags",
    "/capabilities",
    "/v1/model_capabilities"
]

class ModelPollingNode(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ModelPollingNode",
            display_name="LLM Server Model Poller",
            category="LLM/Infra",
            inputs=[
                io.String.Input("server_url", default="http://localhost:11434")
            ],
            outputs=[
                io.Combo.Output("available_models")
            ]
        )

    @classmethod
    def execute(cls, server_url):
        models = []
        # Try each endpoint until a valid response is found
        for endpoint in KNOWN_ENDPOINTS:
            try:
                url = server_url.rstrip("/") + endpoint
                resp = requests.get(url, timeout=3)
                if resp.status_code == 200:
                    data = resp.json()
                    # Handle known response formats
                    if isinstance(data, list):
                        models = data
                    elif "models" in data:
                        models = data["models"]
                    elif "tags" in data:
                        models = data["tags"]
                    elif "capabilities" in data:
                        models = [item["name"] for item in data["capabilities"]]
                    if models:
                        break
            except Exception:
                continue
        # Fallback
        if not models:
            models = ["No models detected"]
        return io.NodeOutput(models)
