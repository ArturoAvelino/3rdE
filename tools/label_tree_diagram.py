import csv
import os
import networkx as nx
from collections import defaultdict


class TreeDiagramGenerator:
    def __init__(self, input_path, output_dir, output_filename, output_filename_tabs=None):
        self.input_path = input_path
        self.output_dir = output_dir
        self.output_filename = output_filename
        self.output_filename_tabs = output_filename_tabs
        self.nodes = {}  # Stores actual row data: id -> row_dict
        self.children_map = defaultdict(
            list) # Stores relationships: parent_id -> [child_ids]

    def _load_data(self):
        """Reads the CSV and builds the adjacency list."""
        if not os.path.exists(self.input_path):
            print(f"Error: The file {self.input_path} was not found.")
            return False

        try:
            with open(self.input_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    # Strip whitespace to be safe
                    row_id = row['id'].strip()
                    parent_id = row['parent_id'].strip() if row.get(
                        'parent_id') else None
                    name = row['name'].strip()

                    # Store node data
                    self.nodes[row_id] = {'name': name, 'parent_id': parent_id}

                    # Map parent to child
                    if parent_id:
                        self.children_map[parent_id].append(row_id)

        except KeyError as e:
            print(f"Error: Missing expected column in CSV: {e}")
            return False
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return False

        return True

    def _check_cycles(self):
        """Checks for cycles in the tree structure using NetworkX."""
        G = nx.DiGraph()
        for node_id, node_data in self.nodes.items():
            parent_id = node_data['parent_id']
            if parent_id and parent_id in self.nodes:
                # Edge from parent to child
                G.add_edge(parent_id, node_id)

        try:
            cycle = nx.find_cycle(G, orientation='original')
            print(f"Error: Cycle detected in the hierarchy! Cycle: {cycle}")
            return True
        except nx.NetworkXNoCycle:
            return False

    def _find_roots(self):
        """Identifies nodes that have no parent or whose parent is not in the dataset."""
        roots = []
        for node_id, node_data in self.nodes.items():
            parent_id = node_data['parent_id']
            # A node is a root if parent_id is None/Empty OR if the parent_id doesn't exist in our loaded nodes
            if not parent_id or parent_id not in self.nodes:
                roots.append(node_id)

        # Sort roots alphabetically for consistent output
        roots.sort(key=lambda x: self.nodes[x]['name'])
        return roots

    def _write_node_recursive(self, file_handle, node_id, prefix=""):
        """
        Recursive function to write the tree structure.

        Args:
            file_handle: Open file object to write to.
            node_id: Current node ID.
            prefix: The indentation string for the current level.
        """
        # Get children and sort them alphabetically
        children = self.children_map.get(node_id, [])
        children.sort(key=lambda x: self.nodes[x]['name'])

        count = len(children)
        for i, child_id in enumerate(children):
            is_last_child = (i == count - 1)
            child_name = self.nodes[child_id]['name']

            # Define the connector and the extension for the next level
            connector = "|---- "
            if is_last_child:
                extension = "      "
            else:
                extension = "|     "

            # Write the child line
            file_handle.write(f"{prefix}{connector}{child_name} ({child_id})\n")

            # Recursively write the child's subtree
            self._write_node_recursive(file_handle, child_id,
                                       prefix + extension)

            # Add the vertical spacing gap between siblings, connecting the lines
            if not is_last_child:
                # Only add spacing if the current child was a branch (had children)
                # This separates complex branches but keeps leaves compact
                if self.children_map.get(child_id):
                    file_handle.write(f"{prefix}|\n")

    def _write_node_recursive_tabs(self, file_handle, node_id, depth=0):
        """
        Recursive function to write the tree structure using 4-space tabs.

        Args:
            file_handle: Open file object to write to.
            node_id: Current node ID.
            depth: Current depth in the tree (starts at 0).
        """
        # Get children and sort them alphabetically
        children = self.children_map.get(node_id, [])
        children.sort(key=lambda x: self.nodes[x]['name'])

        # Indentation using 4 spaces per depth level (plus one level for current node relative to parent)
        # The root is at depth 0 (no indentation), children at depth 1 (4 spaces), etc.
        indent = "    " * depth

        for child_id in children:
            child_name = self.nodes[child_id]['name']

            # Write the child line with indentation
            file_handle.write(f"{indent}{child_name} ({child_id})\n")

            # Recursively write the child's subtree
            self._write_node_recursive_tabs(file_handle, child_id, depth + 1)

    def generate(self):
        """Main execution method."""
        print(f"Loading data from {self.input_path}...")
        if not self._load_data():
            return

        print("Checking for cycles...")
        if self._check_cycles():
            print("Generation aborted due to cycles.")
            return

        roots = self._find_roots()
        if not roots:
            print("No root nodes found. Check your parent_id logic.")
            return

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except OSError as e:
                print(f"Error creating directory {self.output_dir}: {e}")
                return

        full_output_path = os.path.join(self.output_dir, self.output_filename)

        try:
            # Generate the standard tree diagram (with pipes)
            with open(full_output_path, 'w', encoding='utf-8') as f:
                for i, root_id in enumerate(roots):
                    # Write root name
                    root_name = self.nodes[root_id]['name']
                    f.write(f"{root_name} ({root_id})\n")

                    # Recursively write children
                    self._write_node_recursive(f, root_id, prefix="")

                    # Add extra space between separate root trees if there are multiple
                    if i < len(roots) - 1:
                        f.write("\n\n")

            print(f"Success! Tree diagram generated at: {full_output_path}")

            # Generate the second diagram (with tabs) if filename provided
            if self.output_filename_tabs:
                full_output_path_tabs = os.path.join(self.output_dir, self.output_filename_tabs)
                with open(full_output_path_tabs, 'w', encoding='utf-8') as f:
                    for i, root_id in enumerate(roots):
                        # Write root name
                        root_name = self.nodes[root_id]['name']
                        f.write(f"{root_name} ({root_id})\n")

                        # Recursively write children using tabs logic
                        # Start indentation at 1 level deep (4 spaces) because root is level 0
                        self._write_node_recursive_tabs(f, root_id, depth=1)

                        # Add extra space between separate root trees if there are multiple
                        if i < len(roots) - 1:
                            f.write("\n") # Single newline for cleaner separation in tab mode

                print(f"Success! Tab-indented tree diagram generated at: {full_output_path_tabs}")

        except IOError as e:
            print(f"Error writing to file: {e}")

# Helper function to run the generator
def generate_tree_diagram(input_csv, output_dir, output_filename, output_filename_tabs=None):
    generator = TreeDiagramGenerator(input_csv, output_dir, output_filename, output_filename_tabs)
    generator.generate()

# ########################################################60
# Use example

# if __name__ == "__main__":
#     # Example usage
#     # You can change these paths to test locally
#     INPUT_FILE = 'input.csv'
#     OUTPUT_DIR = 'output_diagrams'
#     OUTPUT_FILE = 'tree_structure.txt'
#     OUTPUT_FILE_TABS = 'tree_structure_tabs.txt'

#     # Generate dummy file for testing if it doesn't exist
#     if not os.path.exists(INPUT_FILE):
#         print(f"Creating dummy input file: {INPUT_FILE}")
#         with open(INPUT_FILE, 'w', encoding='utf-8') as f:
#             f.write("id,name,parent_id,color,label_tree_id,source_id\n")
#             f.write("4491,Other Acari,4200,ce0f8f,6,\n")
#             f.write("4200,Acari,4199,2a74e4,6,\n")
#             f.write("4199,Arachnida,4198,31e475,6,\n")
#             f.write("4198,Metazoa,,c20ba9,6,\n")
#             f.write("4206,Crustacea,4198,c20ba9,6,\n")
#             f.write("4208,Myriapoda,4198,c20ba9,6,\n")
#             f.write("4201,Araneae +5mm,4199,31e475,6,\n")
#             f.write("4492,Mesostigmata (Gamase),4200,31e475,6,\n")
#             f.write("4208,Myriapoda,4198,c20ba9,6,\n")
#             f.write("4201,Araneae +5mm,4199,31e475,6,\n")
#             f.write("4492,Mesostigmata (Gamase),4200,31e475,6,\n")

#         generate_tree_diagram(INPUT_FILE, OUTPUT_DIR, OUTPUT_FILE, OUTPUT_FILE_TABS)

