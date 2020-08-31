#!/usr/bin/env bash
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [[ ! -z apt-get ]]; then
	# install chrome and chromedriver
	CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
	sudo dpkg -i google-chrome*
	sudo apt-get -f install
	rm google-chrome-stable_current_amd64.deb

	wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	rm chromedriver_linux64.zip
	sudo mv -f chromedriver /usr/local/bin/chromedriver
	sudo chown root:root /usr/local/bin/chromedriver
	sudo chmod 0755 /usr/local/bin/chromedriver
    else
	echo "The system does not currently supported."
	exit 1;
    fi
else
        echo "The system does not currently supported."
	exit 1;
fi
