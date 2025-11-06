# comfy_receiver_node.py
from comfy_api.latest import io

def majority_vote(results):
    # Basic majority vote for text; can customize for other types
    from collections import Counter
    cleaned = [r for r in results if r]
    if not cleaned:
        return ""
    return Counter(cleaned).most_common(1)[0][0]

def weighted_blend(results, weights=None):
    # For now, just simple averaging (strings concatenated, images use PIL/numpy average)
    cleaned = [r for r in results if r]
    return " | ".join(cleaned)  # Replace logic for images/numeric

def compare_results(results):
    # Simple comparison (return all, or diff/summary)
    cleaned = [r for r in results if r]
    return "\n---\n".join(cleaned)

class ReceiverNode(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ReceiverNode",
            display_name="Workflow Receiver Node",
            category="Orchestration",
            inputs=[
                io.Int.Input("expected_count", min=1, max=8, default=2, display_mode=io.NumberDisplay.slider),
                *[io.String.Input(f"result_{i+1}", default="", multiline=True) for i in range(8)],
                io.Combo.Input("aggregation_mode", options=["Concat", "Vote", "Blend", "Compare"], default="Concat")
            ],
            outputs=[
                io.String.Output("aggregated"),
                io.String.Output("status_summary")
            ]
        )

    @classmethod
    def execute(cls, expected_count, aggregation_mode, *inputs):
        results = list(inputs[:expected_count])
        missing = [str(i+1) for i, r in enumerate(results) if not r]
        status = f"Received {expected_count-len(missing)}/{expected_count}"
        if missing:
            status += f"; Missing: {', '.join(missing)}"
        agg = ""
        if aggregation_mode == "Concat":
            agg = "\n".join([r for r in results if r])
        elif aggregation_mode == "Vote":
            agg = majority_vote(results)
        elif aggregation_mode == "Blend":
            agg = weighted_blend(results)
        elif aggregation_mode == "Compare":
            agg = compare_results(results)
        return io.NodeOutput(agg, status)

# Drop this file into your custom_nodes directory.
# Wire outputs from models/nodes directly into ReceiverNode inputs as needed.
