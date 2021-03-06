# Debug Log

**Explain how you used the the techniques covered (Trace Forward, Trace Backward, Divide & Conquer) to uncover the bugs in each exercise. Be specific!**

In your explanations, you may want to answer:

- What is the expected vs. actual output?
- If there is a stack trace, what useful information does it contain?
- Which technique did you use, on which line numbers?
- What assumptions did you have about each line of code, and which ones were proven to be wrong?

_Example: I noticed that the program should show pizza orders once a new order is made, and that it wasn't showing any. So, I used the trace forward technique starting on line 13. I discovered the bug on line 27 was caused by a typo of 'pzza' instead of 'pizza'._

_Then I noticed another bug .._

## Exercise 1

_I noticed there was a TypeError occuring on line 81, where we append the toppings to the new pizza that the user has ordered. Since I was really new to the codebase, I started from the top of `app.py`, and realized the parameter for the toppings on line 81 was wrong, looking at the class definition for the `PizzaTopping`._

_The second problem I noticed is the print statement after the pizza was added to the db was outputting `None`. At this point I knew a little more, so I traced backward to the form template on `order.html`, and realized that the names on the form fields, was different from what was being referenced in the `/order` route. So I fixed it, and used a print statement on line 86 of `app.py` to verify all the fields of the Pizza ORM were being populated._

_Finally, I had to use divide and conquer to determine why the orders weren't being displayed, by using the `.count()` function on the `home.html` Jinja template. This led me to deduce the error was in the `/order`, right where we were making the call to `db.session.add` This led me to reading to [docs on the SQLAlchemy ORM](https://docs.sqlalchemy.org/en/13/orm/tutorial.html) and a YouTube video by Corey Schaefer, which helped me realized I needed to use the `db.session.commit` statement with every call to `db.session.add`, and to make sure the session was open. The rest of the time I spent using print statements to deduce why the `PizzaTopping` objects weren't being made correctly, because there was an `IntegrityError` that kept appearing, which said that the class needed both the pizza topping type as a string (all uppercase), and the id of a `Pizza` instance. Ultimately, it became clear that the logic of the route also needed to change, because the `Pizza` needs to be inserted before the related models for `PizzaTopping`, so I moved those statements around accordingly._

## Exercise 2

_The first problem I saw was that there was a `KeyError` when trying to parse the JSON. Using this info I traced back to where the API call was being made, and decided to print the JSON. This led me to another error, which the API was being incorrectly made (the response code in the JSON was 4xx). Therefore, I used divide and conquer to first check that the data was being passed from the HTML form correctly, and then being made correctly. I traced forward in the `home.html` template, and realized the names of the field inputs didn't match what was being requested in the app routes, so that was resolved. Next, I looked up some examples on the [OpenWeather Map API](https://openweathermap.org/current), and realized the `place` parameter in the API call really needed to be called `q`. Then, the response from the API was successfully returned with a HTTP 200..._

To make the next paragraph clearer, consider this example of a successful API response:

```
{
    "coord": {
        "lon": -71.0598,
        "lat": 42.3584
    },
    "weather": [
        {
            "id": 804,
            "main": "Clouds",
            "description": "overcast clouds",
            "icon": "04d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 32.81,
        "feels_like": 23.65,
        "temp_min": 30.99,
        "temp_max": 35.01,
        "pressure": 1016,
        "humidity": 86
    },
    "visibility": 10000,
    "wind": {
        "speed": 9.22,
        "deg": 340
    },
    "clouds": {
        "all": 90
    },
    "dt": 1611763678,
    "sys": {
        "type": 1,
        "id": 3486,
        "country": "US",
        "sunrise": 1611748944,
        "sunset": 1611784288
    },
    "timezone": -18000,
    "id": 4930956,
    "name": "Boston",
    "cod": 200
}
```

_...Then the next error was that the `temperature` key wasn't in the JSON response, which threw a `KeyError`. At first instinct I thought to check the route again, but first I thought it'd be better to first use divide and conquer, so I would be sure the HTML template was rendering all the variables from the context dictionary. It already was, so that probably wasn't the most effective debugging decision. Anyway, I looked the example API responses from before, found the real way to get the temperature was with `result_json['main']['temp']`. I made that change where the `KeyError` was, and the issue was resolved._

## Exercise 3

_I used divide and conquer to see the first issue was in `util.py`, and that it had to do with the Merge Sort function. I traced forward through both functions because it was a little different from the implementations I'm used to. Then I saw a few issues, related to just implementing the algorithms the way they are intended to be. Firstly, the comparision operator on line 37 was `>` so I changed it to be `<=`._

_Then I realized the output had more 2's in it than in the input, so I traced back through the three while loops (which help implement the "merge" step of Merge Sort), and realized that `k`, the index of `arr`, needs to increment along with either `i` or `j`, like it does in the first `while` loop (this is in the case the `left_side` and `right_side` have unequal lengths)._

_Lastly, for the binary search algorithm I traced back to where `mid` is initialized, and changed the division operator from `/` to `//`, since that would prevent the `IndexError` in the stack trace. Finally, I used the previous developer's comments to fix the control flow - they understood the algorithm well, we just needed to move the statements to the line numbers where they would match the comments. I only had to add an additional `if` condition on line 52, that would return the index if the `elem` value was found._
