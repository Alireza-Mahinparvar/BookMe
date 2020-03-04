# Project Requirements
### Team 5 Members / Github usernames:
* Dominic Gutierrez / domgutz3
*
*
*

## Project Name: 
MeetUp

## Problem Statement:
Some people are busy and find it hard to find time for meetings with others

## Product Objective:
To allow people to efficiently make meetings with other people when they are free for various reasons

## Functional Requirements

* Users must be able to create an account 
* Users must be able to set their availabilty
* Guests must be able to make appointments with users when they are available
* Users must be able to cancel appointments if need be
* Guests should receive a confirmation page upon making an appointment
* Guests should recieve a confirmation email 

## Non-Functional Requirements

*
*
*

## Use Cases

**Use Case Name: Set Availability**      
**Date: 03/05/2020**

## Summary
Users will be able to choose the dates / times when they     
are available for meetings with guests. These availabilities   
will be stored in users' accounts and will be visible to    
guests who are planning to make appointments with them.

## Actors
Only users with accounts 

## Preconditions
* User must be logged in
* User navigates to account settings

## Triggers
User must select the "Edit Availability" option in his or her account settings

## Primary Sequence
1) System prompts user to select a date
2) User selects day(s) from a calendar
3) System prompts user to select availability start time(s) and end time(s)
4) User selects times on every hour or half hour
5) System asks customer to confirm and save
6) User selects save
7) System updates user's availability information
8) User logs out

## Primary Postconditions
* User's new availabilty will be shown in account
* Guests will only be able to make appointments during user's new availabilty 

## Alternate Sequences
6)  User selects edit
a)  User selects different times
b)  Repeat step 5

### Alternate Trigger
If the user realizes that he or she made a mistake, the user selects edit to select the correct availability times

### Alternate Postconditions
Same as primary postconditions

## Non-functional Requirements
* System should respond to user input within one second
* System displays messages in English

## Glossary
* User = A person with an account who meets with guests
* Guest = A person without an account who schedules meetings with users
* Availability = Set of time frames that appointments can be made with a certain user




