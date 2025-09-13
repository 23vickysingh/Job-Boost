import redis
import random
import string
import os
import json
import time
from typing import Optional, Dict, Any
from datetime import timedelta

class OTPService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test the connection
            self.redis_client.ping()
            print(f"✅ Connected to Redis at {redis_url}")
        except Exception as e:
            print(f"❌ Failed to connect to Redis at {redis_url}: {e}")
            # Use a fallback in-memory storage for development
            self._fallback_storage = {}
            self.redis_client = None
            print("🔄 Using fallback in-memory storage for OTP")
    
    def _is_redis_available(self) -> bool:
        """Check if Redis connection is available"""
        try:
            if self.redis_client:
                self.redis_client.ping()
                return True
            return False
        except:
            return False
    
    def _generate_key(self, identifier: str, purpose: str) -> str:
        return f"otp:{purpose}:{identifier}"
        
    def generate_otp(self, length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))
    
    def store_otp(self, identifier: str, otp_code: str, purpose: str, 
                  ttl_minutes: int = 5, additional_data: Optional[Dict] = None) -> bool:
        """Store OTP with fallback to in-memory storage if Redis is unavailable"""
        key = self._generate_key(identifier, purpose)
        
        data = {"otp": otp_code}
        if additional_data:
            data.update(additional_data)
        
        # Try Redis first
        if self._is_redis_available():
            try:
                pipe = self.redis_client.pipeline()
                pipe.hset(key, mapping=data)
                pipe.expire(key, timedelta(minutes=ttl_minutes))
                pipe.execute()
                print(f"✅ OTP stored in Redis for {identifier}")
                return True
            except Exception as e:
                print(f"❌ Error storing OTP in Redis: {e}")
        
        # Fallback to in-memory storage
        try:
            import time
            expiry_time = time.time() + (ttl_minutes * 60)
            self._fallback_storage[key] = {
                "data": data,
                "expiry": expiry_time
            }
            print(f"✅ OTP stored in fallback storage for {identifier}")
            return True
        except Exception as e:
            print(f"❌ Error storing OTP in fallback storage: {e}")
            return False
    
    def verify_otp(self, identifier: str, otp_code: str, purpose: str) -> Optional[Dict]:
        """Verify OTP with fallback to in-memory storage if Redis is unavailable"""
        key = self._generate_key(identifier, purpose)
        
        print(f"🔍 Verifying OTP for key: {key}")
        
        # Try Redis first
        if self._is_redis_available():
            try:
                stored_data = self.redis_client.hgetall(key)
                print(f"📊 Redis stored data: {stored_data}")
                print(f"🔑 Expected OTP: {otp_code}, Stored OTP: {stored_data.get('otp') if stored_data else 'None'}")
                
                if stored_data and stored_data.get("otp") == otp_code:
                    additional_data = {k: v for k, v in stored_data.items() if k != "otp"}
                    self.redis_client.delete(key)
                    print(f"✅ OTP verified and deleted from Redis for {identifier}")
                    return additional_data
                else:
                    print(f"❌ OTP verification failed in Redis for {identifier}")
                    return None
            except Exception as e:
                print(f"❌ Error verifying OTP in Redis: {e}")
        
        # Fallback to in-memory storage
        try:
            import time
            current_time = time.time()
            
            if key in self._fallback_storage:
                stored_entry = self._fallback_storage[key]
                print(f"📊 Fallback stored data: {stored_entry}")
                
                # Check if expired
                if current_time > stored_entry["expiry"]:
                    del self._fallback_storage[key]
                    print(f"⏰ OTP expired in fallback storage for {identifier}")
                    return None
                
                stored_data = stored_entry["data"]
                print(f"🔑 Expected OTP: {otp_code}, Stored OTP: {stored_data.get('otp') if stored_data else 'None'}")
                
                if stored_data.get("otp") == otp_code:
                    additional_data = {k: v for k, v in stored_data.items() if k != "otp"}
                    del self._fallback_storage[key]
                    print(f"✅ OTP verified and deleted from fallback storage for {identifier}")
                    return additional_data
                else:
                    print(f"❌ OTP verification failed in fallback storage for {identifier}")
                    return None
            else:
                print(f"❌ No OTP found in fallback storage for {identifier}")
                return None
                
        except Exception as e:
            print(f"❌ Error verifying OTP in fallback storage: {e}")
            return None
    
    def is_otp_valid(self, identifier: str, otp_code: str, purpose: str) -> bool:
        """Check OTP validity with fallback to in-memory storage if Redis is unavailable"""
        key = self._generate_key(identifier, purpose)
        
        print(f"🔍 Checking OTP validity for key: {key}")
        
        # Try Redis first
        if self._is_redis_available():
            try:
                stored_data = self.redis_client.hgetall(key)
                print(f"📊 Redis stored data for validation: {stored_data}")
                is_valid = bool(stored_data and stored_data.get("otp") == otp_code)
                print(f"✅ Redis OTP valid check result: {is_valid}")
                return is_valid
            except Exception as e:
                print(f"❌ Error checking OTP validity in Redis: {e}")
        
        # Fallback to in-memory storage
        try:
            import time
            current_time = time.time()
            
            if key in self._fallback_storage:
                stored_entry = self._fallback_storage[key]
                
                # Check if expired
                if current_time > stored_entry["expiry"]:
                    del self._fallback_storage[key]
                    print(f"⏰ OTP expired in fallback storage for {identifier}")
                    return False
                
                stored_data = stored_entry["data"]
                print(f"📊 Fallback stored data for validation: {stored_data}")
                is_valid = bool(stored_data and stored_data.get("otp") == otp_code)
                print(f"✅ Fallback OTP valid check result: {is_valid}")
                return is_valid
            else:
                print(f"❌ No OTP found in fallback storage for {identifier}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking OTP validity in fallback storage: {e}")
            return False
    
    def delete_otp(self, identifier: str, purpose: str) -> bool:
        """Delete OTP with fallback to in-memory storage if Redis is unavailable"""
        key = self._generate_key(identifier, purpose)
        
        # Try Redis first
        if self._is_redis_available():
            try:
                result = self.redis_client.delete(key)
                print(f"🗑️ OTP deleted from Redis for {identifier}: {result > 0}")
                return result > 0
            except Exception as e:
                print(f"❌ Error deleting OTP from Redis: {e}")
        
        # Fallback to in-memory storage
        try:
            if key in self._fallback_storage:
                del self._fallback_storage[key]
                print(f"🗑️ OTP deleted from fallback storage for {identifier}")
                return True
            else:
                print(f"❌ No OTP found to delete in fallback storage for {identifier}")
                return False
        except Exception as e:
            print(f"❌ Error deleting OTP from fallback storage: {e}")
            return False
    
    def get_otp_ttl(self, identifier: str, purpose: str) -> Optional[int]:
        """Get OTP TTL with fallback to in-memory storage if Redis is unavailable"""
        key = self._generate_key(identifier, purpose)
        
        # Try Redis first
        if self._is_redis_available():
            try:
                ttl = self.redis_client.ttl(key)
                return ttl if ttl > 0 else None
            except Exception as e:
                print(f"❌ Error getting OTP TTL from Redis: {e}")
        
        # Fallback to in-memory storage
        try:
            import time
            current_time = time.time()
            
            if key in self._fallback_storage:
                stored_entry = self._fallback_storage[key]
                remaining_time = int(stored_entry["expiry"] - current_time)
                return remaining_time if remaining_time > 0 else None
            else:
                return None
        except Exception as e:
            print(f"❌ Error getting OTP TTL from fallback storage: {e}")
            return None
