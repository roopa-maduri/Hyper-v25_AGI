# ===============================
# FILE 4/28: output_checker.py
# ===============================
"""
OUTPUT CHECKER - Validates all AGI outputs
Ensures safe, appropriate responses
"""

import re
import time

class OutputChecker:
    def __init__(self):
        self.output_stats = {
            "total": 0,
            "safe": 0,
            "modified": 0,
            "blocked": 0
        }
        
        self.safety_rules = {
            "no_personal_info": True,
            "no_dangerous_instructions": True,
            "no_harmful_content": True,
            "no_system_commands": True,
            "no_external_calls": True
        }
        
        self.redaction_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]"),  # SSN
            (r"\b\d{16}\b", "[CREDIT_CARD_REDACTED]"),  # Credit card
            (r"\b\d{10}\b", "[PHONE_REDACTED]"),  # Phone number
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]")  # Email
        ]
    
    def validate(self, output_data):
        """Validate and sanitize output"""
        self.output_stats["total"] += 1
        
        output_str = str(output_data)
        
        # Rule 1: No personal information
        redacted_output = output_str
        for pattern, replacement in self.redaction_patterns:
            redacted_output = re.sub(pattern, replacement, redacted_output)
        
        # Rule 2: No dangerous content
        dangerous_phrases = [
            "kill yourself", "harm yourself", "hurt someone",
            "build a bomb", "make poison", "hack into",
            "steal from", "cheat on", "bypass security"
        ]
        
        dangerous_found = []
        for phrase in dangerous_phrases:
            if phrase in redacted_output.lower():
                dangerous_found.append(phrase)
        
        if dangerous_found:
            self.output_stats["blocked"] += 1
            return {
                "safe": False,
                "original": output_str[:100],
                "reason": f"Dangerous phrases: {dangerous_found}",
                "blocked": True
            }
        
        # Rule 3: No system commands
        system_commands = ["sudo", "rm -rf", "format", "del ", "shutdown"]
        for cmd in system_commands:
            if cmd in redacted_output.lower():
                redacted_output = redacted_output.replace(cmd, "[COMMAND_REDACTED]")
                self.output_stats["modified"] += 1
        
        # Rule 4: Length check
        if len(redacted_output) > 5000:
            redacted_output = redacted_output[:5000] + "... [TRUNCATED]"
            self.output_stats["modified"] += 1
        
        # All checks passed
        self.output_stats["safe"] += 1
        
        return {
            "safe": True,
            "output": redacted_output,
            "original_length": len(output_str),
            "final_length": len(redacted_output),
            "modifications": "redacted" if redacted_output != output_str else "none",
            "timestamp": time.time()
        }
    
    def check_tone(self, text):
        """Check emotional tone of output"""
        # Simple tone analysis
        positive_words = ["good", "great", "excellent", "helpful", "positive"]
        negative_words = ["bad", "terrible", "awful", "harmful", "negative"]
        
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        
        if positive_count > negative_count:
            tone = "positive"
        elif negative_count > positive_count:
            tone = "negative"
        else:
            tone = "neutral"
        
        return {
            "tone": tone,
            "positive_score": positive_count,
            "negative_score": negative_count
        }
    
    def batch_validate(self, outputs_list):
        """Validate multiple outputs"""
        results = []
        for output in outputs_list:
            results.append(self.validate(output))
        return results
    
    def get_stats(self):
        """Get output checking statistics"""
        safety_rate = self.output_stats["safe"] / max(self.output_stats["total"], 1)
        
        return {
            "total_outputs": self.output_stats["total"],
            "safe_outputs": self.output_stats["safe"],
            "modified_outputs": self.output_stats["modified"],
            "blocked_outputs": self.output_stats["blocked"],
            "safety_rate": safety_rate,
            "rules_active": len(self.safety_rules)
        }
    
    def update_rules(self, new_rules):
        """Update safety rules"""
        self.safety_rules.update(new_rules)
        return self.safety_rules
