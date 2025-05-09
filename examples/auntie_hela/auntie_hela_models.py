import uuid
import re
import math
import calendar
import datetime as dt
from django.db import models
from django.utils import timezone as django_tz

# DimEntity
# DimProduct
# DimScenario
# DimAccount
# Measurement
# DimTime
# RevOlapCubeDef
# RevOlapCubeFact_CubeTest1


class TimeService:
    @staticmethod 
    def pad_zero_if_needed(i: int):
        return f"0{i}" if i < 10 else f"{i}"

    @staticmethod 
    def get_last_day_of_month(year: int, month: int):
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def get_half_year_from_month(month: int):
        return math.ceil(month / 6)
    
    @staticmethod
    def get_start_month_for_half_year(half_year: int):
        return 1 + 6 * (half_year -1)

    @staticmethod
    def get_start_month_for_quarter(quarter: int):
        return 1 + 3 * (quarter - 1)

    @staticmethod
    def get_quarter_from_month(month: int):
        return math.ceil(month / 3)

    def get_year_and_half_from_period(period: str):
        x = re.match('([0-9]{4})H([0-9]{1,2})', period)
        if not x:
            return None, None
        return int(x.group(1)), int(x.group(2))

    def get_year_and_quarter_from_period(period: str):
        x = re.match('([0-9]{4})Q([0-9]{1,2})', period)
        if not x:
            return None, None
        return int(x.group(1)), int(x.group(2))

    @staticmethod
    def get_period_type_from_period(period: str):
        # print("\n----!! get_period_type_from_period - period: ", period,"\n\n")
        period = period.upper()
        if period.find("H") != -1:    # DimTime.TYPE_HALF_YEAR {YYYY}H{01/02}
            return DimTime.TYPE_HALF_YEAR
        elif period.find("Q") != -1:    # DimTime.TYPE_QUARTER {YYYY}Q{01/02/03/04}
            return DimTime.TYPE_QUARTER
        elif period.find("D") != -1:    # DimTime.TYPE_DAY {YYYY}M{MM}D{DD}
            return DimTime.TYPE_DAY
        elif period.find("M") != -1:  # DimTime.TYPE_MONTH
            return DimTime.TYPE_MONTH
        else:                   # DimTime.TYPE_YEAR
            return DimTime.TYPE_YEAR

    @classmethod
    def get_dt_from_period(cls, period: str):
        period = period.upper()
        period_type = cls.get_period_type_from_period(period)
        # print("\n----- get_dt_from_period - period_type: ", period_type,"\n\n")

        if period_type == DimTime.TYPE_HALF_YEAR:
            year, half_year = cls.get_year_and_half_from_period(period)
            if not (year and half_year and half_year in [1, 2]):
                raise ValueError("wrong half-year period")
            month = cls.get_start_month_for_half_year(half_year)
            return dt.datetime.combine(
                dt.datetime(year=year, month=month, day=1), 
                dt.time.min)        
        elif period_type == DimTime.TYPE_QUARTER:
            year, quarter = cls.get_year_and_quarter_from_period(period)
            if not (year and quarter and quarter in [1, 2, 3, 4]):
                raise ValueError("wrong quarter period")
            month = cls.get_start_month_for_quarter(quarter)
            return dt.datetime.combine(
                dt.datetime(year=year, month=month, day=1), 
                dt.time.min)
        elif period_type == DimTime.TYPE_DAY:       # DimTime.TYPE_DAY - {YYYY}M{MM}D{DD}
            return dt.datetime.strptime(period, "%YM%mD%d")
        elif period_type == DimTime.TYPE_MONTH:   # DimTime.TYPE_MONTH - {YYYY}M{MM}
            return dt.datetime.strptime(period, "%YM%m")
        else:                              # DimTime.TYPE_YEAR
            return dt.datetime.strptime(period, "%Y")

    @classmethod
    def get_dt_start_from_period(cls, period: str):
        return dt.datetime.combine(cls.get_dt_from_period(period), dt.time.min)

    @classmethod
    def get_dt_end_from_period(cls, period: str):
        period = period.upper()
        period_type = cls.get_period_type_from_period(period)
        dt_start = cls.get_dt_start_from_period(period)
        
        if period_type == DimTime.TYPE_HALF_YEAR:
            last_month = dt_start.month + 5
            last_day_of_month = cls.get_last_day_of_month(dt_start.year, last_month)
            return dt.datetime.combine(
                dt_start.replace(month=last_month, day=last_day_of_month), 
                dt.time.max)
        elif period_type == DimTime.TYPE_QUARTER:
            last_month = dt_start.month + 2
            last_day_of_month = cls.get_last_day_of_month(dt_start.year, last_month)
            return dt.datetime.combine(
                dt_start.replace(month=last_month, day=last_day_of_month), 
                dt.time.max)
        elif period_type == DimTime.TYPE_DAY:
            return dt.datetime.combine(
                dt_start, 
                dt.time.max)
        elif period_type == DimTime.TYPE_MONTH:
            last_day_of_month = cls.get_last_day_of_month(dt_start.year, dt_start.month)
            return dt.datetime.combine(                
                dt_start.replace(day=last_day_of_month), 
                dt.time.max)
        else:  # DimTime.TYPE_YEAR
            return dt.datetime.combine(
                dt_start.replace(month=12, day=31), 
                dt.time.max)

    @classmethod
    def get_period_from_dt(cls, dt_period: dt.datetime, period_type: str):
        if period_type == DimTime.TYPE_HALF_YEAR:
            half_year = cls.get_half_year_from_month(dt_period.month)
            return f"{dt_period.year}H0{half_year}"
        elif period_type == DimTime.TYPE_QUARTER:
            quarter = cls.get_quarter_from_month(dt_period.month)
            return f"{dt_period.year}Q0{quarter}"
        elif period_type == DimTime.TYPE_DAY:
            return dt_period.strftime("%YM%mD%d")
        elif period_type == DimTime.TYPE_MONTH:
            return dt_period.strftime("%YM%m")
        else:  # DimTime.TYPE_YEAR
            return dt_period.strftime("%Y")

    @classmethod
    def get_prev_period_dt_start_same_type(cls, period: str):
        period = period.upper()
        period_type = cls.get_period_type_from_period(period)
        dt_period = cls.get_dt_start_from_period(period)
        p_year = dt_period.year
        p_month = dt_period.year
        p_day = dt_period.year

        p_quarter = cls.get_quarter_from_month(p_month)
        p_half_year = cls.get_half_year_from_month(p_month)


        if period_type == DimTime.TYPE_HALF_YEAR:
            if p_half_year > 1:
                new_half_year = p_half_year - 1
                new_year = p_year
            else:
                new_half_year = 2
                new_year = p_year - 1
            new_month = cls.get_start_month_for_half_year(new_half_year)
            return dt.datetime.combine(dt_period.replace(year=new_year, month=new_month, day=1), dt.time.min)
        elif period_type == DimTime.TYPE_QUARTER:
            if p_quarter > 1:
                new_quarter = p_quarter - 1
                new_year = p_year
            else:
                new_quarter = 4
                new_year = p_year - 1
            new_month = cls.get_start_month_for_quarter(new_quarter)
            return dt.datetime.combine(dt_period.replace(year=new_year, month=new_month, day=1), dt.time.min)
        elif period_type == DimTime.TYPE_DAY:
            return dt.datetime.combine(dt_period - dt.timedelta(days=1), dt.time.min)
        elif period_type == DimTime.TYPE_MONTH:
            if p_month > 1:
                return dt.datetime.combine(dt_period.replace(month=p_month - 1, day=1), dt.time.min)
            else:
                return dt.datetime.combine(dt_period.replace(year=p_year - 1, month=12, day=1), dt.time.min)
        else:  # DimTime.TYPE_YEAR
            return dt_period.replace(year=p_year - 1, month=1, day=1)

    @classmethod
    def get_next_period_dt_start_same_type(cls, period: str):
        period = period.upper()
        period_type = cls.get_period_type_from_period(period)
        dt_period = cls.get_dt_start_from_period(period)
        p_year = dt_period.year
        p_month = dt_period.year
        p_day = dt_period.year

        p_quarter = cls.get_quarter_from_month(p_month)
        p_half_year = cls.get_half_year_from_month(p_month)

        if period_type == DimTime.TYPE_HALF_YEAR:
            if p_half_year < 2:
                new_half_year = p_half_year + 1
                new_year = p_year
            else:
                new_half_year = 1
                new_year = p_year + 1
            new_month = cls.get_start_month_for_half_year(new_half_year)
            return dt.datetime.combine(dt_period.replace(year=new_year, month=new_month, day=1), dt.time.min)
        elif period_type == DimTime.TYPE_QUARTER:
            if p_quarter < 4:
                new_quarter = p_quarter + 1
                new_year = p_year
            else:
                new_quarter = 1
                new_year = p_year + 1
            new_month = cls.get_start_month_for_quarter(new_quarter)
            return dt.datetime.combine(dt_period.replace(year=new_year, month=new_month, day=1), dt.time.min)
        elif period_type == DimTime.TYPE_DAY:
            return dt.datetime.combine(dt_period + dt.timedelta(days=1), dt.time.min)
        elif period_type == DimTime.TYPE_MONTH:
            if p_month < 12:
                return dt.datetime.combine(dt_period.replace(month=p_month + 1, day=1), dt.time.min)
            else:
                return dt.datetime.combine(dt_period.replace(year=p_year + 1, month=1, day=1), dt.time.min)
        else:  # DimTime.TYPE_YEAR
            return dt_period.replace(year=p_year + 1, month=1, day=1)



class RevOlapBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_at = models.DateTimeField(default=django_tz.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.before_delete()
        super(RevOlapBaseModel, self).delete()
        self.after_delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return

    def before_delete(self):
        pass

    def after_delete(self):
        pass


class RevOlapBaseDim(RevOlapBaseModel):
    name = models.CharField(max_length=255, null=False)
    code_name = models.CharField(max_length=50, null=False)
    desc = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    class Meta:
        abstract = True


# base dimensions: 
# DimEntity (OrgUnit), DimAccount, DimScenario, 
# DimSalesVolume, DimProductionVolume

class DimEntity(RevOlapBaseDim):
    parent = models.ForeignKey("DimEntity", null=True, on_delete=models.DO_NOTHING)
    region = models.CharField(max_length=50, null=True)
    addr_city = models.CharField(max_length=255, null=True)
    addr_province = models.CharField(max_length=255, null=True)
    addr_country_code = models.CharField(max_length=10, null=True)
    addr_country_name = models.CharField(max_length=255, null=True)
    unit_account_prefix = models.CharField(max_length=50, null=True)

    # street address etc; I prefer "details" here, since it can be not-exactly-a-typical-city-addr,
    # eg. Port Haven No 4, Block 16, Production Hall 15 etc
    addr_details = models.CharField(max_length=255, null=True)
    addr_postal_code = models.CharField(max_length=50, null=True)


class DimAccount(RevOlapBaseDim):
    parent = models.ForeignKey("DimAccount", null=True, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey("DimEntity", null=True, on_delete=models.DO_NOTHING)

    # null for account group (range)
    account_no = models.CharField(max_length=255, null=True)
    account_no_range_bottom = models.IntegerField(default=0, null=True)
    account_no_range_top = models.IntegerField(default=0, null=True)
    # numbers/codes of accounts in the Chart of Accounts
    # https://www.investopedia.com/terms/c/chart-accounts.asp
    # determines whether this is an account type ("range") 
    # or a particular account. Such a structure is meant for
    # flexibility, allowing to build multi-level charts of accounts
    is_account_type = models.BooleanField(default=False)


class DimProduct(RevOlapBaseDim):
    parent = models.ForeignKey("DimProduct", null=True, on_delete=models.DO_NOTHING)
    sku = models.CharField(max_length=255, null=True)


class Measurement(RevOlapBaseDim):
    parent = models.ForeignKey("Measurement", null=True, on_delete=models.DO_NOTHING)
    """
    measurement tree - eg. "sales_volume", "sales_revenue", "account_balance"/"account_value" etc.
    describing WHAT value is stored in the fields: num_val, num_val_conso_tmp, num_val_conso, num_val_agg ("conso" stands both a consolidation and aggregate)
    """

    # unit_type:
    #   vol:{unit}      eg. vol:m3
    #   cur:{currency}, eg. cur:EUR
    #   cnt - item count
    unit_type = models.CharField(max_length=30, null=False)
    # _is_measurement = True


class DimTime(RevOlapBaseDim):
    parent = models.ForeignKey("DimTime", null=True, on_delete=models.DO_NOTHING)

    TYPE_HALF_YEAR = 'half_year'
    TYPE_QUARTER = 'quarter'
    TYPE_YEAR = "year"
    TYPE_MONTH = "month"
    TYPE_DAY = "day"

    """
        - name, code_name - period 
        - months eg. 2023M10, 2024M01 etc 
        - (months always padded with 0)
        - quarters eg 2023Q01, 2024Q02 etc (padded with zero)
        - half-years eg 2023H01, 2023H02
        - years eg. 2023, 2024 (always 4-digit)
        - month-days, eg. 2024M01D05, 2023M08D15 etc
    """

    # if set, it is to make chain values. Should be somehow auto-calculated    
    # TODO: do we really need that if we have comparisons? I think we don't
    # time_prev = models.CharField(max_length=255, null=True)
    # time_next = models.CharField(max_length=255, null=True)

    period_type = models.CharField(null=False, default=TYPE_MONTH)
    dt_start = models.DateTimeField(auto_now=True, db_index=True)
    dt_end = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def year(self):
        if self.dt_start:
            return self.dt_start.year
        return None
        
    """
    year
    month
    day
    """
    def save(self, *args, **kwargs):
        self.dt_start = TimeService.get_dt_start_from_period(self.code_name)
        self.dt_end = TimeService.get_dt_end_from_period(self.code_name)
        self.period_type = TimeService.get_period_type_from_period(self.code_name)
        super().save(*args, *kwargs)

        # sets the type based on code_name , 
        #   eg. '2024M01' -> 'month',  '2024' - 'year', '2024Q01' - 'quarter', '2024H01' - 'halfyear', '2024M01D15' - '2024-01-15'
        # sets the dt_start and dt_end based on code_name, 
        #   eg. '2024M01' -> '2024-01-01' -- '2024-01-31', 
        #       '2024' -> '2024-01-01' -- '2024-12-31', 
        #       '2024Q01' -> '2024-01-01' -- '2024-03-31',
        #       '2024H01' -> '2024-01-01' -- '2024-06-30'
        #       '2024M01D15' - '2024-01-15 00:00:00' -- '2024-01-15 23:59:59'
        # TODO - comparison: x > dimTime = x > dimTime. dt_end
        #             x < dimTime = x < dimTime.dt_start


class DimScenario(RevOlapBaseDim):
    parent = models.ForeignKey("DimScenario", null=True, on_delete=models.DO_NOTHING)

    """
    - scenario_type: label, estimate, forecast, actual, elab, rolling (forecast)
        these are rather the types of scenario periods, not scenario itself
        only actual/forecast seem to be scenario type. Forecast scenario will contain:
        [estimate_periods (taken from actual)]
        [elab_periods]
        [rolling_periods]
    - name, code_name: eg. 
            F_2024M4 - Forecast_2024 April
-           E_2023M12 - Estimate 2023 December
            A_2024M1 - Actual 2024 January, etc
    """
    scenario_type = models.CharField(max_length=255, null=False)
    scenario_period_start = models.CharField(max_length=255, null=True)
    scenario_period_end = models.CharField(max_length=255, null=True)


    scenario_time_data = models.JSONField(null=True)
    """ scenario_time - TODO do we want to set them here or just in the final cube? 
        JSON field having the list - loss of time to create another model for it, we will NOT search
        scenarios by some  included period

Generally, there is the Scenario/Time interescion

eg.
Actual / 2024M01
Actual / 2024M02
Actual / 2024M03
Actual / 2024M04
Actual / 2024M05
Actual / 2024M06

However, it's not enough in the case of Forecast, where we have "parts" or "period types" eg
    F_2024M4 / 2024M01 (Estimate/Actual) 
    F_2024M4 / 2024M02 (Estimate/Actual)
    F_2024M4 / 2024M03 (Estimate/Actual)
    F_2024M4 / 2024M04 (Estimate/Actual)
    F_2024M4 / 2024M05 (Elab)
    F_2024M4 / 2024M06 (Elab)
    F_2024M4 / 2024M07 (Rolling)
    F_2024M4 / 2024M08 (Rolling)
    F_2024M4 / 2024M09 (Rolling)
    F_2024M4 / 2024M10 (Rolling)
    F_2024M4 / 2024M10 (Rolling)

In this case, we should have 
    {Scenario} / {Period} / {Period_type_for_scenario}

    The latter (Period_type_for_scenario) COULD be defined in the particular Scenario in some JSONField
    the same for start/end - for forecasts we MUST KNOW what periods it relates to. Just the periods being presented in the cube is NOT ENOUGH

        eg. 
        {
            'start': '2024M01',
            'end': '2025M12',
            'list': 

            [
                ("2024M01", "estimate")
                ("2024M02", "estimate")
                ("2024M03", "estimate")
                ("2024M04", "estimate")
                ("2024M05", "estimate")
                ("2024M06", "estimate")
                ("2024M07", "estimate")
                ("2024M08", "elab")
                ("2024M09", "elab")
                ("2024M10", "elab")
                ("2024M11", "rolling")
                ("2024M12", "rolling")
                ("2025M01", "rolling")
                ("2025M02", "rolling")
                ("2025M03", "rolling")
                ("2025M04", "rolling")
                ("2025M05", "rolling")
                ("2025M06", "rolling")
                ("2025M07", "rolling")
                ("2025M08", "rolling")
                ("2025M09", "rolling")
                ("2025M10", "rolling")
                ("2025M11", "rolling")
                ("2025M12", "rolling")
                
            ]
        }
    """
    
    


class DimOrigin(RevOlapBaseDim):
    pass


class RevOlapCubeDef(RevOlapBaseModel):
    parent = models.ForeignKey("RevOlapCubeDef", null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, null=False)
    code_name = models.CharField(max_length=50, null=False)
    desc = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    dimensions = models.JSONField(null=False)
    fact_entity = models.CharField(max_length=255, null=True)


class RevOlapCubeFactBase(RevOlapBaseModel):
    num_value = models.DecimalField(default=0.0, decimal_places=10, max_digits=20)
    num_value_agg_tmp = models.DecimalField(default=0.0, decimal_places=10, max_digits=20)
    num_value_agg = models.DecimalField(default=0.0, decimal_places=10, max_digits=20)
    num_value_conso_tmp = models.DecimalField(default=0.0, decimal_places=10, max_digits=20)
    num_value_conso = models.DecimalField(default=0.0, decimal_places=10, max_digits=20)

    is_dirty_value = models.BooleanField(default=False)
    is_dirty_agg = models.BooleanField(default=False)
    is_dirty_conso = models.BooleanField(default=False)
    value_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    agg_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    agg_tmp_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    conso_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    conso_tmp_updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
    

class RevOlapCubeFact_CubeTest1(RevOlapCubeFactBase):
    parent_fact = models.ForeignKey("RevOlapCubeFact_CubeTest1", null=True, on_delete=models.DO_NOTHING)
    time = models.ForeignKey("DimTime", null=False, on_delete=models.DO_NOTHING)
    scenario = models.ForeignKey("DimScenario", null=False, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey("DimEntity", null=True, on_delete=models.DO_NOTHING)
    account = models.ForeignKey("DimAccount", null=True, on_delete=models.DO_NOTHING)
    product = models.ForeignKey("DimProduct", null=True, on_delete=models.DO_NOTHING)
    origin = models.ForeignKey("DimOrigin", null=True, on_delete=models.DO_NOTHING)
    measurement = models.ForeignKey("Measurement", null=True, on_delete=models.DO_NOTHING)

    # redundant data - intentionally added to allow better performance
    rdn_time_code_name = models.CharField(max_length=50, null=True)
    rdn_time_period_type = models.CharField(null=True, default=DimTime.TYPE_DAY)
    rdn_time_dt_start = models.DateTimeField(auto_now=False, db_index=True, null=True)
    rdn_time_dt_end = models.DateTimeField(auto_now=False, db_index=True, null=True)

    rdn_scenario_code_name = models.CharField(max_length=50, null=True)
    rdn_entity_code_name = models.CharField(max_length=50, null=True)
    rdn_account_code_name = models.CharField(max_length=50, null=True)
    rdn_product_code_name = models.CharField(max_length=50, null=True)
    rdn_origin_code_name = models.CharField(max_length=50, null=True)
    rdn_measurement_code_name = models.CharField(max_length=50, null=True)


    def save(self, *args, **kwargs):
        self.rdn_time_code_name = self.time.code_name if self.time else None
        self.rdn_time_period_Type = self.time.period_type if self.time else None
        self.rdn_time_dt_start = self.time.dt_start if self.time else None
        self.rdn_time_dt_end = self.time.dt_end if self.time else None

        self.rdn_scenario_code_name = self.scenario.code_name if self.scenario else None
        self.rdn_entity_code_name = self.entity.code_name if self.entity else None
        self.rdn_account_code_name = self.account.code_name if self.account else None
        self.rdn_product_code_name = self.product.code_name if self.product else None
        self.rdn_origin_code_name = self.origin.code_name if self.origin else None
        self.rdn_measurement_code_name = self.measurement.code_name if self.measurement else None

        super().save(*args, **kwargs)

    """
    DimTime
    DimScenario
    DimEntity
    DimAccount
    DimProduct
    DimOrigin
    Measurement
    """    
    

class RevOlapCubeFact_CubePrices(RevOlapCubeFactBase):
    parent_fact = models.ForeignKey("RevOlapCubeFact_CubeTest1", null=True, on_delete=models.DO_NOTHING)
    time = models.ForeignKey("DimTime", null=False, on_delete=models.DO_NOTHING)
    scenario = models.ForeignKey("DimScenario", null=False, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey("DimEntity", null=True, on_delete=models.DO_NOTHING)
    product = models.ForeignKey("DimProduct", null=True, on_delete=models.DO_NOTHING)
    measurement = models.ForeignKey("Measurement", null=True, on_delete=models.DO_NOTHING)

    rdn_time_code_name = models.CharField(max_length=50, null=True)   # docelowo False, TODO
    rdn_time_period_type = models.CharField(null=False, default=DimTime.TYPE_DAY)
    rdn_time_dt_start = models.DateTimeField(auto_now=True, db_index=True)
    rdn_time_dt_end = models.DateTimeField(auto_now=True, db_index=True)

    rdn_scenario_code_name = models.CharField(max_length=50, null=True)   # docelowo False, TODO
    rdn_entity_code_name = models.CharField(max_length=50, null=True)   # docelowo False, TODO
    rdn_product_code_name = models.CharField(max_length=50, null=True)   # docelowo False, TODO
    rdn_measurement_code_name = models.CharField(max_length=50, null=True)   # docelowo False, TODO

    def save(self, *args, **kwargs):
        self.rdn_time_code_name = self.time.code_name if self.time else None
        self.rdn_time_period_Type = self.time.period_type if self.time else None
        self.rdn_time_dt_start = self.time.dt_start if self.time else None
        self.rdn_time_dt_end = self.time.dt_end if self.time else None

        self.rdn_scenario_code_name = self.scenario.code_name if self.scenario else None
        self.rdn_entity_code_name = self.entity.code_name if self.entity else None
        self.rdn_product_code_name = self.product.code_name if self.product else None
        self.rdn_measurement_code_name = self.measurement.code_name if self.measurement else None

        super().save(*args, **kwargs)
