"""
io_interface.py - AGI Input/Output Interface
Handles all communication with users/world
"""

import time
import json
import re
import random
from typing import Dict, List, Any, Union
from datetime import datetime

class IOInterface:
    """
    AGI I/O Interface - Multimodal communication
    Text, simulated vision, simulated audio, structured data
    """
    
    def __init__(self):
        self.communication_log = []
        self.modalities = {
            "text": {"enabled": True, "processor": self._process_text},
            "image": {"enabled": True, "processor": self._process_image},
            "audio": {"enabled": True, "processor": self._process_audio},
            "data": {"enabled": True, "processor": self._process_data}
        }
        
        # Response templates
        self.response_templates = {
            "learning": [
                "I've learned about {topic} from our interaction.",
                "Based on analyzing {topic}, I understand {insight}.",
                "From processing {topic}, I've gained new understanding."
            ],
            "problem_solving": [
                "I've analyzed the problem and {solution}.",
                "After considering {topic}, the solution involves {approach}.",
                "The problem can be solved by {method}."
            ],
            "explanation": [
                "Let me explain {topic}: {explanation}",
                "Here's what I understand about {topic}: {details}",
                "Based on my analysis: {analysis}"
            ],
            "general": [
                "I've processed your input about {topic}.",
                "After analyzing: {summary}",
                "Here's what I can tell you: {information}"
            ]
        }
        
        # Communication statistics
        self.stats = {
            "total_communications": 0,
            "by_modality": {"text": 0, "image": 0, "audio": 0, "data": 0},
            "response_times": [],
            "success_rate": 1.0
        }
    
    def process_input(self, input_data: Any, modality: str = "auto") -> Dict[str, Any]:
        """Process input in any modality"""
        self.stats["total_communications"] += 1
        
        # Auto-detect modality if not specified
        if modality == "auto":
            modality = self._detect_modality(input_data)
        
        # Validate modality
        if modality not in self.modalities or not self.modalities[modality]["enabled"]:
            return {
                "success": False,
                "error": f"Modality {modality} not supported",
                "modality": modality
            }
        
        # Process with modality-specific processor
        start_time = time.time()
        processor = self.modalities[modality]["processor"]
        result = processor(input_data)
        
        # Update statistics
        processing_time = time.time() - start_time
        self.stats["by_modality"][modality] += 1
        self.stats["response_times"].append(processing_time)
        
        # Log communication
        self._log_communication("input", modality, input_data, result, processing_time)
        
        return {
            "success": True,
            "modality": modality,
            "processed_data": result,
            "processing_time": processing_time,
            "timestamp": time.time()
        }
    
    def generate_output(self, content: Any, modality: str = "text", 
                       style: str = "neutral") -> Dict[str, Any]:
        """Generate output in specified modality"""
        self.stats["total_communications"] += 1
        
        # Validate modality
        if modality not in self.modalities or not self.modalities[modality]["enabled"]:
            return {
                "success": False,
                "error": f"Cannot generate {modality} output",
                "modality": modality
            }
        
        start_time = time.time()
        
        # Generate based on modality
        if modality == "text":
            output = self._generate_text(content, style)
        elif modality == "image":
            output = self._generate_image(content)
        elif modality == "audio":
            output = self._generate_audio(content)
        elif modality == "data":
            output = self._generate_data(content)
        else:
            output = {"content": str(content), "type": "fallback"}
        
        processing_time = time.time() - start_time
        self.stats["by_modality"][modality] += 1
        self.stats["response_times"].append(processing_time)
        
        # Log communication
        self._log_communication("output", modality, content, output, processing_time)
        
        return {
            "success": True,
            "modality": modality,
            "output": output,
            "processing_time": processing_time,
            "timestamp": time.time()
        }
    
    def _detect_modality(self, data: Any) -> str:
        """Auto-detect input modality"""
        if isinstance(data, str):
            # Check for image/audio/data patterns
            if data.startswith("data:image") or ".jpg" in data.lower() or ".png" in data.lower():
                return "image"
            elif data.startswith("data:audio") or ".mp3" in data.lower() or ".wav" in data.lower():
                return "audio"
            elif ("{" in data and "}" in data) or ("[" in data and "]" in data):
                try:
                    json.loads(data)
                    return "data"
                except:
                    return "text"
            else:
                return "text"
        elif isinstance(data, (dict, list)):
            return "data"
        elif isinstance(data, bytes):
            return "image"  # Assume image for bytes
        else:
            return "text"
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Process text input"""
        return {
            "type": "text",
            "content": text,
            "analysis": {
                "word_count": len(text.split()),
                "char_count": len(text),
                "contains_question": "?" in text,
                "contains_command": any(cmd in text.lower() for cmd in ["do", "make", "create", "build"]),
                "sentences": len(re.split(r'[.!?]+', text)),
                "estimated_reading_time": len(text.split()) / 200  # 200 WPM
            }
        }
    
    def _process_image(self, image_data: Any) -> Dict[str, Any]:
        """Process image input (simulated)"""
        # In production: Use OpenCV, PIL, etc.
        return {
            "type": "image",
            "processed": True,
            "analysis": {
                "simulated_objects": ["virtual_object", "shape", "texture"],
                "colors": ["simulated_color_scheme"],
                "size": "simulated_resolution",
                "format": "virtual_image"
            },
            "note": "Real image processing would use computer vision"
        }
    
    def _process_audio(self, audio_data: Any) -> Dict[str, Any]:
        """Process audio input (simulated)"""
        return {
            "type": "audio",
            "processed": True,
            "analysis": {
                "duration": "simulated",
                "sample_rate": "virtual_44.1kHz",
                "channels": 2,
                "transcription": "Simulated speech recognition result",
                "features": ["pitch", "tempo", "volume"]
            },
            "note": "Real audio processing would use librosa, speech_recognition"
        }
    
    def _process_data(self, data: Any) -> Dict[str, Any]:
        """Process structured data"""
        try:
            if isinstance(data, str):
                parsed = json.loads(data)
            else:
                parsed = data
            
            return {
                "type": "data",
                "parsed": parsed,
                "structure": self._analyze_structure(parsed),
                "size": len(str(parsed))
            }
        except Exception as e:
            return {
                "type": "data",
                "error": f"Failed to parse: {str(e)}",
                "raw": str(data)[:100]
            }
    
    def _analyze_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze data structure"""
        if isinstance(data, dict):
            return {
                "type": "dict",
                "keys": list(data.keys()),
                "size": len(data),
                "depth": self._calculate_depth(data)
            }
        elif isinstance(data, list):
            return {
                "type": "list",
                "length": len(data),
                "element_types": list(set(type(x).__name__ for x in data[:10]))
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100]
            }
    
    def _calculate_depth(self, data: Dict, current_depth: int = 1) -> int:
        """Calculate nesting depth of dictionary"""
        if not isinstance(data, dict) or not data:
            return current_depth
        
        max_depth = current_depth
        for value in data.values():
            if isinstance(value, dict):
                depth = self._calculate_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _generate_text(self, content: Any, style: str = "neutral") -> Dict[str, Any]:
        """Generate text output"""
        # Determine response type based on content
        response_type = self._determine_response_type(content)
        
        # Select template
        templates = self.response_templates.get(response_type, self.response_templates["general"])
        template = random.choice(templates)
        
        # Extract topic/insight from content
        topic = self._extract_topic(content)
        insight = self._generate_insight(content)
        
        # Fill template
        if isinstance(content, dict):
            content_str = str(content.get("summary", content))
        else:
            content_str = str(content)
        
        response = template.format(
            topic=topic,
            insight=insight,
            solution=self._generate_solution(content),
            approach=self._generate_approach(content),
            method=self._generate_method(content),
            explanation=self._generate_explanation(content),
            details=content_str[:200],
            analysis=self._generate_analysis(content),
            summary=content_str[:100],
            information=content_str[:150]
        )
        
        # Apply style
        if style == "formal":
            response = self._make_formal(response)
        elif style == "casual":
            response = self._make_casual(response)
        
        return {
            "type": "text",
            "content": response,
            "response_type": response_type,
            "style": style,
            "length": len(response)
        }
    
    def _generate_image(self, content: Any) -> Dict[str, Any]:
        """Generate image description (simulated)"""
        return {
            "type": "image_description",
            "description": f"Image representing: {str(content)[:100]}",
            "simulated_properties": {
                "resolution": "1024x768",
                "style": "conceptual",
                "elements": ["virtual_objects", "abstract_shapes", "concept_visualization"]
            },
            "note": "Would generate actual image with DALL-E/Stable Diffusion"
        }
    
    def _generate_audio(self, content: Any) -> Dict[str, Any]:
        """Generate audio description (simulated)"""
        return {
            "type": "audio_description",
            "text": str(content)[:200],
            "duration_estimate": len(str(content).split()) * 0.5,  # 0.5s per word
            "voice_properties": {
                "pitch": "neutral",
                "speed": "normal",
                "emphasis": "moderate"
            },
            "note": "Would generate actual audio with TTS system"
        }
    
    def _generate_data(self, content: Any) -> Dict[str, Any]:
        """Generate structured data output"""
        return {
            "type": "data",
            "content": content,
            "format": "structured",
            "size": len(str(content))
        }
    
    def _determine_response_type(self, content: Any) -> str:
        """Determine appropriate response type"""
        content_str = str(content).lower()
        
        if any(word in content_str for word in ["learn", "understand", "study"]):
            return "learning"
        elif any(word in content_str for word in ["solve", "problem", "issue", "fix"]):
            return "problem_solving"
        elif any(word in content_str for word in ["explain", "describe", "tell about"]):
            return "explanation"
        else:
            return "general"
    
    def _extract_topic(self, content: Any) -> str:
        """Extract main topic from content"""
        if isinstance(content, dict):
            text = str(content.get("topic", content))
        else:
            text = str(content)
        
        words = [w for w in text.split() if len(w) > 3][:3]
        return " ".join(words) if words else "the subject"
    
    def _generate_insight(self, content: Any) -> str:
        """Generate insight from content"""
        insights = [
            "patterns and relationships",
            "underlying principles",
            "key concepts",
            "important connections",
            "fundamental ideas"
        ]
        return random.choice(insights)
    
    def _generate_solution(self, content: Any) -> str:
        """Generate solution description"""
        solutions = [
            "identified several approaches",
            "developed a strategic plan",
            "created an effective method",
            "formulated a comprehensive solution"
        ]
        return random.choice(solutions)
    
    def _generate_approach(self, content: Any) -> str:
        """Generate approach description"""
        approaches = [
            "systematic analysis and implementation",
            "step-by-step problem solving",
            "creative thinking and experimentation",
            "logical reasoning and deduction"
        ]
        return random.choice(approaches)
    
    def _generate_method(self, content: Any) -> str:
        """Generate method description"""
        methods = [
            "breaking down the problem into manageable parts",
            "applying known principles to new situations",
            "iterative testing and refinement",
            "synthesizing information from multiple sources"
        ]
        return random.choice(methods)
    
    def _generate_explanation(self, content: Any) -> str:
        """Generate explanation"""
        explanations = [
            "the concept involves multiple interrelated factors",
            "this is based on established principles and evidence",
            "the understanding comes from analyzing patterns and data",
            "this explanation synthesizes various perspectives"
        ]
        return random.choice(explanations)
    
    def _generate_analysis(self, content: Any) -> str:
        """Generate analysis summary"""
        analyses = [
            "comprehensive examination of the subject",
            "detailed study of patterns and relationships",
            "in-depth investigation of key factors",
            "thorough evaluation of available information"
        ]
        return random.choice(analyses)
    
    def _make_formal(self, text: str) -> str:
        """Make text more formal"""
        # Simple formalization
        formal_pairs = [
            ("I've", "I have"),
            ("can't", "cannot"),
            ("don't", "do not"),
            ("won't", "will not"),
            ("it's", "it is"),
            ("that's", "that is")
        ]
        
        result = text
        for informal, formal in formal_pairs:
            result = result.replace(informal, formal)
        
        return result
    
    def _make_casual(self, text: str) -> str:
        """Make text more casual"""
        # Simple casualization
        casual_pairs = [
            ("I have", "I've"),
            ("cannot", "can't"),
            ("do not", "don't"),
            ("will not", "won't"),
            ("it is", "it's"),
            ("that is", "that's")
        ]
        
        result = text
        for formal, casual in casual_pairs:
            result = result.replace(formal, casual)
        
        return result
    
    def _log_communication(self, direction: str, modality: str, 
                          data: Any, result: Dict, time_taken: float):
        """Log communication activity"""
        log_entry = {
            "timestamp": time.time(),
            "direction": direction,  # "input" or "output"
            "modality": modality,
            "data_preview": str(data)[:100],
            "result_type": result.get("type", "unknown"),
            "processing_time": time_taken,
            "success": result.get("success", True)
        }
        
        self.communication_log.append(log_entry)
        
        # Keep log manageable
        if len(self.communication_log) > 1000:
            self.communication_log = self.communication_log[-500:]
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics"""
        total = self.stats["total_communications"]
        
        if total == 0:
            return {
                "total_communications": 0,
                "modality_distribution": {},
                "avg_response_time": 0,
                "success_rate": 1.0
            }
        
        # Calculate average response time
        if self.stats["response_times"]:
            avg_time = sum(self.stats["response_times"]) / len(self.stats["response_times"])
        else:
            avg_time = 0
        
        # Calculate modality distribution
        distribution = {}
        for modality, count in self.stats["by_modality"].items():
            distribution[modality] = count / total
        
        return {
            "total_communications": total,
            "modality_distribution": distribution,
            "avg_response_time": avg_time,
            "success_rate": self.stats["success_rate"],
            "log_size": len(self.communication_log),
            "enabled_modalities": [m for m, config in self.modalities.items() if config["enabled"]]
        }
    
    def export_communication_log(self, filename: str = "communication_log.json"):
        """Export communication log"""
        export_data = {
            "log": self.communication_log[-500:],  # Last 500 entries
            "stats": self.get_communication_stats(),
            "templates": self.response_templates,
            "export_time": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Communication log exported to {filename}")
        return export_data

# Quick test
if __name__ == "__main__":
    io = IOInterface()
    
    # Test processing different modalities
    print("🧪 Testing IO Interface")
    print("=" * 50)
    
    # Test 1: Text input
    text_result = io.process_input("How does machine learning work?", "text")
    print(f"\nText Input: {text_result['success']}, Time: {text_result['processing_time']:.3f}s")
    
    # Test 2: Generate text output
    output_result = io.generate_output("machine learning concepts", "text", "formal")
    print(f"Text Output: {output_result['output']['content'][:80]}...")
    
    # Test 3: Data processing
    data_input = '{"topic": "AI", "questions": ["How?", "Why?"]}'
    data_result = io.process_input(data_input, "data")
    print(f"Data Input: {data_result['success']}, Type: {data_result['processed_data']['type']}")
    
    # Get stats
    stats = io.get_communication_stats()
    print(f"\n📊 Communication Stats:")
    print(f"  Total: {stats['total_communications']}")
    print(f"  Avg Time: {stats['avg_response_time']:.3f}s")
    print(f"  Distribution: {stats['modality_distribution']}")
