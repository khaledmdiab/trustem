from collections import defaultdict
import os
import sys
import mat
import numpy as np
import scipy.io as io

__author__ = 'Khaled Diab (kdiab@sfu.ca)'


EP_RATING = 'rating.mat'
EP_TRUST = 'trustnetwork.mat'


class DataGen:
    def __init__(self, r_file, t_file, uik=10, uuk=100):
        """uik=10 and uuk=100 will give user-item matrix of size 731x175 and user-user matrix of size 731x731"""
        self.rate_contents = mat.read(r_file)
        self.trust_contents = mat.read(t_file)
        self.uik = uik
        self.uuk = uuk
        self.users = None
        self.items = None
        self.ui_matrix = None
        self.uu_matrix = None

        self.rate_contents = self.rate_contents['rating']
        self.trust_contents = self.trust_contents['trustnetwork']

    def generate(self):
        self.users, self.items = self._get_users_items()
        users_index_map = {user_id: idx for idx, user_id in enumerate(self.users)}
        items_index_map = {item_id: idx for idx, item_id in enumerate(self.items)}
        self.ui_matrix = self._build_user_item_matrix(users_index_map, items_index_map)
        self.uu_matrix = self._build_user_user_matrix(users_index_map)

    def _get_users_items(self):
        print "Filtering Input Data ..."
        items_dict = defaultdict(int)
        trust_dict = defaultdict(int)

        for t_vector in self.trust_contents:
            trust_dict[t_vector[0]] += 1

        filtered_users = [k for k, x in trust_dict.iteritems() if x >= self.uuk]

        # tuple of (user id, item id, category id, rating value, helpfulness)
        for r_vector in self.rate_contents:
            if r_vector[0] in filtered_users:
                items_dict[r_vector[1]] += 1
        items = [item_id for item_id, rating_count in items_dict.iteritems() if rating_count >= self.uik]

        filtered_users.sort()
        items.sort()
        return filtered_users, items

    def _build_user_item_matrix(self, user_map, item_map):
        print "Building User Item Matrix ..."
        matrix = np.zeros((len(user_map), len(item_map)))
        for r_vector in self.rate_contents:
            user_id = r_vector[0]
            item_id = r_vector[1]
            if user_id in user_map and item_id in item_map:
                rating = r_vector[3]
                user_idx = user_map[user_id]
                item_idx = item_map[item_id]
                matrix[user_idx][item_idx] = rating
        return matrix

    def _build_user_user_matrix(self, user_map):
        print "Building User User Matrix ..."
        matrix = np.zeros((len(user_map), len(user_map)))
        for t_vector in self.trust_contents:
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

    generator = DataGen(rating_file, trust_file)
    generator.generate()
    # After generate, you get:
    # generator.users: User Ids list
    # generator.items: Item Ids list
    # generator.ui_matrix: User-Item Matrix
    # generator.uu_matrix: User-User Matrix

    print generator.ui_matrix.size, generator.uu_matrix.size

    # save to *.mat files
    # users_dict = {'users': s_users}
    # io.savemat("users", users_dict)
    # items_dict = {'items': s_items}
    # io.savemat("items", items_dict)
    # user_item_dict = {'user_item': ui_matrix}
    # io.savemat("user_item", user_item_dict)
    # user_user_dict = {'user_user': uu_matrix}
    # io.savemat("user_user", user_user_dict)



