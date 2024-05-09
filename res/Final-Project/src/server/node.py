class Node:
    """This class present node in the tree of subjects/projects"""

    def __init__(
        self,
        id: int = None,
        name: str = "",
        description: str = "",
        parent: int = None,
        budget_amount: float = None,
    ) -> None:
        self._id = id
        self._name = name
        self._description = description
        self._parent = parent
        self._allocated_budget_amount = budget_amount
        self._children: list["Node"] = []
        self.checked = False

    def get_id(self) -> int:
        """
        Return the id of the node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.get_id()
        1
        """
        return self._id

    def get_name(self) -> str:
        """
        Return the name of the node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.get_name()
        'Node 1'
        """
        return self._name

    def get_description(self) -> str:
        """
        Return the description of the node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.get_description()
        'This is node 1'
        """
        return self._description

    def get_parent_id(self) -> int:
        """
        Return the id of the parent node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', 2, 100)
        >>> node1.get_parent()
        2
        """
        return self._parent

    def get_allocated_budget_amount(self) -> float:
        """
        Return the allocated budget amount of the node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.get_allocated_budget_amount()
        100
        """
        return self._allocated_budget_amount

    def get_children(self) -> list["Node"]:
        """
        Return the list of children nodes.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node2 = Node(2, 'Node 2', 'This is node 2', 1, 50)
        >>> node1.add_child(node2)
        >>> list_of_nodes = node1.get_children()
        >>> list[0].get_id()
        2
        """
        return self._children

    def set_parent_id(self, new_parent_id: int) -> None:
        """
        Set node parent.
        """
        self._parent = new_parent_id

    def set_description(self, new_description: str) -> None:
        """
        Set the description of the node to the given value.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.set_description('This is the new description of node 1')
        >>> node1.get_description()
        'This is the new description of node 1'
        """
        self._description = new_description

    def set_allocated_budget_amount(self, new_allocated_budget_amount: float) -> None:
        """
        Return the allocated budget amount of the node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node1.set_allocated_budget_amount(200)
        200
        """
        self._allocated_budget_amount = new_allocated_budget_amount

    def add_child(self, child: "Node") -> None:
        """
        Add the given node as a child of this node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node2 = Node(2, 'Node 2', 'This is node 2', 1, 50)
        >>> node1.add_child(node2)
        >>> node1.get_children()[0].get_id()
        2
        """
        self._children.append(child)

    def remove_child(self, child_id: int) -> None:
        """
        Remove a child node with the given id from this node.

        >>> node1 = Node(1, 'Node 1', 'This is node 1', None, 100)
        >>> node2 = Node(2, 'Node 2', 'This is node 2', 1, 50)
        >>> node3 = Node(3, 'Node 3', 'This is node 3', 2, 25)
        >>> node1.add_child(node2)
        >>> node2.add_child(node3)
        >>> node2.remove_child(2)
        >>> node2.remove_child(3)
        >>> node2.get_children()
        []
        """
        for child in self._children:
            if child.get_id() == child_id:
                self._children.remove(child)
            return

        raise ValueError(f"No child node with id {child_id} was found")

    def remove_child_by_id_and_name(self, node_id: int, node_name: str) -> bool:
        for child in self._children:
            if child.get_id() == node_id and child.get_name() == node_name:
                self._children.remove(child)
                return True

        return False

    # @staticmethod
    def _print_node(node, level=0, is_last=False) -> None:
        """
        Print the current node and its children in a hierarchical format.

        Args:
            node (Node): The node to print.
            level (int): The current depth level of the tree. Default is 0.
            is_last (bool): Indicates whether the node is the last child of its parent. Default is False.
        """
        # print the name and value (if any) of the current node
        prefix = "└" if is_last else "├"
        value_str = (
            f": {node._allocated_budget_amount}"
            if node._allocated_budget_amount is not None
            else ""
        )
        print(" " * level * 2 + prefix + "─ " + node._name + value_str)
        # recursively print the children nodes
        children_count = len(node._children)
        for i, child in enumerate(node._children):
            is_last_child = i == children_count - 1
            Node._print_node(child, level + 1, is_last_child)

    def to_dict(self):
        children = []
        for child in self.get_children():
            children.append(child.to_dict())

        node_dict = {
            "id": self.get_id(),
            "name": self.get_name(),
            "description": self.get_description(),
            "parent": self.get_parent_id(),
            "allocated_budget_amount": self.get_allocated_budget_amount(),
            "checked": self.checked,
            "children": children,
        }

        return node_dict

    def __str__(self):
        return f"id: {self._id} | name: {self._name}  | description: {self._description}\
            parent: {self._parent} | allocated_budget_amount: {self._allocated_budget_amount} | children: {self._children}"
