## About script
this tool make bruteforce HTTP Authentication Creds on multiple urls in short time <br> 
the tool have argument -p, --proxies , this arg will use proxies to skip block, can use one or multiple via file and will found default proxies file in wordlists directory please choose -p 'default' to use it <br>
NOTIC: wordlists/proxies-raw.txt file , It is updated every time run tool and contains larger of 400 valid proxy

## Installation
pip3 install -r requirements.txt

## Usage
short arg     | long arg      | Description
------------- | ------------- |-------------
-u            | --url         | unique url to testing
-us           | --urls        | File contain urls Ex: urls.txt
-c            | --creds    	  | File contain http auth creds
-p            | --proxies     | File contains proxy:port
-t            | --threads     | Thread number to MultiProccess [speed tool] , Default 30
-T            | --timeout     | Timeout if delay request, Default is 1
-s            | --sleep       | sleep after every request
-v            | --view     	  | display request sended
-o            | --output      | save success results in file
-h            | --help        | show the help message and exit

if you want use multiple proxy ==> seperator via [,] or choose file

## Examples
- Default usage
```python
python3 httpAuth.py -us https.txt
```
- Put multiple proxies  
```python
python3 httpAuth.py -us https.txt -p '198.168.1.1:8080,198.168.1.79:8080'
```
- My usage
```python
python3 httpAuth.py -us https.txt --threads 200 --timeout 10 --sleep 5 -p proxies_file.txt
```
- try many testing
```python
python3 httpAuth.py --urls https.txt --threads 200 --timeout 10 -m
```
