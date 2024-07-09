# Lightning Maths!

## Overview
Lightning Maths! is a web-based application based on Flask, Python, and HTML designed to help a user improve their speed and accuracy in basic math operations, including, addition, subtraction, multiplication, division, and exponentiation. It stores all user data in a database managed with SQL.

## Video Demonstration
Can be found on YouTube. The link is [youtu.be/giQ1wp9dERg](youtu.be/giQ1wp9dERg).

## Code Download
The code for Lightning Maths is on GitHub. It may be downloaded at [github.com/code50/103399534/tree/main/project](github.com/code50/103399534/tree/main/project). ***MAKE SURE TO GIVE CREDIT TO VIHAAN ANAND IF SHARED OR USED.***

## Breakdown & Explanation
### `/` (homepage)
Contains two buttons, leading to the page to take a test and the statistics page. The navbar at the top contains different elements based on logged-in vs logged-out state. If logged in, they are "Home", "Take a Test", "View Statistics", and "Log Out". Else, they are "Home", "Log In", and "Sign Up".

### `/signup` (signup page)
A form redirecting to `/signup` via POST. Contains three fields: one for username, one for password, and one for password repeat (to prevent accidental password creation). When submitted, it adds the user to the database, and then redirects him to the login page so he can log in.

### `/login` (login page)
A form redirecting to `/login` via POST. Contains two fields, one for username and one for password. When submitted, it is checked against the database of users and passwords. If the user exists and provided the correct password, a cookie is stored allowing the user to access "login required" functions.

### `/logout` (logout route)
A route that does not show anything. It simply clears the cookie stored by `login` and then redirects to the login page so a user can login to a different account.

### `/practise` (start practise round page)
A form redirecting to `/practise` via POST. It contains one numerical field for the number of questions, and one dropdown field asking the user which type of question they would like to practise (from addition, subtraction, multiplication, division, exponentiation, and roots). When submitted, it processes this information and adds it to the database, along with the start time for later time calculations. It then sends the user to the round at `/practise/round`.

### `/practise/round` (practise round page)
Very simple page. First, it uses [Python's `random` library](https://docs.python.org/3/library/random.html) to generate a random question of the type given. This question is added to the database for future score calculations. It then uses [MathJax](https://www.mathjax.org) to display the math question on the page. Underneath this is a form field in which the user can type their answer to the question. This form is then submitted to `/practise/round` via POST for processing of the answer. The answer is added to
the question entry in the database, and the user is redirected to `/practise/round` to continue the test if more questions are remaining.

### `/practise/finish` (round summary page)
This page is fully form-free. First, it adds the end time to the database for calculations. Each question is reviewed to calculate the score, and the round entry is used to identify the time taken. The page contains simple statistics about the round the user just completed. It gives their score (as a fraction and percentage), the amount of time it took for them to complete it, and the average time taken per question. Below this is a button to take them to an interactive "practise incorrect questions" experience. They can go home at this point, or use this interface to practise incorrect questions.

### `/practise/practise` (practise incorrect questions page)
This page is similar to the `/practise/round` page, but it has some differences. First, it includes a bar at the top for each question saying "Your answer is correct!" and things of that sort. Next, it doesn't update the database in any way, shape, or form. After all of the incorrect questions are practised, the user is redirected to the homepage.

### `/stats` (statistics page)
This page is entirely text-based and contains 4 statistics: your average accuracy, your average time per question, everyone's average accuracy, and everyone's average time per question.
