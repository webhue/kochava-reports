# Kochava Reports
Python library to request and query reports in the Kochava platform. It can be used to generate reports and query for some metadata. The implemented functionality is not exhaustive and is focused on generating reports. Scheduling reports is currently not possible.

# Creating the client:

```python
from kochavareports import KochavaClient, KochavaCredentials


credentials = KochavaCredentials('my API key', 'my app guid')
client = KochavaClient(credentials)
```

# Creating a report:

Creating a one-time report is easy:

```python
request_data = {
	'time_start': '2017-01-25',
	'time_end': '2017-02-07',
	'traffic': [
		'click',
		'install'
	],
	'traffic_grouping': [
		'network',
		'campaign'
	],
	'time_series': '1'
}
token = client.create_report(**request_data)
print token
```

```time_start``` and ```time_end``` parameters can be ISO formatted strings, datetime objects or timestamps: they are converted internally to a timestamp, as required by the API.

More report parameters and usage examples can be found here:

[Requesting and Scheduling Reports](https://support.kochava.com/analytics-reports-api/api-v1-2-requesting-and-scheduling-reports)

[Call Structure](https://support.kochava.com/analytics-reports-api/api-v1-2-call-structure)

If you want a Detail report instead of a Summary report (default), you can add an additional parameter ```reportCategory='detail'```.

The returned token can be used to check the report progress and read the report data, as seen below.

# Getting the report progress and read it:

Once a report has been queued you can check it's progress at any time. If it's completed you can read the report data:

```python
response = client.get_report_progress(token)
if response.is_completed():
    report_data = client.read_report(response.get_report_url())
    print report_data
else:
    print response.progress
```

See here a list of reports fields:

[Reports Overview](https://support.kochava.com/analytics-reports-api/reports-overview)

# Polling until the report is completed:

If you don't have complex code and you are happy waiting until the report is completed you can use this code which does some basic polling:

```python
result = client.poll_report(token)
print result
```

The above code does simple polling: it waits for 15 seconds and then check the report progress every second. When finished, the report result is returned. These parameters should work most of the time but you can change them like this, if needed:

```python
result = client.poll_report(token, retry_interval_seconds=1,
                            start_delay_seconds=15, max_retries=30)
print result
```

```max_retries``` parameter (30, by default) is used to avoid infinite loop issues or possible rate-limiting issues. If you expect the report to take a long time to be completed you can set ```start_delay_seconds``` to a higher value.

If the ```max_retries``` limit has been reached a ```kochavareports.exception.PollMaxRetryException``` will be raised.

# Misc

When making calls, you should generally check for ```kochavareports.exception.HttpException```, which will wrap around a ```requests.exceptions.RequestException``` adding some utility methods. All other exceptions extend the ```ApiException``` base class.

# License

MIT. 'nuff said.

# TODO

 - Unit tests.

