import Constants
import HelperFunctions
import Logger
import time

from Enums import VideoQualityTypeEnum


class BaseServer:
    def __init__(self, server_dict):
        self.ServerName = server_dict['server']
        self.Priority = server_dict['priority']

    def navigateServer(self, web_driver, url):
        pass

    def __str__(self):
        return 'Server = {name}, Priority = {priority}'.format(name=self.ServerName, priority=self.Priority)


class FOR_AD(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


# Implemented - Saves in current location
class MP4UPLOAD(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)
        self.TEXT_DOWNLOAD_BTN_ID = 'downloadbtn'

    def navigateServer(self, web_driver, url):
        vid_quality_url_map = {}
        for window in web_driver.window_handles:
            try:
                web_driver.switch_to_window(window)
                if not HelperFunctions.compareUrls(web_driver.current_url, url):
                    continue
                download_btn = web_driver.find_element_by_id(self.TEXT_DOWNLOAD_BTN_ID)
                web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, download_btn)
            except Exception, ex:
                Logger.addExceptionLog(ex.message, __name__)
        return vid_quality_url_map

class OLOAD(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


class OPENUPLOAD(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


class OPENLOAD(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        vid_quality_url_map = {}
        for window in web_driver.window_handles:
            try:
                web_driver.switch_to_window(window)
                if not HelperFunctions.compareUrls(web_driver.current_url, url):
                    continue
                download_btn = web_driver.find_element_by_id("btnDl")
                web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, download_btn)
                HelperFunctions.closeWindows(web_driver, True)
            except Exception, ex:
                Logger.addExceptionLog(ex.message, __name__)
        return vid_quality_url_map
        pass


# Implemented
class RAPIDVIDEO(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        vid_quality_url_map = {}
        for window in web_driver.window_handles:
            try:
                web_driver.switch_to_window(window)
                if not HelperFunctions.compareUrls(web_driver.current_url, url):
                    continue

                videos_div_elem = web_driver.find_element_by_class_name(Constants.TEXT_VIDEO)
                video_urls_tags = videos_div_elem.find_elements_by_tag_name(Constants.IDF_ANCHOR)
                for video_urls_tag in video_urls_tags:
                    quality = VideoQualityTypeEnum.translateToEnum(video_urls_tag.text)
                    vid_quality_url_map[quality] = video_urls_tag.get_attribute(Constants.IDF_HREF)
                break
            except Exception, ex:
                Logger.addExceptionLog(ex.message, __name__)
        return vid_quality_url_map


class STREAMANGO(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


class VIDCDN(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


class VIDSTREAMING(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        pass


# Implemented
class XSTREAMCDN(BaseServer):
    def __init__(self, server_dict):
        BaseServer.__init__(self, server_dict)

    def navigateServer(self, web_driver, url):
        vid_quality_url_map = {}
        for window in web_driver.window_handles:
            try:
                web_driver.switch_to_window(window)
                if not HelperFunctions.compareUrls(web_driver.current_url, url):
                    continue
                self.waitCoundown(web_driver)
                vid_quality_url_map = self.formVideoQualityUrlMap(web_driver)
                break
            except Exception, ex:
                Logger.addExceptionLog(ex.message, __name__)
        return vid_quality_url_map

    def waitCoundown(self, web_driver):
        curr_countdown_time = HelperFunctions.getCountdownValue(web_driver)
        download_button = web_driver.find_element_by_id(Constants.ELEM_ID_DOWNLOAD)
        web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, download_button)
        HelperFunctions.closeWindows(web_driver, True)
        num_tries = curr_countdown_time * 2
        has_is_loading_button = True

        while curr_countdown_time > 0 and num_tries > 0 and has_is_loading_button:
            time.sleep(Constants.SLEEP_TIME_SHORT)
            HelperFunctions.closeWindows(web_driver, True)
            curr_countdown_time = HelperFunctions.getCountdownValue(web_driver)
            has_is_loading_button = HelperFunctions.hasIsLoadingButton(web_driver)
            num_tries -= 1

    def formVideoQualityUrlMap(self, web_driver):
        count, vid_quality_url_map = 0, {}
        while count < 10:
            try:
                download_links_para = web_driver.find_elements_by_class_name(Constants.CLASS_P_DOWNLOAD)
                for para in download_links_para:
                    anchor = para.find_elements_by_tag_name(Constants.IDF_ANCHOR)[0]
                    quality = VideoQualityTypeEnum.translateToEnum(anchor.text)
                    vid_quality_url_map[quality] = anchor.get_attribute(Constants.IDF_HREF)
                break
            except Exception, e:
                pass
            count += 1
            time.sleep(Constants.SLEEP_TIME_SHORT)
        return vid_quality_url_map
