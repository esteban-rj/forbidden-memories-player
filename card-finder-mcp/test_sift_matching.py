#!/usr/bin/env python3
"""
Test SIFT Image Matching
========================

Tests for SIFT-based image matching functionality.
"""

import pytest
import os
from sift import has_sift_match, image_to_base64


class TestSiftMatching:
    """Test cases for SIFT image matching."""
    
    @pytest.fixture
    def base_image_path(self):
        """Path to the base image (InterfazJuego.png)."""
        return "template-test/InterfazJuego.png"
    
    @pytest.fixture
    def template_paths(self):
        """Paths to template images."""
        return {
            "template_1": "template-test/template_1.png",
            "template_2": "template-test/template_2.png", 
            "template_3": "template-test/template_3.png"
        }
    
    @pytest.fixture
    def base_image_base64(self, base_image_path):
        """Base image in base64 format."""
        assert os.path.exists(base_image_path), f"Base image not found: {base_image_path}"
        return image_to_base64(base_image_path)
    
    @pytest.fixture
    def template_base64_dict(self, template_paths):
        """Template images in base64 format."""
        base64_dict = {}
        for name, path in template_paths.items():
            assert os.path.exists(path), f"Template {name} not found: {path}"
            base64_dict[name] = image_to_base64(path)
        return base64_dict
    
    def test_template_1_should_match(self, base_image_base64, template_base64_dict):
        """Test that template_1.png matches with InterfazJuego.png."""
        assert base_image_base64 is not None, "Failed to convert base image to base64"
        assert template_base64_dict["template_1"] is not None, "Failed to convert template_1 to base64"
        
        result = has_sift_match(base_image_base64, template_base64_dict["template_1"])
        assert result is True, f"Expected template_1 to match, but got {result}"
    
    def test_template_2_should_match(self, base_image_base64, template_base64_dict):
        """Test that template_2.png matches with InterfazJuego.png."""
        assert base_image_base64 is not None, "Failed to convert base image to base64"
        assert template_base64_dict["template_2"] is not None, "Failed to convert template_2 to base64"
        
        result = has_sift_match(base_image_base64, template_base64_dict["template_2"])
        assert result is True, f"Expected template_2 to match, but got {result}"
    
    def test_template_3_should_not_match(self, base_image_base64, template_base64_dict):
        """Test that template_3.png does NOT match with InterfazJuego.png."""
        assert base_image_base64 is not None, "Failed to convert base image to base64"
        assert template_base64_dict["template_3"] is not None, "Failed to convert template_3 to base64"
        
        result = has_sift_match(base_image_base64, template_base64_dict["template_3"])
        assert result is False, f"Expected template_3 to NOT match, but got {result}"
    
    def test_all_templates_exist(self, template_paths):
        """Test that all template files exist."""
        for name, path in template_paths.items():
            assert os.path.exists(path), f"Template {name} not found: {path}"
    
    def test_base_image_exists(self, base_image_path):
        """Test that the base image exists."""
        assert os.path.exists(base_image_path), f"Base image not found: {base_image_path}"
    
    def test_base64_conversion(self, base_image_path, template_paths):
        """Test that base64 conversion works for all images."""
        # Test base image conversion
        base64_result = image_to_base64(base_image_path)
        assert base64_result is not None, f"Failed to convert base image to base64: {base_image_path}"
        assert len(base64_result) > 0, f"Base64 result is empty for base image: {base_image_path}"
        
        # Test template conversions
        for name, path in template_paths.items():
            base64_result = image_to_base64(path)
            assert base64_result is not None, f"Failed to convert {name} to base64: {path}"
            assert len(base64_result) > 0, f"Base64 result is empty for {name}: {path}"


if __name__ == "__main__":
    # Run tests directly if executed as script
    pytest.main([__file__, "-v"]) 