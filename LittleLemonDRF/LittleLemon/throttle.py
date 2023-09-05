from rest_framework.throttling import UserRateThrottle

class TenPerMinute(UserRateThrottle):
    scope='ten'