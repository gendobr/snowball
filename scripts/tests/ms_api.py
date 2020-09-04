from lib.msacademic import Api
import time
import fire
import configparser
import json


def main(config=None):
    # read configuration file
    conf = configparser.ConfigParser()
    # conf.readfp(open(dir+'/config.ini'))
    conf.read_file(open(config))

    rest_endpoint = json.loads(conf.get('msacademic', 'restEndpoint'))
    subscription_key = conf.get('msacademic', 'subscriptionKey')
    include_topics = json.loads(conf.get('msacademic', 'msAcademicIncludeTopicsIds'))

    api = Api(subscription_key, rest_endpoint, include_topics)
    # res = api.load_by_ids(["1710476689"], verbose=True)
    # res = api.load_by_ids(["2893479785"], verbose=True)
    # res = api.load_by_rids(["1710476689"], verbose=True)
    res = api.load_by_rids(["2893479785"], verbose=True)

    print("++++++++++++++++++++++++")
    print(res)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(main)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0, ))
