import math
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = [
    'january', 'february', 'march', 'april', 'may', 'june'
]
days = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
]

def round_fn(value, divider):
    if int(str(value % divider)[0]) > 5:
        return math.ceil(value)
    elif int(str(value % divider)[0]) < 5:
        return math.floor(value)

def get_selection(input_option, options):
    while True:
        selection = input("Which {} would you like to explore: ".format(input_option))
        if selection.lower() not in options:
            print(
                "You selected a {0} for which we have no data.\nPlease choose from among {1}".format(
                    input_option, ", ".join(options)
                )
            )
            continue
        break
    return selection

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_selection("city", ["chicago", "new york city", "washington"])


    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_selection("month", ["all", *months])


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_selection(
        "day", ["all", *days]
    )


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city], index_col=0)
    df['Start Time'] = pd.to_datetime(df['Start Time'], yearfirst=True)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].groupby(df['month']).count().idxmax()
    most_common_month = months[most_common_month - 1]
    print("\nThe most common month is {}".format(most_common_month))


    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].groupby(df['day_of_week']).count().idxmax()
    print("\nThe most common day of the week is {}".format(most_common_day))


    # TO DO: display the most common start hour
    most_common_hour = df['hour'].groupby(df['hour']).count().idxmax()
    print("\nThe most common start hour is {}".format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(2)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    used_start_station = df['Start Station'].groupby(df['Start Station']).count().idxmax()
    print("\nThe most commonly used start station is {}".format(used_start_station))


    # TO DO: display most commonly used end station
    used_end_station = df['End Station'].groupby(df['End Station']).count().idxmax()
    print("\nThe most commonly used end station is {}".format(used_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    """'Jefferson Dr & 14th St SW', 'Jefferson Dr & 14th St SW'"""
    start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(
        "\nThe most frequent combination of start and end station trip is;\n {0} and {1}\n".format(
            start_end_station[0], start_end_station[1]
        )
    )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(2)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # total travel time in days
    tt_day_time = total_travel_time / 86400
    tt_day_time = round_fn(tt_day_time, 86400)
    print(
        "\nThe total travel time is {0} seconds which is approximately {1} days".format(
            total_travel_time, tt_day_time
        )
    )


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # mean travel time in minutes
    mean_minute_time = mean_travel_time / 60
    mean_minute_time = round_fn(mean_minute_time, 60)
    print(
        "\nThe mean travel time is {0} seconds which is approximately {1} minutes".format(
            mean_travel_time, mean_minute_time
        )
    )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(2)
    time.sleep(2)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_counts = [*df['User Type'].groupby(df['User Type']).count().items()]
    print("The counts of user types are:")
    for pair in user_types_counts:
        print("User Type: {}\t Count: {}".format(pair[0], pair[1]))


    # TO DO: Display counts of gender
    try:
        user_types_counts = [*df['Gender'].groupby(df['Gender']).count().items()]
        print("\nThe counts of genders are:")
        for pair in user_types_counts:
            print("Gender: {}\t Count: {}".format(pair[0], pair[1]))
    except KeyError:
        print("\nUnfortunately, the city you chose does not have data on gender")


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_yr = int(df['Birth Year'].sort_values().iloc[0])
        recent_birth_yr = int(df['Birth Year'].sort_values(ascending=False).iloc[0])
        commonest_birth_yr = int(df['Birth Year'].mode()[0])
        print(
            "\n{}, {} and {} are the earliest, most recent and most common years of birth respectively".format(
                earliest_birth_yr, recent_birth_yr, commonest_birth_yr
            )
        )
    except KeyError:
        print("\nUnfortunately, the city you chose does not have data on year of birth")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(2)

def display_raw_data(df):
    row_count = 0
    while True:
        see_data = input("\nWould you like to see 5 (more) lines raw data? Enter yes or no.\n")
        if see_data.lower() not in ["no", "yes"]:
            print("Sorry, I only accept a yes or no to this question")
        elif see_data == "no":
            break
        else:
            previous_count = row_count + 5
            while row_count < df.size and row_count < previous_count:
                print(df.iloc[row_count].to_dict())
                row_count += 1
                

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ["no", "yes"]:
            print("Sorry, I only accept a yes or no to this question")
        elif restart.lower() == "no":
            break


if __name__ == "__main__":
	main()
