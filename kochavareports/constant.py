class ReportCategory(object):
    SUMMARY = 'summary'
    DETAIL = 'detail'


class SummaryReportType(object):
    NETWORK = 'network'
    CAMPAIGN = 'campaign'


class Traffic(object):
    CLICK = 'click'
    IMPRESSION = 'impression'
    INSTALL = 'install'
    EVENT = 'event'
    REENGAGEMENT = 'reengagement'
    TRAFFIC_VERIFICATION = 'trafficverif'
    INFLUENCER_IMPRESSION = 'influencer_imp'
    INFLUENCER_CLICK = 'influencer_click'
    FRACTIONAL = 'fractional'


class DateTimeGranularity(object):
    HOURLY = '1'
    DAILY = '24'
    WEEKLY = '168'
    MONTHLY = '720'
