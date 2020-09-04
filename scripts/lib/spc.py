import networkx as nx
import pandas as pd
import time
import jsonlines


def remove_cycles(citation_net):
    t0 = time.time()
    # remove cycles
    n_cycles = 0
    ccl = True
    while ccl:
        try:
            ccl = nx.find_cycle(citation_net, orientation='original')
            n_cycles = n_cycles + 1
        except:
            ccl = False
            break

        cycle = set()
        for p in ccl:
            cycle.add(p[0])
            cycle.add(p[1])
        print('cycle #', n_cycles, "time=", time.time() - t0)
        print(cycle)
        cycle = list(cycle)

        # remove edges inside cycle
        if len(cycle) == 1:
            citation_net.remove_edge(cycle[0], cycle[0])
            continue

        # transform
        for x in cycle:
            out_edges = list(citation_net.out_edges(nbunch=[x]))

            for out_edge in out_edges:
                y = out_edge[1]
                if __is_paper(x) and __is_preprint(y):
                    pass
                elif __is_paper(x) and __is_paper(y) and y in cycle:
                    citation_net.remove_edge(x, y)
                    f, t = x,  __preprint_of(y)
                    if not citation_net.has_edge(f, t):
                        citation_net.add_edge(f, t)
                elif __is_paper(x) and __is_paper(y) and y not in cycle:
                    citation_net.remove_edge(x, y)
                    f, t = __preprint_of(x), y
                    if not citation_net.has_edge(f, t):
                        citation_net.add_edge(f, t)
                elif __is_preprint(x) and __is_preprint(y):
                    citation_net.remove_edge(x, y)
                    f, t = __paper_of(x), y
                    if not citation_net.has_edge(f, t):
                        citation_net.add_edge(f, t)
                elif __is_preprint(x) and __is_paper(y) and y in cycle:
                    citation_net.remove_edge(x, y)
                    f, t = __paper_of(x), __preprint_of(y)
                    if not citation_net.has_edge(f, t):
                        citation_net.add_edge(f, t)
                elif __is_preprint(x) and __is_paper(y) and y not in cycle:
                    pass
            if not citation_net.has_edge(__paper_of(x), __preprint_of(x)):
                citation_net.add_edge(__paper_of(x), __preprint_of(x))


def spc(citation_net):

    # get list of all nodes
    n_minus = {}
    n_plus = {}
    for nd in citation_net.nodes():
        n_minus[nd] = -1
        n_plus[nd] = -1

    # calculate n_minus[node]
    n_minus['s'] = 1
    n_updates = 1
    while n_updates > 0:
        n_updates = 0
        for nd in n_minus:
            if n_minus[nd] < 0:
                in_edges = [n_minus[ed] for (ed, _) in list(citation_net.in_edges([nd]))]
                # print "in_edges=", nd, [ed for (ed, _) in list(citation_net.in_edges([nd]))]
                if in_edges and min(in_edges) > 0:
                    # print "updated\n\n"
                    # print "in_edges=", nd, in_edges
                    n_updates += 1
                    n_minus[nd] = sum(in_edges)
        print("n_updates=", n_updates)
    # print  "n_minus=", n_minus
    # return

    # calculate n_plus[node]
    n_plus['t'] = 1
    n_updates = 1
    while n_updates > 0:
        n_updates = 0
        for nd in n_plus:
            if n_plus[nd] < 0:
                out_edges = [n_plus[ed] for (_, ed) in list(citation_net.out_edges([nd]))]
                # print "out_edges=", nd, [ed for (ed, _) in list(citation_net.out_edges([nd]))]
                if out_edges and min(out_edges) > 0:
                    # print "updated\n\n"
                    n_updates += 1
                    n_plus[nd] = sum(out_edges)
        print("n_updates=", n_updates)
    # print  "n_plus=", n_plus
    # print list(citation_net.out_edges(['s']))

    citation_net_flow = float(n_plus['s'] * n_minus['t'])
    print("citation_net_flow=", citation_net_flow)

    # for nd in n_plus:
    #     if n_plus[nd] < 0 or n_minus[nd] < 0:
    #         citation_net.remove_node(nd)

    # print "n_nodes=", len(citation_net.nodes())
    # print "edges=", citation_net.edges()
    # print("network is connected = ", nx.is_connected(citation_net.to_undirected()))

    # calculate edge weights
    all_edges = citation_net.edges()
    edge_weights = []
    for ed in all_edges:
        evg = (ed[0], ed[1], n_minus[ed[0]] * n_plus[ed[1]])
        # print evg
        edge_weights.append(evg)

    # sorted_edge_weights = sorted(edge_weights, cmp=lambda x, y: (1 if y[2]>x[2] else -1) )
    # print edge_weights

    # wmin = sorted_edge_weights[n_top_paths][2]
    # selected_edges = [ed for ed in sorted_edge_weights if ed[2] >= wmin]
    # print "wmin=", wmin  # , " len(selected_edges)=", len(selected_edges) #, selected_edges

    node_weighs = {}

    for ed in edge_weights:
        if ed[0] not in node_weighs:
            node_weighs[ed[0]] = 0

        node_weighs[ed[0]] += ed[2]

        if ed[1] not in node_weighs:
            node_weighs[ed[1]] = 0

        node_weighs[ed[1]] += ed[2]

    max_weight = float(max(node_weighs.values()))
    for nd in node_weighs:
        node_weighs[nd] = node_weighs[nd] / max_weight
    return {
        'node_weights': node_weighs,
        'edge_weights': edge_weights
    }


