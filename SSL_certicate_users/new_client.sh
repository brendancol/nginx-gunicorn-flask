#!/bin/bash

function usage () {
	echo "$0 [username]"
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

mkdir -p ${USERS_DIR}

# Create the Client Key and CSR
openssl genrsa -des3 -out ${USERS_DIR}/${USERNAME}.key 1024
openssl req -new -key ${USERS_DIR}/${USERNAME}.key -out ${USERS_DIR}/${USERNAME}.csr

# Sign the client certificate with our CA cert.  Unlike signing our own server cert, this is what we want to do.
openssl x509 -req -days 365 -in ${USERS_DIR}/${USERNAME}.csr -CA $SSL_CERTS_DIR/ca.crt -CAkey $SSL_PRIVATE_DIR/ca.key -CAserial $SSL_DIR/ca/serial -CAcreateserial -out ${USERS_DIR}/${USERNAME}.crt

echo "making p12 file"
#browsers need P12s (contain key and cert)
openssl pkcs12 -export -clcerts -in ${USERS_DIR}/${USERNAME}.crt -inkey ${USERS_DIR}/${USERNAME}.key -out ${USERS_DIR}/${USERNAME}.p12

echo "made ${USERS_DIR}/${USERNAME}.p12"
