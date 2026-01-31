"""
LLM Configuration module for Brand Identity Workflow.
Supports both OpenAI (paid) and Ollama (free local models).
"""

import os

# Available model presets
# For Ollama models, just use the model string - LiteLLM handles the rest
MODEL_PRESETS = {
    # Free local models via Ollama
    "qwen2.5-vl": {
        "model": "ollama/qwen2.5-vl",
        "description": "Qwen 2.5 VL - Best for visual tasks and tool use"
    },
    "qwen2.5": {
        "model": "ollama/qwen2.5",
        "description": "Qwen 2.5 - Fast general purpose model"
    },
    "llama3.2": {
        "model": "ollama/llama3.2",
        "description": "Llama 3.2 - Meta's latest open model"
    },
    "deepseek-v3": {
        "model": "ollama/deepseek-v3",
        "description": "DeepSeek V3 - Great for agents and tool use (MIT license)"
    },
    "mistral": {
        "model": "ollama/mistral",
        "description": "Mistral - Fast and efficient"
    },
    # OpenAI models (paid)
    "gpt-4o": {
        "model": "gpt-4o",
        "description": "OpenAI GPT-4o - Best quality (paid)"
    },
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "description": "OpenAI GPT-4o Mini - Good balance of cost/quality (paid)"
    },
}

# Default model - change this to use a different model by default
DEFAULT_MODEL = os.getenv("CREWAI_MODEL", "qwen2.5")


def get_llm(model_name: str = None) -> str:
    """
    Get an LLM model string for CrewAI agents.

    Args:
        model_name: Name of the model preset to use.
                   If None, uses DEFAULT_MODEL or CREWAI_MODEL env var.

    Returns:
        Model string for CrewAI (e.g., "ollama/qwen2.5")
    """
    model_name = model_name or DEFAULT_MODEL

    if model_name not in MODEL_PRESETS:
        available = ", ".join(MODEL_PRESETS.keys())
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")

    config = MODEL_PRESETS[model_name]
    return config["model"]


def list_available_models():
    """Print available model presets."""
    print("\nAvailable LLM Models:")
    print("=" * 60)
    print("\nFREE (Local via Ollama):")
    for name, config in MODEL_PRESETS.items():
        if config["model"].startswith("ollama/"):
            print(f"  {name:15} - {config['description']}")

    print("\nPAID (OpenAI):")
    for name, config in MODEL_PRESETS.items():
        if not config["model"].startswith("ollama/"):
            print(f"  {name:15} - {config['description']}")

    print(f"\nCurrent default: {DEFAULT_MODEL}")
    print("Set CREWAI_MODEL env var to change default.")
    print("=" * 60)


if __name__ == "__main__":
    list_available_models()
