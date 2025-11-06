from comfy_api.latest import ComfyExtension, io
import requests

class LLM_OllamaLoader(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LLM_OllamaLoader",
            display_name="LLM Ollama Loader",
            category="LLM",
            inputs=[
                io.String.Input("server_url", default="http://localhost:11434"),
                io.String.Input("model_name", default="llama2"),
            ],
            outputs=[io.String.Output()]
        )
    @classmethod
    def execute(cls, server_url, model_name):
        # Load via Ollama API
        response = requests.post(f"{server_url}/api/models/load", json={"name": model_name})
        return io.NodeOutput(response.text)

class LLM_OllamaPrompt(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LLM_OllamaPrompt",
            display_name="LLM Ollama Prompt",
            category="LLM",
            inputs=[
                io.String.Input("server_url", default="http://localhost:11434"),
                io.String.Input("model_name", default="llama2"),
                io.String.Input("prompt", default="What is diffusion?"),
            ],
            outputs=[io.String.Output()]
        )
    @classmethod
    def execute(cls, server_url, model_name, prompt):
        resp = requests.post(f"{server_url}/api/generate", json={"model": model_name, "prompt": prompt})
        return io.NodeOutput(resp.text)
