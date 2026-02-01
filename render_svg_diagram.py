import requests
import base64
import json
import pathlib

def render_mermaid_to_svg(mermaid_code: str, output_file: pathlib.Path):
    """
    Renders a Mermaid diagram code into an SVG file using the Mermaid.ink API.
    """
    # Encode the Mermaid code to base64 for the API
    encoded_mermaid = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    # Construct the API URL for SVG output
    api_url = f"https://mermaid.ink/svg/{encoded_mermaid}"

    print(f"Requesting SVG from Mermaid.ink API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the SVG content to the specified file
        output_file.write_bytes(response.content)
        print(f"Success! SVG diagram saved to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error rendering SVG: {e}")
        if response is not None:
            print(f"Response content: {response.text}")

async def main(): # Renamed to async main for consistency, but not strictly async here
    markdown_file = pathlib.Path("ARCHITECTURE.md")
    output_file = pathlib.Path("frontend_architecture.svg")

    # 1. Read the Markdown file and extract the Mermaid code
    print(f"Reading diagram from {markdown_file}...")
    try:
        content = markdown_file.read_text()
        # Use regex to find the content within the mermaid code block
        import re
        match = re.search(r"```mermaid(.*)```", content, re.DOTALL)
        if not match:
            print("Error: Could not find a 'mermaid' code block in the file.")
            return
        diagram_code = match.group(1).strip()
    except FileNotFoundError:
        print(f"Error: {markdown_file} not found.")
        return

    # 2. Render and save the SVG
    render_mermaid_to_svg(diagram_code, output_file)

if __name__ == "__main__":
    # Run the synchronous main function
    import asyncio
    asyncio.run(main())
