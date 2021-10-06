
from pprint import pprint
import time
import urllib
import httpx
import json
import pickle
from splinter import Browser
from selenium import webdriver
from config.td_config import TdConfig

from config.td_config import TdConfig


class TD_Authorization:

    def __init__(self):
        self.config = TdConfig()

    def __getattr__(self, attr):
        if attr == "access_token":
            return self._retrieve_access_token()

    def _check_config(self):
        try:
            _ = pickle.load(open("config/config.pickle", "rb"))
            return _
        except:
            pass

    def _retrieve_access_token(self):
        try:
            _ = pickle.load(open("config/auth_token.pickle", "rb"))
            return _
        except:
            self.o_auth()

    def td_login(self):
        self._retrieve_access_token()
        if self.access_token['refresh_token_expires_at'] - 100 <= int(time.time()):
            self.o_auth()
        elif self.access_token['access_token_expires_at'] - 50 <= int(time.time()):
            self.o_auth_refresh()
        else:
            #print(f"{self._access_token_dict['refresh_token_expires_at'] -int(time.time())} seconds to refresh token expiration")
            #print(f"{self._access_token_dict['access_token_expires_at']-int(time.time())} seconds to access token expiration")
            print('Checking token status...')

    def o_auth(self):
        print('Authenticating please wait...')
        executable_path = {'executable_path': r'/usr/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)
        method = 'GET'
        url = 'https://auth.tdameritrade.com/auth?'
        client_code = self.config.api_key + '@AMER.OAUTHAP'
        payload = {'response_type': 'code',
                   'redirect_uri': 'http://127.0.0.1',
                   'client_id': client_code}
        built_url = httpx.Request(method, url, params=payload)
        # print(built_url.url)
        built_url = str(built_url.url)
        # print(type(built_url))
        browser.visit(built_url)
        payload = {'username': self.config.account_number,
                   'password': self.config.password}
        browser.find_by_id("username0").first.fill(payload['username'])
        browser.find_by_id("password1").first.fill(payload['password'])
        browser.find_by_id("accept").first.click()
        time.sleep(1)
        browser.find_by_text('Can\'t get the text message?').first.click()
        time.sleep(1)
        browser.find_by_value("Answer a security question").first.click()
        time.sleep(1)
        # for question in self.questions:
        for question in self.config.QUESTIONS:
            if browser.is_text_present(question):
                browser.find_by_id('secretquestion0').first.fill(
                    self.config.QUESTIONS[question])
        time.sleep(1)
        # print(browser.is_element_present_by_id('rememberdevice'))
        browser.find_by_xpath(
            '//*[@id="authform"]/main/div[5]/span/label').click()
        time.sleep(1)
        browser.find_by_id('accept').first.click()
        time.sleep(1)
        browser.find_by_id('accept').first.click()
        time.sleep(1)
        new_url = browser.url
        # print(new_url)
        parse_url = urllib.parse.unquote(new_url.split('code=')[1])
        browser.quit()
        parse_url
        # define the endpoint
        url = 'https://api.tdameritrade.com/v1/oauth2/token'

        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        payload = {'grant_type': 'authorization_code',
                   'access_type': 'offline',
                   'code': parse_url,
                   'client_id': self.config.api_key,
                   'redirect_uri': self.config.redirect_uri}
        # post the data

        authReply = httpx.post(url, headers=headers, data=payload)
        #print("type authreply",type(authReply))
        decoded_content = authReply.json()
        #print("type decoded content",type(decoded_content))
        access_token_expires_at = int(time.time())+1800
        decoded_content.update({'refresh_token_created_at': int(time.time()),
                                'refresh_token_expires_at': int(time.time())+7776000,
                                'access_token_expires_at': access_token_expires_at})
        #print(json.dumps(decoded_content, indent=4))
        _ = json.dumps(decoded_content, indent=4)
        # print("json dumps type",type(_))
        self._access_token_dict = decoded_content
        pickle.dump(decoded_content, open(
            "config/auth_token.pickle", "wb"))
        return decoded_content

    def o_auth_refresh(self):
        print('Obtaining a new token....')
        url = 'https://api.tdameritrade.com/v1/oauth2/token'

        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        payload = {'grant_type': 'refresh_token',
                   'refresh_token': self.access_token['refresh_token'],
                   # 'code':parse_url,
                   'client_id': self.config.api_key,
                   'redirect_uri': self.config.redirect_uri}
        # post the data

        authReply = httpx.post(url, headers=headers, data=payload)

        decoded_content = authReply.json()
        access_token_expires_at = int(time.time())+1800
        decoded_content.update({'refresh_token': self.access_token['refresh_token'],
                                'refresh_token_created_at': int(time.time()),
                                'refresh_token_expires_at': self.access_token['refresh_token_expires_at'],
                                'access_token_expires_at': access_token_expires_at})
        self._access_token_dict = decoded_content
        pickle.dump(decoded_content, open(
            "config/auth_token.pickle", "wb"))

        # print(decoded_content)
