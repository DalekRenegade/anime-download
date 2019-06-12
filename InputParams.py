import Constants
from Enums import InputCategoryEnum, AnimeCategoryEnum


class InputParams:
    def __init__(self, ids, url, episodes, anime_category, add_new_anime=False):
        self.InputCategory = InputCategoryEnum.NONE
        if ids:
            self.InputCategory = InputCategoryEnum.ID
        elif url:
            self.InputCategory = InputCategoryEnum.URL
        self.Episodes = episodes
        if self.InputCategory == InputCategoryEnum.URL and not self.Episodes:
            self.Episodes = Constants.DOWNLOAD_ALL
        self.AnimeCategory = anime_category if anime_category else AnimeCategoryEnum.ALL
        self.AnimeReference = [url] if self.InputCategory == InputCategoryEnum.URL else ids
        self.AddNewAnime = add_new_anime
