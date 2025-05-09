import datetime as dt
import random
import auntie_hela_models as models

class SampleData:
    def __init__(self):
        pass

    def _make_entity(self, parent, name, code_name, desc, region, addr_city, addr_country_name, addr_details, 
                     addr_postal_code, is_active=True, is_visible=True):
        print("\n==== _make_entity: code_name: ", code_name, "\n")
        e = models.DimEntity(parent=parent, name=name, code_name=code_name, desc=desc, 
                             region=region, addr_country_name=addr_country_name, addr_city=addr_city, 
                             addr_details=addr_details, addr_postal_code=addr_postal_code, 
                             is_active=is_active, is_visible=is_visible)
        e.save()
        return e

    def _make_product(self, parent, name, code_name, desc, sku, is_active=True, is_visible=True):
        print("\n==== _make_product: code_name: ", code_name, "\n")
        m = models.DimProduct(parent=parent, name=name, code_name=code_name, desc=desc, sku=sku, 
                              is_active=is_active, is_visible=is_visible)
        m.save()
        return m

    def _make_scenario(self, parent, name, code_name, desc, scenario_type, is_active=True, is_visible=True):
        print("\n==== _make_scenario: code_name: ", code_name, "\n")
        m = models.DimScenario(parent=parent, name=name, code_name=code_name, desc=desc, 
                               scenario_type=scenario_type, is_active=is_active, is_visible=is_visible)
        m.save()
        return m

    def _make_account(self, parent, name, code_name, desc, account_no, entity=None, 
                      account_no_range_bottom=None, account_no_range_top=None, 
                      is_account_type=False,  is_active=True, is_visible=True):        
        print("\n==== _make_account: code_name: ", code_name, "\n")
        m = models.DimAccount(parent=parent, name=name, code_name=code_name, desc=desc, 
                              account_no=account_no,
                              entity=entity,
                              account_no_range_bottom=account_no_range_bottom,
                              account_no_range_top=account_no_range_top,
                              is_account_type=is_account_type,
                              is_active=is_active, is_visible=is_visible)
        m.save()
        return m

    def _make_measurement(self, parent, name, code_name, desc, unit_type, is_active=True, is_visible=True):
        print("\n==== _make_measurement: code_name: ", code_name, "\n")
        m = models.Measurement(parent=parent, name=name, code_name=code_name, desc=desc,
                               unit_type=unit_type,
                               is_active=is_active, is_visible=is_visible)
        m.save()
        return m

    def _make_time(self, parent, name, code_name, desc, period_type=None, 
                   is_active=True, is_visible=True):        
        print("\n==== _make_time: code_name: ", code_name, "\n")
        m = models.DimTime(parent=parent, name=name, code_name=code_name, desc=desc, 
                           period_type=period_type,
                          is_active=is_active, is_visible=is_visible)
        m.save()
        return m
    
    def _make_cube_def(self, parent, name, code_name, desc, fact_entity, dimensions, is_active=True, is_visible=True):
        m = models.RevOlapCubeDef(parent=parent,
                            name=name,
                            code_name=code_name,
                            desc=desc,
                            is_active=is_active,
                            is_visible=is_visible,
                            dimensions=dimensions,
                            fact_entity=fact_entity)
        m.save()
        return m
    
    def _make_fact_CubeTest1(self, parent_fact, time, scenario, entity, account, product, origin, measurement, num_value):
        m = models.RevOlapCubeFact_CubeTest1(
            parent_fact=parent_fact,
            time=time,
            scenario=scenario,
            entity=entity,
            account=account,
            product=product,
            origin=origin,
            measurement=measurement,
            num_value=num_value,           
        )
        m.save()
        return m


    def make_sample_data_for_fixtures(self):
        ALL_DT_START = dt.datetime.now()

        top_entity = self._make_entity(None, "Ciocia Hela Restaurant Chain", "CH_TOP", "", "UE_PL", "Gdańsk", "Poland", "ul. Grunwaldzka 121", "80-101")

        top_entities_countries = {
            'pl': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Poland", "CH_TOP_PL", "", "UE_PL", "Gdańsk", "Poland", "al. Hallera 151", "80-200"),
            'de': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Germany", "CH_TOP_DE", "", "UE_DE", "Berlin", "Germany", "Adenauerstrasse 123", "01-222"),
            'fr': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain France", "CH_TOP_FR", "", "UE_FR", "Paris", "France", "156 Champs Elysees", "75004"),
            'uk': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain", "CH_TOP_UK", "", "UK", "London", "United Kingdom", "123 Piccadilly Street", "1J 9LL"),
        }

        top_entities_country_districts = {
            'pl_pm': self._make_entity(top_entities_countries['pl'], "Ciocia Hela Restaurant Chain Poland - Pomorskie HQ", "CH_TOP_PL_PM", "", "UE_PL", "Gdańsk", "Poland", "al. Hallera 152", "80-201"),
            'pl_mz': self._make_entity(top_entities_countries['pl'], "Ciocia Hela Restaurant Chain Poland - Mazowieckie HQ", "CH_TOP_PL_MZ", "", "UE_PL", "Warszawa", "Poland", "al. Jerozolimskie 263", "01-504"),
            'pl_ld': self._make_entity(top_entities_countries['pl'], "Ciocia Hela Restaurant Chain Poland - Łódzkie HQ", "CH_TOP_PL_LD", "", "UE_PL", "Łódź", "Poland", "ul. Piotrkowska 254", "90-003"),
            'pl_ds': self._make_entity(top_entities_countries['pl'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie HQ", "CH_TOP_PL_DS", "", "UE_PL", "Wrocław", "Poland", "al. Armii Krajowej 356", "50-014"),

            'de_land_be': self._make_entity(top_entities_countries['de'], "Ciocia Hela Restaurant Chain Germany - Land Berlin HQ", "CH_TOP_DE_LAND_BE", "", "UE_DE", "Berlin", "Germany", "Adenauerstrasse 124", "10319"),
            'de_land_sh': self._make_entity(top_entities_countries['de'], "Ciocia Hela Restaurant Chain Germany - Land Schleswig-Holstein HQ", "CH_TOP_DE_LAND_SH", "", "UE_DE", "Hamburg", "Germany", "18 Wexstrasse", "20259"),                        
            'de_land_by': self._make_entity(top_entities_countries['de'], "Ciocia Hela Restaurant Chain Germany - Land Bayern HQ", "CH_TOP_DE_LAND_BY", "", "UE_DE", "München", "Germany", "18 Agnes-Bernauer-Strasse", "82002"),                        
            'de_land_mv': self._make_entity(top_entities_countries['de'], "Ciocia Hela Restaurant Chain Germany - Land Mecklenburg-Vorpommern HQ", "CH_TOP_DE_LAND_MV", "", "UE_DE", "Schwerin", "Germany", "15 Luebeckerstrasse", "82002"),                        

            'fr_idf': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain France - Île-de-France", "CH_TOP_FR_IDF", "", "UE_FR", "Paris", "France", "157 Champs Elysees", "75004"),
            'fr_hdf': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain France - Hauts-de-France", "CH_TOP_FR_HDF", "", "UE_FR", "Lille", "France", "169 Rue Solférino", "59000"),
            'fr_pac': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur", "CH_TOP_FR_PAC", "", "UE_FR", "Marseilles", "France", "16 Canebière", "13004"),
            'fr_occ': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain France - Occitanie", "CH_TOP_FR_OCC", "", "UE_FR", "Toulouse", "France", " 17 Rue Matabiau", "31000"),

            'uk_tli': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - Greater London", "CH_TOP_UK_TLI", "", "UK", "London", "United Kingdom", "124 Piccadilly Street", "1J 9LL"),
            'uk_tld': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - North West", "CH_TOP_UK_TLD", "", "UK", "Liverpool", "United Kingdom", "155 Smithdown Rd", "L7 4JF"),
            'uk_tlj': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South East", "CH_TOP_UK_TLJ", "", "UK", "Southampton", "United Kingdom", "27 Archers Rd", "SO15 2LS"),
            'uk_tlk': self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West", "CH_TOP_UK_TLK", "", "UK", "Plymouth", "United Kingdom", "244 North Rd W", "PL1 5DG"),
        }

        # virtual hqs, used just for calculations (consolidations, aggregations etc)
        top_entities_cities_virtual_hqs = {
            'pl__pm_gda': {"m":15, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Gdańsk VHQ", "CH_TOP_PL_PM_GDA", "", "UE_PL", "Gdańsk", "Poland", "", "")},
            'pl__pm_gdy': {"m":15, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Gdynia VHQ", "CH_TOP_PL_PM_GDY", "", "UE_PL", "Gdynia", "Poland", "", "")},
            'pl__pm_sop': {"m":5, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Sopot VHQ", "CH_TOP_PL_PM_SOP", "", "UE_PL", "Sopot", "Poland", "", "")},
            'pl__pm_wej': {"m":10, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Wejherowo VHQ", "CH_TOP_PL_PM_WEJ", "", "UE_PL", "Wejherowo", "Poland", "", "")},
            'pl__pm_tcz': {"m":8, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Tczew VHQ", "CH_TOP_PL_PM_TCZ", "", "UE_PL", "Tczew", "Poland", "", "")},
            'pl__pm_prs': {"m":3, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Pruszcz VHQ", "CH_TOP_PL_PM_PRS", "", "UE_PL", "Pruszcz Gdański", "Poland", "", "")},
            'pl__pm_slp': {"m":15, "c":0, "e": self._make_entity(top_entities_country_districts['pl_pm'], "Ciocia Hela Restaurant Chain Poland - Pomorskie Słupsk VHQ", "CH_TOP_PL_PM_SLP", "", "UE_PL", "Słupsk", "Poland", "", "")},
            'pl__mz_wa': {"m": 25, "c":0, "e": self._make_entity(top_entities_country_districts['pl_mz'], "Ciocia Hela Restaurant Chain Poland - Mazowieckie Warszawa VHQ", "CH_TOP_PL_MZ_WAW", "", "UE_PL", "Warszawa", "Poland", "", "")},
            'pl__mz_wp': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['pl_mz'], "Ciocia Hela Restaurant Chain Poland - Mazowieckie Płock VHQ", "CH_TOP_PL_MZ_WAW", "", "UE_PL", "Płock", "Poland", "", "")},
            'pl__mz_wr': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['pl_mz'], "Ciocia Hela Restaurant Chain Poland - Mazowieckie Radom VHQ", "CH_TOP_PL_MZ_", "", "UE_PL", "Radom", "Poland", "", "")},
            'pl__mz_wnd': {"m": 9, "c":11, "e": self._make_entity(top_entities_country_districts['pl_mz'], "Ciocia Hela Restaurant Chain Poland - Nowy Dwór Mazowiecki VHQ", "CH_TOP_PL_MZ_", "", "UE_PL", "Nowy Dwór Mazowiecki", "Poland", "", "")},
            'pl__ld_el': {"m": 30,"c":0, "e": self._make_entity(top_entities_country_districts['pl_ld'], "Ciocia Hela Restaurant Chain Poland - Łódzkie Łódź VHQ", "CH_TOP_PL_LD_LD", "", "UE_PL", "Łódź", "Poland", "", "")},
            'pl__ld_ep': {"m": 15,"c":0, "e": self._make_entity(top_entities_country_districts['pl_ld'], "Ciocia Hela Restaurant Chain Poland - Łódzkie Piotrków Trybunalski VHQ", "CH_TOP_PL_LD_EP", "", "UE_PL", "Piotrków Trybunalski", "Poland", "", "")},
            'pl__ld_epa': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['pl_ld'], "Ciocia Hela Restaurant Chain Poland - Łódzkie Pabianice VHQ", "CH_TOP_PL_LD_EPA", "", "UE_PL", "Pabianice", "Poland", "", "")},
            'pl__ds_dw': {"m": 20,  "c":0, "e": self._make_entity(top_entities_country_districts['pl_ds'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie Wrocław VHQ", "CH_TOP_PL_DS_DW", "", "UE_PL", "Wrocław", "Poland", "", "")},
            'pl__ds_db': {"m": 10,  "c":0, "e": self._make_entity(top_entities_country_districts['pl_ds'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie Wałbrzych VHQ", "CH_TOP_PL_DS_DB", "", "UE_PL", "Wałbrzych", "Poland", "", "")},
            'pl__ds_dj': {"m": 10,  "c":0, "e": self._make_entity(top_entities_country_districts['pl_ds'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie Jelenia Góra VHQ", "CH_TOP_PL_DS_DJ", "", "UE_PL", "Jelenia Góra", "Poland", "", "")},
            'pl__ds_dl': {"m": 15,  "c":0, "e": self._make_entity(top_entities_country_districts['pl_ds'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie Legnica VHQ", "CH_TOP_PL_DS_DL", "", "UE_PL", "Legnica", "Poland", "", "")},
            'pl__ds_dlu': {"m": 15, "c":10, "e": self._make_entity(top_entities_country_districts['pl_ds'], "Ciocia Hela Restaurant Chain Poland - Dolnośląskie Lubin VHQ", "CH_TOP_PL_DS_DLU", "", "UE_PL", "Lubin", "Poland", "", "")},
            'de__land_be_be': {"m": 30, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_be'], "Ciocia Hela Restaurant Chain Germany - Land Berlin - Berlin VHQ", "CH_TOP_DE_LAND_BE", "", "UE_DE", "Berlin", "Germany", "", "")},
            'de__land_sh_hh': {"m": 30, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_sh'], "Ciocia Hela Restaurant Chain Germany - Land Schleswig-Holstein - Hamburg VHQ", "CH_TOP_DE_LAND_SH_HH", "", "UE_DE", "Hamburg", "Germany", "", "")},
            'de__land_sh_hl': {"m": 25, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_sh'], "Ciocia Hela Restaurant Chain Germany - Land Schleswig-Holstein - Lübeck VHQ", "CH_TOP_DE_LAND_SH_HL", "", "UE_DE", "Lübeck", "Germany", "", "")},
            'de__land_sh_hb': {"m": 20, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_sh'], "Ciocia Hela Restaurant Chain Germany - Land Schleswig-Holstein - Bremen VHQ", "CH_TOP_DE_LAND_SH_HB", "", "UE_DE", "Bremen", "Germany", "", "")},
            'de__land_by_muc': {"m": 25, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_by'], "Ciocia Hela Restaurant Chain Germany - Land Bayern -	München VHQ", "CH_TOP_DE_LAND_BY_MUC", "", "UE_DE", "München", "Germany", "", "")},
            'de__land_by_n': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_by'], "Ciocia Hela Restaurant Chain Germany - Land Bayern - Nürnberg VHQ", "CH_TOP_DE_LAND_BY_N", "", "UE_DE", "Nürnberg", "Germany", "", "")},
            'de__land_by_a': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_by'], "Ciocia Hela Restaurant Chain Germany - Land Bayern - Augsburg VHQ", "CH_TOP_DE_LAND_BY_A", "", "UE_DE", "Augsburg", "Germany", "", "")},
            'de__land_mv_hro': {"m": 18, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_mv'], "Ciocia Hela Restaurant Chain Germany - Land Mecklenburg-Vorpommern - Rostock VHQ", "CH_TOP_DE_LAND_MV_HRO", "", "UE_DE", "Rostock", "Germany", "", "")},
            'de__land_mv_sn': {"m": 15, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_mv'], "Ciocia Hela Restaurant Chain Germany - Land Mecklenburg-Vorpommern - Schwerin VHQ", "CH_TOP_DE_LAND_MV_SN", "", "UE_DE", "Schwerin", "Germany", "", "")},
            'de__land_mv_hgw': {"m": 20, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_mv'], "Ciocia Hela Restaurant Chain Germany - Land Mecklenburg-Vorpommern - Schwerin VHQ", "CH_TOP_DE_LAND_MV_SN", "", "UE_DE", "Schwerin", "Germany", "", "")},
            'de__land_mv_nb': {"m": 13, "c":0, "e": self._make_entity(top_entities_country_districts['de_land_mv'], "Ciocia Hela Restaurant Chain Germany - Land Mecklenburg-Vorpommern - Neubrandenburg VHQ", "CH_TOP_DE_LAND_MV_NB", "", "UE_DE", "Neubrandenburg", "Germany", "", "")},
            'fr__idf_par': {"m": 40, "c":0, "e": self._make_entity(top_entities_country_districts['fr_idf'], "Ciocia Hela Restaurant Chain France - Île-de-France - Paris VHQ", "CH_TOP_FR_IDF_PAR", "", "UE_FR", "Paris", "France", "", "")},
            'fr__idf_hds': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['fr_idf'], "Ciocia Hela Restaurant Chain France - Île-de-France - Hauts-de-Seine VHQ", "CH_TOP_FR_IDF_HDS", "", "UE_FR", "Hauts-de-Seine", "France", "", "")},
            'fr__idf_vdo': {"m": 15, "c":0, "e": self._make_entity(top_entities_country_districts['fr_idf'], "Ciocia Hela Restaurant Chain France - Île-de-France - Val-d'Oise VHQ", "CH_TOP_FR_IDF_VDS", "", "UE_FR", "Val-d'Oise", "France", "", "")},
            'fr__idf_ssd': {"m": 20, "c":0, "e": self._make_entity(top_entities_country_districts['fr_idf'], "Ciocia Hela Restaurant Chain France - Île-de-France - Seine-Saint-Denis VHQ", "CH_TOP_FR_IDF_VDS", "", "UE_FR", "Seine-Saint-Denis", "France", "", "")},
            'fr__hdf_lil': {"m": 15, "c":0, "e": self._make_entity(top_entities_country_districts['fr_hdf'], "Ciocia Hela Restaurant Chain France - Hauts-de-France - Lille VHQ", "CH_TOP_FR_HDF_LIL", "", "UE_FR", "Lille", "France", "", "")},
            'fr__hdf_doi': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['fr_hdf'], "Ciocia Hela Restaurant Chain France - Hauts-de-France - Douai VHQ", "CH_TOP_FR_HDF_DOI", "", "UE_FR", "Douai", "France", "", "")},
            'fr__hdf_lns': {"m": 5, "c":0, "e": self._make_entity(top_entities_country_districts['fr_hdf'], "Ciocia Hela Restaurant Chain France - Hauts-de-France - Lens VHQ", "CH_TOP_FR_HDF_LNS", "", "UE_FR", "Lens", "France", "", "")},
            'fr__hdf_btn': {"m": 13, "c":0, "e": self._make_entity(top_entities_country_districts['fr_hdf'], "Ciocia Hela Restaurant Chain France - Hauts-de-France - Béthune VHQ", "CH_TOP_FR_HDF_BTN", "", "UE_FR", "Béthune", "France", "", "")},
            'fr__hdf_vcn': {"m": 12, "c":0, "e": self._make_entity(top_entities_country_districts['fr_hdf'], "Ciocia Hela Restaurant Chain France - Hauts-de-France - Valenciennes VHQ", "CH_TOP_FR_HDF_VCN", "", "UE_FR", "Valenciennes", "France", "", "")},
            'fr__pac_mrs': {"m": 25, "c":0, "e": self._make_entity(top_entities_country_districts['fr_pac'], "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur - Marseilles VHQ", "CH_TOP_FR_PAC_MRS", "", "UE_FR", "Marseilles", "France", "", "")},
            'fr__pac_tou': {"m": 20, "c":0, "e": self._make_entity(top_entities_country_districts['fr_pac'], "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur - Toulon VHQ", "CH_TOP_FR_PAC_TOU", "", "UE_FR", "Toulon", "France", "", "")},
            'fr__pac_aix': {"m": 10, "c":0, "e": self._make_entity(top_entities_country_districts['fr_pac'], "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur - Aix-en-Provence VHQ", "CH_TOP_FR_PAC_AIX", "", "UE_FR", "Aix-en-Provence", "France", "", "")},
            'fr__pac_nic': {"m": 25, "c":0, "e": self._make_entity(top_entities_country_districts['fr_pac'], "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur - Nice VHQ", "CH_TOP_FR_PAC_NIC", "", "UE_FR", "Nice", "France", "", "")},
            'fr__pac_avn': {"m": 30, "c":0, "e": self._make_entity(top_entities_country_districts['fr_pac'], "Ciocia Hela Restaurant Chain France - Provence-Alpes-Côte d’Azur - Avignon VHQ", "CH_TOP_FR_PAC_AVI", "", "UE_FR", "Avignon", "France", "", "")},
            'fr__occ_tou': {"m": 27, "c":0, "e": self._make_entity(top_entities_country_districts['fr_occ'], "Ciocia Hela Restaurant Chain France - Occitanie - Toulouse VHQ", "CH_TOP_FR_OCC_TOU", "", "UE_FR", "Toulouse", "France", "", "")},
            'fr__occ_mpl': {"m": 13, "c":0, "e": self._make_entity(top_entities_country_districts['fr_occ'], "Ciocia Hela Restaurant Chain France - Occitanie - Montpellier VHQ", "CH_TOP_FR_OCC_MPL", "", "UE_FR", "Montpellier", "France", "", "")},
            'fr__occ_nim': {"m": 14, "c":0, "e": self._make_entity(top_entities_country_districts['fr_occ'], "Ciocia Hela Restaurant Chain France - Occitanie - Nîmes VHQ", "CH_TOP_FR_OCC_NIM", "", "UE_FR", "Nîmes", "France", "", "")},
            'fr__occ_ppn': {"m": 12, "c":0, "e": self._make_entity(top_entities_country_districts['fr_occ'], "Ciocia Hela Restaurant Chain France - Occitanie - Perpignan VHQ", "CH_TOP_FR_OCC_PPN", "", "UE_FR", "Perpignan", "France", "", "")},
            'fr__occ_bzr': {"m": 14, "c":0, "e": self._make_entity(top_entities_country_districts['fr_occ'], "Ciocia Hela Restaurant Chain France - Occitanie - Béziers VHQ", "CH_TOP_FR_OCC_BZR", "", "UE_FR", "Béziers", "France", "", "")},
            'uk__tli_lon': {"m": 50, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - Greater London - London VHQ", "CH_TOP_UK_TLI_LON", "", "UK", "London", "United Kingdom", "", "")},
            'uk__tld_liv': {"m": 30, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - North West - Liverpool VHQ", "CH_TOP_UK_TLD", "", "UK", "Liverpool", "United Kingdom", "", "")},
            'uk__tld_man': {"m": 20, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - North West - Manchester VHQ", "CH_TOP_UK_TLD", "", "UK", "Liverpool", "United Kingdom", "", "")},
            'uk__tlj_shm': {"m": 18, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South East - Southampton VHQ", "CH_TOP_UK_TLJ_SHM", "", "UK", "Southampton", "United Kingdom", "", "")},
            'uk__tlj_btc': {"m": 20, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South East - Brighton and Cove VHQ", "CH_TOP_UK_TLJ_BTC", "", "UK", "Brighton and Cove", "United Kingdom", "", "")},
            'uk__tlj_cnt': {"m": 15, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South East - Canterbury VHQ", "CH_TOP_UK_TLJ_CNT", "", "UK", "Canterbury", "United Kingdom", "", "")},
            'uk__tlj_pts': {"m": 10, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South East - Portsmouth VHQ", "CH_TOP_UK_TLJ_PTS", "", "UK", "Portsmouth", "United Kingdom", "", "")},
            'uk__tlk_plm': {"m": 10, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West - Plymouth VHQ", "CH_TOP_UK_TLK_PLM", "", "UK", "Plymouth", "United Kingdom", "", "")},
            'uk__tlk_brs': {"m": 14, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West - Bristol VHQ", "CH_TOP_UK_TLK_BRS", "", "UK", "Bristol", "United Kingdom", "", "")},
            'uk__tlk_brm': {"m": 16, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West - Bournemouth VHQ", "CH_TOP_UK_TLK_BRS", "", "UK", "Bournemouth", "United Kingdom", "", "")},
            'uk__tlk_clt': {"m": 11, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West - Cheltenham VHQ", "CH_TOP_UK_TLK_CLT", "", "UK", "Cheltenham", "United Kingdom", "", "")},
            'uk__tlk_ext': {"m": 14, "c":0, "e": self._make_entity(top_entity, "Ciocia Hela Restaurant Chain Britain - South West - Exeter VHQ", "CH_TOP_UK_TLK_ext", "", "UK", "Exeter", "United Kingdom", "", "")},
        }

        entities_leaves = {}

        streets_pl = ['Al. Grunwaldzka', 
                      'Al. Tadeusza Kościuszki', 
                      'ul. Adama Mickiewicza',  
                      'Al. gen. Józefa Hallera', 
                      'Al. Armii Krajowej', 
                      'Al. Marszałka Józefa Piłsudskiego', 
                      'ul. Zbigniewa Herberta',
                      'ul. Marii Dąbrowskiej',
                      'ul. Henryka Sienkiewicza',
                      'ul. Krzysztofa Kamila Baczyńskiego',
                      'ul. Kaletnicza',
                      'ul. Zofii Nałkowskiej',
                      'al. Marii Skłodowskiej-Curie',
                      'ul. Juliusza Słowackiego', 
                      'ul. Szewska',
                      'ul. Krawiecka',
                      'ul. Wałowa',
                      'ul. Podwale',
                      'ul. Admiralska',
                      'ul. Cypriana Kamila Norwida',
                      'ul. Wspólna',
                      'ul. Kowalska',
                      'ul. Rzemieślnicza',
                      'ul. Rzeźnicka',
                      'Al. Jana Pawła II', 
                      'ul. Długa', 
                      'ul. Emilii Plater',
                      'ul. Wesoła',
                      'ul. Czesława Miłosza',
                      'ul. Kwiatowa', 
                      'ul. Powstańców Warszawskich',
                      'ul. Ireny Sendlerowej',
                      'Al. Generała Władysława Sikorskiego',
                      'Al. Marii Konopnickiej',
                      'ul. Ewy Szelburg-Zarembiny',
                      'ul. Akacjowa', 
                      'ul. Adama Asnyka',
                      'ul. Wisławy Szymborskiej',
                      'ul. Podmiejska',
                      'ul. Kręta', 
                      'ul. Szeroka', 
                      'ul. Bolesława Prusa',
                      'ul. Elizy Orzeszkowej',
                      'ul. Rzeczna', 
                      'ul. Starowiejska',
        ]
        streets_de = ['Konrad-Adenauer-Strasse', 'Hamburger Strasse', 'Willy-Brandt-Strasse', 'Wolfgang-Amadeus-Mozart-Strasse', 'Ludwig-Johann-von-Beethoven-Strasse', 'Koenigstrasse']
        streets_fr = ['Rue Guy Fabre', 
                      'Rue Victor Hugo', 
                      'Avenue Charles de Gaulle', 
                      'Place de la République', 
                      'Rue Jacques Brel', 
                      'Rue Duivier', 
                      'Rue Baillet',
                      'Rue Montorgueil',
                      'Rue Joe Dassin',
                      'Rue Louis de Funès',
                      'Rue Jacques Brel',
                      'Rue François Mitterrand',
                      'Rue Jacques Brel',
                      'Boulevard Chave',
                      'Rue François Villon',
                      "Rue Marie Sklodowska-Curie",
                      "Rue Edith Piaf",
                      "Rue de l'Éventail",
                      "Rue Giacomo Mattéoti",
                      "Rue Lavoisier",
                      'Boulevard de Gaulle',
                      "Rue d'Artagnan",
                      'Avenue Montaigne',
                      "Rue Richelieu",
                      'Rue Jacques Yves Cousteau',
                      'Rue du Commandant Cousteau',
                      'Rue Van Gogh',
                      'Rue de Versailles',
                      "Rue de l'Hospital",
                      'Avenue de Versailles',
                      "Rue Marquis",
                      'Rue Louis Comte',
                      'Rue Claude Monet',
                      'Rue Louis Malle',
                      'Rue Louis Pasteur',
                      'Rue de Rivoli',
                      'Rue de Tocqueville',
                      'Rue du Tapis-Vert',
                      'Rue Danton',
                      'Rue de la Gare',
                      'Rue Robespierre',
                      'Place Charles de Gaulle',
                      'Avenue Jean Moulin',
                      'Cours Saint-Louis',
                      'Av. de Tourville', 
                      'Avenue Alexandre Dumas']
        streets_uk = ['Shaw Street', 
                      'Eastgate', 
                      'Westgate', 
                      'North Gate', 
                      'South Gate', 
                      'Victoria Road',
                      'Victoria Street',
                      'Lancaster Street', 
                      'Orchard Street', 
                      'Princess Street', 
                      'William Harris Way', 
                      'Nelson Street',
                      'Windsor Street',
                      'Station Street',
                      'High Street',
                      'Tudor Street', 
                      'Canal Street', 
                      'Travers Street',
                      'Port Street',
                      'Boston Rd', 
                      'Wood Street',
                      'Forest Street',
                      'William Shakespeare Street',
                      'Shepherd Street', 
                      'Blake Street',
                      'Albany Rd', 
                      'King George Street', 
                      'King Albert Street', 
                      "King Henry's Road",
                      "King Richard Street",
                      "King Edward Street",
                      "St Bartholomew Street",
                      'King James Street',
                      "King Cross Road",
                      'Mercia Road', 
                      'Winston Churchill Avenue',
                      'Winchester Street',
                      'York Street', 
                      'Tolkien Road',
                      'Veterans Street', 
                      'Cromwell Street', 
                      'Main Street',
                      "Park Road",
                      "Church Road",
                      "Church Street",
                      "London Road",
                      "Queen Elizabeth Street", 
                      "Queen Mary Street", 
                      "King John Street" ]

        street = ""

        for i in top_entities_cities_virtual_hqs:
            ent = top_entities_cities_virtual_hqs[i]
            for j in range(0, ent['m']):
                if i.find("pl__") != -1:
                    street = random.choice(streets_pl)
                elif i.find('fr__') != -1:
                    street = random.choice(streets_fr)
                elif i.find('de__') != -1:
                    street = random.choice(streets_de)
                    pass
                elif i.find('uk__') != -1:
                    street = random.choice(streets_uk)
                    pass
                number = random.randrange(1, 125)
                code_name = i + "_outlet_" + str(j + 1)
                parent = ent['e']
                leaf = self._make_entity(ent['e'], code_name.upper(), code_name.upper(), "", parent.region, parent.addr_city, 
                                  parent.addr_country_name, parent.addr_details, parent.addr_postal_code, True, True)
                
                entities_leaves[code_name] = leaf

        top_prod = self._make_product(None, "Products", "products", "Products","000-000-000-000")

            # entities_leaves

        # e = models.DimEntity

        d_top = self._make_product(top_prod, "Potrawy", "dishes", "Gotowe potrawy", "") 
        d_breakfast = self._make_product(d_top, "Dania śniadaniowe/Breakfast dishes", "brk_dishes", "Dania śniadaniowe/Breakfast dishes", "")
        d_dinner = self._make_product(d_top, "Dania obiadowe/Dinner dishes", "din_dishes", "Dania obiadowe/Dinner dishes", "")
        d_supper = self._make_product(d_top, "Kolacje/Supper dishes", "sup_dishes", "Kolacje/Supper dishes", "")
        d_extras = self._make_product(d_top, "Dodatki/Extras", "extras", "Dodatki/Extras", "")
        d_starters = self._make_product(d_top, "Przekąski/starters", "starters", "Przekąski/starters", "")
        d_drinks_non_alco = self._make_product(d_top, "Napoje bezalkoholowe/Non-alcoholic beverages", "d_drinks_non_alco", "Napoje bezalkoholowe/Non-alcoholic beverages", "")
        d_drinks_alco = self._make_product(d_top, "Napoje alkoholowe/Alcoholic beverages", "d_drinks_alco", "Napoje alkoholowe/Alcoholic beverages", "")
                

        foods = {
            'd_d_01' : {'price_eur': 10.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Schabowy/Pork cutlet", "din_01", "Schabowy/pork cutlet", "001-000-011")},
            'd_d_02' : {'price_eur': 11.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Hamburger", "din_02", "Hamburger", "001-000-012")},
            'd_d_03' : {'price_eur': 8.2,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Zupa Rybna/Fish Soup", "din_03", "Zupa Rybna/Fish Soup", "001-000-013")},
            'd_d_04' : {'price_eur': 8.5,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Rosół z kury/Chicken broth", "din_04", "Rosół z kury/Chicken broth", "001-000-014")},
            'd_d_05' : {'price_eur': 13.4, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Naleśniki z jagodami/Pancakes with blueberries", "din_05", "Naleśniki z jagodami/Pancakes with blueberries", "001-000-015")},
            'd_d_06' : {'price_eur': 18.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Dorsz smażony/Fried cod", "din_06", "Dorsz smażony/Fried cod", "001-000-016")},
            'd_d_07' : {'price_eur': 17.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Dorsz pieczony/Baked cod", "din_07", "Dorsz pieczony/Baked cod", "001-000-017")},
            'd_d_08' : {'price_eur': 15.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Flaki/tripe dish", "din_08", "Flaki/tripe dish", "001-000-018")},
            'd_d_09' : {'price_eur': 7.0,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Kotlet mielony/Meatloaf", "din_09", "Kotlet mielony/Meatloaf", "001-000-019")},
            'd_d_10' : {'price_eur': 16.0, 'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_dinner, "Kurczak pieczony/Roasted chicken", "din_10", "Kurczak pieczony/Roasted chicken", "001-000-020")},
            'd_b_01' : {'price_eur': 6.0,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_breakfast, "Jajka i bekon/Eggs and bacon", "brk_01", "Jajka i bekon/Eggs and bacon", "001-000-002")},
            'd_e_01' : {'price_eur': 1.0,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_breakfast, "Gotowane ziemniaki/Boiled potatoes", "ext_01", "Gotowane ziemniaki/Boiled potatoes", "001-000-003")},
            'd_e_02' : {'price_eur': 2.0,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_breakfast, "Frytki/French Fries", "ext_02", "Frytki/French Fries", "001-000-004")},
            'd_e_03' : {'price_eur': 2,    'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_breakfast, "Pieczone ziemniaki/Baked potatoes", "ext_03", "Pieczone ziemniaki/Baked potatoes", "001-000-005")},
            'd_e_04' : {'price_eur': 0.5,  'price_pln': 0, 'price_gbp': 0.0, 'prd': self._make_product(d_breakfast, "Chleb/Bread", "ext_04", "Chleb/Bread", "001-000-006")},
        }

        drinks_non_alco = {
            'coffee':          {'price_eur': 1.5, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Kawa/Coffee", "drn_cof", "Kawa/Coffee", "001-000-111")},
            'espresso':        {'price_eur': 1.6, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Kawa Espresso/Espresso Coffee", "drn_cof_esp", "Kawa/Espresso", "001-000-112")},
            'latte':           {'price_eur': 2.0, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Kawa Latte/Latte Coffee", "drn_cof_lat", "Kawa Latte/Latte Coffee", "001-000-113")},
            'tea':             {'price_eur': 1.2, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Herbata/Tea", "drinks_tea", "Herbata/Tea", "001-000-121")},
            'gr_tea':          {'price_eur': 1.3, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Zielona Herbata/Green Tea", "drinks_tea", "Zielona Herbata/Green Tea", "001-000-122")},
            'cola':            {'price_eur': 0.7, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Cola 0.5L", "drn_co_05l", "Cola 0.5L", "001-000-104")},
            'orange_juice':    {'price_eur': 1.0, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Sok pomarańczowy/Orange Juice 0.5L", "drn_or_ju_05l", "Cola 0.5L", "001-000-105")},
            'water_bubble':    {'price_eur': 0.9, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Woda gazowana 0.5L", "drinks_bubble_water_05L", "Woda gazowana 0.5L", "001-000-106")},
            'water_flat':      {'price_eur': 0.8, 'price_pln': 0.0, 'price_gbp': 0.0,   'prd':  self._make_product(d_drinks_non_alco, "Woda niegazowana 0.5L", "drinks_flat_water_05L", "Woda niegazowana 0.5L", "001-000-107")},
        }        

        drinks_alco = {
            'beer_pils':            {"price_eur": 2.0,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo pils/Pils beer", "drn_br_pls", "Piwo pils/Pils beer", "001-002-101")},
            'beer_ale':             {"price_eur": 2.4,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo górnej fermentacji/Ale beer", "drn_br_ale", "Piwo górnej fermentacji/Ale beer", "001-002-102")},
            'beer_wheat':           {"price_eur": 2.8,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo pszeniczne/Wheat beer", "drn_br_wht", "Piwo pszeniczne/Wheat beer", "001-002-103")},
            'beer_dark':            {"price_eur": 2.5,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo ciemne/Dark beer", "drn_br_drk", "Piwo ciemne/Dark beer", "001-002-104")},
            'beer_non_alco_wht':    {"price_eur": 2.1,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo bezalkoholowe pszeniczne/Non-alcoholic beer (wheat)", "drn_br_drk", "Piwo bezalkoholowe pszeniczne/Non-alcoholic beer (wheat)", "001-002-105")},
            'beer_non_alco_pls':    {"price_eur": 2.2,  "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Piwo bezalkoholowe pils/Non-alcoholic beer (pils)", "drn_br_drk", "Piwo bezalkoholowe pils/Non-alcoholic beer (pils)", "001-002-106")},
            'wine_red_dry':         {"price_eur": 15.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino czerwone wytrawne/Dry red wine", "drn_br_drk", "Wino czerwone wytrawne/Dry red wine", "001-003-101")},
            'wine_red_med':         {"price_eur": 13.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino czerwone półwytrawne/Medium Dry red wine", "drn_br_drk", "Wino czerwone półwytrawne/Medium Dry red wine", "001-003-102")},
            'wine_red_sweet':       {"price_eur": 10.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino czerwone słodkie/Sweet red wine", "drn_br_drk", "Wino czerwone słodkie/Sweet red wine", "001-003-103")},
            'wine_white_dry':       {"price_eur": 11.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino białe wytrawne/Dry white wine", "drn_br_drk", "Wino białe wytrawne/Dry white wine", "001-003-104")},
            'wine_white_med':       {"price_eur": 14.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino białe półwytrawne/Medium Dry white wine", "drn_br_drk", "Wino białe półwytrawne/Medium Dry white wine", "001-003-105")},
            'wine_white_sweet':     {"price_eur": 15.0, "price_pln": 0.0, "price_gbp": 0.0,   "prd": self._make_product(d_drinks_alco, "Wino białe słodkie/Sweet white wine", "drn_br_drk", "Wino białe słodkie/Sweet white wine", "001-003-106")},
        }

        for i in foods:
            foods[i]['price_pln'] = 4.31* foods[i]['price_eur']
            foods[i]['price_gbp'] = 0.86* foods[i]['price_eur']

        for i in drinks_non_alco:
            drinks_non_alco[i]['price_pln'] = 4.31* drinks_non_alco[i]['price_eur']
            drinks_non_alco[i]['price_gbp'] = 0.86* drinks_non_alco[i]['price_eur']

        for i in drinks_alco:
            drinks_alco[i]['price_pln'] = 4.31* drinks_alco[i]['price_eur']
            drinks_alco[i]['price_gbp'] = 0.86* drinks_alco[i]['price_eur']


        d_scen_top = self._make_scenario(None, "Scenario", "SCN", "Scenario", "label")
        d_scen_act = self._make_scenario(d_scen_top, "Actual", "SCN_ACT", "Actual", "actual")
        d_scen_est = self._make_scenario(d_scen_top, "Estimate", "SCN_EST", "Estimate", "estimate")
        d_scen_for = self._make_scenario(d_scen_top, "Forecast", "SCN_FOR", "Forecast", "forecast")
        d_scen_elb = self._make_scenario(d_scen_top, "Elab", "SCN_ELB", "Elab", "elab")
        d_scen_rol = self._make_scenario(d_scen_top, "Rolling", "SCN_ROL", "Rolling", "rolling")

        d_acc_top = self._make_account(None, "Account", "ACC", "Account", None, None, None, None, True)

        # https://www.accountingtools.com/articles/chart-of-accounts-numbering.html
        d_acc_category_assets_top = self._make_account(d_acc_top, "Assets", "ACC_AST", "Assets", None, None, "100", "199", True)
        d_acc_category_liabilities_top = self._make_account(d_acc_top, "Liabilities", "ACC_LBL", "Liabilities", None, None, "200", "299", True)
        d_acc_category_equities_top = self._make_account(d_acc_top, "Equities", "ACC_EQT", "Equities", None, None, "300", "399", True)
        d_acc_category_revenues_top = self._make_account(d_acc_top, "Revenues", "ACC_RVN", "Revenues", None, None, "400", "499", True)
        d_acc_category_expenses_top = self._make_account(d_acc_top, "Expenses", "ACC_EXP", "Expenses", None, None, "500", "599", True)

        # d_acc_3digit_top = self._make_account(d_acc_top, "3-digit account", "ACC_3DG", "3-digit account", None, None, None, None, True)
        # d_acc_3digit_top = self._make_account(d_acc_top, "5-digit account", "ACC_5DG", "5-digit account", None, None, None, None, True)
        # d_acc_7digit_top = self._make_account(d_acc_top, "7-digit account", "ACC_7DG", "7-digit account", None, None, None, None, True)
        
        m_top = self._make_measurement(None, "Measurement", "MSM_TOP", "Measurement", "")
        m_sal_cnt = self._make_measurement(m_top, "Sales Volume", "MSM_SAL_CNT", "Sales Volume", "cnt")
        
        m_top_sal_rev = self._make_measurement(m_top, "Sales Revenue", "MSM_SAL_REV", "Sales Revenue", "")

        m_rev_eur = self._make_measurement(m_top_sal_rev, "Sales Revenue EUR", "MSM_SAL_REV_EUR", "Sales Revenue EUR", "cur:EUR")
        m_rev_pln = self._make_measurement(m_top_sal_rev, "Sales Revenue PLN", "MSM_SAL_REV_PLN", "Sales Revenue PLN", "cur:PLN")
        m_rev_usd = self._make_measurement(m_top_sal_rev, "Sales Revenue USD", "MSM_SAL_REV_USD", "Sales Revenue USD", "cur:USD")
        m_rev_gbp = self._make_measurement(m_top_sal_rev, "Sales Revenue GBP", "MSM_SAL_REV_GBP", "Sales Revenue GBP", "cur:GBP")

        m_top_acb = self._make_measurement(m_top, "Account Balance", "MSM_ACB", "Account Balance", "")
        m_acb_pln = self._make_measurement(m_top_acb, "Account Balance PLN", "MSM_ACB_PLN", "Account Balance PLN", "cur:PLN")
        m_acb_eur = self._make_measurement(m_top_acb, "Account Balance EUR", "MSM_ACB_EUR", "Account Balance EUR", "cur:EUR")
        m_acb_usd = self._make_measurement(m_top_acb, "Account Balance USD", "MSM_ACB_USD", "Account Balance USD", "cur:USD")
        m_acb_gbp = self._make_measurement(m_top_acb, "Account Balance GBP", "MSM_ACB_GBP", "Account Balance GBP", "cur:GBP")
        
        start_year = 2014
        end_year = 2034


        ti_years = {}
        ti_yhs = {}
        ti_yqs = {}
        ti_yms = {}
        ti_ymds = {}

        for year in range(start_year, end_year + 1):
            y_code_name = f"{year}"
            d_y = self._make_time(None, y_code_name, y_code_name, y_code_name, models.DimTime.TYPE_YEAR)
            ti_years[y_code_name] = d_y

            for half in range(1, 2 + 1):
                yh_code_name = f"{year}H0{half}"
                d_yh = self._make_time(d_y, yh_code_name, yh_code_name, yh_code_name, models.DimTime.TYPE_HALF_YEAR)
                ti_yhs[yh_code_name] = d_yh

            for quarter in range(1, 4 + 1):
                yq_code_name = f"{year}Q0{quarter}"
                d_yq = self._make_time(d_y, yq_code_name, yq_code_name, yq_code_name, models.DimTime.TYPE_QUARTER)
                ti_yqs[yq_code_name] = d_yq

            for month in range(1, 12 + 1): 
                month_label = models.TimeService.pad_zero_if_needed(month)
                ym_code_name = f"{year}M{month_label}"
                d_ym = self._make_time(d_y, ym_code_name, ym_code_name, ym_code_name, models.DimTime.TYPE_MONTH)
                ti_yms[ym_code_name] = d_ym

                for day in range(1, models.TimeService.get_last_day_of_month(year, month) + 1):
                    day_label = models.TimeService.pad_zero_if_needed(day)
                    ymd_code_name = f"{year}M{month_label}D{day_label}"
                    d_ymd = self._make_time(d_ym, ymd_code_name, ymd_code_name, ymd_code_name, models.DimTime.TYPE_DAY)
                    ti_ymds[ymd_code_name] = d_ymd

        self._make_cube_def(None, "Test Cube 1", "test_cube_1", "Test Cube 1 ABC", "RevOlapCubeFact_CubeTest1", {
            'time': 'DimTime', 
            'scenario': 'DimScenario', 
            'entity': 'DimEntity', 
            'account': 'DimAccount', 
            'product': 'DimProduct', 
            'origin': 'DimOrigin', 
            'measurement': 'Measurement'})

        year_price_factors = {
            2014: 1.0,
            2015: 1.15,
            2016: 1.20,
            2017: 1.11,
            2018: 1.09,
            2019: 1.10,
            2020: 1.01,
            2021: 1.06,
            2022: 1.08,
            2023: 1.09,
            2024: 1.30,
            2025: 1.29,
            2026: 1.31,
            2027: 1.33,
            2028: 1.21,
            2029: 1.24,
            2030: 1.22,
            2031: 1.24,
            2032: 1.23,
            2033: 1.21,
            2034: 1.20,
        }

        for ymd_cn in ti_ymds:
            ymd_obj = ti_ymds[ymd_cn]
            if ymd_obj.year in year_price_factors:
                price_factor = year_price_factors[ymd_obj.year]
            else:
                price_factor = 1.0

            print(f"\n====== FACT CN: {ymd_cn} YEAR: {ymd_obj.year} PRICE FACTOR: {price_factor} \n")
            for ent_cn in entities_leaves:
                ent_obj = entities_leaves[ent_cn]
                if ent_cn.find('pl__') == 0:   # POLAND
                    price_handle = 'price_pln'
                    mes_rev_cur = m_rev_pln
                elif (ent_cn.find('fr__') == 0) or (ent_cn.find('de__') == 0) :   # FRANCE, GERMANY
                    price_handle = 'price_eur'
                    mes_rev_cur = m_rev_eur
                elif (ent_cn.find('uk__') == 0) or (ent_cn.find('uk__') == 0) :   # UNITED KINGDOM
                    price_handle = 'price_gbp'
                    mes_rev_cur = m_rev_eur
                else:
                    price_handle = 'price_eur'
                    mes_rev_cur = m_rev_eur

                print(f"\n====== FACT: {ymd_cn} ENT: {ent_cn} PRICE HANDLE: {price_handle} \n")

                for prd_i in foods:
                    price = foods[prd_i][price_handle] * price_factor
                    val_cnt = random.randrange(100, 1999)
                    val_money = val_cnt * price 
                    print(f"\n========== PRD {foods[prd_i]['prd'].name}. PRICE HANDLE: {price_handle} PRICE: {price} VAL CNT: {val_cnt} VAL MONEY: {val_money} \n")
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, foods[prd_i]['prd'], None, m_sal_cnt, val_cnt)
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, foods[prd_i]['prd'], None, mes_rev_cur, val_money)

                for prd_i in drinks_non_alco:
                    price = drinks_non_alco[prd_i][price_handle] * price_factor
                    val_cnt = random.randrange(100, 1999)
                    val_money = val_cnt * price 
                    print(f"\n========== PRD {drinks_non_alco[prd_i]['prd'].name}. PRICE HANDLE: {price_handle} PRICE: {price} VAL CNT: {val_cnt} VAL MONEY: {val_money} \n")
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, drinks_non_alco[prd_i]['prd'], None, m_sal_cnt, val_cnt)
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, drinks_non_alco[prd_i]['prd'], None, mes_rev_cur, val_money)

                for prd_i in drinks_alco:
                    price = drinks_alco[prd_i][price_handle] * price_factor
                    val_cnt = random.randrange(100, 1999)
                    val_money = val_cnt * price 
                    print(f"\n========== PRD {drinks_alco[prd_i]['prd'].name}. PRICE HANDLE: {price_handle} PRICE: {price} VAL CNT: {val_cnt} VAL MONEY: {val_money} \n")
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, drinks_alco[prd_i]['prd'], None, m_sal_cnt, val_cnt)
                    self._make_fact_CubeTest1(None, ymd_obj, d_scen_act, ent_obj, None, drinks_alco[prd_i]['prd'], None, mes_rev_cur, val_money)

        # self._make_fact_CubeTest1(None)
        ALL_DT_END = dt.datetime.now()
        print("\n\n============ [[[[[[[[[[[[[[[[[[ ----- TIME STATISTICS ----- ]]]]]]]]]]]]]]]]]] ============= \n\n")
        print(f"\n\n============ STARTED AT: {ALL_DT_START.strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        print(f"\n\n============ FINISHED AT: {ALL_DT_END.strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        print("\n\n============ [[[[[[[[[[[[[[[[[[ ----- /TIME STATISTICS ----- ]]]]]]]]]]]]]]]]]] ============= \n\n")

