import os
import statsig
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FeatureFlags:
    """
    Feature flag service using Statsig for A/B testing and gradual rollouts
    """
    
    def __init__(self):
        self.statsig_sdk_key = os.getenv("STATSIG_SDK_KEY")
        self.initialized = False
        
        if self.statsig_sdk_key and self.statsig_sdk_key != "YOUR_STATSIG_SDK_KEY":
            try:
                statsig.initialize(self.statsig_sdk_key)
                self.initialized = True
                logger.info("Statsig initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Statsig: {e}")
        else:
            logger.warning("STATSIG_SDK_KEY not set, using default values")
    
    def get_user_id(self, user_id: Optional[str] = None) -> str:
        """Generate or use provided user ID"""
        return user_id or "anonymous_user"
    
    def should_show_advanced_quantum_features(self, user_id: Optional[str] = None) -> bool:
        """Feature flag for advanced quantum chemistry features"""
        if not self.initialized:
            return False  # Default to off if Statsig not available
        
        try:
            return statsig.get_config("advanced_quantum_features", self.get_user_id(user_id))
        except Exception as e:
            logger.warning(f"Statsig error: {e}")
            return False
    
    def should_show_molecular_analogs_v2(self, user_id: Optional[str] = None) -> bool:
        """Feature flag for enhanced molecular analogs"""
        if not self.initialized:
            return True  # Default to on for enhanced analogs
        
        try:
            return statsig.get_config("molecular_analogs_v2", self.get_user_id(user_id))
        except Exception as e:
            logger.warning(f"Statsig error: {e}")
            return True
    
    def should_use_enhanced_ml_predictions(self, user_id: Optional[str] = None) -> bool:
        """Feature flag for enhanced ML predictions"""
        if not self.initialized:
            return False  # Default to off
        
        try:
            return statsig.get_config("enhanced_ml_predictions", self.get_user_id(user_id))
        except Exception as e:
            logger.warning(f"Statsig error: {e}")
            return False
    
    def should_enable_voice_generation(self, user_id: Optional[str] = None) -> bool:
        """Feature flag for voice generation features"""
        if not self.initialized:
            return True  # Default to on
        
        try:
            return statsig.get_config("voice_generation", self.get_user_id(user_id))
        except Exception as e:
            logger.warning(f"Statsig error: {e}")
            return True
    
    def get_analysis_algorithm(self, user_id: Optional[str] = None) -> str:
        """Get which analysis algorithm to use"""
        if not self.initialized:
            return "standard"  # Default algorithm
        
        try:
            config = statsig.get_config("analysis_algorithm", self.get_user_id(user_id))
            return config.get("algorithm", "standard")
        except Exception as e:
            logger.warning(f"Statsig error: {e}")
            return "standard"
    
    def log_analysis_event(self, user_id: str, event_name: str, properties: Dict[str, Any]):
        """Log custom events to Statsig"""
        if not self.initialized:
            return
        
        try:
            statsig.log_event(
                user_id=user_id,
                event_name=event_name,
                properties=properties
            )
        except Exception as e:
            logger.warning(f"Statsig logging error: {e}")
    
    def get_experiment_variant(self, experiment_name: str, user_id: Optional[str] = None) -> str:
        """Get experiment variant for A/B testing"""
        if not self.initialized:
            return "control"  # Default to control group
        
        try:
            return statsig.get_config(experiment_name, self.get_user_id(user_id))
        except Exception as e:
            logger.warning(f"Statsig experiment error: {e}")
            return "control"
