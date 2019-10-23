## Example of collecting metrics with multithreading

__There was no particular information being provided, so it was decided to make and example with a help of testing ZABBIX server (10k+ metrics). Python 3.6 was used for development.__

**1.** If one is willing to test this utility, go get a **pyzabbix** module:
```sh
pip3 install py-zabbix
```

**2.** Run the application:
```sh
python3 task.py
```

**3.** Enter desired dates

**4.** Watch average of metric values being calculated with multitreading
