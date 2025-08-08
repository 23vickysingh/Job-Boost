import redis
import random
import string
import os
import json
from typing import Optional, Dict, Any
from datetime import timedelta

class OTPService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
    
    def _generate_key(self, identifier: str, purpose: str) -> str:
        """Generate Redis key for OTP storage."""
        return f"otp:{purpose}:{identifier}"
        
    def generate_otp(self, length: int = 6) -> str:
        """Generate a random numeric OTP."""
        return ''.join(random.choices(string.digits, k=length))
    
    def store_otp(self, identifier: str, otp_code: str, purpose: str, 
                  ttl_minutes: int = 5, additional_data: Optional[Dict] = None) -> bool:
        """
        Store OTP in Redis with automatic expiration and optional additional data.
        
        Args:
            identifier: User identifier (email)
            otp_code: The OTP code
            purpose: Purpose of OTP (registration, password_reset)
            ttl_minutes: TTL in minutes (default: 5)
            additional_data: Optional additional data to store with OTP
            
        Returns:
            bool: True if stored successfully, False otherwise
        """
        key = self._generate_key(identifier, purpose)
        
        try:
            # Store OTP and additional data as a hash
            data = {"otp": otp_code}
            if additional_data:
                data.update(additional_data)
            
            # Use pipeline for atomic operations
            pipe = self.redis_client.pipeline()
            pipe.hset(key, mapping=data)
            pipe.expire(key, timedelta(minutes=ttl_minutes))
            pipe.execute()
            
            return True
        except Exception as e:
            print(f"Error storing OTP in Redis: {e}")
            return False
    
    def verify_otp(self, identifier: str, otp_code: str, purpose: str) -> Optional[Dict]:
        """
        Verify OTP and delete it (one-time use). Returns stored additional data.
        
        Args:
            identifier: User identifier (email)
            otp_code: The OTP code to verify
            purpose: Purpose of OTP (registration, password_reset)
            
        Returns:
            Dict: Additional data stored with OTP or None if invalid
        """
        key = self._generate_key(identifier, purpose)
        
        try:
            stored_data = self.redis_client.hgetall(key)
            if not stored_data or stored_data.get("otp") != otp_code:
                return None
            
            # Extract additional data (excluding OTP)
            additional_data = {k: v for k, v in stored_data.items() if k != "otp"}
            
            # Delete OTP after verification (one-time use)
            self.redis_client.delete(key)
            
            return additional_data
        except Exception as e:
            print(f"Error verifying OTP: {e}")
            return None
    
    def is_otp_valid(self, identifier: str, otp_code: str, purpose: str) -> bool:
        """
        Check if OTP is valid without consuming it.
        
        Args:
            identifier: User identifier (email)
            otp_code: The OTP code to check
            purpose: Purpose of OTP (registration, password_reset)
            
        Returns:
            bool: True if OTP is valid, False otherwise
        """
        key = self._generate_key(identifier, purpose)
        
        try:
            stored_data = self.redis_client.hgetall(key)
            return bool(stored_data and stored_data.get("otp") == otp_code)
        except Exception as e:
            print(f"Error checking OTP validity: {e}")
            return False
    
    def delete_otp(self, identifier: str, purpose: str) -> bool:
        """
        Manually delete OTP from Redis.
        
        Args:
            identifier: User identifier (email)
            purpose: Purpose of OTP (registration, password_reset)
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        key = self._generate_key(identifier, purpose)
        
        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error deleting OTP: {e}")
            return False
    
    def get_otp_ttl(self, identifier: str, purpose: str) -> Optional[int]:
        """
        Get remaining TTL for OTP in seconds.
        
        Args:
            identifier: User identifier (email)
            purpose: Purpose of OTP (registration, password_reset)
            
        Returns:
            Optional[int]: TTL in seconds or None if expired/not found
        """
        key = self._generate_key(identifier, purpose)
        
        try:
            ttl = self.redis_client.ttl(key)
            return ttl if ttl > 0 else None
        except Exception as e:
            print(f"Error getting OTP TTL: {e}")
            return None
