import getopt
import sys

import Constants
import HelperFunctions
import Logger
from Enums import AnimeCategoryEnum, InputCategoryEnum
from InputParams import InputParams


def extractParametersFromArgv(argv, anime_dict):
    ids, url, episodes = [], '', ''
    input_category, anime_category = InputCategoryEnum.NONE, AnimeCategoryEnum.ALL
    add_new_anime = False
    try:
        if len(argv) % 2 == 1 and ('-l' in argv or '--list' in argv):
            printAnimeList(anime_dict, AnimeCategoryEnum.ALL)
            sys.exit()

        opts, _ = getopt.getopt(argv, "hrl:i:u:e:a:", ["list=", "ids=", "url=", "episodes=", "add="])
        for opt, arg in opts:
            if opt == '-h':
                printArgsHelp()
                sys.exit()
            elif opt == '-r':
                ids = Constants.DOWNLOAD_ALL
                break
            elif opt in ("-a", "--add"):
                url = arg.strip().lower()
                add_new_anime = True
            elif opt in ("-i", "--ids"):
                ids = HelperFunctions.resolveSpecialCharSeparatedStr(arg.strip())
            elif opt in ("-u", "--url"):
                url = arg.strip().lower()
            elif opt in ("-e", "--episodes"):
                episodes = arg.strip().lower()
            elif opt in ("-l", "--list"):
                anime_category = AnimeCategoryEnum.translateToEnum(arg.strip().lower())
                anime_category = anime_category if anime_category is not AnimeCategoryEnum.NONE else AnimeCategoryEnum.ALL
                printAnimeList(anime_dict, anime_category)
                sys.exit()

    except Exception, e:
        Logger.addExceptionLog(e.message, __name__)
        printArgsHelp()
        sys.exit(2)

    if ids == Constants.DOWNLOAD_ALL:
        filtered_ids = anime_dict.keys()
    else:
        filtered_ids = [x for x in ids if x in anime_dict.keys()]
    if len(filtered_ids) == 0 and not HelperFunctions.validateUrl(url):
        print 'Invalid IDs and/or URL. Usage:'
        for key, val in Constants.ARGS_HELP_TEXT.items():
            print key, val
        sys.exit(2)
    anime_input_params = InputParams(filtered_ids, url, episodes, anime_category, add_new_anime)
    return anime_input_params


def printArgsHelp():
    print '---------------------------------------------------------------'
    print 'Command line params to use the application:'
    print '---------------------------------------------------------------'
    for key, val in Constants.ARGS_HELP_TEXT.iteritems():
        print key, val
    print '---------------------------------------------------------------'


def printAnimeList(anime_dict, category):
    if category is not AnimeCategoryEnum.NONE and anime_dict:
        header_keys = ['ID', 'Category', 'Anime Title', 'Episodes']
        adjustments = {}
        for header_key in header_keys:
            adjustments[header_key] = len(header_key)
        for _, anime in anime_dict.items():
            adjustments[header_keys[0]] = max(adjustments[header_keys[0]], len(str(anime.id)))
            adjustments[header_keys[1]] = max(adjustments[header_keys[1]], len(anime.category.name))
            adjustments[header_keys[2]] = max(adjustments[header_keys[2]], len(anime.name))
            adjustments[header_keys[3]] = max(adjustments[header_keys[3]], len(anime.episodes))
        total_length = sum(adjustments.values())
        print '-' * (total_length + len(adjustments) * 3)
        for idx, header_key in enumerate(header_keys):
            print header_key.center(adjustments[header_key]),
            if idx < len(header_keys) - 1:
                print ' ',
            else:
                print ''
        print '-' * (total_length + len(adjustments) * 3)
        for anime_id, anime in anime_dict.items():
            if anime.category == category or category == AnimeCategoryEnum.ALL:
                print str(anime_id).ljust(adjustments[header_keys[0]]), '-',
                print anime.category.name.center(adjustments[header_keys[1]]), '-',
                print anime.name.center(adjustments[header_keys[2]]), '-',
                print anime.episodes.ljust(adjustments[header_keys[3]])
        print '-' * (total_length + len(adjustments) * 3)
