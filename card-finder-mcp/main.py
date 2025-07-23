"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
from PIL import Image
import os
import base64
from io import BytesIO
import requests
from resnet import ResNETImageComparator

# Create an MCP server
mcp = FastMCP("ResNETImageComparator")

# Initialize ResNET comparator
resnet_comparator = ResNETImageComparator()

@mcp.tool()
def find(image1_base64: str, image2_base64: str) -> str:
    """Compare two images using base64 encoded data"""
    try:
        # Decodificar base64 a bytes
        img1_data = base64.b64decode(image1_base64)
        img2_data = base64.b64decode(image2_base64)
        
        # Cargar imágenes desde bytes
        img1 = Image.open(BytesIO(img1_data))
        img2 = Image.open(BytesIO(img2_data))
        
        # Tu lógica de comparación aquí
        return f"Imágenes cargadas: {img1.size} y {img2.size}"
        
    except Exception as e:
        return f"Error al cargar imágenes: {str(e)}"