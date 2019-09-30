import requests
import sys
import time
import json


class VkUser:
    def __init__(self, user_id=None):
        self.access_token = 'token_here'
        self.user_id = user_id

    def get_user_id(self):
        if self.user_id is None:
            self.user_id = input('Введите UserID: \n')
        u_init_params = {
            'user_ids': str(self.user_id),
            'fields': 'screen_name,user_id',
            'access_token': self.access_token,
            'v': 5.101
        }
        time.sleep(0.32)
        u_init_resp = requests.get(
            'https://api.vk.com/method/users.get',
            params=u_init_params
        )
        user_dict = u_init_resp.json()
        if user_dict['response'][0].get('deactivated') == 'deleted':
            print('\nСтраница пользователя удалена')
            sys.exit()
        user_id = (user_dict['response'][0]['id'])
        return user_id

    def __str__(self):
        return f'https://vk.com/id{self.get_user_id()}'

    def get_friends_list(self):
        time.sleep(0.32)
        gf_params = {
            'user_id': self.get_user_id(),
            'access_token': self.access_token,
            'v': 5.101
        }
        gf_resp = requests.get(
            'https://api.vk.com/method/friends.get',
            params=gf_params,
        )
        gf_dict = gf_resp.json()
        gf_list = []
        for friend in gf_dict['response']['items']:
            gf_list.append(friend)
        return gf_list

    def __repr__(self):
        return f'VkUser_{self.user_id}'

    def __and__(self, other):
        self_set = set(self.get_friends_list())
        other_set = set(other.get_friends_list())
        intersection = self_set & other_set
        int_list = []
        for item in intersection:
            item = VkUser(item)
            int_list.append(item)
        return int_list

    def get_mutual_friends(self, target_id):
        time.sleep(0.32)
        mf_params = {
            'source_uid': self.get_user_id(),
            'target_uid': target_id,
            'access_token': self.access_token,
            'v': 5.101
        }
        mf_response = requests.get(
            'https://api.vk.com/method/friends.getMutual',
            params=mf_params
        )
        mf_dict = mf_response.json()
        mf_list = []
        for friend in mf_dict['response']:
            friend = VkUser(friend)
            mf_list.append(friend)
        return mf_list


if __name__ == "__main__":
    lokkjo = VkUser(50392257)
    dan = VkUser(134187014)

    print('\nЗадача 1\n')
    print(lokkjo.get_mutual_friends(134187014))

    print('\nЗадача 2\n')
    print(lokkjo & dan)

    print('\nЗадача 3\n')
    print(lokkjo)
    print(dan)
