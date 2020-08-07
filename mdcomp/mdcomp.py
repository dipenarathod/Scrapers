# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 01:16:30 2020

@author: Dipen
"""

import requests
from bs4 import BeautifulSoup as bs
import re

md_comp_name=[]
md_comp_price=[]
def md_comp_data(name,price):
    url="https://mdcomputers.in/"
    soup=bs(requests.get(url).content)
    #menu=soup.find("ul",attrs={"class":"megamenu"})
    links=soup.find_all("a")
    true_links=[]
    for link in links:
        try:
            if((link["href"].startswith("http")) and (not("account" in link["href"])) and (not("login" in link["href"])) 
              and (not(link["href"].endswith("mdcomputers.in"))) and (not(link["href"].endswith("mdcomputers.in/")))):
                    true_links.append(link["href"])
        except:
            pass
    for link in true_links:
        soup_link=bs(requests.get(link).content)
        items=soup_link.select("div.product-item-container")
        for item in items:
            #print(item.h4.get_text(),end=" ")
            temp=item.h4.get_text().strip()
            if(temp not in name):
                name.append(temp)
                price_temp=item.find("span",attrs={"class":"price-new"}).get_text().strip()
                price.append(int(re.sub(r'[^\w]', '', price_temp)))
            #name.append(item.h4.get_text().strip())
            #print(item.find("span",attrs={"class":"price-new"}).get_text())
            #price.append(item.find("span",attrs={"class":"price-new"}).get_text().strip())
            #price_temp=item.find("span",attrs={"class":"price-new"}).get_text().strip()
            #price.append(int(re.sub(r'[^\w]', '', price_temp)))
        #print("#"*30)


md_comp_data(md_comp_name,md_comp_price)

import sqlite3
conn=sqlite3.connect("Parts.db")
def create_table(table_name,conn):
    cursor=conn.cursor()
    command="CREATE TABLE IF NOT EXISTS "+table_name+"(Name text,price Real)"
    cursor.execute(command)
    #cursor.execute("CREATE TABLE IF NOT EXISTS mdcomp(Name text, price Real)")


create_table('mdcomp',conn)
def data_transfer(names,prices,table_name,conn):
    cursor=conn.cursor()
    for i in range(len(prices)):
        tup=(names[i],prices[i])
        sql=''' INSERT INTO '''+table_name+'''(Name,price)
              VALUES(?,?) '''
        cursor.execute(sql,tup)
        conn.commit()
        
data_transfer(md_comp_name,md_comp_price,'mdcomp',conn)

def read_from_table(table_name,conn):
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM '+table_name)
    data = cursor.fetchall()
    print(data)
    for row in data:
        print(row)
    conn.commit()
read_from_table('mdcomp',conn)

def delete_all_entries(table_name,conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM '+table_name
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
#delete_all_entries('mdcomp',conn)