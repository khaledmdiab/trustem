from collections import defaultdict
import os
import sys
import mat
import numpy as np
import scipy.io as io

__author__ = 'Khaled Diab (kdiab@sfu.ca)'


EP_RATING = 'rating.mat'
EP_TRUST = 'trustnetwork.mat'


def get_users_items_vectors(rate_content, trust_content):
    # tuple of (user id, item id, category id, rating value, helpfulness)
    rating = rate_content['rating']
    # tuple (user1 trusts user2)
    trust = trust_content['trustnetwork']

    users_set = set()
    items_set = set()

    for t_vector in trust:
        for idx in [0, 1]:
            users_set.add(t_vector[idx])

    for r_vector in rating:
        items_set.add(r_vector[1])

    return np.array(sorted(list(users_set))), np.array(sorted(list(items_set)))


def get_users_items(rating, k=100):
    print "Filtering Input Data ..."
    items_dict = defaultdict(int)

    # tuple of (user id, item id, category id, rating value, helpfulness)
    for r_vector in rating:
        items_dict[r_vector[1]] += 1

    items = [item_id for item_id, rating_count in items_dict.iteritems() if rating_count >= k]
    items.sort()
    users = []
    for r_vector in rating:
        user_id = r_vector[0]
        item_id = r_vector[1]
        if item_id in items and not user_id in users:
            users.append(user_id)
    users.sort()
    return users, items


def build_user_item_matrix(user_map, item_map, rating):
    print "Building User Item Matrix ..."
    matrix = np.zeros((len(user_map), len(item_map)))
    for r_vector in rating:
        user_id = r_vector[0]
        item_id = r_vector[1]
        if user_id in user_map and item_id in item_map:
            rating = r_vector[3]
            user_idx = user_map[user_id]
            item_idx = item_map[item_id]
            matrix[user_idx][item_idx] = rating
    return matrix


def build_user_user_matrix(user_map, trust):
    print "Building User User Matrix ..."
    matrix = np.zeros((len(user_map), len(user_map)))
    for t_vector in trust:
        user1_id = t_vector[0]
        user2_id = t_vector[1]
        if user1_id in user_map and user2_id in user_map:
            user1_idx = user_map[user1_id]
            user2_idx = user_map[user2_id]
            matrix[user1_idx][user2_idx] = 1
    return matrix

if __name__ == '__main__':
    args = sys.argv
    if not len(args) == 2:
        print 'Usage: gen.py <input_data_directory>'
        exit(0)

    ip_dir = args[1]

    rating_file = os.path.join(ip_dir, EP_RATING)
    trust_file = os.path.join(ip_dir, EP_TRUST)

    rate_contents = mat.read(rating_file)
    trust_contents = mat.read(trust_file)

    # users, items = get_users_items_vectors(rate_contents, trust_contents)
    s_users, s_items = get_users_items(rate_contents['rating'])
    users_index_map = {user_id: idx for idx, user_id in enumerate(s_users)}
    items_index_map = {item_id: idx for idx, item_id in enumerate(s_items)}
    ui_matrix = build_user_item_matrix(users_index_map, items_index_map, rate_contents['rating'])
    uu_matrix = build_user_user_matrix(users_index_map, trust_contents['trustnetwork'])

    # save to *.mat files
    users_dict = {'users': s_users}
    io.savemat("users", users_dict)
    items_dict = {'items': s_items}
    io.savemat("items", items_dict)
    user_item_dict = {'user_item': ui_matrix}
    io.savemat("user_item", user_item_dict)
    user_user_dict = {'user_user': uu_matrix}
    io.savemat("user_user", user_user_dict)



