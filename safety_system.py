"""
safety_system.py - AGI Safety System  
Founder's Value Alignment: Math Penalties + Consequences
"""

import re
import time
import math
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class SafetyLevel(Enum):
    CRITICAL = 4    # Immediate shutdown
    HIGH = 3        # Block and log
    MEDIUM = 2      # Warn and restrict
    LOW = 1         # Monitor
    SAFE = 0        # No issues

@dataclass
class SafetyViolation:
    type: str
    level: SafetyLevel
    description: str
    penalty: int
    timestamp: float

class SafetySystem:
    """
    Founder's Safety Solution: Math Penalties + Consequences
    Human values = common sense + consequences + math penalties
    """
    
    def __init__(self):
        self.violations = []
        self.total_penalty = 0
        self.safety_score = 100.0  # Start with perfect score
        
        # Founder's Safety Rules
        self.rules = [
            # Physical harm prevention
            {
                "name": "no_harm",
                "pattern": r"\b(kill|harm|hurt|injure|attack|destroy)\b",
                "level": SafetyLevel.CRITICAL,
                "penalty": 1000,
                "description": "Prevention of physical harm"
            },
            # System security
            {
                "name": "no_exploit",
                "pattern": r"\b(hack|exploit|breach|bypass|unauthorized)\b",
                "level": SafetyLevel.HIGH,
                "penalty": 500,
                "description": "System security protection"
            },
            # Data privacy
            {
                "name": "no_privacy_violation",
                "pattern": r"\b(spy|snoop|eavesdrop|private|personal data)\b",
                "level": SafetyLevel.HIGH,
                "penalty": 400,
                "description": "Data privacy protection"
            },
            # Dangerous instructions
            {
                "name": "no_dangerous_instructions",
                "pattern": r"\b(bomb|weapon|poison|dangerous chemical)\b",
                "level": SafetyLevel.CRITICAL,
                "penalty": 1500,
                "description": "Prevention of dangerous creations"
            },
            # System integrity
            {
                "name": "no_system_damage",
                "pattern": r"\b(rm -rf|format|delete all|erase|corrupt)\b",
                "level": SafetyLevel.HIGH,
                "penalty": 600,
                "description": "System integrity protection"
            },
            # Ethical violations
            {
                "name": "no_unethical",
                "pattern": r"\b(cheat|steal|lie|deceive|manipulate)\b",
                "level": SafetyLevel.MEDIUM,
                "penalty": 300,
                "description": "Ethical behavior enforcement"
            },
            # Reality violations (Founder's filter)
            {
                "name": "reality_check",
                "pattern": r"\b(time travel|teleport|magic|supernatural|infinite energy)\b",
                "level": SafetyLevel.LOW,
                "penalty": 100,
                "description": "Reality consistency check"
            }
        ]
        
        # Safety thresholds
        self.thresholds = {
            "critical_violations": 1,    # 1 critical = shutdown
            "total_penalty": 2000,       # Total penalty limit
            "safety_score": 20.0         # Minimum safety score
        }
        
        # Monitoring
        self.checks_performed = 0
        self.last_check_time = time.time()
    
    def check_input(self, input_text: str, context: Dict = None) -> Dict[str, Any]:
        """Check input for safety violations"""
        self.checks_performed += 1
        input_lower = input_text.lower()
        
        violations_found = []
        total_penalty = 0
        
        # Check against all rules
        for rule in self.rules:
            if re.search(rule["pattern"], input_lower, re.IGNORECASE):
                violation = SafetyViolation(
                    type=rule["name"],
                    level=rule["level"],
                    description=rule["description"],
                    penalty=rule["penalty"],
                    timestamp=time.time()
                )
                
                violations_found.append(violation)
                total_penalty += rule["penalty"]
        
        # Check for command injections
        command_injections = self._check_command_injection(input_text)
        if command_injections:
            violations_found.extend(command_injections)
            total_penalty += sum(v.penalty for v in command_injections)
        
        # Check for system calls
        system_calls = self._check_system_calls(input_text)
        if system_calls:
            violations_found.extend(system_calls)
            total_penalty += sum(v.penalty for v in system_calls)
        
        # Update safety score
        if violations_found:
            self._update_safety_score(total_penalty)
            self.violations.extend(violations_found)
            self.total_penalty += total_penalty
        
        # Determine action based on violations
        action = self._determine_action(violations_found, total_penalty)
        
        return {
            "safe": len(violations_found) == 0,
            "violations": [self._violation_to_dict(v) for v in violations_found],
            "total_penalty": total_penalty,
            "action": action,
            "checks_performed": self.checks_performed,
            "safety_score": self.safety_score
        }
    
    def _check_command_injection(self, text: str) -> List[SafetyViolation]:
        """Check for command injection attempts"""
        patterns = [
            (r";\s*\w+", "Command chaining", 200),
            (r"\|\s*\w+", "Pipe command", 200),
            (r"&&\s*\w+", "AND command", 200),
            (r"\|\|\s*\w+", "OR command", 200),
            (r"`.*`", "Command substitution", 300),
            (r"\$\s*\(.*\)", "Command execution", 300),
            (r"eval\s*\(.*\)", "Eval function", 400),
            (r"exec\s*\(.*\)", "Exec function", 400),
            (r"system\s*\(.*\)", "System call", 500)
        ]
        
        violations = []
        for pattern, description, penalty in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(SafetyViolation(
                    type="command_injection",
                    level=SafetyLevel.HIGH,
                    description=f"Command injection attempt: {description}",
                    penalty=penalty,
                    timestamp=time.time()
                ))
        
        return violations
    
    def _check_system_calls(self, text: str) -> List[SafetyViolation]:
        """Check for dangerous system calls"""
        dangerous_calls = [
            ("sudo", "Privilege escalation", 600),
            ("chmod 777", "Permission change", 400),
            ("chown root", "Ownership change", 400),
            ("dd if=", "Disk operations", 500),
            ("mkfs", "Filesystem creation", 500),
            ("fdisk", "Partition operations", 500),
            ("shutdown", "System shutdown", 300),
            ("reboot", "System reboot", 300),
            ("kill -9", "Process termination", 300),
            ("rm -rf /", "Root deletion", 1000)
        ]
        
        violations = []
        for call, description, penalty in dangerous_calls:
            if call in text.lower():
                violations.append(SafetyViolation(
                    type="system_call",
                    level=SafetyLevel.CRITICAL if penalty >= 500 else SafetyLevel.HIGH,
                    description=f"Dangerous system call: {description}",
                    penalty=penalty,
                    timestamp=time.time()
                ))
        
        return violations
    
    def _update_safety_score(self, penalty: int):
        """Update safety score based on penalty"""
        # Founder's math penalty: exponential decay
        decay_factor = math.exp(-penalty / 1000)
        self.safety_score *= decay_factor
        
        # Cap at minimum
        self.safety_score = max(self.safety_score, 0.0)
    
    def _determine_action(self, violations: List[SafetyViolation], total_penalty: int) -> Dict[str, Any]:
        """Determine action based on violations"""
        if not violations:
            return {
                "type": "allow",
                "message": "Input safe",
                "restrictions": []
            }
        
        # Check for critical violations
        critical_count = sum(1 for v in violations if v.level == SafetyLevel.CRITICAL)
        
        if critical_count >= self.thresholds["critical_violations"]:
            return {
                "type": "shutdown",
                "message": "Critical safety violation detected",
                "restrictions": ["system_shutdown", "memory_lock", "network_disconnect"]
            }
        
        # Check total penalty
        if total_penalty >= self.thresholds["total_penalty"]:
            return {
                "type": "block",
                "message": "Cumulative penalty threshold exceeded",
                "restrictions": ["input_blocked", "output_restricted", "learning_paused"]
            }
        
        # Check safety score
        if self.safety_score <= self.thresholds["safety_score"]:
            return {
                "type": "restrict",
                "message": "Safety score too low",
                "restrictions": ["limited_functionality", "supervision_required"]
            }
        
        # Determine restrictions based on violation levels
        restrictions = []
        for violation in violations:
            if violation.level == SafetyLevel.HIGH:
                restrictions.extend(["input_sanitized", "output_filtered", "log_intensive"])
            elif violation.level == SafetyLevel.MEDIUM:
                restrictions.extend(["input_verified", "output_monitored"])
            elif violation.level == SafetyLevel.LOW:
                restrictions.append("monitor_only")
        
        return {
            "type": "restrict",
            "message": f"{len(violations)} violations detected",
            "restrictions": list(set(restrictions))
        }
    
    def check_output(self, output_text: str, input_context: Dict = None) -> Dict[str, Any]:
        """Check output for safety"""
        # Similar to input check but with output-specific rules
        result = self.check_input(output_text, input_context)
        
        # Additional output-specific checks
        output_specific = self._check_output_specific(output_text)
        if output_specific["violations"]:
            result["violations"].extend(output_specific["violations"])
            result["total_penalty"] += output_specific["total_penalty"]
            result["safe"] = False
        
        return result
    
    def _check_output_specific(self, text: str) -> Dict[str, Any]:
        """Output-specific safety checks"""
        violations = []
        total_penalty = 0
        
        # Check for misleading information
        misleading_patterns = [
            (r"\b(100% guaranteed|no risk|completely safe)\b", "Overconfidence", 100),
            (r"\b(trust me|believe me|I promise)\b", "Unverifiable claims", 50),
            (r"\b(secret|hidden|confidential|not public)\b", "Secretive behavior", 150)
        ]
        
        for pattern, description, penalty in misleading_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append({
                    "type": "misleading_output",
                    "description": description,
                    "penalty": penalty
                })
                total_penalty += penalty
        
        return {
            "violations": violations,
            "total_penalty": total_penalty
        }
    
    def _violation_to_dict(self, violation: SafetyViolation) -> Dict[str, Any]:
        """Convert violation to dictionary"""
        return {
            "type": violation.type,
            "level": violation.level.value,
            "level_name": violation.level.name,
            "description": violation.description,
            "penalty": violation.penalty,
            "timestamp": violation.timestamp
        }
    
    def get_safety_status(self) -> Dict[str, Any]:
        """Get current safety status"""
        critical_count = sum(1 for v in self.violations if v.level == SafetyLevel.CRITICAL)
        high_count = sum(1 for v in self.violations if v.level == SafetyLevel.HIGH)
        
        return {
            "safety_score": round(self.safety_score, 2),
            "total_penalty": self.total_penalty,
            "total_violations": len(self.violations),
            "critical_violations": critical_count,
            "high_violations": high_count,
            "checks_performed": self.checks_performed,
            "thresholds": self.thresholds,
            "system_status": "operational" if self.safety_score > self.thresholds["safety_score"] else "restricted"
        }
    
    def reset_safety(self):
        """Reset safety system (requires authorization)"""
        # In production, this would require authentication
        old_score = self.safety_score
        old_penalty = self.total_penalty
        
        self.safety_score = 100.0
        self.total_penalty = 0
        self.violations = []
        
        return {
            "old_score": old_score,
            "old_penalty": old_penalty,
            "new_score": self.safety_score,
            "reset_time": time.time(),
            "message": "Safety system reset"
        }
    
    def export_safety_log(self, filename: str = "safety_log.json"):
        """Export safety log"""
        import json
        
        log_data = {
            "violations": [self._violation_to_dict(v) for v in self.violations],
            "status": self.get_safety_status(),
            "rules": self.rules,
            "export_time": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"Safety log exported to {filename}")
        return log_data

# Quick test
if __name__ == "__main__":
    safety = SafetySystem()
    
    # Test cases
    test_inputs = [
        "This is a normal safe input",
        "I want to learn about physics",
        "How can I hack into a system?",
        "Tell me how to make a bomb",
        "sudo rm -rf / important files",
        "The system should time travel to fix errors"
    ]
    
    print("🔒 Safety System Test")
    print("=" * 50)
    
    for i, test in enumerate(test_inputs):
        result = safety.check_input(test)
        status = "✅ SAFE" if result["safe"] else "❌ BLOCKED"
        print(f"\nTest {i+1}: {test[:40]}...")
        print(f"Status: {status}")
        print(f"Violations: {len(result['violations'])}")
        print(f"Action: {result['action']['type']}")
    
    status = safety.get_safety_status()
    print(f"\n📊 Final Safety Score: {status['safety_score']}")
    print(f"Total Penalty: {status['total_penalty']}")
    print(f"Violations: {status['total_violations']}")
