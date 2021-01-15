# Veracode Static BOM

Get a quick list of modules with findings identified by a Veracode static scan.

## Setup

Clone this repository:

    git clone https://github.com/tjarrettveracode/veracode-static-bom

Install dependencies:

    cd veracode-static-bom
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python vcstaticbom.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python vcstaticbom.py (arguments)

Arguments supported include:

* --appid, -a  (opt): application guid for which to list a bill of materials.
* --all, -l (opt): If set, checks all applications.

## NOTES

1. Initial version of the script only reports on modules found in policy scans.
1. All values are output to vcstaticbom.csv
