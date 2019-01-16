# -*- coding: utf-8 -*-


from locust import HttpLocust, TaskSet, task
import random
import logging
import re
import json
import config as conf
from itertools import cycle
from requests.auth import HTTPBasicAuth
import base64
import re

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NexusTaskSet(TaskSet):


  def on_start(self):

    ''' load data files containing uris, logins '''
    with open(conf.urifile) as u:
      self.uris = [ x.strip() for x in u.readlines() ]
      self.uris_cycle = cycle(self.uris)
    with open(conf.loginfile) as l:
      self.logins = [ x.strip() for x in l.readlines() ]
      self.logins_cycle = cycle(self.logins)

  def randomValue(self):
    self.uri = random.choice(self.uris)
    self.login = random.choice(self.logins)


  def nextValue(self):
    self.uri = next(self.uris_cycle)
    self.uris.remove(self.value)
    self.uris_cycle = cycle(self.uris)
    self.login = next(self.logins_cycle)
    self.logins_cycle = cycle(self.logins)



  @task(1)
  def send_nexus(self):

    ## pick a random uri or cycle through the data file:
    self.randomValue()
    #self.nextValue()


    login = "{}".format(self.login)
    url = "{}".format(self.uri)
    logging.debug("##### Locust script: login = {} / uri = {}".format(url, login))


    headers_fetch = dict()
    #headers_fetch['Host'] = "talend-update.talend.com"
    #headers_fetch['Cookie'] = "NXSESSIONID={}".format(self.basic_token)

    res = self.client.get(url, headers=headers_fetch, auth=HTTPBasicAuth(login.split(':')[0],login.split(':')[1]), verify=False, name='Fetch')



class TalendNexusLocust(HttpLocust):
  task_set = NexusTaskSet
  # wait timeframe in ms
  min_wait = conf.TTimeMin
  max_wait = conf.TTimeMax
  #host = 'https://192.168.17.36:443'
  host = 'https://talend-update.talend.com:443'


if __name__ == '__main__': # for testing directly
  l = TalendNexusLocust()
  l.host = 'https://talend-update.talend.com:443'
  ts = NexusTaskSet(l)
  ts.on_start()
  ts.send_nexus()

