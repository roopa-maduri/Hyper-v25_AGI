"""
virtual_world.py - Virtual Environment Generator
Founder's Data Solution: Infinite synthetic training
"""

import random
import time
import json
from typing import Dict, List, Any

class VirtualWorld:
    def __init__(self):
        self.world_counter = 0
        self.world_history = []
        self.object_templates = self._load_object_templates()
        self.scene_templates = self._load_scene_templates()
        
    def generate_world(self, task_description: str, complexity: str = "medium") -> Dict[str, Any]:
        """Generate a virtual world for any task"""
        self.world_counter += 1
        world_id = f"WORLD{self.world_counter:06d}"
        
        print(f"🌍 Generating Virtual World: {world_id}")
        print(f"   Task: {task_description[:80]}...")
        print(f"   Complexity: {complexity}")
        
        # Generate world based on task
        world = {
            "id": world_id,
            "task": task_description,
            "complexity": complexity,
            "objects": self._generate_objects(task_description, complexity),
            "environment": self._generate_environment(task_description),
            "rules": self._generate_rules(complexity),
            "goals": self._generate_goals(task_description),
            "state": "initialized",
            "timestamp": time.time(),
            "metadata": {
                "version": "1.0",
                "generator": "HyperAGI_Virtual_Engine",
                "physics_level": self._get_physics_level(complexity)
            }
        }
        
        self.world_history.append(world)
        return world
    
    def _generate_objects(self, task: str, complexity: str) -> List[Dict[str, Any]]:
        """Generate virtual objects"""
        objects = []
        obj_count = self._get_object_count(complexity)
        
        # Extract keywords from task
        keywords = self._extract_keywords(task)
        
        for i in range(obj_count):
            # Choose object type based on task or random
            if keywords and random.random() > 0.5:
                obj_type = random.choice(keywords)
            else:
                obj_type = random.choice(list(self.object_templates.keys()))
            
            # Get template and customize
            template = self.object_templates.get(obj_type, self.object_templates["generic"])
            obj = self._customize_object(template.copy(), i, complexity)
            
            objects.append(obj)
        
        return objects
    
    def _generate_environment(self, task: str) -> Dict[str, Any]:
        """Generate environment settings"""
        env_type = self._determine_environment_type(task)
        
        environments = {
            "indoor": {
                "type": "indoor",
                "lighting": "artificial",
                "size": "room_scale",
                "weather": "none",
                "acoustics": "reverberant"
            },
            "outdoor": {
                "type": "outdoor",
                "lighting": "natural",
                "size": "open_world",
                "weather": random.choice(["clear", "partly_cloudy", "light_rain"]),
                "acoustics": "open"
            },
            "abstract": {
                "type": "abstract",
                "lighting": "conceptual",
                "size": "infinite",
                "weather": "none",
                "acoustics": "perfect"
            },
            "technical": {
                "type": "technical",
                "lighting": "studio",
                "size": "laboratory",
                "weather": "controlled",
                "acoustics": "anechoic"
            }
        }
        
        return environments.get(env_type, environments["abstract"])
    
    def _generate_rules(self, complexity: str) -> Dict[str, Any]:
        """Generate physics and interaction rules"""
        rule_sets = {
            "simple": {
                "gravity": 9.8,
                "friction": 0.3,
                "elasticity": 0.5,
                "collision": "simple",
                "time_flow": 1.0,
                "interaction_limit": 10
            },
            "medium": {
                "gravity": 9.8,
                "friction": random.uniform(0.2, 0.8),
                "elasticity": random.uniform(0.3, 0.9),
                "collision": "advanced",
                "time_flow": random.uniform(0.8, 1.2),
                "interaction_limit": 25
            },
            "complex": {
                "gravity": random.uniform(1.6, 9.8),  # Moon to Earth gravity
                "friction": random.uniform(0.1, 0.9),
                "elasticity": random.uniform(0.1, 0.95),
                "collision": "realistic",
                "time_flow": random.uniform(0.5, 2.0),
                "interaction_limit": 100
            }
        }
        
        return rule_sets.get(complexity, rule_sets["medium"])
    
    def _generate_goals(self, task: str) -> List[Dict[str, Any]]:
        """Generate goals for the virtual world"""
        goals = []
        
        # Primary goal from task
        goals.append({
            "id": "primary",
            "description": f"Complete task: {task[:100]}",
            "type": "achievement",
            "priority": "high",
            "success_criteria": "Task completed successfully"
        })
        
        # Secondary learning goals
        secondary_goals = [
            {"id": "learn_patterns", "description": "Recognize patterns in environment", "type": "learning"},
            {"id": "optimize_actions", "description": "Optimize action sequences", "type": "efficiency"},
            {"id": "adapt_behavior", "description": "Adapt to environment changes", "type": "adaptation"}
        ]
        
        goals.extend(random.sample(secondary_goals, random.randint(1, 2)))
        
        return goals
    
    def _load_object_templates(self) -> Dict[str, Dict]:
        """Load object templates"""
        return {
            "generic": {
                "type": "object",
                "interactable": True,
                "properties": {"mass": 1.0, "size": "medium"},
                "states": ["idle", "active", "interacted"]
            },
            "tool": {
                "type": "tool",
                "interactable": True,
                "properties": {"function": "assist", "durability": 100},
                "states": ["available", "in_use", "depleted"]
            },
            "interface": {
                "type": "interface",
                "interactable": True,
                "properties": {"input_methods": ["touch", "voice"], "responsiveness": "high"},
                "states": ["ready", "active", "processing"]
            },
            "data_node": {
                "type": "data",
                "interactable": True,
                "properties": {"data_capacity": 1000, "transfer_rate": "fast"},
                "states": ["empty", "storing", "transmitting"]
            },
            "obstacle": {
                "type": "obstacle",
                "interactable": False,
                "properties": {"blocking": True, "damage": 0},
                "states": ["static", "damaged"]
            }
        }
    
    def _load_scene_templates(self) -> Dict[str, List]:
        """Load scene templates"""
        return {
            "learning": ["classroom", "library", "laboratory", "workshop"],
            "problem_solving": ["puzzle_room", "maze", "challenge_course", "test_chamber"],
            "creation": ["studio", "workshop", "fab_lab", "construction_site"],
            "exploration": ["wilderness", "ruins", "city", "space_station"]
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        words = [w.lower() for w in text.split() if w.lower() not in stop_words and len(w) > 2]
        return list(set(words))[:5]
    
    def _determine_environment_type(self, task: str) -> str:
        """Determine environment type from task"""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["room", "inside", "interior", "house"]):
            return "indoor"
        elif any(word in task_lower for word in ["outside", "outdoor", "nature", "landscape"]):
            return "outdoor"
        elif any(word in task_lower for word in ["technical", "lab", "computer", "machine"]):
            return "technical"
        else:
            return "abstract"
    
    def _get_object_count(self, complexity: str) -> int:
        """Get number of objects based on complexity"""
        return {"simple": 3, "medium": 8, "complex": 15}.get(complexity, 8)
    
    def _get_physics_level(self, complexity: str) -> str:
        """Get physics simulation level"""
        return {"simple": "basic", "medium": "realistic", "complex": "advanced"}.get(complexity, "realistic")
    
    def _customize_object(self, template: Dict, index: int, complexity: str) -> Dict[str, Any]:
        """Customize object template"""
        obj_id = f"obj_{index:03d}"
        
        # Add ID and position
        template["id"] = obj_id
        template["position"] = {
            "x": random.uniform(-10, 10),
            "y": random.uniform(0, 5),
            "z": random.uniform(-10, 10)
        }
        
        # Customize based on complexity
        if complexity == "complex":
            template["properties"]["quality"] = random.choice(["low", "medium", "high"])
            template["states"].append("customized")
        
        return template
    
    def execute_in_world(self, world_id: str, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute actions in virtual world"""
        # Find world
        world = next((w for w in self.world_history if w["id"] == world_id), None)
        if not world:
            return {"error": f"World {world_id} not found"}
        
        print(f"🎮 Executing {len(actions)} actions in {world_id}")
        
        results = []
        world_state = "active"
        
        for i, action in enumerate(actions):
            action_result = self._execute_action(world, action, i)
            results.append(action_result)
            
            # Update world state if action changes it
            if action_result.get("world_state_change"):
                world_state = action_result["world_state_change"]
        
        # Update world
        world["state"] = world_state
        world["last_activity"] = time.time()
        
        return {
            "world_id": world_id,
            "actions_executed": len(actions),
            "results": results,
            "final_state": world_state,
            "successful_actions": sum(1 for r in results if r.get("success", False)),
            "timestamp": time.time()
        }
    
    def _execute_action(self, world: Dict, action: Dict, index: int) -> Dict[str, Any]:
        """Execute single action"""
        action_type = action.get("type", "unknown")
        
        # Simulate action execution
        success = random.random() > 0.2  # 80% success rate
        
        result = {
            "action_id": index,
            "type": action_type,
            "description": action.get("description", f"Action {index}"),
            "success": success,
            "timestamp": time.time()
        }
        
        if success:
            result["outcome"] = f"Successfully executed {action_type}"
            result["changes"] = ["World state updated", "Objects modified"]
            
            # Special outcomes for certain actions
            if action_type == "learn":
                result["knowledge_gained"] = random.randint(1, 5)
            elif action_type == "create":
                result["object_created"] = f"new_object_{random.randint(100, 999)}"
        else:
            result["outcome"] = f"Failed to execute {action_type}"
            result["reason"] = random.choice([
                "Object not interactable",
                "Insufficient resources",
                "Physics constraint",
                "Timing issue"
            ])
        
        return result
    
    def get_world_stats(self) -> Dict[str, Any]:
        """Get virtual world statistics"""
        return {
            "worlds_generated": self.world_counter,
            "worlds_active": sum(1 for w in self.world_history if w.get("state") == "active"),
            "total_objects": sum(len(w.get("objects", [])) for w in self.world_history),
            "environment_types": list(set(w.get("environment", {}).get("type", "unknown") for w in self.world_history)),
            "last_world": self.world_history[-1]["id"] if self.world_history else None
        }

# Quick test
if __name__ == "__main__":
    vw = VirtualWorld()
    
    # Generate a virtual world
    world = vw.generate_world("Learn to solve physics problems by experimenting with objects", "medium")
    print(f"\nGenerated world: {world['id']}")
    print(f"Objects: {len(world['objects'])}")
    print(f"Environment: {world['environment']['type']}")
    
    # Execute some actions
    actions = [
        {"type": "explore", "description": "Explore the virtual environment"},
        {"type": "interact", "description": "Interact with objects"},
        {"type": "learn", "description": "Learn from interactions"}
    ]
    
    result = vw.execute_in_world(world["id"], actions)
    print(f"\nExecution result: {result['successful_actions']}/{result['actions_executed']} successful")
    
    stats = vw.get_world_stats()
    print(f"\nVirtual World Stats: {stats}")
