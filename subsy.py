# The following is a script in streamlit that uses BinaryEdge and SecurityTrails APIs for subdomain enumeration. It takes input a domain name.
# Most of the code has been written by Codex of OpenAI. I only tweaked it.

import requests
import json
import pandas as pd
import streamlit as st
import time
import os
import re

st.title("Subdomain Enumeration")
st.markdown("This is a simple script that uses BinaryEdge and SecurityTrails APIs to enumerate subdomains.")
st.markdown("**_Note that you will need API keys from BinaryEdge and SecurityTrails._**")

st.sidebar.markdown("**_BinaryEdge API_**")
API_KEY_BE = st.sidebar.text_input("Insert your BinaryEdge API key",type="password")

st.sidebar.markdown("**_SecurityTrails API_**")
API_KEY_ST = st.sidebar.text_input("Insert your SecurityTrails API key",type="password")

domain = st.text_input("Enter the domain name")

def get_subdomains_from_binaryedge(domain, API_KEY_BE):
    url = "https://api.binaryedge.io/v2/query/domains/subdomain/{}".format(domain)
    headers = {"X-Key": API_KEY_BE}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return "BinaryEdge returned status code {}".format(res.status_code)
    else:
        return res.json()

def get_subdomains_from_securitytrails(domain, API_KEY_ST):
    url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(domain)
    headers = {"apikey": API_KEY_ST}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return "SecurityTrails returned status code {}".format(res.status_code)
    else:
        return res.json()
        
def main():
    if st.button("Submit"):
        st.write("Submitting...")
        time.sleep(1)
        try:
            subdomains_binaryedge = get_subdomains_from_binaryedge(domain, API_KEY_BE)
            subdomains_securitytrails = get_subdomains_from_securitytrails(domain, API_KEY_ST)
            sectrails_new = []
            for subdomain in subdomains_securitytrails["subdomains"]:
                subdomain = subdomain+"."+domain
                sectrails_new.append(subdomain)
            st.write("BinaryEdge returned {} subdomains".format(len(subdomains_binaryedge["events"])))
            st.write("SecurityTrails returned {} subdomains".format(len(sectrails_new)))
            st.write("Merging results...")
            time.sleep(1)
            subdomains = list(set(subdomains_binaryedge["events"])) + list(set(sectrails_new))  
            st.write("Merged {} subdomains".format(len(subdomains)))
            st.write("Saving results...")
            time.sleep(1)
            #subdomains = [x[0] for x in subdomains]
            subdomains = list(set(subdomains))
            df = pd.DataFrame(subdomains)
            df.to_csv("subdomains.csv")
            st.write("Saved to subdomains.csv")
            st.write(df)
        except Exception as e:
            st.write(e)

if __name__ == "__main__":
    main()
