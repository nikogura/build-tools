#!/usr/bin/env bash

# Assumes repo is named after cookbook, and cookbook is checked out to ./repo-name

NODENAME=''
CHEF_CLIENT_NAME=''
CHEF_ORG_NAME=''
CHEF_SERVER=''
CHECKOUT_DIR=''
SUPERMARKET=''
GITHUB_REPO=''
GITHUB_ORG=''

ORGS=()

echo "Installing Chef DK"

sudo rpm -Uvh --replacepkgs https://packages.chef.io/stable/el/7/chefdk-0.12.0-1.el7.x86_64.rpm

sudo chef geminstall chef-vault-testfixtures


echo "Writing knife.rb"
mkdir -p .chef

KNIFE_CONFIG=$(cat <<'EOF'
current dir = File.dirname(__FILE__)
log_level           :info
log_location        STDOUT
node_name           $NODENAME
client_key          \"#{current_dir}$CHEF_CLIENT_NAME.pem\"
chef_server_url     '$CHEF_SERVER/organizations/$CHEF_ORG_NAME'
cookbook_path       [\"#{current_dir}/..\", \"$CHECKOUT_DIR\"]

knife[:supermatket_site = '$SUPERMARKET'
knife[:vault_mode]      = 'client'
EOF
)

echo "$KNIFE_CONFIG" > .chef/knife.rb

echo "Adding Chef Client PEM"

CHEF_PEM=$(cat <<'EOF'
EOF
)

echo "$CHEF_PEM" > .chef/$CHEF_CLIENT_NAME.pem


echo "Uploading to Chef Server at $CHEF_SERVER"

for org in "${orgs[@]}"; do
    echo "Sed Command: sed -i \"s|chef_server_url.*|chef_server_url '$CHEF_SERVER/organizaitons/$org'|\" .chef/knife.rb "
    sed -i "s|chef_server_url.*|chef_server_url '$CHEF_SERVER/organizaitons/$org'|" .chef/knife.rb

    echo "Knife Contents:"
    cat .chef/knife.rb

    berks install
    berks upload
done




