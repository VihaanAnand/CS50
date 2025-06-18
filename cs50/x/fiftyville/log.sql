-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Understand what data I am given
.tables

-- Understand the crime_scene_reports table
.schema crime_scene_reports

-- Get crime description of mystery
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
-- Description: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

-- Understand the interviews table
.schema interviews

-- Find interviews of witnesses
SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- Useful Interviews: 161, 162, 163
-- Interview 161: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Interview 162: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Interview 163: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Understand the bakery_security_logs table
.schema bakery_security_logs

-- Find bakery security logs for within 10 minutes
SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 5 AND minute <= 25;

-- Understand the atm_transactions table
.schema atm_transactions

-- Find ATM transactions for the day on Leggett Street
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";

-- Understand the phone_calls table
.schema phone_calls

-- Find phone calls for the day that were less than a minute
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Understand the flights table
.schema flights

-- Find airport code for Fiftyville
.schema airports
SELECT * FROM airports WHERE city = "Fiftyville";
-- Fiftyville Regional Airport: ID 8, CSF

-- Find flights out of Fiftyville for the next day
SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = 8 ORDER BY hour ASC, minute ASC;
-- Earliest Flight: ID 36, to airport 4

-- Find airport name for airport 4
SELECT * FROM airports WHERE id = 4;
-- ID 4: LGA, New York City
-- theother  possitibility is also ord chicago

-- Understand the passengers table
.schema passengers

-- Find people on the flight
SELECT * FROM passengers WHERE flight_id = 36;
SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- Find the thief
SELECT * FROM (SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)) WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 5 AND minute <= 25) AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60);
-- Could be Sofia, Kelsey, or Bruce
SELECT * FROM bank_accounts WHERE person_id IN (SELECT id FROM (SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)) WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 5 AND minute <= 25) AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60));
-- IS person 686048
SELECT * FROM people WHERE id = 686048;
-- ID 686048: Bruce

-- Find the accomplice
SELECT * FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE id = 686048) AND year = 2021 AND month = 7 AND day = 28 AND duration < 60);
-- Accomplice: Robin