#!/usr/bin/env bash

source /scripts/env-data.sh

SETUP_LOCKFILE="${CONF_LOCKFILE_DIR}/.pg_hba.conf.lock"
if [ -f "${SETUP_LOCKFILE}" ]; then
  return 0
fi


# This script will setup pg_hba.conf

# Reconfigure pg_hba if environment settings changed
cat ${ROOT_CONF}/pg_hba.conf.template > ${ROOT_CONF}/pg_hba.conf
echo "USE CUSTOM Script for pg_hba.conf!"
echo "local   all             all                                     trust" >> $ROOT_CONF/pg_hba.conf
echo "host    all             all             127.0.0.1/32            trust" >> $ROOT_CONF/pg_hba.conf
echo "host    all             all             0.0.0.0/0               trust" >> $ROOT_CONF/pg_hba.conf
echo "host    all             all             192.168.1.0/24          trust" >> $ROOT_CONF/pg_hba.conf
echo "host    all             all             127.0.0.1       255.255.255.255     trust" >> $ROOT_CONF/pg_hba.conf
echo "host    all             all             localhost               trust" >> $ROOT_CONF/pg_hba.conf

# Put lock file to make sure conf was not reinitialized
export PASSWORD_AUTHENTICATION
envsubst < $ROOT_CONF/pg_hba.conf > /tmp/pg_hba.conf && mv /tmp/pg_hba.conf $ROOT_CONF/pg_hba.conf
touch ${SETUP_LOCKFILE}
