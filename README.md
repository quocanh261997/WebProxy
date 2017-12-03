#### Name: Quoc Anh Nguyen, Andre Le
#### Class: CSE 283 - Section A
#### Date: 12/02/2017
#### Assignment: Project 2: Web Proxy

## Instructions running the program

1. Download the zip file and extract it
2. Make sure you have installed Python 2 on your computer
3. This step is different for the different type of Operating System your are using:

 * If you use Windows, go to **Control Panel** => **Internet Options** => **Connections** => **LAN Settings** => **Proxy Server**. Once in it, check the box for **Proxy Server where Use a proxy server for your LAN**, and enter the *Address* and *Port* that you would use for the proxy. To fine-tune the proxy settings such that they are only applied to HTTP (and not HTTPS, FTP, etc.) you can use the **Advanced** push button.In this case, the address should be **localhost** and port number will be of your choice.

 * If you use Ubuntu, go to Unity Dash and type **"Network"**, and choose the **Network Proxy** option. Change the method from **Automatic** to **Manual** and enter the address and port for HTTP Proxy only. In this case, the address should be **localhost** and port number will be of your choice. Once done, click **Apply system wide** to enable it.

 * If you use MacOS, choose **System Preferences** and click **Network**. Choose **Advanced** and then choose **Proxies**. Configure the address and the port number there and apply it. In this case, the address should be **localhost** and port number will be of your choice.

4. Open your terminal and navigate to the extracted folder. Type in this command:
```
python proxy.py <yourPortNumber>
```
with *yourPortNumber* as the port you would like the proxy to serve with. This port number **must** match the port number that you enter in the proxy settings in the last step.

5. The proxy should send in a message in the terminal saying "Ready to serve, listening to port ...."

6. Open any browser, and type in the website name you would like to see.

7. If the websites you enter has contents or urls matched one of the bad keywords, it will be redirected to one of the error website. **Note: This only applies to website serves over HTTP**

8. Enter **Ctrl+C** to terminate the proxy. Remember to change back the proxy settings to resume your normal network activities.

## Manual
* The function **serve_connection** implements feature 2.
* The function **contains_keywords** and **serve_connection** implements feature 3.
* Line **17** supports user choice of port number
* The function **check_for_content** checks for which content needed to be check and implements feature 8

## Functionality
* The proxy can get you to your basic webpages
* It will block that webpage if it contains bad keywords in the url or content, and redirect you back to the error webpage. Note this only applies to HTTP webpage. Other HTTPS won't be blocked

## Testing
* The code can go through every case that the project requires, except the bad content file, since it cannot decode the data and cannot do a check for bad keywords to block it.
* We have tested with these following pages.
- http://ceclnx01.eas.miamioh.edu/~gomezlin/goodtest1.txt the proxy did not block this page.
- http://ceclnx01.eas.miamioh.edu/~gomezlin/goodtest2.html the proxy did not block this page.
- http://ceclnx01.eas.miamioh.edu/~gomezlin/SpongeBob.html which has bad keywords ("spongebob") in the URL, so the proxy blocks requests for undesirable URL and redirect to the error page.
- http://www.nick.com/spongebob-squarepants/ which has bad keywords ("spongebob") in the URL, so the proxy blocks requests for undesirable URL and redirect to the error page.
* The proxy works with Chrome, Firefox, Safari, and other major browsers.
* The test does not work when we search the keyword on Google, Wikipedia or Youtube, because both Google and Youtube uses https and our proxy only works with http.
* Here is the video contains the testing of the proxy: https://youtu.be/dphFxYutDQA