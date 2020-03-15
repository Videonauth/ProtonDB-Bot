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
        self.steam_is_free = bool(False)
        self.steam_short_description = str(f'')
        self.steam_detailed_description = str(f'')
        self.steam_about = str(f'')
        self.steam_header_image = str(f'')
        self.steam_legal_notice = str(f'')
        self.steam_platforms = dict({})
        self.steam_publishers = list([])
        self.steam_price_overview = dict({})
        self.steam_release_date = str(f'')
        self.steam_coming_soon = bool(False)
        self.steam_required_age = str(f'')

        # metacritic
        self.metacritic_score = int(-1)
        self.metacritic_link = str(f'')

        # Initialize ProtonDB variables
        self.proton_db_current_rating = None
        self.proton_db_number_reports = None
        self.proton_db_trending = None
        self.proton_db_best_rating = None

        # Derivate price data
        self.steam_price_euro = float(0.000)
        self.steam_price_us = float(0.000)

    def __str__(self) -> str:
        return f'Data Object: {self.steam_id}: {self.steam_name}'

    def to_dict(self) -> dict:
        return dict(
            created=self.created,
            last_updated_steamfront=self.last_updated_steamfront,
            last_modified=self.last_modified,
            steam_id=self.steam_id,
            steam_name=self.steam_name,
            steam_short_description=self.steam_short_description,
            steam_detailed_description=self.steam_detailed_description,
            steam_about=self.steam_about,
            steam_header_image=self.steam_header_image,
            steam_legal_notice=self.steam_legal_notice,
            steam_is_free=self.steam_is_free,
            steam_price_euro=self.steam_price_euro,
            steam_price_us=self.steam_price_us,
            steam_platforms=self.steam_platforms,
            steam_publishers=self.steam_publishers,
            steam_price_overview=self.steam_price_overview,
            steam_release_date=self.steam_release_date,
            steam_coming_soon=self.steam_coming_soon,
            steam_required_age=self.steam_required_age,
            metacritic_score=self.metacritic_score,
            metacritic_link=self.metacritic_link,
            known_abrevations=self.known_abrevations,
            last_shown=self.last_shown,
            count_shown=self.count_shown,
            proton_db_current_rating=self.proton_db_current_rating,
            proton_db_number_reports=self.proton_db_number_reports,
            proton_db_trending=self.proton_db_trending,
            proton_db_best_rating=self.proton_db_best_rating
        )

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
