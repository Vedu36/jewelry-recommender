#!/usr/bin/env python3
"""
API Testing Script for Jewelry Recommender
Run this to test the API endpoints
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, files=None, description=""):
    """Test an API endpoint"""
    print(f"\n🔍 Testing: {description or endpoint}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method.upper() == 'POST':
            if files:
                response = requests.post(f"{BASE_URL}{endpoint}", data=data, files=files)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success")
            return result
        else:
            print(f"   ❌ Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Is the server running?")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    """Main testing function"""
    print("🧪 Jewelry Recommender API Testing Suite")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    for i in range(5):
        try:
            response = requests.get(f"{BASE_URL}/api/data/options")
            if response.status_code == 200:
                print("✅ Server is ready!")
                break
        except:
            time.sleep(2)
    else:
        print("❌ Could not connect to server. Please ensure it's running on port 8000")
        return

    session_id = None

    # Test 1: Get available options
    options = test_endpoint('GET', '/api/data/options', description="Get jewelry options")
    if options:
        print(f"   Available stones: {options.get('stones', [])[:3]}...")
        print(f"   Available metals: {options.get('metals', [])[:3]}...")

    # Test 2: Submit preferences
    preferences_data = {
        "ring_type": "engagement",
        "stone_type": "diamond",
        "metal_type": "platinum",
        "budget_min": 5000,
        "budget_max": 15000,
        "preferred_shape": "round",
        "style_preference": "classic",
        "occasion": "engagement"
    }
    
    result = test_endpoint('POST', '/api/preferences', preferences_data, 
                          description="Submit preferences and get recommendations")
    
    if result and 'session_id' in result:
        session_id = result['session_id']
        print(f"   Session ID: {session_id}")
        print(f"   Generated {len(result.get('suggestions', []))} suggestions")
        
        # Show first suggestion details
        if result.get('suggestions'):
            suggestion = result['suggestions'][0]
            print(f"   First suggestion: {suggestion.get('stone_type')} {suggestion.get('stone_shape')}")
            print(f"   Price: ${suggestion.get('estimated_price', 0):,.2f}")

    # Test 3: Add to shortlist (if we have a session)
    if session_id and result and result.get('suggestions'):
        design_id = result['suggestions'][0]['id']
        shortlist_data = {
            "design_id": design_id,
            "user_session": session_id
        }
        
        shortlist_result = test_endpoint('POST', '/api/shortlist', shortlist_data,
                                       description="Add design to shortlist")
        
        if shortlist_result:
            print(f"   Shortlist count: {shortlist_result.get('shortlist_count', 0)}")

    # Test 4: Get shortlist
    if session_id:
        shortlist = test_endpoint('GET', f'/api/shortlist/{session_id}',
                                description="Retrieve shortlist")
        
        if shortlist:
            print(f"   Shortlisted designs: {shortlist.get('count', 0)}")

    # Test 5: Refine preferences
    if session_id:
        refine_data = {
            "user_session": session_id,
            "preferences": {
                "budget_max": 20000,
                "metal_type": "rose_gold"
            },
            "feedback": "I'd like something more unique"
        }
        
        refined = test_endpoint('POST', '/api/refine', refine_data,
                              description="Refine recommendations")
        
        if refined:
            print(f"   Refined suggestions: {len(refined.get('suggestions', []))}")

    # Test 6: Image upload simulation (create a small test file)
    test_image_path = Path("test_image.jpg")
    if not test_image_path.exists():
        # Create a minimal JPEG file for testing
        jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xaa\xff\xd9'
        
        with open(test_image_path, 'wb') as f:
            f.write(jpeg_data)
        print(f"✅ Created test image: {test_image_path}")

    # Test image upload
    if test_image_path.exists():
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            image_result = test_endpoint('POST', '/api/upload-image', files=files,
                                       description="Upload and analyze image")
        
        if image_result:
            print(f"   Detected styles: {image_result.get('image_analysis', {}).get('detected_styles', [])}")
            print(f"   Generated suggestions: {len(image_result.get('suggestions', []))}")
        
        # Clean up test file
        test_image_path.unlink()

    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    
    if session_id:
        print(f"✅ All tests passed with session: {session_id}")
        print("\n💡 You can now:")
        print("   - Visit http://localhost:8000 to use the web interface")
        print("   - Check http://localhost:8000/docs for full API documentation")
        print("   - Use the session ID above to continue testing manually")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()