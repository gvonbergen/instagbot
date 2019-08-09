"""
This is the main runner for igbot
"""

import argparse
from typing import Dict

import gspread
import random

from instapy import InstaPy
from instapy import set_workspace
from oauth2client.service_account import ServiceAccountCredentials


def gspread_auth(key):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
    return gspread.authorize(creds)

def serialize_from_string(entry: str, data_type: str) -> (int, str, bool):
    if data_type == 'int':
        return int(entry)
    elif data_type == 'bool':
        return bool(entry)
    else: # assume it is already string
        return entry

def dict_remove_empty_entries(dictionary: Dict) -> Dict:
    return {k: v for k, v in dictionary.items() if v}

def parse_arguments():
    parser = argparse.ArgumentParser(description='GDocs usage for Instapy')
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('--authkey', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sheet')
    group.add_argument('--sheet-key')
    group.add_argument('--sheet-url')
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--like-locations')
    parser.add_argument('--like-users')
    parser.add_argument('--like-tags')
    parser.add_argument('--interact-followers')
    return parser.parse_args()


class InstaGBot:
    def __init__(self, args, settings=None):
        self.spreadsheet = args.sheet or args.sheet_key or args.sheet_url
        self.gclient = gspread_auth(args.authkey)
        self.settings_tab = 'settings' or settings
        self.settings = self.load_settings(self.settings_tab)
        self.ip = None

    def sheet(self, worksheet):
        if args.sheet:
            document = self.gclient.open(self.spreadsheet)
        elif args.sheet_key:
            document = self.gclient.open_by_key(self.spreadsheet)
        elif args.sheet_url:
            document = self.gclient.open_by_url(self.spreadsheet)
        else:
            document = None
            raise()
        wks = document.worksheet(worksheet)
        return wks

    def load_settings(self, settings_tab):
        wks = self.sheet(settings_tab)
        sheet_entries = wks.get_all_values()
        settings = {}
        for entry in sheet_entries[1:]:
            k = entry[0]
            v = serialize_from_string(entry[1], entry[2])
            settings.update({k: v})
        settings = dict_remove_empty_entries(settings)
        return settings

    def get_rows(self, worksheet, row=1):
        wks = self.sheet(worksheet)
        values = wks.row_values(row)
        return values

    def get_cols(self, worksheet, col=1):
        wks = self.sheet(worksheet)
        values = wks.col_values(col)
        random.shuffle(values)
        return values

    def get_all_values(self, worksheet):
        wks = self.sheet(worksheet)
        values = wks.get_all_values()
        return values

    def settings_get_value(self, key):
        wks = self.sheet(self.settings_tab)
        cell = wks.find(key)
        value = wks.cell(cell.row, cell.col + 1).value
        return value

    def setup(self, args):
        set_workspace(path=args.workspace)
        self.ip = InstaPy(username=args.user,
                          password=args.password,
                          headless_browser=True)
        # set_sleep_reduce

        # set_action_delays

        # set_do_comment

        # set_comments

        # set_do_follow

        # set_do_like
        self.ip.set_do_like(enabled=self.settings['set_do_like_enabled'],
                            percentage=self.settings['set_do_like_percentage'])

        # set_dont_like

        # set_mandatory_words

        # set_user_interact
        self.ip.set_user_interact(amount=self.settings['set_user_interact_amount'],
                                  percentage=self.settings['set_user_interact_percentage'],
                                  randomize=self.settings['set_user_interact_randomize'],
                                  media=self.settings['set_user_interact_media'])

        # set_ignore_users

        # set_ignore_if_contains

        # set_dont_include

        # set_use_clarifai

        # set_smart_hashtags

        # set_smart_location_hashtags

        # set_mandatory_language

        # clarifai_check_img_for

        # set_relationship_bounds

        # set_skip_users

        # set_delimit_liking

        # set_delimit_commenting

        # set_simulation
        self.ip.set_simulation(enabled=False)

        # set_dont_unfollow_active_users

        # set_blacklist
        self.ip.set_quota_supervisor(enabled=self.settings['set_quota_supervisor_enabled'],
                                     peak_likes=(self.settings['set_quota_supervisor_likes_hour'],
                                                 self.settings['set_quota_supervisor_likes_day']),
                                     sleep_after=[self.settings['set_quota_supervisor_sleepafter']],
                                     stochastic_flow=self.settings['set_quota_supervisor_stochflow'])

        # set_do_reply_to_comments

        # set_comment_replies

        # set_use_meaningcloud

        # set_use_yandex

if __name__ == '__main__':

    args = parse_arguments()
    print(args)

    bot = InstaGBot(args)
    bot.setup(args)

    # ---------------- #
    # -- PROCESSING -- #
    # ---------------- #

    bot.ip.login()

    # -- Liking -- #
    # like_by_locations
    if args.like_locations:
        bot.ip.like_by_locations(locations=bot.get_cols(args.like_locations),
                                 amount=bot.settings['like_by_locations_amount'],
                                 media=bot.settings['like_by_locations_media'],
                                 skip_top_posts=True)

    # like_by_tags
    if args.like_tags:
        bot.ip.like_by_tags(tags=bot.get_cols(args.like_tags),
                            amount=bot.settings['like_by_tags_amount'],
                            skip_top_posts=bot.settings['like_by_tags_skip'],
                            use_smart_hashtags=bot.settings['like_by_tags_smart_ht'],
                            use_smart_location_hashtags=bot.settings['like_by_tags_smart_location_ht'],
                            interact=bot.settings['like_by_tags_interact'],
                            randomize=bot.settings['like_by_tags_randomize'],
                            media=bot.settings['like_by_tags_media'])

    # like_by_users

    if args.like_users:
        bot.ip.like_by_users(usernames=bot.get_cols(args.like_users),
                             amount=bot.settings['like_by_users_amount'],
                             randomize=bot.settings['like_by_users_randomize'],
                             media=bot.settings['like_by_users_media'])

    # like_from_image

    # like_by_feed

    # like_by_feed_generator

    # -- Interacting -- #

    # interact_by_users

    # interact_by_users_tagged_posts

    # interact_user_followers
    if args.interact_followers:
        """
        Functions needs set_do_* and set_user_interact
        """
        bot.ip.interact_user_followers(bot.get_cols(args.interact_followers),
                                       amount=bot.settings['interact_user_followers_amount'],
                                       randomize=bot.settings['interact_user_followers_randomize'])

    # interact_user_following

    # interact_by_URL

    # interact_by_comments

    # -- Commenting -- #

    # comment_by_locations

    # -- Following -- #

    # follow_commenters

    # follow_likers

    # follow_by_list

    # follow_user_followers

    # follow_user_following

    # follow_by_locations

    # follow_by_tags

    # accept_follow_requests

    # unfollow_users

    # remove_follow_requests

    # -- Grabbing -- #

    # grab_followers

    # grab_following

    # -- Picking -- #

    # pick_unfollowers

    # pick_nonfollowers

    # pick_fans

    # pick_mutual_following

    # join_pods

    bot.ip.end()
