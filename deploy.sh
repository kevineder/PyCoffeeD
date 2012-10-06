EXPECTED_ARGS=1

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` {ip to raspeberry pi}"
  exit 1
fi

IP_ADDRESS=$1

echo "Deploying to $IP_ADDRESS..."

SSH="ssh pi@$IP_ADDRESS "
SCP_LOC="pi@$IP_ADDRESS:/home/pi/PyCoffeeD"
$SSH "rm -rf /home/pi/PyCoffeeD; mkdir -p /home/pi/PyCoffeeD"
scp ./Scale.py $SCP_LOC
scp ./CoffeeD.py $SCP_LOC
scp -r ./static $SCP_LOC
$SSH "chmod -R 755 /home/pi/PyCoffeeD"
