# unit_of_work.py
from typing import Dict, List, Type, Any
from repository_pattern import Customer, CustomerRepository, InMemoryCustomerRepository

class UnitOfWork:
    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []
        self.repositories = {
            Customer: InMemoryCustomerRepository()
        }
    
    def register_new(self, obj):
        self.new_objects.append(obj)
    
    def register_dirty(self, obj):
        if obj not in self.dirty_objects and obj not in self.new_objects:
            self.dirty_objects.append(obj)
    
    def register_removed(self, obj):
        if obj in self.new_objects:
            self.new_objects.remove(obj)
            return
        self.removed_objects.append(obj)
    
    def commit(self):
        for obj in self.new_objects:
            repo = self.repositories[type(obj)]
            repo.add(obj)
        
        for obj in self.dirty_objects:
            repo = self.repositories[type(obj)]
            repo.update(obj)
        
        for obj in self.removed_objects:
            repo = self.repositories[type(obj)]
            repo.delete(obj.id)
        
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()
    
    def rollback(self):
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()
    
    def get_repository(self, entity_type: Type) -> CustomerRepository:
        return self.repositories.get(entity_type)

# Tests para Unit of Work
import unittest

class TestUnitOfWork(unittest.TestCase):
    def setUp(self):
        self.uow = UnitOfWork()
        self.customer1 = Customer(id=None, name="Test 1", email="test1@example.com")
        self.customer2 = Customer(id=None, name="Test 2", email="test2@example.com")
    
    def test_register_new(self):
        self.uow.register_new(self.customer1)
        self.assertEqual(len(self.uow.new_objects), 1)
    
    def test_commit_new_objects(self):
        self.uow.register_new(self.customer1)
        self.uow.commit()
        repo = self.uow.get_repository(Customer)
        self.assertEqual(len(repo.get_all()), 1)
        self.assertEqual(len(self.uow.new_objects), 0)
    
    def test_register_dirty(self):
        # First add and commit a customer
        self.uow.register_new(self.customer1)
        self.uow.commit()
        
        # Then modify it
        self.customer1.name = "Modified"
        self.uow.register_dirty(self.customer1)
        self.assertEqual(len(self.uow.dirty_objects), 1)
    
    def test_commit_dirty_objects(self):
        self.uow.register_new(self.customer1)
        self.uow.commit()
        
        self.customer1.name = "Modified"
        self.uow.register_dirty(self.customer1)
        self.uow.commit()
        
        repo = self.uow.get_repository(Customer)
        updated = repo.get_by_id(self.customer1.id)
        self.assertEqual(updated.name, "Modified")
    
    def test_register_removed(self):
        self.uow.register_new(self.customer1)
        self.uow.commit()
        
        self.uow.register_removed(self.customer1)
        self.assertEqual(len(self.uow.removed_objects), 1)
    
    def test_commit_removed_objects(self):
        self.uow.register_new(self.customer1)
        self.uow.register_new(self.customer2)
        self.uow.commit()
        
        self.uow.register_removed(self.customer1)
        self.uow.commit()
        
        repo = self.uow.get_repository(Customer)
        self.assertEqual(len(repo.get_all()), 1)
        self.assertIsNone(repo.get_by_id(self.customer1.id))
    
    def test_rollback(self):
        self.uow.register_new(self.customer1)
        self.uow.register_dirty(self.customer2)
        self.uow.register_removed(Customer(id=99, name="Test", email="test@example.com"))
        
        self.uow.rollback()
        
        self.assertEqual(len(self.uow.new_objects), 0)
        self.assertEqual(len(self.uow.dirty_objects), 0)
        self.assertEqual(len(self.uow.removed_objects), 0)

if __name__ == "__main__":
    unittest.main()