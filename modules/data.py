import time
import modules.core as core

__version__ = core.__version__


class Data(object):
    """
    Main data class for the search database.
    """
    # Constructor, here all variables the data class has are initialized
    def __init__(self) -> None:
        # Fill the time variables (this is the only place where they are the same).
        # NOTE: self.created is to be treated immutable except on copying in an objects dict output!
        self.created = time.time()

        # Timestamp of last modification done to the data set.
        self.last_modified = self.created

        # Timestamps of the different websites when last requested data from them.
        self.last_updated_steam_search = self.created
        self.last_updated_steamdb = self.created
        self.last_updated_protondb = self.created
        self.last_updated_steamfront = self.created

        # Bot metrics
        self.last_shown = self.created
        self.count_shown = int(0)

        # Initialize the list of known abrevations.
        self.known_abrevations = list([])

        # The data we get from the app-list.json from steam
        self.steam_id = int(-1)
        self.steam_name = str('')

        # Data we fetch via steamfront API library
        self.steam_appid = int(-1)
        self.name = str(f'')
        self.type = str(f'')
        self.release_date = dict({})
        self.recommendations = dict({})
        self.supported_languages = str(f'')
        # Pricing
        self.is_free = bool(False)
        self.price_overview = dict({})
        self.dlc = list([])
        self.package_groups = list([])
        self.packages = list([])
        # Categories information
        self.categories = dict({})
        self.genres = list([])
        self.achievements = dict({})
        # Developer and publisher info including support and website link
        self.developers = list([])
        self.publishers = list([])
        self.legal_notice = str(f'')
        self.support_info = dict({})
        self.website = str(f'')
        self.ext_user_account_notice = str(f'')
        # Metacritic
        self.metacritic = dict({})
        # Description and about
        self.short_description = str(f'')
        self.detailed_description = str(f'')
        self.about_the_game = str(f'')
        # Image and screenshots
        self.background = str(f'')
        self.header_image = str(f'')
        self.screenshots = list([])
        self.movies = list([])
        # Platforms and requirements information
        self.platforms = dict({})
        self.linux_requirements = dict({})
        self.mac_requirements = dict({})
        self.pc_requirements = dict({})
        self.controller_support = str(f'')
        # Age information
        self.required_age = str(f'')

        # Data we fetch from ProtonDB
        self.confidence = str(f'')
        self.score = float(0.000)
        self.tier = str(f'')
        self.total = int(-1)
        self.trendingTier = str(f'')
        self.bestReportedTier = str(f'')

        # Derivate data
        self.native = bool(False)
        self.steam_price_euro = float(0.000)
        self.steam_price_us = float(0.000)

    def to_dict(self) -> dict:
        return dict(
            # The time variables.
            # NOTE: self.created is to be treated immutable except on copying in an objects dict output!
            created=self.created,
            # Timestamp of last modification done to the data set.
            last_modified=self.last_modified,
            # Timestamps of the different websites when last requested data from them.
            last_updated_steam_search=self.last_updated_steam_search,
            last_updated_steamdb=self.last_updated_steamdb,
            last_updated_protondb=self.last_updated_protondb,
            last_updated_steamfront=self.last_updated_steamfront,
            # Bot metrics
            last_shown=self.last_shown,
            count_shown=self.count_shown,
            # Initialize the list of known abrevations.
            known_abrevations=self.known_abrevations,
            # The data we get from the app-list.json from steam
            steam_id=self.steam_id,
            steam_name=self.steam_name,
            # Data we fetch via steamfront API library
            steam_appid=self.steam_appid,
            name=self.name,
            type=self.type,
            release_date=self.release_date,
            recommendations=self.recommendations,
            supported_languages=self.supported_languages,
            # Pricing
            is_free=self.is_free,
            price_overview=self.price_overview,
            dlc=self.dlc,
            package_groups=self.package_groups,
            packages=self.packages,
            # Categories information
            categories=self.categories,
            genres=self.genres,
            achievements=self.achievements,
            # Developer and publisher info including support and website link
            developers=self.developers,
            publishers=self.publishers,
            legal_notice=self.legal_notice,
            support_info=self.support_info,
            website=self.website,
            ext_user_account_notice=self.ext_user_account_notice,
            # Metacritic
            metacritic=self.metacritic,
            # Description and about
            short_description=self.short_description,
            detailed_description=self.detailed_description,
            about_the_game=self.about_the_game,
            # Image and screenshots
            background=self.background,
            header_image=self.header_image,
            screenshots=self.screenshots,
            movies=self.movies,
            # Platforms and requirements information
            platforms=self.platforms,
            linux_requirements=self.linux_requirements,
            mac_requirements=self.mac_requirements,
            pc_requirements=self.pc_requirements,
            controller_support=self.controller_support,
            # Age information
            required_age=self.required_age,
            # Data we fetch from ProtonDB
            confidence=self.confidence,
            score=self.score,
            tier=self.tier,
            total=self.total,
            trendingTier=self.trendingTier,
            bestReportedTier=self.bestReportedTier,
            # Derivate data
            native=self.native,
            steam_price_euro=self.steam_price_euro,
            steam_price_us=self.steam_price_us
        )

    def __str__(self) -> str:
        return f'{self.to_dict()}'

    def from_dict(self, dict_item: dict):
        # Fill the time variables.
        # NOTE: self.created is to be treated immutable except on copying in an objects dict output!
        if f'created' in dict_item.keys():
            if dict_item.get(f'created') < self.created:
                self.created = float(dict_item.get(f'created'))
        # Timestamp of last modification done to the data set.
        if f'last_modified' in dict_item.keys():
            if dict_item.get(f'last_modified') < time.time():
                self.last_modified = time.time()
        # Timestamps of the different websites when last requested data from them.
        if f'last_updated_steam_search' in dict_item.keys():
            self.last_updated_steam_search = float(dict_item.get(f'last_updated_steam_search'))
        if f'last_updated_steamdb' in dict_item.keys():
            self.last_updated_steamdb = float(dict_item.get(f'last_updated_steamdb'))
        if f'last_updated_protondb' in dict_item.keys():
            self.last_updated_protondb = float(dict_item.get(f'last_updated_protondb'))
        if f'last_updated_steamfront' in dict_item.keys():
            self.last_updated_steamfront = float(dict_item.get(f'last_updated_steamfront'))
        # Bot metrics
        if f'last_shown' in dict_item.keys():
            self.last_shown = float(dict_item.get(f'last_shown'))
        if f'count_shown' in dict_item.keys():
            self.count_shown = int(dict_item.get(f'count_shown'))
        # Initialize the list of known abrevations.
        if f'known_abrevations' in dict_item.keys():
            self.known_abrevations = list(dict_item.get(f'known_abrevations'))
        # The data we get from the app-list.json from steam
        if f'steam_id' in dict_item.keys():
            if self.steam_id == -1 and int(dict_item.get(f'steam_id')) != -1:
                self.steam_id = int(dict_item.get(f'steam_id'))
        if f'steam_name' in dict_item.keys():
            self.steam_name = str(dict_item.get(f'steam_name'))
        # Data we fetch via steamfront API library
        if f'steam_appid' in dict_item.keys():
            self.steam_appid = int(dict_item.get(f'steam_appid'))
        if f'name' in dict_item.keys():
            self.name = str(dict_item.get(f'name'))
        if f'type' in dict_item.keys():
            self.type = str(dict_item.get(f'type'))
        if f'release_date' in dict_item.keys():
            self.release_date = dict(dict_item.get(f'release_date'))
        if f'recommendations' in dict_item.keys():
            self.recommendations = dict(dict_item.get(f'recommendations'))
        if f'supported_languages' in dict_item.keys():
            _tmp_str = core.html_to_discord(str(dict_item.get(f'supported_languages')))
            self.supported_languages = str(_tmp_str)
        # Pricing
        if f'is_free' in dict_item.keys():
            self.is_free = bool(dict_item.get(f'is_free'))
        if f'price_overview' in dict_item.keys():
            self.price_overview = dict(dict_item.get(f'price_overview'))
        if f'dlc' in dict_item.keys():
            self.dlc = list(dict_item.get(f'dlc'))
        if f'package_groups' in dict_item.keys():
            self.package_groups = list(dict_item.get(f'package_groups'))
        if f'packages' in dict_item.keys():
            self.packages = list(dict_item.get(f'packages'))
        # Categories information
        if f'categories' in dict_item.keys():
            self.categories = dict(dict_item.get(f'categories'))
        if f'genres' in dict_item.keys():
            self.genres = list(dict_item.get(f'genres'))
        if f'achievements' in dict_item.keys():
            self.achievements = dict(dict_item.get(f'achievements'))
        # Developer and publisher info including support and website link
        if f'developers' in dict_item.keys():
            self.developers = list(dict_item.get(f'developers'))
        if f'publishers' in dict_item.keys():
            self.publishers = list(dict_item.get(f'publishers'))
        if f'legal_notice' in dict_item.keys():
            self.legal_notice = str(dict_item.get(f'legal_notice'))
        if f'support_info' in dict_item.keys():
            self.support_info = dict(dict_item.get(f'support_info'))
        if f'website' in dict_item.keys():
            self.website = str(dict_item.get(f'website'))
        if f'ext_user_account_notice' in dict_item.keys():
            self.ext_user_account_notice = str(dict_item.get(f'ext_user_account_notice'))
        # Metacritic
        if f'metacritic' in dict_item.keys():
            self.metacritic = dict(dict_item.get(f'metacritic'))
        # Description and about
        if f'short_description' in dict_item.keys():
            _tmp_str = core.html_to_discord(str(dict_item.get(f'short_description')))
            self.short_description = str(_tmp_str)
        if f'detailed_description' in dict_item.keys():
            _tmp_str = core.html_to_discord(str(dict_item.get(f'detailed_description')))
            self.detailed_description = str(_tmp_str)
        if f'about_the_game' in dict_item.keys():
            _tmp_str = core.html_to_discord(str(dict_item.get(f'about_the_game')))
            self.about_the_game = str(_tmp_str)
        # Image and screenshots
        if f'background' in dict_item.keys():
            self.background = str(dict_item.get(f'background'))
        if f'header_image' in dict_item.keys():
            self.header_image = str(dict_item.get(f'header_image'))
        if f'screenshots' in dict_item.keys():
            self.screenshots = list(dict_item.get(f'screenshots'))
        if f'movies' in dict_item.keys():
            self.movies = list(dict_item.get(f'movies'))
        # Platforms and requirements information
        if f'platforms' in dict_item.keys():
            self.platforms = dict(dict_item.get(f'platforms'))
        if f'linux_requirements' in dict_item.keys():
            self.linux_requirements = dict(dict_item.get(f'linux_requirements'))
        if f'mac_requirements' in dict_item.keys():
            self.mac_requirements = dict(dict_item.get(f'mac_requirements'))
        if f'pc_requirements' in dict_item.keys():
            self.pc_requirements = dict(dict_item.get(f'pc_requirements'))
        if f'controller_support' in dict_item.keys():
            self.controller_support = str(dict_item.get(f'controller_support'))
        # Age information
        if f'required_age' in dict_item.keys():
            self.required_age = str(dict_item.get(f'required_age'))

        # Data we fetch from ProtonDB
        if f'confidence' in dict_item.keys():
            self.confidence = str(dict_item.get(f'confidence'))
        if f'score' in dict_item.keys():
            self.score = float(dict_item.get(f'score'))
        if f'tier' in dict_item.keys():
            self.tier = str(dict_item.get(f'tier'))
        if f'total' in dict_item.keys():
            self.total = int(dict_item.get(f'total'))
        if f'trendingTier' in dict_item.keys():
            self.trendingTier = str(dict_item.get(f'trendingTier'))
        if f'bestReportedTier' in dict_item.keys():
            self.bestReportedTier = str(dict_item.get(f'bestReportedTier'))

        # Derivate data
        if f'native' in dict_item.keys():
            self.native = bool(dict_item.get(f'native'))
        if f'steam_price_euro' in dict_item.keys():
            self.steam_price_euro = float(dict_item.get(f'steam_price_euro'))
        if f'steam_price_us' in dict_item.keys():
            self.steam_price_us = float(dict_item.get(f'steam_price_us'))


if __name__ == f'__main__':
    pass
