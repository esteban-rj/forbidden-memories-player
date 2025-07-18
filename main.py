import cv2
import numpy as np
import mss
import time
import argparse
from typing import Optional, Tuple


class WindowCapture:
    def __init__(self, monitor_index: int = 1):
        """
        Initialize window capture with specified monitor.
        
        Args:
            monitor_index: Monitor index (0 for primary, 1 for secondary, etc.)
        """
        self.sct = mss.mss()
        self.monitor_index = monitor_index
        self.monitors = self.sct.monitors
        
    def get_monitor_info(self) -> dict:
        """Get information about available monitors."""
        return {
            'monitors': self.monitors,
            'current_monitor': self.monitors[self.monitor_index] if self.monitor_index < len(self.monitors) else self.monitors[1]
        }
    
    def capture_monitor(self, monitor_index: Optional[int] = None) -> np.ndarray:
        """
        Capture the specified monitor.
        
        Args:
            monitor_index: Monitor to capture (uses self.monitor_index if None)
            
        Returns:
            Captured image as numpy array
        """
        if monitor_index is None:
            monitor_index = self.monitor_index
            
        if monitor_index >= len(self.monitors):
            print(f"Monitor {monitor_index} not available. Using monitor 1.")
            monitor_index = 1
            
        monitor = self.monitors[monitor_index]
        screenshot = self.sct.grab(monitor)
        
        # Convert to numpy array
        img = np.array(screenshot)
        # Convert from BGRA to BGR (remove alpha channel)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Capture a specific region of the screen.
        
        Args:
            x, y: Top-left coordinates
            width, height: Dimensions of the region
            
        Returns:
            Captured image as numpy array
        """
        region = {
            'top': y,
            'left': x,
            'width': width,
            'height': height
        }
        
        screenshot = self.sct.grab(region)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img


class WindowDisplay:
    def __init__(self, window_name: str = "Window Capture"):
        """
        Initialize window display.
        
        Args:
            window_name: Name of the display window
        """
        self.window_name = window_name
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
    def show_image(self, image: np.ndarray, resize_factor: float = 0.5):
        """
        Display an image in the window.
        
        Args:
            image: Image to display
            resize_factor: Factor to resize the image (0.5 = half size)
        """
        if resize_factor != 1.0:
            height, width = image.shape[:2]
            new_width = int(width * resize_factor)
            new_height = int(height * resize_factor)
            image = cv2.resize(image, (new_width, new_height))
            
        cv2.imshow(self.window_name, image)
        
    def wait_key(self, delay: int = 1) -> int:
        """
        Wait for a key press.
        
        Args:
            delay: Delay in milliseconds
            
        Returns:
            Key code pressed
        """
        return cv2.waitKey(delay)
        
    def destroy(self):
        """Destroy the display window."""
        cv2.destroyAllWindows()


def list_monitors():
    """List all available monitors."""
    sct = mss.mss()
    monitors = sct.monitors
    
    print("Available monitors:")
    for i, monitor in enumerate(monitors):
        print(f"  Monitor {i}: {monitor['width']}x{monitor['height']} at ({monitor['left']}, {monitor['top']})")
    
    return monitors


def continuous_capture(monitor_index: int = 1, resize_factor: float = 0.5, fps: int = 30):
    """
    Continuously capture and display a monitor.
    
    Args:
        monitor_index: Monitor to capture
        resize_factor: Factor to resize the display
        fps: Target frames per second
    """
    capture = WindowCapture(monitor_index)
    display = WindowDisplay(f"Monitor {monitor_index} Capture")
    
    # Get monitor info
    monitor_info = capture.get_monitor_info()
    print(f"Capturing: {monitor_info['current_monitor']}")
    print(f"Press 'q' to quit, 's' to save screenshot")
    
    frame_delay = 1.0 / fps
    
    try:
        while True:
            start_time = time.time()
            
            # Capture the monitor
            frame = capture.capture_monitor()
            
            # Display the frame
            display.show_image(frame, resize_factor)
            
            # Handle key presses
            key = display.wait_key(1)
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('s'):
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
            
            # Maintain target FPS
            elapsed = time.time() - start_time
            if elapsed < frame_delay:
                time.sleep(frame_delay - elapsed)
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        display.destroy()


def capture_region_continuous(x: int, y: int, width: int, height: int, 
                            resize_factor: float = 1.0, fps: int = 30):
    """
    Continuously capture and display a specific region.
    
    Args:
        x, y: Top-left coordinates of the region
        width, height: Dimensions of the region
        resize_factor: Factor to resize the display
        fps: Target frames per second
    """
    capture = WindowCapture()
    display = WindowDisplay(f"Region Capture ({x},{y},{width}x{height})")
    
    print(f"Capturing region: ({x}, {y}) {width}x{height}")
    print(f"Press 'q' to quit, 's' to save screenshot")
    
    frame_delay = 1.0 / fps
    
    try:
        while True:
            start_time = time.time()
            
            # Capture the region
            frame = capture.capture_region(x, y, width, height)
            
            # Display the frame
            display.show_image(frame, resize_factor)
            
            # Handle key presses
            key = display.wait_key(1)
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('s'):
                timestamp = int(time.time())
                filename = f"region_screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
            
            # Maintain target FPS
            elapsed = time.time() - start_time
            if elapsed < frame_delay:
                time.sleep(frame_delay - elapsed)
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        display.destroy()


def main():
    parser = argparse.ArgumentParser(description="Window capture and display tool")
    parser.add_argument("--list-monitors", action="store_true", 
                       help="List available monitors and exit")
    parser.add_argument("--monitor", type=int, default=1,
                       help="Monitor index to capture (default: 1)")
    parser.add_argument("--region", nargs=4, type=int, metavar=("X", "Y", "WIDTH", "HEIGHT"),
                       help="Capture specific region instead of full monitor")
    parser.add_argument("--resize", type=float, default=0.5,
                       help="Resize factor for display (default: 0.5)")
    parser.add_argument("--fps", type=int, default=30,
                       help="Target FPS (default: 30)")
    
    args = parser.parse_args()
    
    if args.list_monitors:
        list_monitors()
        return
    
    print("Window Capture Tool")
    print("===================")
    
    if args.region:
        x, y, width, height = args.region
        capture_region_continuous(x, y, width, height, args.resize, args.fps)
    else:
        continuous_capture(args.monitor, args.resize, args.fps)


if __name__ == "__main__":
    main()
