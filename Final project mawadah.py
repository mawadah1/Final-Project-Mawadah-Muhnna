import docker
import time
client = docker.from_env()
client.swarm.leave(force=True)
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
print("Starting the swarm:")
client.swarm.init()
print("swarm id: ", client.swarm.attrs['ID'])
print("swarm name: ", client.swarm.attrs['Spec']['Name'])
print("swarm creation date: ", client.swarm.attrs['CreatedAt'])
print("\nCreating the network:")
client.networks.create("se443_test_net", driver = "overlay", scope ="global",
ipam = docker.types.IPAMConfig(pool_configs = [docker.types.IPAMPool(subnet = "10.10.10.0/24")]))

for network in client.networks.list():
    if network.name == "se443_test_net":
        print("network id: ", network.id)
        print("network name: ", network.name)
        print("network creation date: ", network.attrs['Created'])

print("\nCreating the broker:")
client.services.create("eclipse-mosquitto", name = "broker", 
restart_policy = {"Name":"always"}).scale(3)
#docker.types.RestartPolicy(condition = "any")).scale(3)


print("service id: ", client.services.list()[0].id)
print("service name: ", client.services.list()[0].name)
print("service creation date: ", client.services.list()[0].attrs['CreatedAt'])
print("service number of replicas: ", client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])


# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
 

print("\nCreating the Subscriber :")
client.services.create("efrecon/mqtt-client", name="Subscriber",  restart_policy = {"Name":"always"}, 
networks=["se443_test_net"], command='sub -h host.docker.internal -t alfaisal_uni -v').scale(3)
print("Subscriber ID: ", client.services.list()[0].id)
print("Subscriber Name: ", client.services.list()[0].name)
print("Subscriber Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
print("Subscriber number of replicas: ", client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])


print("\nCreating the Publisher :")
client.services.create("efrecon/mqtt-client", name="Publisher",  restart_policy = {"Name":"always"},
 networks=["se443_test_net"], command='pub -h host.docker.internal -t alfaisal_uni -m "<191550 - Mawadah - Almuhnna>"').scale(3)
print("Publisher ID: ", client.services.list()[0].id)
print("Publisher Name: ", client.services.list()[0].name)
print("Publisher Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
print("Publisher number of replicas: ", client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

time.sleep(300)

# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
 
print("\nRemoving the Network and Services:")


print("Removing the Publisher:", end="")
client.services.get("Publisher").remove()
print("Done with Removing the Publisher!")


print("Removing the Subscriber:", end="")
client.services.get("Subscriber").remove()
print("Done Removing the Subcriber!")


print("Removing the broker:", end="")
client.services.get("broker").remove()
print("Done with Removing broker!")


print("Removing the Network:", end="")
client.networks.get("se443_test_net").remove()
print("Done with Removing the Network!")

print("Removing the Swarm:", end="")
client.swarm.leave(force=True)
print("Done Removing the Swarm!")