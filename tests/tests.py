import requests as r
import sys
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker

'''
https://gist.github.com/nik1997/6cb1a0406d4024d913f044fb3bba92d2
'''
#bash
'''
docker swarm init
docker stack deploy -c web/docker-compose.yml cs162-swarm
echo "Sleeping now for 5s"
sleep 5
python tests.py
docker stack rm cs162-swarm
docker swarm leave --force
'''
'''
docker swarm init;docker stack deploy -c web/docker-compose.yml cs162-swarm;cat "Sleeping now";sleep 5s;python tests.py;docker stack rm cs162-swarm;docker swarm leave --force
'''


## setup
database_uri = 'postgresql://cs162_user:cs162_password@localhost:5432/cs162'
engine = create_engine(database_uri, echo = True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()


class Expression(Base):
    __tablename__ = 'expression'

    id = Column(Integer, primary_key=True)
    text = Column(String(200))
    value = Column(Numeric)
    now = Column(DateTime, default=datetime.utcnow)

# session.drop_all()
# session.create_all()

# test1
# defining the api-endpoint
results = {}
API_ENDPOINT = "http://localhost:5000/add"

valid_test_exp = "1 + 1"
data = {'expression': valid_test_exp}

resp_test1 = r.post(url = API_ENDPOINT, data = data)

print("\n\n result of test 1")
print(resp_test1.status_code, resp_test1.reason)
try:
    if resp_test1.status_code == 200:
        results['test1'] = "PASS"
    else:
        results['test1'] = "FAIL"
        raise Exception('Test of valid POSt request failed')
except Exception as e:
    print(e)
    sys.exit(0)

# test2
print("\n\n---test2----")

abc = Expression
return_exp = session.query(Expression).filter(Expression.text == valid_test_exp).first()
# print(expressions)
print("\n\n---test2----")
try:
    if return_exp != None:
        print("{} = {}. Created at {}".format(return_exp.text, return_exp.value, return_exp.now))
        results['test2'] = "PASS"
    else:
        results['test2'] = "FAIL"
        raise Exception('TEST FAILED of valid POSt request did not save data to database')
except Exception as e:
    print(e)
    sys.exit(0)
print("\n")


#test 3
# Invalid data
# defining the api-endpoint
print("\n\n---Testing Invalid Data")

invalid_test_exp = "1 + a"
data = {'expression': invalid_test_exp}
API_ENDPOINT = "http://localhost:5000/add"

print('Datasent {}'.format(data))
# sending post request and saving response as response object
r = r.post(url = API_ENDPOINT, data = data)
print(r.status_code, r.reason)
try:
    if r.status_code == 500:
        results['test3'] = "PASS"
    else:
        results['test3'] = "FAIL"
        raise Exception('TEST FAILED: No failed(500) response for Invalid expression')
except Exception as e:
    print(e)
    sys.exit(0)
print("\n")

print("\n")
#

# test2
print("\n\n---test4----")

abc = Expression
return_exp = session.query(Expression).filter(Expression.text == invalid_test_exp).first()
try:
    if return_exp == None:
        results['test4'] = "PASS"
    else:
        results['test4'] = "FAIL"
        raise Exception('TEST FAILED of invalid expression saved in the database')
except Exception as e:
    print(e)
    sys.exit(0)
print("\n")

print("\n")

print("\n\n\n")
print(results)
print("All tests passed YAHOOOOO")
