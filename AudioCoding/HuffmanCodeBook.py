#from https://gist.github.com/jasonrdsouza/1c9c895f43497d15eb2e

import collections
Counter=collections.Counter()
from Queue import PriorityQueue

def huffman(symbol_list):
    #find the frequency of each symbol appearance
    counts = collections.Counter(symbol_list).most_common()
    total = len(symbol_list)
    queue = PriorityQueue()
    for (val,count) in counts:
        queue.put((count, val))
    largest_node_count = 0
    # Create the Huffman tree
    while total != largest_node_count:
        node1 = queue.get_nowait()
        node2 = queue.get_nowait()

        
        new_count = node1[0] + node2[0]
        largest_node_count = new_count if new_count > largest_node_count else largest_node_count
        queue.put((new_count, (node1,node2)))
    huffman_tree_root = queue.get(False)
    
    # generate the symbol to huffman code mapping
    lookup_table = huffman_tree_to_table(huffman_tree_root, "", {})
    return lookup_table

def huffman_tree_to_table(root, prefix, lookup_table):
    """Converts the Huffman tree rooted at "root" to a lookup table"""
    if type(root[1]) != tuple:
        # leaf node
        lookup_table[root[1]] = prefix
    else:
        huffman_tree_to_table(root[1][0], prefix + "0", lookup_table)
        huffman_tree_to_table(root[1][1], prefix + "1", lookup_table)
    return lookup_table
