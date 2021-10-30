#!/bin/python
# coding=utf-8

import requests
import sys
import re
import codecs
from getpass import getpass
from simple_term_menu import TerminalMenu

OGS_CLIENT_ID="***REMOVED***"
OGS_CLIENT_SECRET="***REMOVED***"

def komi_replacement(m):
    s = m.group()
    n = int(s[3:-1])
    new = str(2*n)
    return "KM[" + new[:-2] + "." + new[-2:] + "]"

def fix_komi(sgf):
    regex = r"KM\[[1-9][0-9]*\]"
    return re.sub(regex, komi_replacement, sgf)

def get_uid(username):
    values = { 
            "srcuid":0,
            "dstuid":0,
            "dstuin":0,
            "username":username,
            "accounttype":0,
            "clienttype":0
            }
    url = "http://h5.foxwq.com/getFechInfo/wxnseed/txwq_fetch_personal_info"
    try:
        response = requests.get(url,data=values)
        return response.json()['uid']
    except Exception as e:
        print(e)
        sys.exit(1)

def game_list(lastCode, username, uid):
    chessid = []
    names = []
 
    values = {
    "type": 4,
    "lastCode": lastCode,
    "FindUserName": username, 
    "uid": uid, 
    
    "RelationTag": 0}

    url = "http://happyapp.huanle.qq.com/cgi-bin/CommonMobileCGI/TXWQFetchChessList"
    try:
        response = requests.post(url,data=values)
        response.encoding="utf-8"
        chesslist = response.json()['chesslist']
        for d in chesslist:
            chessid.append(d['chessid'])
            starttime = d['starttime'].split(' ')[0].replace('-', '.')
            id = d['chessid'][10:]
            blackenname = d['blackenname']
            whiteenname = d['whiteenname']
            names.append(starttime + ' ' + blackenname + ' VS ' + whiteenname + ' (' + id + ')' )
        return chessid, names
    except Exception as e:
        print(e)
        sys.exit(1)

def download_sgf(cid):
    values = {
    "chessid": cid
    }
    url = "http://happyapp.huanle.qq.com/cgi-bin/CommonMobileCGI/TXWQFetchChess"
    sgf = ""
    for i in range(10):
        try:
            response = requests.post(url,data=values)
            response.encoding="utf-8"
            sgf = response.json()['chess']
            break
        except Exception as e:
            if i == 9:
                print(e)
                sys.exit(1)
    return sgf

def get_ogs_token(username, password):
    values = { 
            "grant_type":"password",
            "username":username,
            "password":password,
            "client_id":OGS_CLIENT_ID,
            "client_secret":OGS_CLIENT_SECRET,
            }
    url = "https://online-go.com/oauth2/token/"
    try:
        response = requests.post(url,data=values)
        response_json = response.json()
        return response_json['token_type'], response_json['access_token']
    except Exception as e:
        print(e)
        sys.exit(1)

def upload_to_ogs(filename, sgf, token_type, access_token):
    headers = {
            "Authorization":token_type+" "+access_token
            }
    files = {'file': (filename, sgf, 'application/x-go-sgf')}
    url = "https://online-go.com/api/v1/me/games/sgf/0"
    try:
        response = requests.post(url,headers=headers,files=files)
        if response.json()['success'] == "Files uploaded":
            return True
        else:
            return False
    except Exception as e:
        print(e)
        sys.exit(1)


def main():
    ogs_upload = False
    ogs_access_token = ""
    ogs_token_type = ""

    print("What do you want to do with the downloaded Fox games?")
    options = ["Upload to OGS", "Save to disk"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()

    if index == None:
        print("Aborting.")
        sys.exit(0)
    elif index == 0:
        ogs_upload = True
        ogs_token_type, ogs_access_token = get_ogs_token(input("OGS username: "), getpass("OGS password: "))

    username = input("Fox username: ")

    uid = get_uid(username)

    lastCode = ""
    while True:
        chessids, names = game_list(lastCode, username, uid)

        
        n = len(names)
        names.append("older games ...")

        if n == 0:
            if lastCode == "":
                print("No games found. Exiting.")
                break
            else:
                print("No older games found.")
                chessids = oldchessids
                names = oldnames

        terminal_menu = TerminalMenu(names)
        index = terminal_menu.show()
        if index == None:
            print("Aborting.")
            break
        if index == n:
            lastCode = chessids[-1]
            oldchessids = chessids
            oldnames = names
        else:
            print(f"Downloading {names[index]} ...")
            filename=names[index]+".sgf"
            sgf = fix_komi(download_sgf(chessids[index]))
            if ogs_upload:
                upload_to_ogs(filename, sgf, ogs_token_type, ogs_access_token)
            else:
                f = codecs.open(filename, 'w', 'utf-8')
                f.write(sgf)
                f.close()
            break

if __name__ == "__main__":
    main()
