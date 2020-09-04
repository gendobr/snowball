
# import sys
import os.path
import time
import fire
import configparser
import jsonlines
import networkx as nx
import lib.spc as spc


def do_spc(config=None,
             outfile=None,
             initems=None,
             inedgelist=None
             ):
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
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
        print(('snowballoutput not found'))
        return
    print(('infile', file_path_items))
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
        print(("raw network is connected = ", nx.is_connected(citation_net.to_undirected())))
        spc.remove_cycles(citation_net)
        spc.add_source_and_target(citation_net)
        print("decycled network is connected = ", nx.is_connected(citation_net.to_undirected()))
        nx.write_edgelist(citation_net, file_path_edge_list)
    # =====================================================

    # =====================================================
    # place to store downloaded and selected item
    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/008_search_path_count_output.jsonl'
    print(('output', file_path_output))
    # =====================================================

    print(('len(citation_net.nodes())', len(citation_net.nodes())))
    print("decycled network is connected = ", nx.is_connected(citation_net.to_undirected()))

    # calculate SPC weights
    spc_result = spc.spc(citation_net)
    edge_weights = spc_result['edge_weights']
    node_weights = spc_result['node_weights']

    # calculate SPC threshold
    sorted_weights = sorted(node_weights.values(), key=lambda x: -x )
    weight_min = sorted_weights[n_top_paths]
    print("weight_min=", weight_min)

    # select items that have large weights
    selected_item_ids = set([spc.__paper_of(str(nd)) for nd in node_weights if node_weights[spc.__paper_of(str(nd))] >= weight_min])
    ordered_items = sorted([ (node_weights[nd], nd) for nd in selected_item_ids ], reverse=True)

    # =========================================================================
    # save selected items
    print(('selected items', len(selected_item_ids)))
    with jsonlines.open(file_path_output, mode='a') as writer:
        for spc_weight, item_id in ordered_items:
            item_id = spc.__paper_of(str(item_id))
            if item_id in items:
                item = items[item_id]
                if item['year'] < 2010:
                    continue
                item['spc'] = spc_weight
                print(('id', item['id'], 'spc', item['spc'], 'year', item['year'], 'title', item['title']))
                writer.write(item)
    # /save selected items
    # =========================================================================
    return
    #
    # # =========================================================================
    # # do main path analysis
    # edge_distances = {}
    # for ed in edge_weights:
    #     edge_distances[(ed[0], ed[1])] = 1.0 / ed[2]
    #
    # def distance_measure(x, y):
    #     return edge_distances[(x, y)] if (x, y) in edge_distances else 100
    #
    # reading_plan = set()
    # weighted_paths = list()
    # for item_id in selected_item_ids:
    #     path_1 = nx.astar_path(citation_net, 's', str(item_id), distance_measure)
    #     path_2 = nx.astar_path(citation_net, str(item_id), 't', distance_measure)
    #     path_1.extend(path_2[1:])
    #     reading_plan.update(path_1)
    #     path_weight = sum([distance_measure(path_1[i-1], path_1[i]) for i in range(1, len(path_1))])
    #     weighted_paths.append((path_weight, path_1,))
    #     # print((path_weight, path_1,))
    #
    # print('main path')
    # # print(nx.astar_path(citation_net, 's', 't', distance_measure))
    # print(sorted(weighted_paths))
    #
    # print('reading_plan')
    # print(reading_plan)
    #
    # # =========================================================================
    #
    # # =========================================================================
    # # save selected items
    # print('selected items')
    # with jsonlines.open(file_path_output, mode='a') as writer:
    #     for item_id in items:
    #         item_id = spc.__paper_of(str(item_id))
    #         item = items[item_id]
    #         if item_id in reading_plan:
    #             item['spc'] = node_weights[item_id]
    #             print(('id', item['id'], 'spc', item['spc'], 'year', item['year'], 'title', item['title']))
    #             writer.write(item)
    # # /save selected items
    # # =========================================================================


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_spc)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
