# Shibboleth EDS DiscoFeed generator
Small python3 script that converts Metadata XML to DiscoFeed JSON format for Shibboleth Embedded Discovery Service

# Instructions

* `sudo apt install python3`

* `cd /opt ; sudo git clone https://github.com/malavolti/shib-eds-discofeed-generator.git`

* Configure your Apache:
  * `sudo cp /opt/shib-eds-discofeed-generator/shib-eds-df-gen.conf /etc/apache2/sites-available`

* Put the following command into your preferred CRON Jobs:
  * Choose ONE of the following command to consider only ONE metadata stream:
    * IDEM Test Metadata: 
      * `/usr/bin/wget http://md.idem.garr.it/metadata/idem-test-metadata-sha256.xml -O /opt/shib-eds-discofeed-generator/input/idem-test-metadata-sha256.xml >> /opt/shib-eds-discofeed-generator/wget.log 2>&1`
    * IDEM Production Metadata:
      * `/usr/bin/wget http://md.idem.garr.it/metadata/idem-metadata-sha256.xml -O /opt/shib-eds-discofeed-generator/input/idem-metadata-sha256.xml >> /opt/shib-eds-discofeed-generator/wget.log 2>&1`
    * EDUGAIN2IDEM Metadata:
      * `/usr/bin/wget http://md.idem.garr.it/metadata/edugain2idem-metadata-sha256.xml -O /opt/shib-eds-discofeed-generator/input/edugain2idem-metadata-sha256.xml >> /opt/shib-eds-discofeed-generator/wget.log 2>&1`

  * Use one of the following commands to generate EDS JSON file for the specific stream:
    * IDEM Test Metadata:
      * `/usr/bin/python3 /opt/shib-eds-discofeed-generator/extractDataFromMD.py -m /opt/shib-eds-discofeed-generator/input/idem-test-metadata-sha256.xml -o /opt/shib-eds-discofeed-generator/output/idem-test-eds.json > /opt/shib-eds-discofeed-generator/md-parsing.log 2>&1`
    * IDEM Production Metadata:
      * `/usr/bin/python3 /opt/shib-eds-discofeed-generator/extractDataFromMD.py -m /opt/shib-eds-discofeed-generator/input/idem-metadata-sha256.xml -o /opt/shib-eds-discofeed-generator/output/idem-prod-eds.json > /opt/shib-eds-discofeed-generator/md-parsing.log 2>&1`
    * EDUGAIN2IDEM Metadata:
      * `/usr/bin/python3 /opt/shib-eds-discofeed-generator/extractDataFromMD.py -m /opt/shib-eds-discofeed-generator/input/edgugain2idem-metadata-sha256.xml -o /opt/shib-eds-discofeed-generator/output/edugain2idem-eds.json > /opt/shib-eds-discofeed-generator/md-parsing.log 2>&1`

  Example Crontab:
  ```bash
  20 * * * * /usr/bin/wget http://md.idem.garr.it/metadata/edugain2idem-metadata-sha256.xml -O /opt/shib-eds-discofeed-generator/input/edugain2idem-metadata-sha256.xml >> /opt/shib-eds-discofeed-generator/wget.log 2>&1

  21 * * * * /usr/bin/python3 /opt/shib-eds-discofeed-generator/extractDataFromMD.py -m /opt/shib-eds-discofeed-generator/input/edugain2idem-metadata-sha256.xml -o /opt/shib-eds-discofeed-generator/output/edugain2idem-eds.json > /opt/shib-eds-discofeed-generator/md-parsing.log 2>&1
  ```

* Enable Shib EDS DiscoFeed Generator site:
  * `sudo a2ensite shib-eds-df-gen.conf`
  * `sudo systemctl reload apache2.service`
