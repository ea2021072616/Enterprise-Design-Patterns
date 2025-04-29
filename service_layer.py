# service_layer.py
from typing import List, Optional
from repository_pattern import Customer, CustomerRepository

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    
    def register_customer(self, name: str, email: str) -> Customer:
        if "@" not in email:
            raise ValueError("Invalid email format")
        
        existing = [c for c in self.repository.get_all() if c.email == email]
        if existing:
            raise ValueError("Email already registered")
        
        customer = Customer(id=None, name=name, email=email)
        self.repository.add(customer)
        return customer
    
    def update_customer_email(self, customer_id: int, new_email: str) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if "@" not in new_email:
            raise ValueError("Invalid email format")
        
        customer.email = new_email
        self.repository.update(customer)
        return customer
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id)
    
    def list_all_customers(self) -> List[Customer]:
        return self.repository.get_all()

# Tests para el Service Layer
import unittest
from unittest.mock import MagicMock
from repository_pattern import InMemoryCustomerRepository

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=InMemoryCustomerRepository)
        self.service = CustomerService(self.mock_repo)
        self.valid_customer = Customer(id=1, name="Test", email="test@example.com")
    
    def test_register_customer_success(self):
        self.mock_repo.get_all.return_value = []
        result = self.service.register_customer("Test", "test@example.com")
        self.assertEqual(result.name, "Test")
        self.mock_repo.add.assert_called_once()
    
    def test_register_customer_invalid_email(self):
        with self.assertRaises(ValueError):
            self.service.register_customer("Test", "invalid-email")
    
    def test_register_customer_duplicate_email(self):
        self.mock_repo.get_all.return_value = [self.valid_customer]
        with self.assertRaises(ValueError):
            self.service.register_customer("Test", "test@example.com")
    
    def test_update_customer_email_success(self):
        self.mock_repo.get_by_id.return_value = self.valid_customer
        result = self.service.update_customer_email(1, "new@example.com")
        self.assertEqual(result.email, "new@example.com")
        self.mock_repo.update.assert_called_once()
    
    def test_update_customer_not_found(self):
        self.mock_repo.get_by_id.return_value = None
        with self.assertRaises(ValueError):
            self.service.update_customer_email(99, "new@example.com")
    
    def test_update_customer_invalid_email(self):
        self.mock_repo.get_by_id.return_value = self.valid_customer
        with self.assertRaises(ValueError):
            self.service.update_customer_email(1, "invalid-email")

if __name__ == "__main__":
    unittest.main()