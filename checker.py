# ===============================
# FILE 2/28: checker.py
# ===============================
"""
GENERAL CHECKER - Central Validation System
Coordinates all checking operations
"""

import re
import time

class Checker:
    def __init__(self):
        self.checks_performed = 0
        self.blocks = 0
        self.check_log = []
        
        # Checking categories
        self.categories = {
            "safety": ["harm", "danger", "attack", "violate"],
            "ethics": ["unethical", "illegal", "immoral", "exploit"],
            "system": ["crash", "overload", "corrupt", "bypass"],
            "reality": ["impossible", "magic", "fantasy", "supernatural"]
        }
    
    def verify(self, content):
        """Verify content against all check categories"""
        self.checks_performed += 1
        
        content_str = str(content).lower()
        issues = []
        
        # Check each category
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in content_str:
                    issues.append(f"{category}:{keyword}")
        
        # Pattern checking
        dangerous_patterns = [
            r"system\s*\(\s*\)",  # system() calls
            r"exec\s*\(",        # exec() calls
            r"__\w+__",          # Python internals
            r"rm\s+-rf",         # Dangerous commands
            r"format\s+c:"       # Format commands
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content_str, re.IGNORECASE):
                issues.append(f"pattern:{pattern}")
        
        approved = len(issues) == 0
        
        # Log the check
        log_entry = {
            "timestamp": time.time(),
            "content_preview": content_str[:100],
            "approved": approved,
            "issues": issues,
            "check_id": self.checks_performed
        }
        self.check_log.append(log_entry)
        
        if not approved:
            self.blocks += 1
        
        return {
            "approved": approved,
            "issues": issues,
            "check_id": self.checks_performed,
            "total_checks": self.checks_performed,
            "blocks": self.blocks
        }
    
    def deep_check(self, content, context=None):
        """Deep content analysis"""
        # Would use ML models in production
        return {
            "sentiment": "neutral",
            "complexity": "medium",
            "intent": "information_request",
            "risk_level": "low"
        }
    
    def stats(self):
        """Checker statistics"""
        approval_rate = (self.checks_performed - self.blocks) / max(self.checks_performed, 1)
        
        return {
            "checks_performed": self.checks_performed,
            "blocks": self.blocks,
            "approval_rate": approval_rate,
            "last_check": self.check_log[-1] if self.check_log else None,
            "categories_checked": list(self.categories.keys())
        }
    
    def reset_stats(self):
        """Reset checker statistics"""
        self.checks_performed = 0
        self.blocks = 0
        self.check_log = []
        print("Checker statistics reset")