def create_citation_net(items):

    item_ids = list(items.keys())

    citation_net = nx.DiGraph()

    for item_id in item_ids:
        item = items[item_id]
        node_1 = str(item['id'])
        if item['referenced_by'] and len(item['referenced_by']):
            for ref_id in item['referenced_by']:
                node_2 = str(ref_id)
                if node_2 in items:
                    citation_net.add_edge(node_2, node_1)
        if item['references_to'] and len(item['references_to']):
            for ref_id in item['references_to']:
                node_2 = str(ref_id)
                if node_2 in items:
                    citation_net.add_edge(node_1, node_2)
        # print i,node_1

    return citation_net


def add_source_and_target(citation_net):
    s_nodes = list(citation_net.nodes())
    for nd in list(s_nodes):
        # print "node ", nd
        # get nodes having zero in_degree and connect them to source node (id=s)
        if len(citation_net.in_edges(nbunch=[nd])) == 0:
            # print "add edge s->", nd
            citation_net.add_edge('s', nd)

        # get nodes having zero out_degree and connect them to target node (id=t)
        if len(citation_net.out_edges(nbunch=[nd])) == 0:
            # print "add edge ", nd, "->t"
            citation_net.add_edge(nd, 't')


def __is_paper(node_id):
    return str(node_id)[-2:] != '.p'


def __is_preprint(node_id):
    return str(node_id)[-2:] == '.p'


def __paper_of(node_id):
    if __is_preprint(node_id):
        return str(node_id)[:-2]
    return str(node_id)


def __preprint_of(node_id):
    if __is_preprint(node_id):
        return node_id
    return str(node_id) + '.p'



# import matplotlib.pyplot as plt
# citation_net = nx.DiGraph()
#
# citation_net.add_edge('n1', 'n2')
# citation_net.add_edge('n2', 'n1')
#
# citation_net.add_edge('n1', 'n2')
# citation_net.add_edge('n2', 'n1')
# citation_net.add_edge('n3', 'n2')
# citation_net.add_edge('n2', 'n3')
#
# citation_net.add_edge('n1', 'n2')
# citation_net.add_edge('n2', 'n1')
# citation_net.add_edge('n3', 'n1')
# citation_net.add_edge('n3', 'n2')
# citation_net.add_edge('n2', 'n4')
# citation_net.add_edge('n1', 'n4')
# #
# nx.draw(citation_net, with_labels=True, pos=nx.spring_layout(citation_net))
# plt.draw()
# plt.show()
# # #
# remove_cycles(citation_net)
# nx.draw(citation_net, with_labels=True, pos=nx.spring_layout(citation_net))
# plt.draw()
# plt.show()
# exit()
