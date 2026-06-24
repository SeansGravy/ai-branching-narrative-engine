import json
import os

# Simple Branching Narrative Engine - MVP Prototype
# Tracks state, choices, and can be extended with AI generation for dynamic branches

class NarrativeEngine:
    def __init__(self, save_file="story_state.json"):
        self.save_file = save_file
        self.state = self.load_state()
        self.current_scene = self.state.get("current_scene", "start")
    
    def load_state(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_state(self):
        with open(self.save_file, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def present_scene(self, scenes):
        """Display current scene and choices"""
        scene_data = scenes.get(self.current_scene, {})
        print("\n" + "="*60)
        print(scene_data.get("description", "Scene missing..."))
        print("\nChoices:")
        for i, choice in enumerate(scene_data.get("choices", []), 1):
            print(f"{i}. {choice['text']}")
        print("="*60)
    
    def make_choice(self, choice_index, scenes):
        """Process choice and update state"""
        scene_data = scenes.get(self.current_scene, {})
        choices = scene_data.get("choices", [])
        if 1 <= choice_index <= len(choices):
            selected = choices[choice_index - 1]
            # Update state with consequences
            for key, value in selected.get("effects", {}).items():
                self.state[key] = value
            # Move to next scene
            self.current_scene = selected.get("next_scene", "end")
            self.state["current_scene"] = self.current_scene
            self.save_state()
            print(f"\nYou chose: {selected['text']}")
            return True
        return False

# Example story definition (expandable / AI-generatable)
def get_example_story():
    return {
        "start": {
            "description": "You stand at the threshold of an unknown path. A mysterious device in your hand pulses with possibilities. The air hums with potential.",
            "choices": [
                {"text": "Activate the device and step forward", "next_scene": "device_path", "effects": {"curiosity": 1}},
                {"text": "Observe carefully first", "next_scene": "observe_path", "effects": {"caution": 1}},
                {"text": "Turn back and seek familiar ground", "next_scene": "end_safe", "effects": {"safety": 1}}
            ]
        },
        "device_path": {
            "description": "The device awakens, revealing branching realities. Visions of alternate paths flood your mind.",
            "choices": [
                {"text": "Dive deeper into the visions", "next_scene": "deep_dive", "effects": {"knowledge": 2}},
                {"text": "Use it to contact an ally", "next_scene": "ally_contact", "effects": {"connection": 1}}
            ]
        },
        "observe_path": {
            "description": "Careful observation reveals hidden patterns in the landscape. A safer but slower route emerges.",
            "choices": [
                {"text": "Follow the patterns", "next_scene": "patterns_follow", "effects": {"wisdom": 1}}
            ]
        },
        # Add more scenes as needed
        "end_safe": {
            "description": "You return to safety, but wonder what you might have discovered. The adventure ends... for now.",
            "choices": []
        }
        # Extend with more dynamic/AI-filled scenes
    }

if __name__ == "__main__":
    engine = NarrativeEngine()
    story = get_example_story()
    
    print("=== AI Branching Narrative Engine Prototype ===")
    print("Type 'quit' to exit. State is saved automatically.")
    
    while engine.current_scene != "end" and engine.current_scene not in ["end_safe"]:  # Expand end conditions
        engine.present_scene(story)
        try:
            user_input = input("\nYour choice (number): ").strip()
            if user_input.lower() == "quit":
                break
            choice_num = int(user_input)
            if not engine.make_choice(choice_num, story):
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
    
    print("\nStory session ended. Final state:", engine.state)