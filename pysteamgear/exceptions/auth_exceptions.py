
class AuthExceptions():

    class MissingPassword(Exception):
        pass

    class MissingSteamID(Exception):
        pass

    class CaptchaRequiredLoginIncorrect(Exception):
        pass

    class CaptchaRequired(Exception):
        pass

    class EmailCodeRequired(Exception):
        pass

    class TwoFactorCodeRequired(Exception):
        pass

    class TooManyLoginFailures(Exception):
        pass

    class LoginIncorrect(Exception):
        pass
