import csv


def main():
    users = {}
    with open('twitter_small.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=' ')
        for row in reader:
            if row['user1'] not in users:
                users[row['user1']] = True
            if row['user2'] not in users:
                users[row['user2']] = True

    with open('twitter_tiny.csv', 'w', newline='') as csvfile:
        fieldnames = ['id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in users.keys():
            writer.writerow({'id': user})


if __name__ == "__main__":
    main()
