import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload email addresses for use in Zodiac')
    parser.add_argument(
        '-e',
        '--emails',
        dest='emails',
        help='File of emails to upload'
    )

    parser.add_argument(
        '-u',
        '--username',
        dest='username',
        help='Who to login as',
        required=True
    )

    parser.add_argument(
        '-p',
        '--password',
        dest='password',
        help='Password for user',
        required=True
    )

    parser.add_argument(
        '-c',
        '--company',
        dest="company",
        help="The company to use, not required unless you have multiple access",
        required=False,
        default=None
    )

    parser.add_argument(
        '--api',
        dest="api",
        help="The Zodiac API to use. Not required for most clients.",
        required=False,
        default=None
    )

    parser.add_argument(
        '--api-version',
        dest="api_version",
        help="The Zodiac API version to use",
        required=False,
        default=None
    )

    args = parser.parse_args()
    client = api.Zodiac(
        args.username,
        args.password,
        company=args.company,
        api=args.api,
        api_version=args.api_version
    )
    client.upload_emails(args.emails)
