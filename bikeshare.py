# bikeshare.py
# Author: hamza mehdawi
# Description: Analyzes US bikeshare data for Chicago, NYC, and Washington.
# The user can filter by city, month, and day of the week.

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
         Asks user to specify a city, month, and day to analyze.

         Returns:
             (str) city - name of the city to analyze
             (str) month - name of the month to filter by, or "all" to apply no month filter
             (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        city = input("Enter the city (chicago, new york city, washington): ").strip().lower()
        if city in valid_cities:
            break
        else:
            print("Invalid city. Please choose from chicago, new york city, or washington.")

    while True:
        month = input("Enter the month (all, january, february, ..., june): ").strip().lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Please choose from all, january, february, march, april, may, or june.")

    while True:
        day = input("Enter the day (all, monday, tuesday, ..., sunday): ").strip().lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Please choose a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    """ load CSV files as per user requstes   """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Start Time'].dt.month == month]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.title()]

    return df


def time_stats(df):
    """Displays the most frequent times of travel."""

    print('\n 1-Calculating Times of Travel\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].value_counts().idxmax()
    print('Most Common Month: ', months[common_month - 1].title())

    common_day = df['day_of_week'].value_counts().idxmax()
    print('Most Common Day:   ', common_day)

    common_hour = df['hour'].value_counts().idxmax()
    print('Most Common Hour:  ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)




def station_stats(df):
    """Displays the most popular stations and trip."""

    print('\n 2-Calculating The Most Popular Stations and Trip\n')
    start_time = time.time()

    common_start = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station: ', common_start)

    common_end = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:   ', common_end)

    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip:          ', common_trip[0], ' → ', common_trip[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



def trip_duration_stats(df):
    """Displays the total and average trip duration."""

    print('\n 3-Calculating Trip Duration\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_time, 60)
    hours, minutes = divmod(minutes, 60)
    print(f'Total Travel Time:  {int(hours)}h {int(minutes)}m {int(seconds)}s')

    mean_time = df['Trip Duration'].mean()
    minutes, seconds = divmod(mean_time, 60)
    print(f'Mean Travel Time:   {int(minutes)}m {int(seconds)}s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_user_data(df):
    """Displays statistics on bikeshare users."""

    if df.empty:
        print("DataFrame is empty.")
        return

    start_loc = 0

    while start_loc < len(df):
        show_data = input(
            f'\nShow rows {start_loc} to {start_loc+5}? (yes/no): '
        ).strip().lower()

        if show_data == 'no':
            break

        if show_data != 'yes':
            print("Please enter yes or no.")
            continue

        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

    print("Exiting raw data view...")



def user_stats(data):
    """Displays statistics on bikeshare users."""
    print('\n 4-Calculating User Stats...\n')
    if data.empty:
        print("No data available.")
        print('-'*40)
        return
    print('\n 4-Calculating User Stats...\n')
    start_time = time.time()

    user_types = data['User Type'].value_counts()
    print('User Types:\n', user_types.to_string())

    if 'Gender' in data.columns:
        gender_counts = data['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts.to_string())
    else:
        print('\nGender data not available for this city.')

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in data.columns:
        earliest    = int(data['Birth Year'].min())
        most_recent = int(data['Birth Year'].max())
        most_common = int(data['Birth Year'].value_counts().idxmax())
        print(f'\nEarliest Year of Birth:    {earliest}')
        print(f'Most Recent Year of Birth: {most_recent}')
        print(f'Most Common Year of Birth: {most_common}')
    else:
        print('\nBirth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data found. Please try different information.\n")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_user_data(df)


        while True:
            restart = input('\n Would you like to restart? Enter yes or no.\n').strip().lower()
            if restart in ['yes', 'no']:
                break

        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
