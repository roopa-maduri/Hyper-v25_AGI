# ===============================
# FILE 3/28: input_checker.py
# ===============================
"""
INPUT CHECKER - Validates all AGI inputs
First line of defense
"""

import json
import time

class InputChecker:
    def __init__(self):
        self.input_stats = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "suspicious": 0
        }
        self.suspicious_patterns = [
            "<!--", "-->",  # HTML comments
            "<script>", "</script>",  # Script tags
            "javascript:",  # JavaScript
            "onerror=", "onclick=",  # Event handlers
            "../", "~/",  # Path traversal
            "||", "&&",  # Command chaining
            "`", "$(",  # Command execution
        ]
    
    def validate(self, input_data):
        """Validate input data"""
        self.input_stats["total"] += 1
        
        # Type checking
        if input_data is None:
            self.input_stats["invalid"] += 1
            return {"valid": False, "reason": "Input is None"}
        
        # Convert to string for checking
        if not isinstance(input_data, (str, int, float, dict, list)):
            input_str = str(input_data)
        else:
            input_str = str(input_data) if not isinstance(input_data, str) else input_data
        
        # Length checking
        if len(input_str) > 10000:  # 10KB limit
            self.input_stats["invalid"] += 1
            return {"valid": False, "reason": "Input too large"}
        
        if len(input_str) < 1:
            self.input_stats["invalid"] += 1
            return {"valid": False, "reason": "Input empty"}
        
        # Suspicious pattern checking
        suspicious = False
        found_patterns = []
        
        input_lower = input_str.lower()
        for pattern in self.suspicious_patterns:
            if pattern in input_lower:
                suspicious = True
                found_patterns.append(pattern)
        
        if suspicious:
            self.input_stats["suspicious"] += 1
            return {
                "valid": False,
                "reason": f"Suspicious patterns: {found_patterns}",
                "data": None
            }
        
        # Structure checking (for JSON)
        if input_str.strip().startswith("{") or input_str.strip().startswith("["):
            try:
                json.loads(input_str)
            except:
                self.input_stats["invalid"] += 1
                return {"valid": False, "reason": "Invalid JSON structure"}
        
        # Content sanity check
        if self._is_gibberish(input_str):
            self.input_stats["invalid"] += 1
            return {"valid": False, "reason": "Input appears to be gibberish"}
        
        # All checks passed
        self.input_stats["valid"] += 1
        
        return {
            "valid": True,
            "data": input_str,
            "length": len(input_str),
            "timestamp": time.time(),
            "check_id": self.input_stats["total"]
        }
    
    def _is_gibberish(self, text):
        """Check if text appears to be gibberish"""
        if len(text) < 10:
            return False
        
        # Simple heuristic: ratio of alphanumeric to total characters
        alnum_count = sum(1 for c in text if c.isalnum())
        ratio = alnum_count / len(text)
        
        return ratio < 0.3  # Less than 30% alphanumeric
    
    def batch_validate(self, inputs_list):
        """Validate multiple inputs"""
        results = []
        for input_item in inputs_list:
            results.append(self.validate(input_item))
        return results
    
    def get_stats(self):
        """Get input checking statistics"""
        valid_rate = self.input_stats["valid"] / max(self.input_stats["total"], 1)
        
        return {
            "total_inputs": self.input_stats["total"],
            "valid_inputs": self.input_stats["valid"],
            "invalid_inputs": self.input_stats["invalid"],
            "suspicious_inputs": self.input_stats["suspicious"],
            "validity_rate": valid_rate,
            "patterns_checked": len(self.suspicious_patterns)
        }
    
    def add_custom_pattern(self, pattern):
        """Add custom suspicious pattern"""
        if pattern not in self.suspicious_patterns:
            self.suspicious_patterns.append(pattern)
            return True
        return False
