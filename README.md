# impacto-python: Client library for Impacto API, written in Python


## Installation

- `pip install requests`
- Download `impacto.py`

> Note: will be available on PyPI soon.


## Getting objects

First, you need to import the `Impacto` class and authenticate:

```python
from impacto import Impacto

api = Impacto(username=username, password=password)
```

For authentication you can use:
- `username` and `password`; or
- `email` and `password`; or
- `access_token`.


Now, let's get some objects - insights, impacts and stories:

```python
for counter, obj in enumerate(api.insights(), start=1):
    print(f'Insight #{counter}: {obj}')
for counter, obj in enumerate(api.impacts(), start=1):
    print(f'Impact #{counter}: {obj}')
for counter, obj in enumerate(api.stories(), start=1):
    print(f'Story #{counter}: {obj}')
```

> Note 1: these call will return **all objects** since it automatically
> navigate in the pagination provided by the API.

> Note 2: story statistics will not be shown when using `api.stories()` - for
> this you need to get the Story object, as explained below.

You can also get individual objects, like:

```python
my_impact = api.impact(id=123)
my_insight = api.insight(id=123)
my_story = api.story(id=123)  # this one has 'stats' key
```

### Filtering

You can use any filter the API supports in all objects (impacts, insights and
stories) - just pass the parameter to the listing function. Let's filter all
posts by politicians on Facebook linking to the partner's website:

```python
insights = api.insights(date_min='2018-03-01', type='politics', media='facebook')
for counter, obj in enumerate(insights, start=1):
    print(f'Insight #{counter}: {obj}')
```

> Note: check the [API documentation](api.md) for more information on filters.


## Creating Objects

- Create impact: to be done
- Create insight: to be done
