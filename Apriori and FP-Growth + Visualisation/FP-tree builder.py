# "UniqueDotExporter" requires Graphviz program to be installed.

from anytree import NodeMixin, RenderTree
from anytree.exporter import UniqueDotExporter

class FpNode(NodeMixin):
    """Nodes of the fp-tree."""

    def __init__(self, name, path_to_root:str=None, parent=None, link=None, count=1):
        super().__init__()
        self.count = count
        self.name = name
        self.parent = parent
        self.path_to_root = path_to_root
        self.link = link

class  FpTree:
    """Generate Fp-tree for 10 items."""

    def __init__(self):
        self.tree_nodes = {}

        self.last_nodes = {"Перекись-водорода": FpNode("Head-0", "Head-0"), "Пластырь": FpNode("Head-1", "Head-1"),
                           "Активированный-уголь": FpNode("Head-2", "Head-2"), "Зеленка": FpNode("Head-3", "Head-3"),
                           "Цитрамон": FpNode("Head-4", "Head-4"), "Вата": FpNode("Head-5", "Head-5"),
                           "Шприц": FpNode("Head-6", "Head-6"), "Спирт": FpNode("Head-7", "Head-7")}

    def build(self, parent_node, further_items: dict, path_to_root: str = "R"):
        """Build the Fp-tree with nodes and save its structure in tree_nodes dict."""

        cur_item = list(further_items)[0]
        path_to_root += cur_item

        if path_to_root not in self.tree_nodes:
            cur_node = FpNode(cur_item, path_to_root, parent_node,
                              None, further_items[cur_item])

            self.last_nodes[cur_item].link = cur_node
            self.last_nodes[cur_item] = cur_node
            self.tree_nodes[path_to_root] = cur_node

            if len(further_items) != 1:
                self.build(cur_node, dict(list(further_items.items())[1:]), path_to_root)

        else:
            cur_node = self.tree_nodes[path_to_root]
            cur_node.count += 1

            if len(further_items) != 1:
                self.build(cur_node, dict(list(further_items.items())[1:]), path_to_root)
        
    def print_nodes_on_terminal(self):
        """Print each node of the fp-tree on terminal."""

        for node_path, node in self.tree_nodes.items():
            if node.link:
                link_p = node.link.path_to_root
            else:
                link_p = "None"
            print(f"Path: {node_path} | Node: {node.name} | Parent: {node.parent.name} | "
            f"link: {link_p} | Count: {node.count}")

    def save_ascii_tree(self, root_node):
        """Save fp-tree structure graph in ASCII format."""

        with open("fp-tree-ascii-graph.txt","w", encoding='utf8') as outfile:
            for pre, _, node in RenderTree(root_node):
                if node.name == "root":
                    treestr = f"{pre}{node.name}: {node.count}"
                else:
                    if node.link:
                        link_p = node.link.path_to_root
                    else:
                        link_p = "None"
                    treestr = f"{pre}{node.name}: {node.count} (Link={link_p})"
                outfile.write(treestr.ljust(8)+'\n')

        print("-----------------------------------------\n"
        "Tree saved in fp-tree-ascii-graph.txt")

    def save_visual_tree(self, root_node):
        """Save fp-tree structure graph in visual format."""

        UniqueDotExporter(
        root_node,
        nodeattrfunc=lambda node: "shape=box",
        graph="graph",
        edgetypefunc=lambda node,child: "--",
        nodenamefunc=lambda n: f"'{n.name}': {n.count}\n({n.path_to_root})"
        ).to_picture("fp-tree-visual-graph.png")

        print("-----------------------------------------\n"
        "Tree saved in fp-tree-visual-graph.png")


def count_item_freq(input_file_name: str, min_sup: int) -> dict:
    """First scan: Create sorted items frequency with min sup"""

    itms = ['Перекись-водорода','Пластырь','Активированный-уголь','Зеленка','Цитрамон','Вата',
                'Шприц','Спирт']

    items = {"Перекись-водорода": 0, "Пластырь": 0, "Активированный-уголь": 0, "Зеленка": 0, "Цитрамон": 0, "Вата": 0, 
    "Шприц": 0, "Спирт": 0}
    with open(input_file_name,"r") as dataset:
        for record in dataset:
            for item in record.strip('\n').split(','):
                if item in itms:
                    items[item] += 1

    sorted_items = sorted(items.items(), key= lambda x: x[1], reverse=True)
    return {k: v for k, v in sorted_items if v >= min_sup}


def main():
    """Initiate the tree and run the program"""

    MIN_SUP = 1
    dataset_file_name = "pharmacy_busket.csv"
    item_freq_list = count_item_freq(dataset_file_name, MIN_SUP)  # First Scan

    tree = FpTree()
    root_node = FpNode("root")
    # freq = "".join(list(item_freq_list.keys()))
    freq = list(item_freq_list.keys())

    with open(dataset_file_name,"r") as dataset:  # Second Scan
        for record in dataset:
            node_path = {}
            record = record.strip('\n').split(',')
            for item in freq:
                if item in record:
                    node_path[item] = record.count(item)
            if len(node_path) != 0:
                tree.build(root_node, node_path)

    tree.print_nodes_on_terminal()
    tree.save_ascii_tree(root_node)
    tree.save_visual_tree(root_node)

    print("-----------------------------------------")
    print(f"Items frequent list (ordered) (MIN_SUP={MIN_SUP}):\n{item_freq_list}")

if __name__ == "__main__":
    main()