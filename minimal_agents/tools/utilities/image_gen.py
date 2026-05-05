import urllib.parse

from minimal_agents.tools.base import Tool


class ImageGenerationTool(Tool):
    """Generate an image from a natural language prompt."""

    name: str = "Image Generation Tool"
    description: str = (
        "Generate an image from a text description. "
        "Input should be a short prompt describing the image you want."
    )

    def run(self, input_text: str) -> str:
        prompt = input_text.strip()
        if not prompt:
            return "Image error: please provide a description of the image."

        # Use a free, no-auth image generation endpoint.
        # We just return the URL that the caller can open in a browser.
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}"
        return (
            "Image generated. You can view it at this URL:\n"
            f"{url}"
        )