# repository_pattern.py
from abc import ABC, abstractmethod
from typing import List, Optional

class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Customer]:
        pass
    
    @abstractmethod
    def add(self, customer: Customer):
        pass
    
    @abstractmethod
    def update(self, customer: Customer):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers = {}
        self.next_id = 1
    
    def get_by_id(self, id: int) -> Optional[Customer]:
        return self.customers.get(id)
    
    def get_all(self) -> List[Customer]:
        return list(self.customers.values())
    
    def add(self, customer: Customer):
        if customer.id is None:
            customer.id = self.next_id
            self.next_id += 1
        self.customers[customer.id] = customer
    
    def update(self, customer: Customer):
        if customer.id in self.customers:
            self.customers[customer.id] = customer
    
    def delete(self, id: int):
        if id in self.customers:
            del self.customers[id]

# Tests para el Repository Pattern
import unittest

class TestCustomerRepository(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryCustomerRepository()
        self.customer1 = Customer(id=None, name="Test User", email="test@example.com")
        self.customer2 = Customer(id=None, name="Another User", email="another@example.com")
    
    def test_add_customer(self):
        self.repo.add(self.customer1)
        self.assertEqual(len(self.repo.get_all()), 1)
        self.assertIsNotNone(self.customer1.id)
    
    def test_get_by_id(self):
        self.repo.add(self.customer1)
        retrieved = self.repo.get_by_id(self.customer1.id)
        self.assertEqual(retrieved.name, "Test User")
    
    def test_update_customer(self):
        self.repo.add(self.customer1)
        self.customer1.email = "updated@example.com"
        self.repo.update(self.customer1)
        updated = self.repo.get_by_id(self.customer1.id)
        self.assertEqual(updated.email, "updated@example.com")
    
    def test_delete_customer(self):
        self.repo.add(self.customer1)
        self.repo.add(self.customer2)
        self.repo.delete(self.customer1.id)
        self.assertEqual(len(self.repo.get_all()), 1)
        self.assertIsNone(self.repo.get_by_id(self.customer1.id))
    
    def test_get_all_customers(self):
        self.repo.add(self.customer1)
        self.repo.add(self.customer2)
        customers = self.repo.get_all()
        self.assertEqual(len(customers), 2)
        self.assertIn(self.customer1, customers)
        self.assertIn(self.customer2, customers)

if __name__ == "__main__":
    unittest.main()