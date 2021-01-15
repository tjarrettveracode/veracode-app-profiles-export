# Veracode App Profiles Export

Export a list of applications and all the profile properties to CSV.

## Setup

Clone this repository:

    git clone https://github.com/tjarrettveracode/veracode-app-profiles-export

Install dependencies:

    cd veracode-app-profiles-export
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python vcappprofiles.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python vcappprofiles.py (arguments)

Arguments supported include:

* --appid, -a  (opt): application guid for which to list all attributes.
* --all, -l (opt): If set, checks all applications.

## NOTES

1. All values are output to vcappprofiles.csv
