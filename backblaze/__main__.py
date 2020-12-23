from b2sdk import InMemoryAccountInfo, B2Api
from config import config

def main():
    pass

def auth_init_b2():
    """Init b2 api and attach auth"""

    b2_info = InMemoryAccountInfo()
    b2_api = B2Api(b2_info)
    b2_api.authorize_account("production", config.APP_KEY_ID, config.APP_KEY)

    return b2_api

if if __name__ == "__main__":
    main()