import requests
import sys
from datetime import datetime, timedelta
import json

class ServicesTriuckAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                print(f"   Data: {json.dumps(data, indent=2)}")
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            result = {
                "test": name,
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status
            }
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    result["response"] = response_data
                except:
                    pass
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                    result["error"] = error_data
                except:
                    print(f"   Response text: {response.text[:200]}")
                    result["error"] = response.text[:200]

            self.test_results.append(result)
            return success, response.json() if success else {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            self.test_results.append({
                "test": name,
                "success": False,
                "error": "Request timeout"
            })
            return False, {}
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Failed - Connection error: {str(e)}")
            self.test_results.append({
                "test": name,
                "success": False,
                "error": f"Connection error: {str(e)}"
            })
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "test": name,
                "success": False,
                "error": str(e)
            })
            return False, {}

    def test_health_check(self):
        """Test API health check"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/",
            200
        )
        return success

    def test_create_contact(self):
        """Test contact form submission"""
        test_data = {
            "nombre": "Juan Pérez",
            "email": "juan.perez@example.com",
            "telefono": "+34 600 123 456",
            "mensaje": "Necesito información sobre reparación de motor de camión."
        }
        
        success, response = self.run_test(
            "Create Contact Form",
            "POST",
            "api/contact",
            200,
            data=test_data
        )
        
        if success:
            # Verify response contains expected fields
            if 'id' in response and 'nombre' in response:
                print(f"   ✓ Contact created with ID: {response['id']}")
                return True, response['id']
            else:
                print(f"   ⚠ Response missing expected fields")
                return False, None
        return False, None

    def test_get_contacts(self):
        """Test retrieving contact forms"""
        success, response = self.run_test(
            "Get Contact Forms",
            "GET",
            "api/contact",
            200
        )
        
        if success:
            if isinstance(response, list):
                print(f"   ✓ Retrieved {len(response)} contact forms")
                return True
            else:
                print(f"   ⚠ Response is not a list")
                return False
        return False

    def test_create_appointment(self):
        """Test appointment creation"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        test_data = {
            "nombre": "María",
            "apellidos": "García López",
            "email": "maria.garcia@example.com",
            "telefono": "+34 661 388 880",
            "fecha_preferida": tomorrow,
            "hora_preferida": "10:00",
            "tipo_servicio": "Reparación de Motores de Camiones",
            "descripcion": "Motor de camión Volvo con problemas de arranque. Necesito revisión urgente."
        }
        
        success, response = self.run_test(
            "Create Appointment",
            "POST",
            "api/appointments",
            200,
            data=test_data
        )
        
        if success:
            if 'id' in response and 'nombre' in response:
                print(f"   ✓ Appointment created with ID: {response['id']}")
                return True, response['id']
            else:
                print(f"   ⚠ Response missing expected fields")
                return False, None
        return False, None

    def test_get_appointments(self):
        """Test retrieving appointments"""
        success, response = self.run_test(
            "Get Appointments",
            "GET",
            "api/appointments",
            200
        )
        
        if success:
            if isinstance(response, list):
                print(f"   ✓ Retrieved {len(response)} appointments")
                return True
            else:
                print(f"   ⚠ Response is not a list")
                return False
        return False

    def test_contact_validation(self):
        """Test contact form validation (missing required fields)"""
        test_data = {
            "nombre": "Test User",
            "email": "invalid-email"  # Missing telefono and mensaje
        }
        
        success, response = self.run_test(
            "Contact Form Validation (should fail)",
            "POST",
            "api/contact",
            422,  # Expecting validation error
            data=test_data
        )
        return success

    def test_appointment_validation(self):
        """Test appointment validation (missing required fields)"""
        test_data = {
            "nombre": "Test",
            "email": "test@example.com"
            # Missing many required fields
        }
        
        success, response = self.run_test(
            "Appointment Validation (should fail)",
            "POST",
            "api/appointments",
            422,  # Expecting validation error
            data=test_data
        )
        return success

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print("="*60)
        
        if self.tests_passed == self.tests_run:
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Some tests failed")
            print("\nFailed tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}")
                    if 'error' in result:
                        print(f"    Error: {result['error']}")
            return 1

def main():
    # Get backend URL from environment or use default
    import os
    backend_url = os.environ.get('REACT_APP_BACKEND_URL', 'https://services-truck-pro.preview.emergentagent.com')
    
    print("="*60)
    print("🚛 Services Truck API Testing")
    print("="*60)
    print(f"Backend URL: {backend_url}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tester = ServicesTriuckAPITester(backend_url)
    
    # Run tests in sequence
    print("\n📋 Running Backend API Tests...\n")
    
    # 1. Health check
    if not tester.test_health_check():
        print("\n⚠️  Health check failed - API may not be running")
        print("Continuing with other tests...\n")
    
    # 2. Contact form tests
    print("\n--- Contact Form Tests ---")
    contact_success, contact_id = tester.test_create_contact()
    tester.test_get_contacts()
    tester.test_contact_validation()
    
    # 3. Appointment tests
    print("\n--- Appointment Tests ---")
    appointment_success, appointment_id = tester.test_create_appointment()
    tester.test_get_appointments()
    tester.test_appointment_validation()
    
    # Print summary
    exit_code = tester.print_summary()
    
    # Additional info
    if contact_success:
        print(f"\n💡 Test contact created with ID: {contact_id}")
    if appointment_success:
        print(f"💡 Test appointment created with ID: {appointment_id}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
