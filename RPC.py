"""
Minerva - RPC for POX Controller
Resilient Path Computation
"""

import numpy
import copy
#import os
#import datetime
#import time
#import traceback
#from service_thread import ServiceThread

def get_time_now():
    return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''


class RPF():

    flows = 3

    def get_potential_paths(self, src_dpid, dst_dpid, matrix, path=list(), result=list()):
        """
        Find all those candidate paths that might have a resilient path from source to destination
        Old get_resilient_path
        """
        current_path = copy.deepcopy(path)
        current_path.append(dst_dpid)

        if dst_dpid == src_dpid:
            return current_path

        if matrix.max() == 0:
            return None

        dst_array = self.__get_dpid_array(dst_dpid, len(matrix))
        neo_matrix = copy.deepcopy(matrix)
        neo_matrix[dst_dpid - 1].fill(0)
        candidates = self.__get_candidates_to_dst(dst_array, matrix)

        for candidate in candidates:
            circuit = self.get_potential_paths(src_dpid, candidate, neo_matrix, current_path)
            if circuit:
                result.append(circuit)

        return result


    def __get_dpid_array(self, dpid_num, length):
        dpid = list("0" * length)
        dpid_array = numpy.array(dpid, dtype=int)
        dpid_array.put(dpid_num - 1, 1)
        return dpid_array


    def __get_candidates_to_dst(self, dst, matrix):

        #TODO:
        result = (matrix * numpy.matrix(numpy.matrix(dst)).T).T     #Formats the matrix as list
        candidates = list()
        i = 0

        for value in result.tolist()[0]:     #In numpy notation
            if value == 1:
                candidates.append(i + 1)
            i += 1

        return candidates


    def find_places_for_nfs(self, resilient_paths, n_flows, used_nodes=list()):
        required_nf_pairs = n_flows - len(resilient_paths)

        if required_nf_pairs == 0:
            return True

        all_nodes = list()
        r_paths = copy.deepcopy(resilient_paths)

        for r in r_paths:
            all_nodes.extend(r)
        candidates = list()

        for r in all_nodes:
           i = all_nodes.count(r)
           if i >= 2 and r not in candidates and r not in used_nodes:
               candidates.append(r)

        if len(candidates) >= 2:
            return min(candidates), max(candidates)

        elif len(candidates) == 1:
            return candidates[0]

        else:
            return None


    def generate_adjacency_vector(self, array, length):
        empty_array = list("0" * length)
        adj_array = numpy.array(empty_array, dtype=int)

        for i in array:
            adj_array.put(i-1, 1)

        return adj_array.tolist()


    def get_orthogonal_vectors(self, mat, n_flows):
        print "- Get Orthogonal Vectors Method -"
        print "Init Mat: ", mat
        orthogonal_map = mat.dot(mat.T)
        orthogonal_vector_list = list()
        print "Orthogonal map: ", orthogonal_map
        orthogonal_map = orthogonal_map.T       #Transposed for easy vector indexing
        print "ORTHOGONAL MAP Transposed: ", orthogonal_map

        for row in orthogonal_map:
            if row.sum() == 0:
                orthogonal_vector_list.append(-1)       #zeroed vectors must be treated specially
                continue

            orthogonal_vector_list.append(row.tolist()[0].count(0))

        print "ORTHOGONAL_VECTOR_LIST: ", orthogonal_vector_list
        max_orthogonal_vectors = max(orthogonal_vector_list)
        best_row = orthogonal_map[orthogonal_vector_list.index(max_orthogonal_vectors)]
        src_vector = orthogonal_vector_list.index(max_orthogonal_vectors)
        print "BEST_ROW: ", best_row
        indexes = list()
        best_row = best_row.tolist()[0]

        for i in range(0, len(best_row)):
            if best_row[i] == 0:
                indexes.append(i)

        indexes.insert(src_vector,src_vector)
        result = list()
        print "Indexes: ", indexes

        for i in indexes:
           result.append(mat[i].tolist()[0])

        return result[0:n_flows]


def main(topology, src, dst, n_flows):
    """
    Main RPF algorithm process; Needed Inputs are:
    - Network topology ()
    - End points (src and dst)
    - Number of resilience flows (tipically flows=3: A, B, AxB)
    """
    resilient = RPF()

    #TODO:
    #Network topology should be retrieved from controller and parsed in next format

    dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
            2: {1: 1, 3: 3, 4: 4, 5: 5},
            3: {1: 1, 2: 2, 4: 4, 5: 5},
            4: {1: 1, 2: 2, 3: 3, 5: 5},
            5: {1: 1, 2: 2, 3: 3, 4: 4}, }

    arrays = list()

    for key in dpids.keys():

        conn_row = dpids[key].keys()
        conn_row.sort()
        conn_row_array = numpy.array(conn_row)
        conn_row_array = conn_row_array/conn_row_array
        conn_row = conn_row_array.tolist()
        conn_row.insert((key-1), 0)
        arrays.append(numpy.array(conn_row))

    #TODO:
    #Retrieved topology must be converted into numpy.arrays -> numpy.matrix

    a2 = numpy.array([0, 1, 1, 0])
    b2 = numpy.array([1, 0, 0, 1])
    c2 = numpy.array([1, 0, 0, 1])
    d2 = numpy.array([0, 1, 1, 0])
    #e2 = numpy.array([1, 1, 1, 1, 0])

    #matrix2 = numpy.matrix([a2,b2,c2,d2,e2,f2,g2])
    matrix2 = numpy.matrix([a2, b2, c2, d2])
    src_dpid2 = 1
    dst_dpid2 = 4
    #dst_dpid2 = 7

    result = resilient.get_potential_paths(src_dpid2, dst_dpid2, matrix2)
    final = list()

    for r in result:
        if type(r[0]) == list:
            continue
        final.append(r)

    flows = resilient.flows

    print "final:", final
    len3 = list()
    for i in final:
        if len(i) == 3:
            len3.append(i)
    print len3

    import pprint

    array_list = list()
    for i in final:
        array_list.append(resilient.generate_adjacency_vector(i, 4))

    print "Array_List: ", array_list
    array_list_2 = list()

    for i in array_list:
        while array_list.count(i) > 1:
            array_list.remove(i)

    for i in array_list:
        array_list_2.append(i[1:len(i)-1])

    pprint.pprint(array_list)
    pprint.pprint(array_list_2)
    mat = numpy.matrix(array_list_2)

    final_result = list
    orthogonal_vectors = resilient.get_orthogonal_vectors(mat, 3)
    splitter, merger = resilient.find_places_for_nfs(orthogonal_vectors, 3)

    if splitter and not merger:
        merger = 4
    elif not splitter and not merger:
        merger = 4
        splitter = 1

    for ov in orthogonal_vectors:
        ov.insert(0, src_dpid2)
        ov.append(dst_dpid2)

    if len(orthogonal_vectors) == flows:
        print "The calculate result was that the paths to be taken are: ", paths
    else:
        print "Not enough resilient paths calculated, there should be a splitter on node %d and a merger on %d" %(splitter,merger)

    print "ORTHOGONAL_VECTORS: ", orthogonal_vectors


################################################
if __name__ == "__main__":
    main(None, None, None, None)


