"""
Config Loader for Rawlsing v4.1

Loads and provides access to YAML configuration files that drive the simulation.
Supports path-based lookups, condition evaluation, and formula computation.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from functools import lru_cache


class ConfigLoader:
    """
    Loads and caches YAML configuration files.
    Provides typed access to config data with path-based lookups.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize config loader.
        
        Args:
            config_dir: Path to config directory. Defaults to v2/config/
        """
        if config_dir is None:
            # Default to v2/config/ relative to this file
            base_dir = Path(__file__).parent
            config_dir = base_dir / "config"
        self.config_dir = Path(config_dir)
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._load_all()
    
    def _load_all(self):
        """Load all YAML config files."""
        config_files = {
            "main": "config.yaml",
            "needs": "needs.yaml",
            "strategies": "strategies.yaml",
            "civic_soul": "civic_soul.yaml",
            "relational_roles": "relational_roles.yaml",
            "indices": "indices.yaml",
            "events": "events.yaml",
            "type_driver_sensitivity": "type_driver_sensitivity.yaml",
            "health_levels_riso": "health_levels_riso.yaml",
        }
        
        for key, filename in config_files.items():
            filepath = self.config_dir / filename
            if filepath.exists():
                with open(filepath, 'r') as f:
                    self._configs[key] = yaml.safe_load(f)
            else:
                self._configs[key] = {}
    
    def get(self, config_name: str, path: Optional[str] = None, default: Any = None) -> Any:
        """
        Get config value by name and optional path.
        
        Args:
            config_name: Name of config file (e.g., "needs", "strategies")
            path: Dot-separated path (e.g., "safety.update_formula.base_weight")
            default: Default value if not found
        
        Returns:
            Config value or default
        """
        if config_name not in self._configs:
            return default
        
        config = self._configs[config_name]
        
        if path is None:
            return config
        
        # Navigate path
        parts = path.split('.')
        value = config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def get_needs_config(self, need_name: str) -> Dict[str, Any]:
        """Get configuration for a specific need."""
        return self.get("needs", f"needs.{need_name}", {})
    
    def get_strategy_config(self, strategy_name: str) -> Dict[str, Any]:
        """Get configuration for a specific strategy."""
        return self.get("strategies", f"strategies.{strategy_name}", {})
    
    def get_civic_soul_config(self, condition_name: str) -> Dict[str, Any]:
        """Get configuration for a civic soul condition."""
        return self.get("civic_soul", f"civic_soul.{condition_name}", {})
    
    def get_relational_role_config(self, role_category: str) -> Dict[str, Any]:
        """Get configuration for relational roles."""
        return self.get("relational_roles", f"relational_roles.{role_category}", {})
    
    def evaluate_path(self, path: str, context: Dict[str, Any]) -> Any:
        """
        Evaluate a path expression against a context.
        
        Supports paths like:
        - "world_slice.conflict_intensity"
        - "needs.safety"
        - "identity.gender"
        - "relations.caregiver_warmth"
        
        Args:
            path: Dot-separated path
            context: Dictionary with context objects (world_slice, needs, identity, etc.)
        
        Returns:
            Value from context or None
        """
        parts = path.split('.')
        if len(parts) == 0:
            return None
        
        # Get root object
        root_name = parts[0]
        if root_name not in context:
            return None
        
        obj = context[root_name]
        
        # Navigate through attributes
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None
        
        return obj
    
    def evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a condition string against context.
        
        Supports conditions like:
        - "needs.safety < 40"
        - "identity.gender == 'male'"
        - "world_slice.conflict_intensity > 60"
        - "needs.safety < 40 AND world_slice.conflict_intensity > 50"
        - "needs.safety < 40 OR needs.belonging_group < 30"
        
        Args:
            condition: Condition string
            context: Dictionary with context objects
        
        Returns:
            True if condition is met, False otherwise
        """
        # Support AND/OR operators
        condition = condition.strip()
        
        # "x includes y" - for lists (e.g. relations.norm_conflicts includes 'religious')
        if ' includes ' in condition:
            left, right = condition.split(' includes ', 1)
            left = left.strip()
            right = right.strip()
            left_value = self.evaluate_path(left, context)
            if left_value is None or not isinstance(left_value, (list, tuple)):
                return False
            right_value = right.strip('"\'')
            try:
                right_value = float(right_value)
            except ValueError:
                pass
            return right_value in left_value
        
        # Handle AND (higher precedence)
        if ' AND ' in condition:
            parts = condition.split(' AND ')
            return all(self.evaluate_condition(part.strip(), context) for part in parts)
        
        # Handle OR
        if ' OR ' in condition:
            parts = condition.split(' OR ')
            return any(self.evaluate_condition(part.strip(), context) for part in parts)
        
        # Simple condition parser
        # Support basic comparisons: <, >, <=, >=, ==, !=
        operators = ['<=', '>=', '==', '!=', '<', '>']
        
        for op in operators:
            if op in condition:
                left, right = condition.split(op, 1)
                left = left.strip()
                right = right.strip()
                
                # Evaluate left side (path)
                left_value = self.evaluate_path(left, context)
                if left_value is None:
                    return False
                
                # Evaluate right side (could be path, literal, or number)
                try:
                    # Try as number first
                    right_value = float(right)
                except ValueError:
                    # Try as string (remove quotes)
                    if right.startswith('"') and right.endswith('"'):
                        right_value = right[1:-1]
                    elif right.startswith("'") and right.endswith("'"):
                        right_value = right[1:-1]
                    else:
                        # Try as path
                        right_value = self.evaluate_path(right, context)
                        if right_value is None:
                            return False
                
                # Compare
                if op == '<':
                    return left_value < right_value
                elif op == '>':
                    return left_value > right_value
                elif op == '<=':
                    return left_value <= right_value
                elif op == '>=':
                    return left_value >= right_value
                elif op == '==':
                    return left_value == right_value
                elif op == '!=':
                    return left_value != right_value
        
        # If no operator found, check if it's a boolean path
        value = self.evaluate_path(condition, context)
        if value is not None:
            return bool(value)
        
        return False
    
    def compute_formula(
        self,
        formula_config: Dict[str, Any],
        context: Dict[str, Any],
        inputs_config: Optional[List[Dict[str, Any]]] = None
    ) -> float:
        """
        Compute a formula from config.
        
        Args:
            formula_config: Formula configuration (base, contributions, etc.)
            context: Context for evaluating inputs
            inputs_config: List of input configurations
        
        Returns:
            Computed value (clamped to 0-100)
        """
        base = formula_config.get("base", 50.0)
        result = base
        
        if inputs_config:
            for input_config in inputs_config:
                source = input_config.get("source", "")
                weight = input_config.get("weight", 1.0)
                mapping = input_config.get("mapping", "direct")
                
                # Get value from context
                value = self.evaluate_path(source, context)
                if value is None:
                    continue
                
                # Apply mapping
                if mapping == "direct":
                    contribution = value * weight
                elif mapping == "inverse":
                    contribution = (100 - value) * weight
                elif isinstance(mapping, dict):
                    # Categorical mapping
                    if value in mapping:
                        contribution = mapping[value] * weight
                    else:
                        contribution = 0
                elif mapping == "inverse_decile":
                    # For class_position: lower decile → lower value
                    contribution = (10 - value) * weight
                elif mapping == "direct_decile":
                    # For class_position: higher decile → higher value
                    contribution = value * weight
                else:
                    contribution = value * weight
                
                result += contribution
        
        # Clamp to 0-100
        return max(0.0, min(100.0, result))
    
    def get_all_needs(self) -> List[str]:
        """Get list of all need names."""
        needs = self.get("needs", "needs", {})
        return list(needs.keys())
    
    def get_all_strategies(self) -> List[str]:
        """Get list of all strategy names."""
        strategies = self.get("strategies", "strategies", {})
        return list(strategies.keys())
    
    def get_strategy_update_rules(self, strategy_name: str) -> Dict[str, List[str]]:
        """Get update rules for a strategy (increase_when, decrease_when)."""
        config = self.get_strategy_config(strategy_name)
        return config.get("update_rules", {})
    
    def get_need_update_formula(self, need_name: str) -> Dict[str, Any]:
        """Get update formula for a need."""
        config = self.get_needs_config(need_name)
        return config.get("update_formula", {})
    
    def get_need_main_inputs(self, need_name: str) -> List[str]:
        """Get main inputs for a need."""
        config = self.get_needs_config(need_name)
        return config.get("main_inputs", [])
    
    def get_strategy_structural_availability(self, strategy_name: str) -> Dict[str, Any]:
        """Get structural availability requirements for a strategy."""
        config = self.get_strategy_config(strategy_name)
        return config.get("structural_availability", {})
    
    def reload(self):
        """Reload all config files (useful for development)."""
        self._configs.clear()
        self._load_all()


# Global singleton instance
_loader: Optional[ConfigLoader] = None


def get_config_loader(config_dir: Optional[str] = None) -> ConfigLoader:
    """
    Get the global config loader instance.
    
    Args:
        config_dir: Optional config directory path
    
    Returns:
        ConfigLoader instance
    """
    global _loader
    if _loader is None:
        _loader = ConfigLoader(config_dir)
    return _loader


def reload_configs():
    """Reload all config files."""
    global _loader
    if _loader is not None:
        _loader.reload()

