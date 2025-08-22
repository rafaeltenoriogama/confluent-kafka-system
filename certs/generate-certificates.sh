#!/bin/bash
# Kafka SASL/SSL Setup Script
# Description: Transforms a plaintext Kafka cluster into a SASL/SSL-secured cluster.
# Usage: Run as root or with sudo, and execute on each Kafka broker.

# ------------------------------------------------------------------------------
# 🧰 Step 1: Generate Certificate Authority (CA)
# ------------------------------------------------------------------------------
echo "🔐 Generating Certificate Authority (CA)..."
openssl req -new -x509 -keyout ca.key -out ca.crt -days 365 -subj "/CN=MyKafkaCA" -nodes
# Outputs:
#   - ca.key (CA private key)
#   - ca.crt (CA public certificate, used to sign broker certs)

# ------------------------------------------------------------------------------
# 🔑 Step 2: Create Kafka Keystore (Broker Identity)
# ------------------------------------------------------------------------------
echo "🔑 Creating Kafka Keystore..."
keytool -genkey -keystore kafka.server.keystore.jks \
  -validity 365 -storepass confluent \
  -keypass confluent -dname "CN=kafka" -alias kafka \
  -keyalg RSA -keysize 2048
# Outputs:
#   - kafka.server.keystore.jks (contains broker's private key)

# ------------------------------------------------------------------------------
# ✍️ Step 3: Generate CSR & Sign with CA
# ------------------------------------------------------------------------------
echo "📝 Generating CSR and signing with CA..."
keytool -certreq -keystore kafka.server.keystore.jks \
  -file cert-file -alias kafka -storepass confluent

openssl x509 -req -CA ca.crt -CAkey ca.key -in cert-file \
  -out cert-signed -days 365 -CAcreateserial -sha256
# Outputs:
#   - cert-signed (CA-signed broker certificate)

# ------------------------------------------------------------------------------
# 📥 Step 4: Import CA and Signed Cert into Keystore
# ------------------------------------------------------------------------------
echo "📥 Importing CA and signed cert into keystore..."
keytool -keystore kafka.server.keystore.jks \
  -alias CARoot -import -file ca.crt -storepass confluent -noprompt

keytool -keystore kafka.server.keystore.jks \
  -alias kafka -import -file cert-signed -storepass confluent -noprompt

# ------------------------------------------------------------------------------
# ✅ Step 5: Create Truststore (CA Trust)
# ------------------------------------------------------------------------------
echo "✅ Creating Truststore..."
keytool -keystore kafka.server.truststore.jks \
  -alias CARoot -import -file ca.crt -storepass confluent -noprompt
# Outputs:
#   - kafka.server.truststore.jks (trusts the CA)
# ------------------------------------------------------------------------------
