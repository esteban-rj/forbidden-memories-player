# SIFT Image Comparator MCP Server

A Model Context Protocol (MCP) server for comparing images using SIFT (Scale-Invariant Feature Transform) algorithm.

## Features

- **SIFT-based Image Matching**: Uses OpenCV's SIFT implementation for robust image comparison
- **Base64 Support**: Works with base64-encoded images for easy integration
- **Configurable Parameters**: Adjustable threshold and minimum matches for fine-tuning
- **Batch Processing**: Compare one image against multiple templates
- **Docker Support**: Complete containerization for easy deployment

## MCP Configuration for Claude

### Add to Claude Desktop

1. Open Claude Desktop
2. Go to Settings → Model Context Protocol
3. Add a new server with the following configuration:

```json
{
  "mcpServers": {
    "sift-image-comparator": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/card-finder-mcp",
      "env": {
        "PYTHONPATH": "/path/to/card-finder-mcp"
      }
    }
  }
}
```

### Docker Configuration

If using Docker, use this configuration instead:

```json
{
  "mcpServers": {
    "sift-image-comparator": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "sift-mcp-server"]
    }
  }
}
```

### Available Tools

Once configured, Claude will have access to these tools:

#### `compare_images`
Compare two images using SIFT matching.

**Parameters:**
- `image1_base64` (str): First image in base64 format
- `image2_base64` (str): Second image in base64 format
- `threshold` (float): SIFT matching threshold (0.0-1.0), default 0.4
- `min_matches` (int): Minimum number of matches required, default 4

**Returns:** JSON string with comparison result

#### `find_image_on_template`
Compare one base image against multiple template images.

**Parameters:**
- `base_image_base64` (str): Base image in base64 format
- `template_images_base64` (list): List of template images in base64 format
- `threshold` (float): SIFT matching threshold (0.0-1.0), default 0.4
- `min_matches` (int): Minimum number of matches required, default 4

**Returns:** JSON string with matching results for all templates

## Installation

### Local Development

```bash
# Install dependencies
uv sync

# Run the server
uv run python main.py
```

### Docker

```bash
# Build image
docker build -t sift-mcp-server .

# Run container
docker run -it --rm sift-mcp-server
```

## Usage Examples

### Basic Image Comparison

```python
# Convert images to base64
import base64

with open("image1.png", "rb") as f:
    img1_base64 = base64.b64encode(f.read()).decode()

with open("image2.png", "rb") as f:
    img2_base64 = base64.b64encode(f.read()).decode()

# Compare using Claude
result = compare_images(img1_base64, img2_base64, threshold=0.4, min_matches=4)
```

### Template Matching

```python
# Load base image and templates
base_image = "base64_string_of_base_image"
templates = ["base64_string_template1", "base64_string_template2", "base64_string_template3"]

# Find matches
result = find_image_on_template(base_image, templates, threshold=0.4, min_matches=4)
```

## Testing

Run the test suite:

```bash
# Local
uv run python -m pytest test_sift_matching.py -v

# Docker
./run_tests_docker.sh  # Linux/Mac
.\run_tests_docker.ps1  # Windows
```

## Configuration

- **threshold**: SIFT matching threshold (0.0-1.0), default 0.4
- **min_matches**: Minimum number of matches required, default 4

## Dependencies

- Python 3.12+
- OpenCV
- MCP Server
- pytest (for testing)

## License

MIT License
