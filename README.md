# Hetzner DNS - IP Updater (DDNS) 🕸️

Simple script to update DNS entries on Hetzner DNS service. At the moment it only works for A records.

### Used APIs
The following public APIs are used to request the current public IP.

- https://api.myip.com
- https://api.ipify.org?format=json
- https://api.my-ip.io/ip.json

### Required Environment Variables

| Name        | Description                                                                              |
|-------------|------------------------------------------------------------------------------------------|
| HDNS_TOKEN  | Hetzner DNS API Key (https://docs.hetzner.com/dns-console/dns/general/api-access-token/) |
| SLEEP_TIMER | How long to sleep between runs in seconds                                                |

### Example Configuration (config.json)

The script uses a config.json file in the following format. The file should be mounted to */app/config.json*.

```json
{
  "zones": {
    "example.com": {
      "records": [
        "@",
        "www",
        "test"
      ]
    }
  }
}

```