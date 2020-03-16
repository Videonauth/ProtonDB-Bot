import time
import modules.core as core

__version__ = core.__version__


class Data(object):
    """
    Main data class for the search database.
    """
    # Constructor, here all variables the data class has are initialized
    def __init__(self) -> None:
        # Fill the three time variables (this is the only place where they are the same).
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

    def from_dict(self, _value: dict):
        if f'steam_id' in _value.keys():
            self.steam_id = _value.get(f'steam_id')
        if f'created' in _value.keys():
            self.created = _value.get(f'created')
        if f'last_updated_steamfront' in _value.keys():
            self.last_updated_steamfront = _value.get(f'last_updated_steamfront')
        if f'last_modified' in _value.keys():
            self.last_modified = _value.get(f'last_modified')
        if f'steam_name' in _value.keys():
            self.steam_name = _value.get(f'steam_name')
        if f'steam_short_description' in _value.keys():
            self.steam_short_description = _value.get(f'steam_short_description')
        if f'steam_detailed_description' in _value.keys():
            self.steam_detailed_description = _value.get(f'steam_detailed_description')
        if f'steam_about' in _value.keys():
            self.steam_about = _value.get(f'steam_about')
        if f'steam_price_euro' in _value.keys():
            self.steam_price_euro = _value.get(f'steam_price_euro')
        if f'steam_price_us' in _value.keys():
            self.steam_price_us = _value.get(f'steam_price_us')
        if f'known_abrevations' in _value.keys():
            self.known_abrevations = _value.get(f'known_abrevations')
        if f'last_shown' in _value.keys():
            self.last_shown = _value.get(f'last_shown')
        if f'count_shown' in _value.keys():
            self.count_shown = _value.get(f'count_shown')
        if f'proton_db_current_rating' in _value.keys():
            self.proton_db_current_rating = _value.get(f'proton_db_current_rating')
        if f'proton_db_number_reports' in _value.keys():
            self.proton_db_number_reports = _value.get(f'proton_db_number_reports')
        if f'proton_db_trending' in _value.keys():
            self.proton_db_trending = _value.get(f'proton_db_trending')
        if f'proton_db_best_rating' in _value.keys():
            self.proton_db_best_rating = _value.get(f'proton_db_best_rating')
        # handling steamfront
        if f'steam_appid' in _value.keys():
            if _value.get(f'steam_appid') == self.steam_id:
                pass
            else:
                return
        if f'short_description' in _value.keys():
            self.steam_short_description = _value.get(f'short_description')
        if f'detailed_description' in _value.keys():
            self.steam_detailed_description = _value.get(f'detailed_description')
        if f'about_the_game' in _value.keys():
            self.steam_about = _value.get(f'about_the_game')
        if f'header_image' in _value.keys():
            self.steam_header_image = _value.get(f'header_image')
        if f'legal_notice' in _value.keys():
            self.steam_legal_notice = _value.get(f'legal_notice')
        if f'metacritic' in _value.keys():
            _tmp_dict = _value.get(f'metacritic')
            self.metacritic_score = _tmp_dict.get(f'score')
            self.metacritic_link = _tmp_dict.get(f'url')
        if f'is_free' in _value.keys():
            self.steam_is_free = _value.get(f'is_free')
        if f'platforms' in _value.keys():
            self.steam_platforms = _value.get(f'platforms')
        if f'publishers' in _value.keys():
            self.steam_publishers = _value.get(f'publishers')
        if f'price_overview' in _value.keys():
            self.steam_price_overview = _value.get(f'price_overview')
            if f'currency' in self.steam_price_overview.keys():
                if self.steam_price_overview.get(f'currency') == f'EUR':
                    _tmp_float = float(0.000)
                    _tmp_int = int(0)
                    _tmp_int = int(self.steam_price_overview.get(f'initial'))
                    _tmp_float = float(_tmp_int) / float(10.000)
                    self.steam_price_euro = _tmp_float
                if self.steam_price_overview.get(f'currency') == f'US':
                    _tmp_float = float(0.000)
                    _tmp_int = int(0)
                    _tmp_int = int(self.steam_price_overview.get(f'initial'))
                    _tmp_float = float(_tmp_int) / float(10.000)
                    self.steam_price_us = _tmp_float
        if f'release_date' in _value.keys():
            _tmp_dict = _value.get(f'release_date')
            self.steam_release_date = _tmp_dict.get(f'date')
            self.steam_coming_soon = _tmp_dict.get(f'coming_soon')
        if f'required_age' in _value.keys():
            self.steam_required_age = _value.get(f'required_age')


if __name__ == f'__main__':
    pass
