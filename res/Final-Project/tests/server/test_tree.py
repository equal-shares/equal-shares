import sys
import unittest

sys.path.append("../..")
from src.server.node import Node
from src.server.tree import Tree


class Test_tree(unittest.TestCase):
    def test_add_node(self):
        root = Node(0, "Ministry of Defence", "description", None, 100)
        tree = Tree(root)
        child = Node(1, "node", "description", 0, 50)
        tree.add_node_by_id_and_name(root.get_id(), root.get_name(), child)

        self.assertEqual(len(tree.get_node(0).get_children()), 1)
        self.assertEqual(tree.get_size(), 2)

        for i in range(2, 100):
            node = Node(i, "node", "description", None, 10)
            tree.add_node_by_id_and_name(i - 1, "node", node)

        self.assertEqual(tree.get_size(), 100)

    def test_get_size(self):
        root = Node(0, "Root", "This is the root node", None, 100)
        tree = Tree(root)
        child1 = Node(1, "Child1", "This is a child node", 0, 50)
        child2 = Node(2, "Child2", "This is another child node", 0, 25)
        tree.add_node_by_id_and_name(root.get_id(), root.get_name(), child1)
        tree.add_node_by_id_and_name(root.get_id(), root.get_name(), child2)

        self.assertEqual(tree.get_size(), 3)

    def test_get_budget_amount(self):
        root = Node(0, "Root", "This is the root node", None, 100)
        tree = Tree(root)
        child1 = Node(1, "Child1", "This is a child node", 0, 50)
        child2 = Node(2, "Child2", "This is another child node", 0, 25)
        grandchild = Node(3, "Grandchild", "This is a grandchild node", 1, 10)
        tree.add_node_by_id_and_name(root.get_id(), root.get_name(), child1)

        tree.add_node_by_id_and_name(root.get_id(), root.get_name(), child2)

        tree.add_node_by_id_and_name(child1.get_id(), child1.get_name(), grandchild)
        self.assertEqual(tree.get_budget_amount(), 185)

    def test_is_project(self):
        root = Node(0, "Root", "This is the root node", None, 100)
        tree = Tree(root)
        child1 = Node(1, "Child1", "This is a child node", 0, 50)
        child2 = Node(2, "Child2", "This is another child node", 0, 25)
        grandchild = Node(3, "Grandchild", "This is a grandchild node", 1, 10)
        tree.add_node(0, child1)
        tree.add_node(0, child2)
        tree.add_node(1, grandchild)

        self.assertFalse(tree.is_project(0))
        self.assertFalse(tree.is_project(1))
        self.assertTrue(tree.is_project(2))
        self.assertTrue(tree.is_project(3))

    # def test_to_dict(self):
    #     root = Node(1,'root', 'I am root', None, 0)
    #     child1 = Node(2,'child1', 'project1',None, 15)
    #     child2 = Node(3,'child2', 'project2',None, 35)
    #     child3 = Node(4,'child3', 'project3',None, 30)

    #     tree = Tree(root)
    #     tree.add_node(1, child1)
    #     tree.add_node(1, child2)
    #     tree.add_node(1, child3)

    #     expected = {
    #         'id': 1,
    #         'name': 'root',
    #         'description': 'I am root',
    #         'parent_id': None,
    #         'budget': 0.0,
    #         'children': [
    #             {
    #                 'id': 2,
    #                 'name': 'child1',
    #                 'description': 'project1',
    #                 'parent_id': 1,
    #                 'budget': 15.0,
    #                 'children': []
    #             },
    #             {
    #                 'id': 3,
    #                 'name': 'child2',
    #                 'description': 'project2',
    #                 'parent_id': 1,
    #                 'budget': 35.0,
    #                 'children': []
    #             },
    #             {
    #                 'id': 4,
    #                 'name': 'child3',
    #                 'description': 'project3',
    #                 'parent_id': 1,
    #                 'budget': 30.0,
    #                 'children': []
    #             }
    #         ]
    #     }

    #     self.assertEquals(tree.to_dict(), expected)


if __name__ == "__main__":
    unittest.main()
