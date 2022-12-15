#!/usr/bin/env bash
# Install Nginx if it not already installed
if ! command -v nginx &> /dev/null;
then
    sudo apt-get -y update
    sudo apt-get install -y nginx
    sudo service nginx start
fi
# Create those folders if doesnt alreeady exist
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
#Create a fake HTML with simple content to test your Ngninx configuration
echo "
<!DOCTYPE html>
    <html lang='en'>
        <head>
            <title>Just a configuration script</title>
            
        </head>
        <body>
        <h1 style=color:'blue'>THIS IS MY HEADING</h1>
            <p>Incoming devops, so get ready world!</P>
        </body>
    </html>
" > /data/web_static/releases/test/index.html
# Create a symbolik link that delete and recreated every time is ran
source_file="/data/web_static/current"
destiny_file="/data/web_static/releases/test/"
sudo ln -sf "$destiny_file" "$source_file"
# Give ownership of the /data/ to the ubuntu user and group recursive
sudo chown -R ubuntu:ubuntu /data/
# Update the Ninx configuration to work https://mydomainame.tech/hbnb_static
sudo sed -i "38i \ \tlocation /hbnb_static/ {\n\t\talias $source_file/;\n\t\tautoindex off;\n\t}\n" /etc/nginx/sites-enabled/default
sudo service nginx restart