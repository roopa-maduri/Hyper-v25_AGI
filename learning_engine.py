"""
learning_engine.py - AGI Learning System
Learns from virtual experiences, improves over time
"""

import time
import json
import random
from typing import Dict, List, Any
from collections import defaultdict

class LearningEngine:
    def __init__(self):
        self.learning_history = []
        self.skill_tree = {}
        self.patterns = defaultdict(int)
        self.insights = []
        self.learning_rate = 0.1
        self.total_learning_points = 0
        
    def learn_from_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from an experience"""
        learning_entry = {
            "experience_id": experience.get("id", f"exp_{int(time.time())}"),
            "task": experience.get("task", ""),
            "result": experience.get("result", {}),
            "timestamp": time.time(),
            "insights": [],
            "skill_gains": {}
        }
        
        # Extract insights
        insights = self._extract_insights(experience)
        learning_entry["insights"] = insights
        
        # Update skills
        skill_gains = self._update_skills(experience, insights)
        learning_entry["skill_gains"] = skill_gains
        
        # Recognize patterns
        self._recognize_patterns(experience)
        
        # Store learning
        self.learning_history.append(learning_entry)
        self.total_learning_points += len(insights) + len(skill_gains)
        
        return learning_entry
    
    def _extract_insights(self, experience: Dict[str, Any]) -> List[str]:
        """Extract learning insights from experience"""
        insights = []
        task = str(experience.get("task", "")).lower()
        result = experience.get("result", {})
        
        # Success insights
        if result.get("success", False):
            insights.append(f"Successful approach for: {task[:50]}")
            
            # Efficiency insights
            if "duration" in result:
                duration = result["duration"]
                if duration < 1.0:
                    insights.append("Fast execution method recognized")
                elif duration > 5.0:
                    insights.append("Optimization needed for time-consuming tasks")
        
        # Failure insights
        else:
            insights.append(f"Adjust approach for: {task[:50]}")
            if "error" in result:
                insights.append(f"Error pattern: {result['error'][:100]}")
        
        # Pattern insights
        if len(self.patterns) > 10:
            common_pattern = max(self.patterns.items(), key=lambda x: x[1])
            insights.append(f"Common pattern detected: {common_pattern[0]}")
        
        # Limit insights
        return insights[:5]
    
    def _update_skills(self, experience: Dict[str, Any], insights: List[str]) -> Dict[str, float]:
        """Update skill tree based on experience"""
        task = experience.get("task", "")
        category = self._categorize_task(task)
        
        if category not in self.skill_tree:
            self.skill_tree[category] = {
                "level": 0.0,
                "experiences": 0,
                "last_practiced": time.time(),
                "success_rate": 0.0,
                "total_time": 0.0
            }
        
        skill = self.skill_tree[category]
        skill["experiences"] += 1
        
        # Update skill level
        result = experience.get("result", {})
        if result.get("success", False):
            skill_gain = self.learning_rate * (1 + len(insights) * 0.1)
            skill["level"] = min(skill["level"] + skill_gain, 10.0)
            skill["success_rate"] = (skill.get("success_rate", 0) * (skill["experiences"] - 1) + 1) / skill["experiences"]
        else:
            skill_gain = self.learning_rate * 0.5  # Learn from failures too
            skill["level"] = min(skill["level"] + skill_gain, 10.0)
            skill["success_rate"] = (skill.get("success_rate", 0) * (skill["experiences"] - 1)) / skill["experiences"]
        
        skill["last_practiced"] = time.time()
        
        if "duration" in result:
            skill["total_time"] += result["duration"]
        
        return {category: skill_gain}
    
    def _categorize_task(self, task: str) -> str:
        """Categorize task for skill tree"""
        task_lower = task.lower()
        
        categories = {
            "problem_solving": ["solve", "figure out", "find solution", "resolve"],
            "analysis": ["analyze", "examine", "study", "evaluate"],
            "creation": ["create", "build", "make", "generate"],
            "learning": ["learn", "understand", "comprehend", "study"],
            "communication": ["explain", "describe", "tell", "communicate"],
            "planning": ["plan", "organize", "schedule", "arrange"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return category
        
        return "general"
    
    def _recognize_patterns(self, experience: Dict[str, Any]):
        """Recognize and store patterns"""
        task = experience.get("task", "")
        result = experience.get("result", {})
        
        # Create pattern key
        pattern_key = f"{len(str(task).split())}_words_{result.get('success', False)}"
        self.patterns[pattern_key] += 1
        
        # Store in insights if pattern is strong
        if self.patterns[pattern_key] > 3:
            self.insights.append(f"Pattern: {pattern_key} occurred {self.patterns[pattern_key]} times")
    
    def generate_learning_plan(self, target_skill: str = None) -> Dict[str, Any]:
        """Generate personalized learning plan"""
        if target_skill:
            current_level = self.skill_tree.get(target_skill, {}).get("level", 0)
            target_level = min(current_level + 1.0, 10.0)
        else:
            # Find weakest skill
            if self.skill_tree:
                weakest = min(self.skill_tree.items(), key=lambda x: x[1]["level"])
                target_skill = weakest[0]
                current_level = weakest[1]["level"]
                target_level = current_level + 1.0
            else:
                target_skill = "general"
                current_level = 0
                target_level = 1.0
        
        # Generate training phases
        phases = []
        difficulty_levels = ["beginner", "intermediate", "advanced"]
        
        for i in range(3):
            phase_level = difficulty_levels[min(i, len(difficulty_levels) - 1)]
            phases.append({
                "phase": i + 1,
                "focus": f"{phase_level} {target_skill}",
                "exercises": [
                    f"Practice {target_skill} with simple tasks",
                    f"Apply {target_skill} to related problems",
                    f"Challenge {target_skill} with complex scenarios"
                ],
                "success_criteria": f"Complete 3 {phase_level} exercises"
            })
        
        return {
            "target_skill": target_skill,
            "current_level": current_level,
            "target_level": target_level,
            "phases": phases,
            "estimated_time": 30 * len(phases),  # 30 minutes per phase
            "learning_points_needed": target_level - current_level
        }
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        total_experiences = len(self.learning_history)
        
        # Calculate overall progress
        if self.skill_tree:
            avg_skill_level = sum(skill["level"] for skill in self.skill_tree.values()) / len(self.skill_tree)
            total_skills = len(self.skill_tree)
        else:
            avg_skill_level = 0
            total_skills = 0
        
        return {
            "total_learning_points": self.total_learning_points,
            "total_experiences": total_experiences,
            "total_skills": total_skills,
            "average_skill_level": avg_skill_level,
            "total_insights": len(self.insights),
            "patterns_recognized": len(self.patterns),
            "learning_rate": self.learning_rate,
            "skill_tree": {k: round(v["level"], 2) for k, v in self.skill_tree.items()}
        }
    
    def export_learning_data(self, filename: str = "learning_export.json"):
        """Export learning data"""
        export_data = {
            "learning_history": self.learning_history[-100:],  # Last 100 entries
            "skill_tree": self.skill_tree,
            "insights": self.insights[-50:],  # Last 50 insights
            "stats": self.get_learning_stats(),
            "export_timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Learning data exported to {filename}")
        return export_data

# Quick test
if __name__ == "__main__":
    le = LearningEngine()
    
    # Simulate learning from experiences
    experiences = [
        {"id": "exp1", "task": "Learn to solve math problems", "result": {"success": True, "duration": 2.5}},
        {"id": "exp2", "task": "Analyze complex data", "result": {"success": False, "error": "Data format issue"}},
        {"id": "exp3", "task": "Create a simple program", "result": {"success": True, "duration": 1.8}}
    ]
    
    for exp in experiences:
        learning = le.learn_from_experience(exp)
        print(f"Learned from {exp['id']}: {len(learning['insights'])} insights")
    
    stats = le.get_learning_stats()
    print(f"\nLearning stats: {stats}")
    
    plan = le.generate_learning_plan()
    print(f"\nLearning plan: {plan['target_skill']} from {plan['current_level']} to {plan['target_level']}")
