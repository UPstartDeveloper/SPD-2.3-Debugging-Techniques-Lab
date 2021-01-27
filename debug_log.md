# Debug Log

**Explain how you used the the techniques covered (Trace Forward, Trace Backward, Divide & Conquer) to uncover the bugs in each exercise. Be specific!**

In your explanations, you may want to answer:

- What is the expected vs. actual output?
- If there is a stack trace, what useful information does it contain?
- Which technique did you use, on which line numbers?
- What assumptions did you have about each line of code, and which ones were proven to be wrong?

_Example: I noticed that the program should show pizza orders once a new order is made, and that it wasn't showing any. So, I used the trace forward technique starting on line 13. I discovered the bug on line 27 was caused by a typo of 'pzza' instead of 'pizza'._

_Then I noticed another bug ..._

## Exercise 1

_I noticed there was a TypeError occuring on line 81, where we append the toppings to the new pizza that the user has ordered. Since I was really new to the codebase, I started from the top of `app.py`, and realized the parameter for the toppings on line 81 was wrong, looking at the class definition for the `PizzaTopping`._

_The second problem I noticed is the print statement after the pizza was added to the db was outputting `None`. At this point I knew a little more, so I traced backward to the form template on `order.html`, and realized that the names on the form fields, was different from what was being referenced in the `/order` route. So I fixed it, and used a print statement on line 86 of `app.py` to verify all the fields of the Pizza ORM were being populated._

_Finally, I had to use divide and conquer to determine why the orders weren't being displayed, by using the `.count()` function on the `home.html` Jinja template. This led me to deduce the error was in the `/order`, right where we were making the call to `db.session.add`._
## Exercise 2

[[Your answer goes here!]]

## Exercise 3

[[Your answer goes here!]]
