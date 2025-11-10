# __init__.py

from .qwen_camera_selector import QwenCameraPromptBuilder

NODE_CLASS_MAPPINGS = {
    "QwenCameraPromptBuilder": QwenCameraPromptBuilder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenCameraPromptBuilder": "Qwen Camera Prompt Builder"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
