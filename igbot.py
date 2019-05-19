"""
This is the main runner for igbot
"""

import argparse
import gspread

from instapy import InstaPy
from instapy import set_workspace
from oauth2client.service_account import ServiceAccountCredentials


def gspread_auth(key):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
    return gspread.authorize(creds)


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
    parser.add_argument('--interact-followers')
    return parser.parse_args()


class InstaGBot:
    def __init__(self, spreadsheet, authkey, settings='settings'):
        self.spreadsheet = spreadsheet
        self.authkey = authkey
        self.settings = settings
        self.client = None

    def authorize(self):
        self.client = gspread_auth(self.authkey)

    def sheet(self, worksheet):
        if args.sheet:
            document = self.client.open(self.spreadsheet)
        elif args.sheet_key:
            document = self.client.open_by_key(self.spreadsheet)
        elif args.sheet_url:
            document = self.client.open_by_url(self.spreadsheet)
        else:
            document = None
            raise()
        wks = document.worksheet(worksheet)
        return wks

    def get_rows(self, worksheet, row=1):
        wks = self.sheet(worksheet)
        values = wks.row_values(row)
        return values

    def get_cols(self, worksheet, col=1):
        wks = self.sheet(worksheet)
        values = wks.col_values(col)
        return values

    def get_all_values(self, worksheet):
        wks = self.sheet(worksheet)
        values = wks.get_all_values()
        return values

    def settings_get_value(self, key):
        wks = self.sheet(self.settings)
        cell = wks.find(key)
        value = wks.cell(cell.row, cell.col + 1).value
        return value

    def settings_bool(self, key):
        return bool(self.settings_get_value(key))

    def settings_int(self, key):
        return int(self.settings_get_value(key))

    def settings_text(self, key):
        return self.settings_get_value(key)


if __name__ == '__main__':

    args = parse_arguments()
    print(args)

    if args.sheet:
        bot = InstaGBot(args.sheet, args.authkey)
    elif args.sheet_key:
        bot = InstaGBot(args.sheet_key, args.authkey)
    elif args.sheet_url:
        bot = InstaGBot(args.sheet_url, args.authkey)
    else:
        raise()

    bot.authorize()

    # -- SETTINGS -- #

    set_workspace(path=args.workspace)

    ip = InstaPy(username=args.user,
                 password=args.password,
                 headless_browser=True)

    # set_sleep_reduce

    # set_action_delays

    # set_do_comment

    # set_comments

    # set_do_follow

    # set_do_like

    ip.set_do_like(enabled=bot.settings_bool('set_do_like_enabled'),
                   percentage=bot.settings_int('set_do_like_percentage'))

    # set_dont_like

    # set_mandatory_words

    # set_user_interact

    ip.set_user_interact(amount=bot.settings_int('set_user_interact_amount'),
                         percentage=bot.settings_int('set_user_interact_percentage'),
                         randomize=bot.settings_bool('set_user_interact_randomize'),
                         media=bot.settings_text('set_user_interact_media'))

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

    ip.set_simulation(enabled=False)

    # set_dont_unfollow_active_users

    # set_blacklist

    # set_quota_supervisor
    ip.set_quota_supervisor(enabled=bot.settings_bool('set_quota_supervisor_enabled'),
                            peak_likes=(bot.settings_int('set_quota_supervisor_likes_hour'),
                                        bot.settings_int('set_quota_supervisor_likes_day')),
                            sleep_after=[bot.settings_text('set_quota_supervisor_sleepafter')],
                            stochastic_flow=bot.settings_bool('set_quota_supervisor_stochflow'))

    # set_do_reply_to_comments

    # set_comment_replies

    # set_use_meaningcloud

    # set_use_yandex

    # ---------------- #
    # -- PROCESSING -- #
    # ---------------- #

    ip.login()

    # -- Liking -- #
    # like_by_locations

    if args.like_locations:
        ip.like_by_locations(locations=bot.get_cols(args.like_locations),
                             amount=bot.settings_int('like_by_locations_amount'),
                             media=bot.settings_text('like_by_locations_media'),
                             skip_top_posts=True)

    # like_by_tags

    # like_by_users

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
        ip.interact_user_followers(bot.get_cols(args.interact_followers),
                                   amount=bot.settings_int('interact_user_followers_amount'),
                                   randomize=bot.settings_bool('interact_user_followers_randomize'))

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

    ip.end()
