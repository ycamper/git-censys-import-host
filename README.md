# Censys import-host Git Plugin

This is a simple script that will import a host's history from [Censys](https://search.censys.io) into a Git repository,
allowing for analysts to quickly review the history of a host in a git-intuitive way.

This script attempts to preserve the timestamp of the host change into the commit log, and logs every major action as the commit message.

## Install

1. `pip install -r requirements.txt`
2. Copy `git-import-host.py` to `$PATH/git-import-host` and `chmod +x` to make it executable.

## Run

1. `mkdir host_history/ && cd host_history/`
2. Initialize the repository: `git import-host init`
3. Import the host `1.1.1.1`'s history between 2023-10-01 and 2023-10-03: `git import-host -f 2023-10-01 -t 2023-10-03 1.1.1.1`
4. Profit?

```sh
lz@localhost:~/host_history$ git import-host -f 2023-10-01 -t 2023-10-03 1.1.1.1 
lz@localhost:~/host_history$ git log --reverse -5 -p 1.1.1.1
commit 9266a5875da425df0f17b1eb91b9d8d3ba51af3d
Author: Mark Ellzey <ellzey@censys.io>
Date:   Tue Oct 3 20:37:34 2023 -0400

    replace /services/15/banner

diff --git a/1.1.1.1 b/1.1.1.1
index a0ed4c0..4f75c93 100644
--- a/1.1.1.1
+++ b/1.1.1.1
@@ -1660,8 +1660,8 @@
         },
         "supports_http2": false
       },
-      "observed_at": "2023-10-02T21:49:44.925170113Z",
-      "perspective_id": "PERSPECTIVE_TELIA",
+      "observed_at": "2023-10-03T21:16:46.292795981Z",
+      "perspective_id": "PERSPECTIVE_TATA",
       "port": 8080,
       "service_name": "HTTP",
       "software": [
@@ -1701,10 +1701,10 @@
         "fingerprint": "27d3ed3ed0003ed1dc42d43d00041d6183ff1bfae51ebd88d70384363d525c",
         "cipher_and_version_fingerprint": "27d3ed3ed0003ed1dc42d43d00041d",
         "tls_extensions_sha256": "6183ff1bfae51ebd88d70384363d525c",
-        "observed_at": "2023-09-15T23:58:14.884313902Z"
+        "observed_at": "2023-10-03T23:04:48.296685713Z"
       },
-      "observed_at": "2023-10-02T03:04:25.096217513Z",
-      "perspective_id": "PERSPECTIVE_ORANGE",
+      "observed_at": "2023-10-03T20:16:31.108109682Z",
+      "perspective_id": "PERSPECTIVE_TATA",
       "port": 8443,
       "service_name": "UNKNOWN",
       "software": [
@@ -1715,7 +1715,7 @@
           "source": "OSI_TRANSPORT_LAYER"
         }
       ],
-      "source_ip": "167.94.145.59",
+      "source_ip": "167.94.138.36",
       "tls": {
         "version_selected": "TLSv1_3",
         "cipher_selected": "TLS_CHACHA20_POLY1305_SHA256",
@@ -1828,7 +1828,7 @@
         "banner": "DISPLAY_UTF8",
         "banner_hex": "DISPLAY_HEX"
       },
-      "banner": "HTTP/1.1 301 Moved Permanently\r\nServer: cloudflare\r\nDate:  <REDACTED>\r\nContent-Type: text/html\r\nContent-Length: 167\r\nConnection: keep-alive\r\nLocation: https://1.1.1.1/\r\nCF-RAY: 80f71f64e90f2300-ORD\r\n",
+      "banner": "HTTP/1.1 301 Moved Permanently\r\nServer: cloudflare\r\nDate:  <REDACTED>\r\nContent-Type: text/html\r\nContent-Length: 167\r\nConnection: keep-alive\r\nLocation: https://1.1.1.1/\r\nCF-RAY: 81083a5118f622f7-ORD\r\n",
       "banner_hashes": [
         "sha256:bc0d1d97f59364b0b8fd4bdaf5f864bb04c4bc891b8eb814d002df1316907e18"
       ],
```
