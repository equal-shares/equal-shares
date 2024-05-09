import sys
import unittest

sys.path.append("../..")
from src.server.node import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        # Node initialization for testing
        self.node = Node(1, "Node 1", "This is a node", None, 100.0)

    def test_init1(self):
        # Test case 1: Verify that __init__() method sets attributes correctly
        id = 2
        name = "Node 1"
        description = "This is node 1"
        parent = None
        budget_amount = 100.0

        node = Node(id, name, description, parent, budget_amount)

        self.assertEqual(node.get_id(), id)
        self.assertEqual(node.get_name(), name)
        self.assertEqual(node.get_description(), description)
        self.assertEqual(node.get_parent_id(), parent)
        self.assertEqual(node.get_allocated_budget_amount(), budget_amount)
        self.assertEqual(node.get_children(), [])

    def test_init2(self):
        # Test case 2: Verify that __init__() method sets attributes correctly when parent is not None
        id = 2
        name = "Node 1"
        description = "This is node 1"
        parent = None
        budget_amount = 100.0
        node = Node(id, name, description, parent, budget_amount)

        id = 3
        name = "Node 2"
        description = "This is node 2"
        parent = 1
        budget_amount = 50.0

        node = Node(id, name, description, parent, budget_amount)

        self.assertEqual(node.get_id(), id)
        self.assertEqual(node.get_name(), name)
        self.assertEqual(node.get_description(), description)
        self.assertEqual(node.get_parent_id(), parent)
        self.assertEqual(node.get_allocated_budget_amount(), budget_amount)
        self.assertEqual(node.get_children(), [])

    def test_get_id(self):
        self.assertEqual(self.node.get_id(), 1)

    def test_get_name(self):
        self.assertEqual(self.node.get_name(), "Node 1")

    def test_get_description(self):
        self.assertEqual(self.node.get_description(), "This is a node")

    def test_get_parent_id(self):
        self.assertEqual(self.node.get_parent_id(), None)

    def test_get_allocated_budget_amount(self):
        self.assertEqual(self.node.get_allocated_budget_amount(), 100.0)


if __name__ == "__main__":
    unittest.main()
