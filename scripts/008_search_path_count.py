
# import sys
import os.path
import time
import fire
import configparser
import jsonlines
import networkx as nx
import lib.spc as spc
import psutil
import json


def do_spc(config=None,
             outfile=None,
             initems=None,
             inedgelist=None
             ):
    t0 = time.time()
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '008_search_path_count.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =========

    max_citation_net_nodes = conf.getint('main', 'max_citation_net_nodes')
    n_top_paths = conf.getint('main', 'n_top_paths');

    # =====================================================
    # load downloaded items
    file_path_items = f'{data_dir}/007_restricted_snowball_output.jsonl'

    if initems and os.path.isfile(initems):
        file_path_items = initems
    elif os.path.isfile(file_path_items):
        pass
    else:
        log(('snowballoutput not found',))
        return
    log(('infile', file_path_items))
    with jsonlines.open(file_path_items) as reader:
        items = {str(row['id']): row for row in reader}

    file_path_edge_list = f'{data_dir}/008_search_path_count_edge_list.edgelist'
    if inedgelist and inedgelist == 'resume':
        """
        read existing edge list
        """
        citation_net = nx.read_edgelist(file_path_edge_list, create_using=nx.DiGraph(), nodetype=str)
    elif inedgelist and os.path.isfile(inedgelist):
        """
        read existing edge list
        """
        citation_net = nx.read_edgelist(inedgelist, create_using=nx.DiGraph(), nodetype=str)
    else:
        """
        create and save edge list
        """
        citation_net = spc.create_citation_net(items)
        spc.add_source_and_target(citation_net)
        log(("raw network is connected = ", nx.is_connected(citation_net.to_undirected())))
        spc.remove_cycles(citation_net)
        spc.add_source_and_target(citation_net)
        log(("decycled network is connected = ", nx.is_connected(citation_net.to_undirected())))
        nx.write_edgelist(citation_net, file_path_edge_list)
    # =====================================================

    # =====================================================
    # place to store downloaded and selected item
    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/008_search_path_count_output.jsonl'
    log(('output', file_path_output))
    # =====================================================

    log(('len(citation_net.nodes())', len(citation_net.nodes())))
    log(("decycled network is connected = ", nx.is_connected(citation_net.to_undirected())))

    # calculate SPC weights
    spc_result = spc.spc(citation_net)
    edge_weights = spc_result['edge_weights']
    node_weights = spc_result['node_weights']

    # calculate SPC threshold
    sorted_weights = sorted(node_weights.values(), key=lambda x: -x )
    weight_min = sorted_weights[n_top_paths]
    log(("weight_min", weight_min))

    # select items that have large weights
    selected_item_ids = set([spc.__paper_of(str(nd)) for nd in node_weights if node_weights[spc.__paper_of(str(nd))] >= weight_min])
    ordered_items = sorted([ (node_weights[nd], nd) for nd in selected_item_ids ], reverse=True)

    # =========================================================================
    # save selected items
    log(('selected items', len(selected_item_ids)))
    with jsonlines.open(file_path_output, mode='a') as writer:
        for spc_weight, item_id in ordered_items:
            item_id = spc.__paper_of(str(item_id))
            if item_id in items:
                item = items[item_id]
                if item['year'] < 2010:
                    continue
                item['spc'] = spc_weight
                log(('id', item['id'], 'spc', item['spc'], 'year', item['year'], 'title', item['title']))
                writer.write(item)
    # /save selected items
    # =========================================================================
    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(do_spc)

