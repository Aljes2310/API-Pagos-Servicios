from rest_framework.throttling import UserRateThrottle


class Mil(UserRateThrottle):
    scope = 'mil'

class Dosmil(UserRateThrottle):
    scope="dosmil"