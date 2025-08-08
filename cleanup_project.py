#!/usr/bin/env python3
import os
import shutil

def cleanup_project():
    """Remove all unnecessary files from the Job-Boost project"""
    
    base_path = r"y:\Job-Boost"
    
    # Files to remove from root directory
    root_files_to_remove = [
        "FIXES_APPLIED.md",
        "FRONTEND_MIGRATION_SUMMARY.md", 
        "ISSUE_RESOLUTION_SUMMARY.md",
        "MIGRATION_SUMMARY.md",
        "PROFILE_ENHANCEMENT_SUMMARY.md",
        "PROFILE_SETUP_GUIDE.md",
        "PROFILE_UPDATE_SUMMARY.md",
        "RESUME_PARSER_FIX.md",
        "RESUME_PARSING_DOCS.md",
        "TEST_FIXES.md",
        "start_backend.bat",
        "test_backend.py",
        "test_backend_simple.py", 
        "test_profile_endpoint.py",
        "test_redis_otp.py"
    ]
    
    # Files to remove from BackEnd directory
    backend_files_to_remove = [
        "background_tasks.py",
        "check_db.py",
        "check_db_structure.py", 
        "check_tables.py",
        "cleanup_db.py",
        "clean_prints.py",
        "clean_router_prints.py",
        "comprehensive_trigger_test.py",
        "debug_job_matcher.py",
        "debug_job_matcher_env.py",
        "debug_test.py",
        "drop_old_tables.py",
        "elasticsearch_config.py",
        "ELASTICSEARCH_SETUP.md",
        "FINAL_WORKING_DEMO.py",
        "generate_elasticsearch_api_key.py",
        "init_database.py",
        "INTEGRATION_COMPLETE.md",
        "JOB_MATCHING_README.md",
        "manual_test.py",
        "migrate_database.py",
        "migrate_job_details.py",
        "migrate_resume_data.py",
        "migrate_resume_text.py",
        "QUICK_START_JOB_MATCHING.md",
        "quick_test.py",
        "schemas_clean.py",
        "simple_trigger_test.py",
        "tokens.py",
        "verify_functionality.py",
        "__init__.py"
    ]
    
    # Remove all test_*.py files from BackEnd
    backend_dir = os.path.join(base_path, "BackEnd")
    if os.path.exists(backend_dir):
        for file in os.listdir(backend_dir):
            if file.startswith("test_") and file.endswith(".py"):
                backend_files_to_remove.append(file)
    
    # Directories to remove completely
    dirs_to_remove = [
        os.path.join(base_path, "BackEnd", "scripts"),
        os.path.join(base_path, "BackEnd", "venv"),
        os.path.join(base_path, "BackEnd", "__pycache__"),
        os.path.join(base_path, "BackEnd", "auth", "__pycache__"),
        os.path.join(base_path, "BackEnd", "routers", "__pycache__"),
        os.path.join(base_path, "BackEnd", "services", "__pycache__"),
        os.path.join(base_path, "BackEnd", "utils", "__pycache__")
    ]
    
    # Remove root files
    print("Cleaning root directory...")
    for file in root_files_to_remove:
        file_path = os.path.join(base_path, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file}")
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")
    
    # Remove backend files
    print("\nCleaning BackEnd directory...")
    for file in backend_files_to_remove:
        file_path = os.path.join(base_path, "BackEnd", file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: BackEnd/{file}")
            except Exception as e:
                print(f"❌ Failed to remove BackEnd/{file}: {e}")
    
    # Remove directories
    print("\nRemoving unnecessary directories...")
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to remove directory {dir_path}: {e}")
    
    # Remove unused service files
    print("\nCleaning services directory...")
    services_to_remove = [
        "job_matcher.py",
        "job_scheduler.py", 
        "job_search_trigger.py",
        "periodic_job_search.py",
        "periodic_job_search_v2.py"
    ]
    
    for service in services_to_remove:
        service_path = os.path.join(base_path, "BackEnd", "services", service)
        if os.path.exists(service_path):
            try:
                os.remove(service_path)
                print(f"✅ Removed: services/{service}")
            except Exception as e:
                print(f"❌ Failed to remove services/{service}: {e}")
    
    # Remove unused router files
    print("\nCleaning routers directory...")
    routers_to_remove = ["jobs.py", "profile_clean.py"]
    
    for router in routers_to_remove:
        router_path = os.path.join(base_path, "BackEnd", "routers", router)
        if os.path.exists(router_path):
            try:
                os.remove(router_path)
                print(f"✅ Removed: routers/{router}")
            except Exception as e:
                print(f"❌ Failed to remove routers/{router}: {e}")
    
    print("\n🎉 Project cleanup completed!")
    print("\n📁 Files that should remain:")
    print("Root: .env, .env.example, .gitignore, docker-compose.yml, README.md")
    print("BackEnd: main.py, models.py, schemas.py, database.py, redis_client.py, requirements.txt, Dockerfile, .dockerignore")
    print("BackEnd/auth: dependencies.py, hashing.py, tokens.py, schemas.py")
    print("BackEnd/routers: user.py, profile.py")
    print("BackEnd/services: otp_service.py, __init__.py")
    print("BackEnd/utils: resume_parser.py, __init__.py")
    print("FrontEnd: [Complete frontend application]")

if __name__ == "__main__":
    cleanup_project()
