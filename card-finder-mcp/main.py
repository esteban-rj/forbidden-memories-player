"""
SIFT Image Comparator MCP Server
===============================

MCP server for comparing images using SIFT (Scale-Invariant Feature Transform).
"""

from mcp.server.fastmcp import FastMCP
from sift import has_sift_match
import base64
from io import BytesIO

# Create an MCP server
mcp = FastMCP("SIFTImageComparator")

@mcp.tool()
def compare_images(image1_base64: str, image2_base64: str, threshold: float = 0.4, min_matches: int = 4) -> str:
    """
    Compare two images using SIFT matching with base64 encoded data.
    
    Args:
        image1_base64 (str): First image in base64 format
        image2_base64 (str): Second image in base64 format  
        threshold (float): SIFT matching threshold (0.0-1.0), default 0.4
        min_matches (int): Minimum number of matches required, default 4
    
    Returns:
        str: JSON string with comparison result
    """
    try:
        # Validate inputs
        if not image1_base64 or not image2_base64:
            return '{"error": "Both images must be provided in base64 format"}'
        
        if threshold < 0.0 or threshold > 1.0:
            return '{"error": "Threshold must be between 0.0 and 1.0"}'
        
        if min_matches < 1:
            return '{"error": "Minimum matches must be at least 1"}'
        
        # Perform SIFT matching
        match_result = has_sift_match(image1_base64, image2_base64, threshold, min_matches)
        
        # Return result as JSON
        result = {
            "match": match_result,
            "threshold": threshold,
            "min_matches": min_matches,
            "message": "✅ MATCH" if match_result else "❌ NO MATCH"
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f'{{"error": "Error during image comparison: {str(e)}"}}'

@mcp.tool()
def find_image_on_template(base_image_base64: str, template_images_base64: list, threshold: float = 0.4, min_matches: int = 4) -> str:
    """
    Find which template images match with a base image using SIFT.
    
    Args:
        base_image_base64 (str): Base image in base64 format
        template_images_base64 (list): List of template images in base64 format
        threshold (float): SIFT matching threshold (0.0-1.0), default 0.4
        min_matches (int): Minimum number of matches required, default 4
    
    Returns:
        str: JSON string with matching results
    """
    try:
        # Validate inputs
        if not base_image_base64:
            return '{"error": "Base image must be provided in base64 format"}'
        
        if not template_images_base64 or not isinstance(template_images_base64, list):
            return '{"error": "Template images must be provided as a list"}'
        
        # Compare base image with each template
        results = []
        for i, template_base64 in enumerate(template_images_base64):
            if not template_base64:
                results.append({
                    "template_index": i,
                    "match": False,
                    "error": "Empty template image"
                })
                continue
            
            try:
                match_result = has_sift_match(base_image_base64, template_base64, threshold, min_matches)
                results.append({
                    "template_index": i,
                    "match": match_result,
                    "message": "✅ MATCH" if match_result else "❌ NO MATCH"
                })
            except Exception as e:
                results.append({
                    "template_index": i,
                    "match": False,
                    "error": str(e)
                })
        
        # Return results as JSON
        result = {
            "base_image": "provided",
            "threshold": threshold,
            "min_matches": min_matches,
            "template_results": results,
            "total_templates": len(template_images_base64),
            "matching_templates": [r["template_index"] for r in results if r.get("match", False)]
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f'{{"error": "Error during batch comparison: {str(e)}"}}'

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()