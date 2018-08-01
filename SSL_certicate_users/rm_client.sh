#!/bin/bash

function usage () {
	echo "$0 <username>"
	exit 1
}

if [ $# -ne 1 ]
then
	usage
fi

USERNAME="$1"

SSL_DIR="/etc/ssl"
SSL_PRIVATE_DIR="$SSL_DIR/ca/private"
SSL_CERTS_DIR="$SSL_DIR/ca/certs"
USERS_DIR="${SSL_CERTS_DIR}/users"

# Revoke a particular user's certificate.
openssl ca -name CA_default -revoke ${USERS_DIR}/${USERNAME}.crt -keyfile $SSL_PRIVATE_DIR/ca.key -cert $SSL_CERTS_DIR/ca.crt

# Update the Certificate Revocation list for removing 'user certificates.'
openssl ca -name CA_default -gencrl -keyfile $SSL_PRIVATE_DIR/ca.key -cert $SSL_CERTS_DIR/ca.crt -out $SSL_PRIVATE_DIR/ca.crl -crldays 365
