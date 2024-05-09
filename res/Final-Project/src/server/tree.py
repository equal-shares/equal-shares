from node import Node


class Tree:
    """This class present the tree of subjects and projects (container of Nodes)"""

    def __init__(self, root: Node) -> None:
        self._root = root
        self._node_amount = 0

        if self._root is not None:
            self._node_amount = 1

    def get_root(self) -> Node:
        """
        Return the root node of the tree.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> tree = Tree(node1)
        >>> tree.get_root().get_id()
        1
        """
        return self._root

    def set_root(self, new_root: Node) -> None:
        """
        Set the root node of the tree to the given node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node2 = Node(2, 'Node 2', 'This is node 2', 1, 50)
        >>> tree = Tree(node1)
        >>> tree.set_root(node2)
        >>> tree.get_root().get_id()
        2
        """
        self._root = new_root

    def add_node(self, parent_id: int, new_node: Node) -> bool:
        """
        Add a new node to the tree with the specified parent id.

        >>> root_node = Node(0, 'root', 'I am root', None, 0)
        >>> child_node = Node(1, 'child', 'project', 10)
        >>> tree = Tree(root_node)
        >>> tree.add_node(0, child_node)
        >>> tree.get_size()
        2
        >>> tree.get_node(1,root_node).get_id()
        1
        """
        if new_node is None:
            print("Error!, New Node that inserted is None.")
            return False

        if parent_id is None:
            print("Error!, Parent id that inserted is None.")
            return False

        else:
            parent_node = self.get_node(parent_id)
            if parent_node is None:
                print(f"Error!, There is no Node with id ''{parent_id}'' in the tree")
                return False

        parent_node.add_child(new_node)
        self._node_amount += 1

        return True

    def add_node_by_id_and_name(
        self, parent_id: int, parent_name: str, new_node: Node
    ) -> bool:
        """
        Add a new node to the tree with the specified parent id and name.
        """

        if new_node is None:
            print("Error!, New Node that inserted is None.")
            return False

        if parent_id is None:
            print("Error!, Parent id that inserted is None.")
            return False

        if parent_name is None or "":
            print("Error!, Parent id that inserted is None.")
            return False

        else:
            parent_node = self.get_node_by_name_and_id(parent_id, parent_name)

            if parent_node is None:
                print(
                    f"Error!, There is no Node with id ''{parent_id}'' and name ''{parent_name}'' in the tree"
                )
                return False

        parent_node.add_child(new_node)
        self._node_amount += 1

        return True

    def remove_node(self, parent_id: int, node_id: int) -> bool:
        """
        Removes a node from the tree with the given parent id and child id

        >>> root = Node(1, "root",  "I am root", None , 1000)
        >>> node1 = Node(2, "project1", "I am project1", None, 500)
        >>> node2 = Node(3, "project2", "I am project2", None, 300)
        >>> tree = Tree(root)
        >>> tree.add_node(1, node1)
        >>> tree.add_node(2, node2)
        >>> tree.get_size()
        3
        >>> tree.remove_node(2, 3)
        >>> tree.get_size()
        2
        >>> tree.get_node(3,root)
        None
        """
        node = self.get_node(node_id)

        if node is None:
            print(f"Error!, There is no node in the tree that has the id {node_id}")
            return False

        # Remove children
        for child in node.get_children():
            child.set_parent_id(None)

        # Remove node from beeing child of his parent
        parent_id = node.get_parent_id()
        parent_node = self.get_node(parent_id)
        parent_node.remove_child(node.get_id())

        # Remove parent id from this node
        node.set_parent_id(None)

        self._node_amount -= 1

        return True

    def remove_node_by_id_and_name(
        self, parent_id: int, node_id: int, node_name: str
    ) -> bool:
        """
        Removes a node from the tree with the given parent id and child id

        >>> root = Node(1, "root",  "I am root", None , 1000)
        >>> node1 = Node(2, "project1", "I am project1", None, 500)
        >>> node2 = Node(3, "project2", "I am project2", None, 300)
        >>> tree = Tree(root)
        >>> tree.add_node(1, node1)
        >>> tree.add_node(2, node2)
        >>> tree.get_size()
        3
        >>> tree.remove_node(2, 3)
        >>> tree.get_size()
        2
        >>> tree.get_node(3,root)
        None
        """
        node = self.get_node_by_name_and_id(node_id=node_id, node_name=node_name)

        if node is None:
            print(f"Error!, There is no node in the tree that has the id {node_id}")
            return False

        # Remove children
        for child in node.get_children():
            child.set_parent_id(None)

        # Remove node from beeing child of his parent
        parent_id = node.get_parent_id()
        parent_node = self.get_node(parent_id)
        parent_node.remove_child_by_id_and_name(node_id, node_name)

        # Remove parent id from this node
        node.set_parent_id(None)

        self._node_amount -= 1

        return True

    def get_size(self) -> int:
        """
        Returns the size of the tree

        >>> root = Node(1, "root-subject","I am root" , None, 1000)
        >>> t = Tree(root)
        >>> t.get_size()
        1
        >>> node1 = Node(2, "project", "I am node1", None, 500)
        >>> t.add_node(1, node1)
        >>> t.get_size()
        2
        """
        return self._node_amount

    def get_node_by_name_and_id(self, node_id: int, node_name: str):
        if self._root is None:
            print("Error!, Empty tree")
            return None

        current_node = self._root
        return self._get_node_recursive_by_name_and_id(current_node, node_id, node_name)

    def _get_node_recursive_by_name_and_id(
        self, current_node: Node, target_node_id: int, target_node_name: str
    ) -> Node:
        if (
            target_node_id == current_node.get_id()
            and target_node_name == current_node.get_name()
        ):
            return current_node

        else:
            for child in current_node.get_children():
                found_node = self._get_node_recursive_by_name_and_id(
                    child, target_node_id, target_node_name
                )
                if found_node:
                    return found_node

        return None

    # def get_node_by_name_and_id(self, node_id:int, node_name:str) -> Node:
    #     '''
    #     Return the node with the given id and name in the tree.

    #     Args:
    #     node_id (int): The id of the node to search for.
    #     node_name (str): The name of the node to search for.

    #     Returns:
    #     The node with the given id and name if found, None otherwise.
    #     '''
    #     def dfs(node: Node) -> Node:
    #         if node is None:
    #             return None

    #         if node.get_id() == node_id and node.get_name() == node_name:
    #             return node

    #         for child in node.get_children():
    #             result = dfs(child)
    #             if result is not None:
    #                 return result

    #         return None

    #     return dfs(self.get_root())

    def get_node(self, node_id: int) -> Node:
        """
        Returns the node object with the given id,
        If there is no node with such an id it will return None

        >>> root = Node(1, "root", "I am root", None, 1000)
        >>> node1 = Node(2, "project1", "I am project1", None, 250)
        >>> node2 = Node(3, "project2", "I am project1", None, 500)
        >>> tree = Tree(root)
        >>> tree.add_node(1, node1)
        >>> tree.add_node(2, node2)
        >>> founded_node = tree.get_node(2)
        >>> founded_node.tree.get_name()
        project1
        >>> founded_node = tree.get_node(3)
        >>> founded_node.tree.get_name()
        project2
        """
        if self._root is None:
            print("Error!, Empty tree")
            return None

        current_node = self._root
        return self._get_node_recursive(current_node, node_id)

    def _get_node_recursive(self, current_node: Node, target_node_id: int) -> Node:
        if target_node_id == current_node.get_id():
            return current_node

        else:
            for child in current_node.get_children():
                found_node = self._get_node_recursive(child, target_node_id)
                if found_node:
                    return found_node

        return None

    def get_budget_amount(self) -> float:
        """
        Return the total budget of all the projects and subjects nodes in the tree.

        >>> root_node = Node(1,'root', 'I am root', None, 0)
        >>> child_node1 = Node(2,'child1', 'project1',None, 15)
        >>> child_node2 = Node(3,'child2', 'project2',None, 35)
        >>> child_node3 = Node(4,'child3', 'project3',None, 30)
        >>> tree = Tree(root_node)
        >>> tree.add_node(1, child_node1)
        >>> tree.add_node(1, child_node2)
        >>> tree.add_node(1, child_node3)
        >>> tree.get_budget_amount()
        80
        """
        if self._root is None:
            print("Error!, Empty tree")
            return 0

        current_node = self._root
        return self._get_budget_amount_recursive(
            current_node, current_node.get_allocated_budget_amount()
        )

    def _get_budget_amount_recursive(
        self, current_node: Node, total_budget: float
    ) -> float:
        if current_node is None:
            return total_budget

        if not current_node.get_children():
            return current_node.get_allocated_budget_amount()

        for child in current_node.get_children():
            total_budget += self._get_budget_amount_recursive(
                child, child.get_allocated_budget_amount()
            )

        return total_budget

    def is_project(self, id_node: int) -> bool:
        """
        Return the total budget of all the projects and subjects nodes in the tree.

        >>> root_node = Node(1,'root', 'subject', None, 0)
        >>> child_node1 = Node(2,'child1', 'subject', None, 15)
        >>> child_node2 = Node(3,'child2', 'project2', None, 35)
        >>> child_node3 = Node(4,'grandchild3', 'project3', None, 30)
        >>> tree = Tree(root_node)
        >>> tree.add_node(1, child_node1)
        >>> tree.add_node(1, child_node2)
        >>> tree.add_node(2, child_node3)
        >>> tree.is_project(1)
        False
        >>> tree.is_project(2)
        False
        >>> tree.is_project(3)
        True
        >>> tree.is_project(4)
        True
        """
        node = self.get_node(id_node)
        if node is None:
            print(f"Error!, There is no node with {id_node} in the tree")
            return False

        # if this node doesn't have children
        if not node.get_children() or node.get_children() is None:
            return True

        return False

    def node_exists(self, node_id: int) -> bool:
        if self.get_node(node_id) is None:
            return False

        return True

    def node_exists_by_id_and_name(self, node_id: int, node_name: str) -> bool:
        if self.get_node_by_name_and_id(node_id, node_name) is None:
            return False

        return True

    def to_dict(self) -> dict:
        return self._root.to_dict()

    @staticmethod
    def from_dict(data):
        """
        Build a tree from a nested dictionary.

        Args:
            data (dict): A nested dictionary.

        Returns:
            Tree: A tree object with the root node being the top-level dictionary key.
        """

        def _build_tree(data) -> Node:
            """
            Recursive function to build a tree from a nested dictionary.

            Args:
                data (dict): A nested dictionary.

            Returns:
                Node: A node object representing the root of the tree.
            """
            if isinstance(data, dict):
                # create a root node for the dictionary
                node = Node(name="root")
                # for each key-value pair, create a child node and add it to the root node
                for key, value in data.items():
                    child_node = _build_tree(value)
                    child_node._name = key
                    node.add_child(child_node)
            else:
                # create a leaf node for the value
                node = Node(name="leaf", budget_amount=data)
            return node

        # create a tree object from the root node
        root_node = _build_tree(data)
        return Tree(root_node)

    def print_tree(self) -> None:
        """
        Print the tree in a hierarchical format with each node's name and value (if any).

        Returns:
            None
        """
        if self._root is not None:
            # print the root node and its children
            Node._print_node(self._root)
