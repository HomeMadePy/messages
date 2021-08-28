"""Common fixtures for integration tests."""

import jsonconfig

def integration_test_configured(msgtype):
    """
    Does the user have an 'integration_tester' config profile set up, and
    do they have 'msgtype' set up in that profile?
    """
    with jsonconfig.Config('messages') as cfg:
        data = cfg.data
        return (
            'integration_tester' in data.keys()
            and msgtype in data['integration_tester']
        )
