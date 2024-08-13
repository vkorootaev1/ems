from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    rate = '3/min'
