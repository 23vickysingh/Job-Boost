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
        return f"otp:{purpose}:{identifier}"
        
    def generate_otp(self, length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))
    
    def store_otp(self, identifier: str, otp_code: str, purpose: str, 
                  ttl_minutes: int = 5, additional_data: Optional[Dict] = None) -> bool:

        key = self._generate_key(identifier, purpose)
        
        try:
            data = {"otp": otp_code}
            if additional_data:
                data.update(additional_data)
            
            pipe = self.redis_client.pipeline()
            pipe.hset(key, mapping=data)
            pipe.expire(key, timedelta(minutes=ttl_minutes))
            pipe.execute()
            
            return True
        except Exception as e:
            print(f"Error storing OTP in Redis: {e}")
            return False
    
    def verify_otp(self, identifier: str, otp_code: str, purpose: str) -> Optional[Dict]:

        key = self._generate_key(identifier, purpose)
        
        try:
            print(f"Verifying OTP for key: {key}")
            stored_data = self.redis_client.hgetall(key)
            print(f"Stored data: {stored_data}")
            print(f"Expected OTP: {otp_code}, Stored OTP: {stored_data.get('otp') if stored_data else 'None'}")
            
            if not stored_data or stored_data.get("otp") != otp_code:
                print(f"OTP verification failed for {identifier}")
                return None
            
            additional_data = {k: v for k, v in stored_data.items() if k != "otp"}
            
            self.redis_client.delete(key)
            print(f"OTP verified and deleted for {identifier}")
            
            return additional_data
        except Exception as e:
            print(f"Error verifying OTP: {e}")
            return None
    
    def is_otp_valid(self, identifier: str, otp_code: str, purpose: str) -> bool:

        key = self._generate_key(identifier, purpose)
        
        try:
            print(f"Checking OTP validity for key: {key}")
            stored_data = self.redis_client.hgetall(key)
            print(f"Stored data for validation: {stored_data}")
            is_valid = bool(stored_data and stored_data.get("otp") == otp_code)
            print(f"OTP valid check result: {is_valid}")
            return is_valid
        except Exception as e:
            print(f"Error checking OTP validity: {e}")
            return False
    
    def delete_otp(self, identifier: str, purpose: str) -> bool:

        key = self._generate_key(identifier, purpose)
        
        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error deleting OTP: {e}")
            return False
    
    def get_otp_ttl(self, identifier: str, purpose: str) -> Optional[int]:

        key = self._generate_key(identifier, purpose)
        
        try:
            ttl = self.redis_client.ttl(key)
            return ttl if ttl > 0 else None
        except Exception as e:
            print(f"Error getting OTP TTL: {e}")
            return None
