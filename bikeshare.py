import pandas as pd
import numpy as np
import time


city_data = {

    'chicago' : 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'All']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']


def print_pause(message_to_print):
    print(message_to_print)
    time.sleep(0.5)

def intro():
    print('Hello! Let\'s explore some US bikeshare data!')


def get_filter(): #COLLECTING USER INPUT

    city_name = input('\nWhich city would you like to see data from Chicago, New York or Washington?\n').lower()
    while city_name not in city_data:
        city_name = input('\nPlease select one of the options listed (Chicago, New York or Washington\n').lower()
    if city_name in city_data:
        print_pause('\nYou have selected {}'.format(city_name).title())

    day = input('\nPlease name the day to filter by, or \'all\' to apply no day filter.\n').title()
    while day not in days:
        day = input('\nPlease select the day of the week that you would like filter by or \'all\' to apply no day filter.\n').title()
    if day in days:
        print_pause('\nYou have selected {}'.format(day))

    month = input('\nPlease name the month to filter by, or \'all\' to apply no month filter.'
    '\nPLEASE ENTER THE MONTH IN NUMBER FORMAT (FOR EXAMPLE 1 FOR January)\n').title()
    while month not in months:
        month = input('\nPlease select the month in number format that you would like to filter by or \'all\' to apply no  month filter\n').title()
    if month in months:
        print_pause('\nYou have selected {}'.format(month))

    return city_name, month, day


def load_data(city_name, month, day): #LOADING DATA FOR SPECIFIED CITY FILTER

    df = pd.read_csv(city_data[city_name])

    #convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to creat new coloums
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['station_combo'] = df['Start Station'] + (' to ') + df['End Station']

    if month != 'All' and day != 'All':
        df = df[df['month'] == int(month)]
        df = df[df['day_of_week'] == day]

    return(df)


def time_statistics(df): #CALCULATING TIME STATISTICS

    print_pause('\nCalculating the most popular times of travel\n')

    #Most popular month
    print_pause('The most popular month is: Month {} of the calendar year'.format(df['month'].mode()[0]))

    #Most popular day_of_week
    print_pause('The most popular day of the week is: {}'.format(df['day_of_week'].mode()[0]))

    #Most popular start hour
    print_pause('The most popular hour is: {}'.format(df['hour'].mode()[0]))

    print('')
    print_pause('~'*50)


def station_statistic(df):

    print('\nCalculating the most popular stations & trips\n')

    #most popular starting station
    most_pop_start_station = df['Start Station'].mode()[0]
    print_pause('{} is the most popular start station'.format(most_pop_start_station))

    #most popular ending stations
    most_pop_end_station = df['End Station'].mode()[0]
    print_pause('{} is the most popular end station'.format(most_pop_end_station))

    #most popular combination of start station & end station
    most_pop_combo_station = df['station_combo'].mode()[0]
    print_pause('{} is the most popular combination of start station and end station trips.'.format(most_pop_combo_station))

    print('')
    print_pause('~'*50)


def trip_duration_statistics(df): #CALCULATING TRIP STATISTIC

    print_pause('\nCalculating the total & average trip durations\n')

    #total travel time
    print_pause('The total time travelled is {} seconds'.format(df['Trip Duration'].sum()))

    #average travel time
    print_pause('The average time travelled is {} seconds'.format(df['Trip Duration'].mean()))

    print('')
    print_pause('~'*50)


def user_statistic(df): #USER DATA

    print_pause('\nCalculating user statistics\n')

    #number of users
    print_pause('The number users: {}'.format(df['User Type'].count()))

    #number of users per Gender
    print_pause('The number users by {}'.format(df.groupby(['Gender'])['Gender'].count()))

    #earliest, most recent and most common year of birth
    print_pause('The youngest user was born in {}'.format(df['Birth Year'].max()))
    print_pause('The oldest user was born in {}'.format(df['Birth Year'].min()))
    print_pause('The most popular birth year of our users is {}'.format(df['Birth Year'].mode()[0]))

    print('')
    print_pause('~'*50)


def raw_data(df): #select raw data
    start = 0
    stop = 5
    data_request = input('Do you want to see the first 5 rows of raw data? Y / N ').upper()
    while data_request != 'Y' or data_request != 'N':
        data_request = input('Please enter \'Y\' or \'N\' ').upper()
        if data_request == 'N':
            break
        while data_request == 'Y':
            print(df.iloc[start : stop])
            data_request = input('Do you want to see the next 5 rows of raw data? Y / N ').upper()
            start += 5
            stop += 5
            if data_request == 'N':
                break


def restart():
    restart_question = input('Would you like to restart the program? \'Y\' or \'N\' ').upper()
    if restart_question == 'Y':
        main()
    elif restart_question == 'N':
        print('\nSee you later\n')
    else:
        restart()


def main():
    intro()
    city_name, month, day = get_filter()
    df = load_data(city_name, month, day)
    try:
        time_statistics(df)
        station_statistic(df)
        trip_duration_statistics(df)
        user_statistic(df)
        raw_data(df)
        restart()
    except IndexError:
        print('Looks like the filter is invalid')
        restart()

main()
