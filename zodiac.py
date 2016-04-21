import argparse
import api

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload client to Zodiac")
    parser.add_argument("-f", "--file", dest="filepath", help="File upload", required=True)
    parser.add_argument("-d", "--description", dest="description", help="File description", required=True)
    parser.add_argument("-u", "--username", dest="username", help="Who to login as", required=True)
    parser.add_argument("-p", "--password", dest="password", help="Password for user", required=True)

    args = parser.parse_args()
    client = api.Zodiac(args.username, args.password)
    client.upload_file(args.filepath, args.description)
