# qwen_camera_selector.py

class QwenCameraPromptBuilder:
    """
    Multi-section camera prompt builder for Qwen-Edit-2509 Multiple-Angles.

    Groups (all optional):
      - core_movement            (position moves)
      - orbit_rotation           (around subject)
      - vertical_view            (tilt / angle)
      - lens_framing             (lens / shot type)
      - combined_action          (pre-made combos)
      - keep_character_consistency (toggle for identity stability line)
      - enable_light_restoration (toggle for relighting phrase)
      - extra_instruction        (free-text add-on)

    The node concatenates all non-"None" selections (plus any toggles and
    extra_instruction) into a single STRING output.
    """

    CATEGORY = "Qwen / Utils"

    @classmethod
    def INPUT_TYPES(cls):
        # Core movement
        core_movement_options = [
            "None",
            "Move the camera forward.",
            "Move the camera backward.",
            "Move the camera left.",
            "Move the camera right.",
            "Move the camera up.",
            "Move the camera down.",
        ]

        # Orbit / rotation
        orbit_options = [
            "None",
            "Rotate the camera 45 degrees to the left around the subject.",
            "Rotate the camera 90 degrees to the left around the subject.",
            "Rotate the camera 45 degrees to the right around the subject.",
            "Rotate the camera 90 degrees to the right around the subject.",
            "Rotate the camera 45 degrees to the left.",
            "Rotate the camera 90 degrees to the left.",
            "Rotate the camera 45 degrees to the right.",
            "Rotate the camera 90 degrees to the right.",
        ]

        # Vertical tilt / view
        vertical_options = [
            "None",
            "Tilt the camera up slightly.",
            "Tilt the camera up a lot.",
            "Tilt the camera down slightly.",
            "Tilt the camera down a lot.",
            "Turn the camera to a top-down view.",
            "Turn the camera to a bird’s-eye view.",
            "Turn the camera to a high-angle view looking down at the subject.",
            "Turn the camera to a low-angle view looking up at the subject.",
        ]

        # Lens / framing
        lens_options = [
            "None",
            "Turn the camera to a wide-angle lens.",
            "Turn the camera to an ultra-wide-angle lens.",
            "Turn the camera to a close-up.",
            "Turn the camera to an extreme close-up of the face.",
            "Turn the camera to a medium shot of the subject.",
            "Turn the camera to a full-body shot.",
            "Turn the camera to a long shot showing the whole scene.",
        ]

        # Combined movement + lens
        combined_options = [
            "None",
            "Move the camera forward and turn the camera to a close-up.",
            "Move the camera backward and turn the camera to a wide-angle lens.",
            "Rotate the camera 45 degrees to the left around the subject and tilt the camera down slightly.",
            "Rotate the camera 45 degrees to the right around the subject and tilt the camera up slightly.",
            "Move the camera up and turn the camera to a bird’s-eye view.",
        ]

        return {
            "required": {},
            "optional": {
                "core_movement": (core_movement_options, {"default": "None"}),
                "orbit_rotation": (orbit_options, {"default": "None"}),
                "vertical_view": (vertical_options, {"default": "None"}),
                "lens_framing": (lens_options, {"default": "None"}),
                "combined_action": (combined_options, {"default": "None"}),

                # New: simple toggle instead of mode/safety dropdown logic
                "keep_character_consistency": ("BOOLEAN", {"default": False}),

                # Relighting toggle for the light-restoration LoRA
                "enable_light_restoration": ("BOOLEAN", {"default": False}),

                # Free-text add-on
                "extra_instruction": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt_text",)
    FUNCTION = "build_prompt"

    def build_prompt(
        self,
        core_movement: str = "None",
        orbit_rotation: str = "None",
        vertical_view: str = "None",
        lens_framing: str = "None",
        combined_action: str = "None",
        keep_character_consistency: bool = False,
        enable_light_restoration: bool = False,
        extra_instruction: str = "",
    ):
        parts = []

        def add_if_not_none(value: str):
            if isinstance(value, str) and value != "None":
                parts.append(value)

        # Main camera instructions
        add_if_not_none(combined_action)
        add_if_not_none(core_movement)
        add_if_not_none(orbit_rotation)
        add_if_not_none(vertical_view)
        add_if_not_none(lens_framing)

        # Character consistency toggle
        if keep_character_consistency:
            parts.append("Ensure that the character’s face and body proportions remain unchanged.")

        # Light restoration toggle (English wording)
        if enable_light_restoration:
            parts.append("Remove the shadows and use soft lighting to relight the image.")

        # Extra text
        if isinstance(extra_instruction, str):
            extra = extra_instruction.strip()
            if extra:
                parts.append(extra)

        final_prompt = " ".join(parts).strip()
        return (final_prompt,)
