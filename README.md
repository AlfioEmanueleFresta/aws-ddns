## aws-ddns

A simple Python script to periodically update the A record of DNS records hosted on AWS Route 53.

Only supports IPv4.

This is a personal project, licensed under GPLv3, with absolutely no warranty.


### System requirements

On Debian or Ubuntu:

```
$ sudo apt install python3-venv awscli
```

### AWS set up

1. A Route53 DNS hosted zone with an existing IPv4 `A` record
2. A IAM user with `route53:ChangeResourceRecordSets` permissions for the hosted zone you want to update
3. A named profile with IAM user credentials in `~/.aws/credentials` ([see AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html))
    ```
    $ aws configure
    ```

### Set up

1. Clone this repository
    ```
    $ git clone https://github.com/AlfioEmanueleFresta/aws-ddns
    ```
2. Create a virtual environment
    ```
    $ cd aws-ddns/
    $ python3 -m virtualenv -ppython3 .venv
    ```
3. Install Python requirements
    ```
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    ```
4. Customise your configuration
    ```
    $ cp config.ini.sample config.ini
    $ editor config.ini
    ```

Then, you can manually run the script:

```
$ .venv/bin/python3 update.py
```

Alternatively, you can set up your crontab to periodically execute the script - follow the instructions below.


### Crontab

Set up your crontab to periodically execute the script to keep your DNS config up-to-date.

Check out `crontab.sample`. You can customise the snippet, and add it to your crontab with:

```
$ crontab -e
```

After a few minutes, check `aws-ddns/output.log`, to verify the
script did indeed execute automatically.
