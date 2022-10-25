# find_blueprint_ports
Script to scrape blueprint repository looking for available ports.

Looks for the pattern:
```
    ports:
        loadbalancer_ports: 
            - XXXX
        service_ports:
            - XXXX
```

Returns YAML file containing ports still available from 9000 to 10000:
```
free_ports:
  - XXXX
  - YYYY
  - ZZZZ
```

### Usage
```python main.py```