# Forbidden Memories Player - Window Capture Tool

A Python tool for continuously capturing and displaying window/screen content in real-time.

## Features

- **Monitor Capture**: Capture entire monitors at specified FPS
- **Region Capture**: Capture specific screen regions
- **Real-time Display**: View captured content in a resizable window
- **Screenshot Saving**: Save frames with 's' key
- **Multiple Monitor Support**: Work with any connected monitor
- **Configurable FPS**: Adjust capture rate for performance

## Installation

1. Install dependencies:
```bash
pip install -e .
```

## Usage

### List Available Monitors
```bash
python main.py --list-monitors
```

### Capture Full Monitor
```bash
# Capture monitor 1 (default) at 50% size, 30 FPS
python main.py

# Capture monitor 0 (primary) at 75% size, 60 FPS
python main.py --monitor 0 --resize 0.75 --fps 60
```

### Capture Specific Region
```bash
# Capture region starting at (100, 200) with size 800x600
python main.py --region 100 200 800 600

# Capture region at full size, 15 FPS
python main.py --region 0 0 1920 1080 --resize 1.0 --fps 15
```

## Controls

- **'q'**: Quit the application
- **'s'**: Save current frame as screenshot
- **Ctrl+C**: Force quit (keyboard interrupt)

## Examples

### Basic Usage
```bash
# Start with default settings (monitor 1, 50% size, 30 FPS)
python main.py
```

### High Performance Capture
```bash
# Capture primary monitor at full size, 60 FPS
python main.py --monitor 0 --resize 1.0 --fps 60
```

### Region Monitoring
```bash
# Monitor a specific application window area
python main.py --region 500 300 400 300 --resize 1.5
```

## Technical Details

- Uses `mss` for fast screen capture
- Uses `opencv-python` for image processing and display
- Supports multiple monitors and custom regions
- Configurable FPS with frame timing control
- Automatic color space conversion (BGRA to BGR)

## Requirements

- Python 3.12+
- Linux with X11 or Wayland
- Sufficient RAM for image processing
- Graphics drivers that support screen capture

## Troubleshooting

1. **Permission Issues**: Ensure your user has permission to capture screen content
2. **Performance**: Lower FPS or resize factor if experiencing lag
3. **Monitor Index**: Use `--list-monitors` to see available monitors
4. **Display Issues**: Try different resize factors or monitor indices
