import argparse
import api


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload client to Zodiac')
    parser.add_argument('-u', '--username', dest='username', help='Who to login as', required=True)
    parser.add_argument('-p', '--password', dest='password', help='Password for user', required=True)
    parser.add_argument('-t', '--transactions', dest='transactions', help='The transaction logs to submit', nargs='+', required=True)
    parser.add_argument('-a', '--attributes', dest='attributes', help='The customer attributes file to submit', required=True)
    parser.add_argument('-m', '--model-group', dest='model_group_hash', help='The model group hash you wish to run, provided by Zodiac', required=True)

    args = parser.parse_args()
    client = api.Zodiac(args.username, args.password)
    client.submit_job(args)
